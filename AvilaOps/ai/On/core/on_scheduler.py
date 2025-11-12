"""
⏱️ ON Scheduler - Gerenciador de Turnos dos Agentes
Sistema de agendamento e controle de turnos com persistência
"""
import threading
import time
from datetime import datetime
from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_logger import AgentLogger
from on.core.on_storage import register_shift

class Scheduler:
    """Gerenciador de turnos para agentes do ecossistema On"""
    
    def __init__(self, agent_name):
        self.agent = agent_name
        self.logger = AgentLogger(agent_name)
        self.active_shift = None
        self.shift_thread = None

    def start_shift(self, duration_min=60):
        """Inicia um turno de trabalho para o agente"""
        if self.active_shift:
            self.logger.warning("Turno já está ativo")
            return
            
        start = datetime.utcnow()
        self.active_shift = start
        self.logger.info(f"Turno iniciado - Duração: {duration_min} minutos")
        
        # Executa o turno em thread separada
        self.shift_thread = threading.Thread(
            target=self._run_shift, 
            args=(start, duration_min), 
            daemon=True
        )
        self.shift_thread.start()

    def _run_shift(self, start, duration_min):
        """Executa o turno em background"""
        try:
            # Simula trabalho durante o turno
            time.sleep(duration_min * 60)
            end = datetime.utcnow()
            
            # Registra o turno completo
            self.logger.info("Turno encerrado com sucesso")
            register_shift(
                self.agent, 
                start.isoformat(), 
                end.isoformat(), 
                duration_min, 
                True
            )
            
        except Exception as e:
            self.logger.error(f"Erro durante turno: {e}")
            register_shift(
                self.agent, 
                start.isoformat(), 
                datetime.utcnow().isoformat(), 
                duration_min, 
                False
            )
        finally:
            self.active_shift = None

    def stop_shift(self):
        """Encerra o turno atual prematuramente"""
        if not self.active_shift:
            self.logger.warning("Nenhum turno ativo para encerrar")
            return
            
        self.logger.info("Encerrando turno prematuramente")
        # O cleanup será feito automaticamente pela thread