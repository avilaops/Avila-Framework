"""
ON CORE - Ávila Ops (Modo Produção)
Sistema de orquestração central para operações multinacionais

Responsabilidades:
- Inicializa banco de dados (SQLite)
- Configura telemetria (OpenTelemetry)
- Registra e coordena agentes
- Gerencia turnos de trabalho
- Monitora saúde do sistema
- Mantém operação 24/7
"""

import signal
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import yaml
from rich.console import Console

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_storage import init_db
from on.core.on_logger import AgentLogger
from on.core.on_bus import EventBus
from on.core.on_scheduler import Scheduler
from on.core.on_health import heartbeat
from on.core.on_metrics import (
    task_counter,
    shift_counter,
    agent_heartbeat,
    record_shift_completion
)

console = Console()
BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "core" / "config.yaml"


def load_config() -> Dict[str, Any]:
    """Carrega configuração central do sistema"""
    if not CONFIG_PATH.exists():
        console.print("[red]config.yaml não encontrado em core/[/red]")
        return {}
    data = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    return data or {}


def discover_agents(agents_root: Path) -> List[Dict[str, Any]]:
    """
    Varre a pasta de agentes e lê config.yaml de cada um
    Retorna lista com metadados dos agentes encontrados
    """
    agents_meta: List[Dict[str, Any]] = []

    if not agents_root.exists():
        console.print(f"[yellow]Pasta de agentes não encontrada: {agents_root}[/yellow]")
        return agents_meta

    for agent_dir in agents_root.iterdir():
        if not agent_dir.is_dir():
            continue

        cfg_path = agent_dir / "config.yaml"
        if not cfg_path.exists():
            continue

        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        name = cfg.get("agent_name", agent_dir.name)
        area = cfg.get("area", "Desconhecida")
        significado = cfg.get("significado", "")
        shift_min = cfg.get("shift_min", 60)  # padrão: 60 min

        agents_meta.append(
            {
                "name": name,
                "dir": agent_dir,
                "area": area,
                "significado": significado,
                "shift_min": shift_min,
            }
        )

    return agents_meta


class OnCoreApp:
    """
    Aplicação principal On.Core em modo produção
    Orquestra todos os componentes do sistema
    """

    def __init__(self) -> None:
        self.config: Dict[str, Any] = {}
        self.logger = AgentLogger("On.Core")
        self.bus = EventBus()
        self.schedulers: Dict[str, Scheduler] = {}
        self.running = True
        self.start_time = datetime.utcnow()

    def boot(self) -> None:
        """Inicializa todos os componentes do sistema"""
        console.rule("[bold blue]ON CORE - ÁVILA OPS (Modo Produção)[/bold blue]")
        console.print(f"[cyan]Iniciando em: {self.start_time.isoformat()}[/cyan]\n")

        # 1) Carregar configuração central
        self.config = load_config()
        self.logger.log("Configuração central carregada")
        
        agents_path_cfg = self.config.get("agents_path", "./agents")
        agents_root = (BASE_DIR / Path(agents_path_cfg)).resolve()

        # 2) Inicializar banco de dados central
        init_db()
        self.logger.log("✓ SQLite inicializado (registry/on_core.db)")

        # 3) Inicializar telemetria
        self._init_telemetry()
        self.logger.log("✓ Telemetria OpenTelemetry ativa (Prometheus + Loki + Tempo)")

        # 4) Descobrir e registrar agentes
        agents_meta = discover_agents(agents_root)
        if not agents_meta:
            self.logger.log("⚠️ Nenhum agente encontrado em ./agents")
        else:
            self.logger.log(f"✓ {len(agents_meta)} agente(s) detectado(s)")

        # 5) Inicializar cada agente com seu turno
        for meta in agents_meta:
            name = meta["name"]
            shift_min = meta["shift_min"]

            self.logger.log(
                f"  → {name} registrado (área={meta['area']}, turno={shift_min} min)"
            )

            # Criar scheduler para o agente
            sched = Scheduler(name)
            sched.start_shift(duration_min=shift_min)
            self.schedulers[name] = sched

            # Registrar heartbeat inicial
            heartbeat(name)
            agent_heartbeat.add(1, {"agent": name})

        # 6) Mensagem de inicialização completa
        self.logger.log("=" * 60)
        self.logger.log("🚀 On.Core inicializado em modo serviço")
        self.logger.log(f"📊 Telemetria: http://localhost:3000 (Grafana)")
        self.logger.log(f"🔍 Prometheus: http://localhost:9090")
        self.logger.log(f"📜 Loki: http://localhost:3100")
        self.logger.log("=" * 60)

    def _init_telemetry(self) -> None:
        """
        Inicializa sistema de telemetria
        OpenTelemetry já foi configurado em on_telemetry.py
        """
        try:
            from on.core.on_telemetry import tracer, meter
            
            # Registra evento de inicialização
            with tracer.start_as_current_span("on_core_boot") as span:
                span.set_attribute("service.name", "avilaops-on")
                span.set_attribute("service.version", "1.0.0")
                span.set_attribute("environment", "production")
                
            self.logger.log("Telemetria OpenTelemetry configurada")
            
        except Exception as e:
            self.logger.log(f"⚠️ Erro inicializando telemetria: {e}")

    def _install_signal_handlers(self) -> None:
        """Instala handlers para shutdown gracioso"""
        def _handler(sig, frame):
            self.logger.log(f"🛑 Sinal {sig} recebido. Encerrando On.Core...")
            self.running = False

        # SIGINT (Ctrl+C) e SIGTERM (kill)
        signal.signal(signal.SIGINT, _handler)
        try:
            signal.signal(signal.SIGTERM, _handler)
        except (ValueError, AttributeError):
            # SIGTERM pode não estar disponível em todos os ambientes
            pass

    def run_forever(self) -> None:
        """
        Loop principal de execução
        Mantém o sistema ativo e monitora saúde dos agentes
        """
        self._install_signal_handlers()
        self.boot()

        # Loop passivo de serviço
        heartbeat_interval = 30  # segundos
        last_heartbeat = time.time()

        while self.running:
            current_time = time.time()
            
            # Heartbeat periódico do sistema
            if current_time - last_heartbeat >= heartbeat_interval:
                self._system_heartbeat()
                last_heartbeat = current_time
            
            time.sleep(1)  # Sleep leve para não consumir CPU

        # Shutdown gracioso
        self._shutdown()

    def _system_heartbeat(self) -> None:
        """Heartbeat do sistema central"""
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        
        self.logger.log(f"💓 System heartbeat | Uptime: {uptime:.0f}s")
        
        # Verificar status dos schedulers
        for name, sched in self.schedulers.items():
            if hasattr(sched, 'active') and sched.active:
                heartbeat(name)
            else:
                self.logger.log(f"⚠️ Agente {name} não está ativo")

    def _shutdown(self) -> None:
        """Shutdown gracioso do sistema"""
        self.logger.log("Iniciando shutdown...")
        
        # Parar todos os schedulers
        for name, sched in self.schedulers.items():
            if hasattr(sched, 'stop_shift'):
                sched.stop_shift()
            self.logger.log(f"  → {name} encerrado")
        
        # Registrar métricas finais
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        self.logger.log(f"Uptime total: {uptime:.0f}s")
        
        self.logger.log("✓ On.Core finalizado")


def main() -> None:
    """Função principal de entrada"""
    app = OnCoreApp()
    app.run_forever()


if __name__ == "__main__":
    main()
