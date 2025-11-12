"""
Sistema de Alertas e Notificações Ávila Ops
Gerencia alertas críticos para operações multinacionais
"""

from dataclasses import dataclass
from typing import List, Optional, Callable
from datetime import datetime
from enum import Enum

from on.core.on_logger import AgentLogger
from on.core.on_storage import log as storage_log


class AlertLevel(Enum):
    """Níveis de alerta"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertCategory(Enum):
    """Categorias de alerta"""
    PERFORMANCE = "performance"
    AVAILABILITY = "availability"
    SECURITY = "security"
    COMPLIANCE = "compliance"
    CAPACITY = "capacity"
    OPERATIONAL = "operational"


@dataclass
class Alert:
    """Representação de um alerta"""
    level: AlertLevel
    category: AlertCategory
    title: str
    description: str
    source: str
    timestamp: datetime
    metadata: dict = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None


class AlertManager:
    """
    Gerenciador de alertas corporativos
    Monitora condições críticas e aciona notificações
    """
    
    # Thresholds padrão para alertas
    THRESHOLDS = {
        "sla_compliance_warning": 95.0,  # % - abaixo disso gera warning
        "sla_compliance_critical": 90.0,  # % - abaixo disso gera critical
        "cpu_usage_warning": 70.0,  # % - acima disso gera warning
        "cpu_usage_critical": 90.0,  # % - acima disso gera critical
        "queue_size_warning": 1000,  # mensagens
        "queue_size_critical": 5000,  # mensagens
        "error_rate_warning": 0.05,  # 5% de erro
        "error_rate_critical": 0.10,  # 10% de erro
        "response_time_warning": 2.0,  # segundos
        "response_time_critical": 5.0,  # segundos
    }
    
    def __init__(self):
        self.logger = AgentLogger("AlertManager")
        self.active_alerts: List[Alert] = []
        self.resolved_alerts: List[Alert] = []
        self.alert_handlers: List[Callable] = []
        
    def register_handler(self, handler: Callable):
        """Registra handler customizado para alertas"""
        self.alert_handlers.append(handler)
        self.logger.log(f"Handler de alerta registrado")
    
    def create_alert(
        self,
        level: AlertLevel,
        category: AlertCategory,
        title: str,
        description: str,
        source: str,
        metadata: dict = None
    ) -> Alert:
        """Cria e registra novo alerta"""
        alert = Alert(
            level=level,
            category=category,
            title=title,
            description=description,
            source=source,
            timestamp=datetime.utcnow(),
            metadata=metadata or {}
        )
        
        self.active_alerts.append(alert)
        
        # Log do alerta
        emoji = self._get_alert_emoji(level)
        self.logger.log(
            f"{emoji} [{level.value.upper()}] {category.value}: {title}"
        )
        storage_log(
            agent="alerts",
            message=f"{level.value}|{category.value}|{title}|{description}"
        )
        
        # Acionar handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception as e:
                self.logger.log(f"Erro em handler de alerta: {e}")
        
        return alert
    
    def resolve_alert(self, alert: Alert, resolution_note: str = ""):
        """Marca alerta como resolvido"""
        alert.resolved = True
        alert.resolved_at = datetime.utcnow()
        
        if alert in self.active_alerts:
            self.active_alerts.remove(alert)
            self.resolved_alerts.append(alert)
        
        self.logger.log(f"? Alerta resolvido: {alert.title}")
        if resolution_note:
            self.logger.log(f"  Nota: {resolution_note}")
    
    def check_sla_compliance(self, agent: str, compliance: float):
        """Verifica SLA e gera alertas se necessário"""
        if compliance < self.THRESHOLDS["sla_compliance_critical"]:
            self.create_alert(
                level=AlertLevel.CRITICAL,
                category=AlertCategory.COMPLIANCE,
                title=f"SLA Crítico: {agent}",
                description=f"SLA de {agent} está em {compliance:.1f}% (crítico < {self.THRESHOLDS['sla_compliance_critical']}%)",
                source=agent,
                metadata={"sla_compliance": compliance}
            )
        elif compliance < self.THRESHOLDS["sla_compliance_warning"]:
            self.create_alert(
                level=AlertLevel.WARNING,
                category=AlertCategory.COMPLIANCE,
                title=f"SLA Baixo: {agent}",
                description=f"SLA de {agent} está em {compliance:.1f}% (warning < {self.THRESHOLDS['sla_compliance_warning']}%)",
                source=agent,
                metadata={"sla_compliance": compliance}
            )
    
    def check_resource_usage(self, resource: str, usage_percent: float):
        """Verifica uso de recursos e gera alertas se necessário"""
        if usage_percent > self.THRESHOLDS["cpu_usage_critical"]:
            self.create_alert(
                level=AlertLevel.CRITICAL,
                category=AlertCategory.CAPACITY,
                title=f"Uso Crítico de {resource}",
                description=f"{resource} em {usage_percent:.1f}% (crítico > {self.THRESHOLDS['cpu_usage_critical']}%)",
                source="system",
                metadata={"resource": resource, "usage": usage_percent}
            )
        elif usage_percent > self.THRESHOLDS["cpu_usage_warning"]:
            self.create_alert(
                level=AlertLevel.WARNING,
                category=AlertCategory.CAPACITY,
                title=f"Uso Elevado de {resource}",
                description=f"{resource} em {usage_percent:.1f}% (warning > {self.THRESHOLDS['cpu_usage_warning']}%)",
                source="system",
                metadata={"resource": resource, "usage": usage_percent}
            )
    
    def check_queue_size(self, queue_name: str, size: int):
        """Verifica tamanho da fila e gera alertas se necessário"""
        if size > self.THRESHOLDS["queue_size_critical"]:
            self.create_alert(
                level=AlertLevel.CRITICAL,
                category=AlertCategory.PERFORMANCE,
                title=f"Fila Crítica: {queue_name}",
                description=f"Fila {queue_name} com {size} mensagens (crítico > {self.THRESHOLDS['queue_size_critical']})",
                source=queue_name,
                metadata={"queue_size": size}
            )
        elif size > self.THRESHOLDS["queue_size_warning"]:
            self.create_alert(
                level=AlertLevel.WARNING,
                category=AlertCategory.PERFORMANCE,
                title=f"Fila Crescendo: {queue_name}",
                description=f"Fila {queue_name} com {size} mensagens (warning > {self.THRESHOLDS['queue_size_warning']})",
                source=queue_name,
                metadata={"queue_size": size}
            )
    
    def check_agent_availability(self, agent: str, last_heartbeat: datetime):
        """Verifica disponibilidade do agente"""
        time_since_heartbeat = (datetime.utcnow() - last_heartbeat).total_seconds()
        
        if time_since_heartbeat > 300:  # 5 minutos sem heartbeat
            self.create_alert(
                level=AlertLevel.CRITICAL,
                category=AlertCategory.AVAILABILITY,
                title=f"Agente Inativo: {agent}",
                description=f"Agente {agent} sem heartbeat há {time_since_heartbeat:.0f}s",
                source=agent,
                metadata={"last_heartbeat": last_heartbeat.isoformat()}
            )
        elif time_since_heartbeat > 120:  # 2 minutos sem heartbeat
            self.create_alert(
                level=AlertLevel.WARNING,
                category=AlertCategory.AVAILABILITY,
                title=f"Agente Lento: {agent}",
                description=f"Agente {agent} sem heartbeat há {time_since_heartbeat:.0f}s",
                source=agent,
                metadata={"last_heartbeat": last_heartbeat.isoformat()}
            )
    
    def get_active_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """Retorna alertas ativos, opcionalmente filtrados por nível"""
        if level:
            return [a for a in self.active_alerts if a.level == level]
        return self.active_alerts
    
    def get_summary(self) -> dict:
        """Retorna resumo dos alertas"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "active": {
                "total": len(self.active_alerts),
                "critical": len([a for a in self.active_alerts if a.level == AlertLevel.CRITICAL]),
                "error": len([a for a in self.active_alerts if a.level == AlertLevel.ERROR]),
                "warning": len([a for a in self.active_alerts if a.level == AlertLevel.WARNING]),
                "info": len([a for a in self.active_alerts if a.level == AlertLevel.INFO]),
            },
            "resolved_today": len([
                a for a in self.resolved_alerts
                if a.resolved_at and (datetime.utcnow() - a.resolved_at).days == 0
            ]),
            "by_category": {
                cat.value: len([a for a in self.active_alerts if a.category == cat])
                for cat in AlertCategory
            }
        }
    
    def _get_alert_emoji(self, level: AlertLevel) -> str:
        """Retorna emoji para o nível de alerta"""
        emojis = {
            AlertLevel.INFO: "??",
            AlertLevel.WARNING: "??",
            AlertLevel.ERROR: "?",
            AlertLevel.CRITICAL: "??"
        }
        return emojis.get(level, "??")


# Instância global do gerenciador de alertas
alert_manager = AlertManager()
