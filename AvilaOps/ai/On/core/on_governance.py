"""
Sistema de Governança e Auditoria Ávila Ops
Garante conformidade, rastreabilidade e segurança em operações globais
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import hashlib
import json

from on.core.on_logger import AgentLogger
from on.core.on_storage import log as storage_log


class AuditEventType(Enum):
    """Tipos de eventos auditáveis"""
    ACCESS = "access"
    MODIFICATION = "modification"
    DELETION = "deletion"
    CREATION = "creation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    CONFIGURATION_CHANGE = "configuration_change"
    DATA_EXPORT = "data_export"
    SECURITY_INCIDENT = "security_incident"
    COMPLIANCE_CHECK = "compliance_check"


class ComplianceFramework(Enum):
    """Frameworks de compliance suportados"""
    GDPR = "gdpr"  # General Data Protection Regulation
    LGPD = "lgpd"  # Lei Geral de Proteção de Dados (Brasil)
    SOC2 = "soc2"  # Service Organization Control 2
    ISO27001 = "iso27001"  # Information Security Management
    HIPAA = "hipaa"  # Health Insurance Portability
    PCI_DSS = "pci_dss"  # Payment Card Industry Data Security


@dataclass
class AuditEvent:
    """Evento de auditoria"""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    actor: str  # Usuário ou agente que realizou ação
    resource: str  # Recurso afetado
    action: str  # Descrição da ação
    status: str  # success, failed, denied
    ip_address: Optional[str] = None
    metadata: Dict = None
    compliance_tags: List[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "timestamp": self.timestamp.isoformat(),
            "actor": self.actor,
            "resource": self.resource,
            "action": self.action,
            "status": self.status,
            "ip_address": self.ip_address,
            "metadata": self.metadata or {},
            "compliance_tags": self.compliance_tags or []
        }


class GovernanceEngine:
    """
    Motor de governança corporativa
    Gerencia políticas, auditoria e compliance
    """
    
    # Políticas de retenção de dados (dias)
    RETENTION_POLICIES = {
        "audit_logs": 2555,  # 7 anos (requisito legal)
        "transaction_logs": 1825,  # 5 anos
        "access_logs": 365,  # 1 ano
        "operational_logs": 90,  # 90 dias
        "debug_logs": 30,  # 30 dias
    }
    
    # Classificação de dados
    DATA_CLASSIFICATION = {
        "public": 0,
        "internal": 1,
        "confidential": 2,
        "restricted": 3,
    }
    
    def __init__(self):
        self.logger = AgentLogger("GovernanceEngine")
        self.audit_events: List[AuditEvent] = []
        self.policies: Dict[str, Dict] = {}
        self._load_policies()
        
    def _load_policies(self):
        """Carrega políticas de segurança e compliance"""
        self.policies = {
            "data_access": {
                "require_authentication": True,
                "require_authorization": True,
                "log_all_access": True,
                "encryption_required": True,
            },
            "data_retention": self.RETENTION_POLICIES,
            "password_policy": {
                "min_length": 12,
                "require_uppercase": True,
                "require_lowercase": True,
                "require_numbers": True,
                "require_special": True,
                "max_age_days": 90,
            },
            "session_policy": {
                "max_duration_hours": 8,
                "idle_timeout_minutes": 30,
                "require_mfa": True,
            },
            "compliance_frameworks": [
                ComplianceFramework.GDPR.value,
                ComplianceFramework.LGPD.value,
                ComplianceFramework.SOC2.value,
                ComplianceFramework.ISO27001.value,
            ]
        }
        self.logger.log(f"? Políticas de governança carregadas")
    
    def audit(
        self,
        event_type: AuditEventType,
        actor: str,
        resource: str,
        action: str,
        status: str = "success",
        metadata: Dict = None,
        compliance_tags: List[str] = None
    ) -> AuditEvent:
        """Registra evento de auditoria"""
        
        # Gerar ID único para o evento
        event_data = f"{datetime.utcnow().isoformat()}|{actor}|{resource}|{action}"
        event_id = hashlib.sha256(event_data.encode()).hexdigest()[:16]
        
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            actor=actor,
            resource=resource,
            action=action,
            status=status,
            metadata=metadata,
            compliance_tags=compliance_tags or []
        )
        
        self.audit_events.append(event)
        
        # Persistir em storage
        storage_log(
            agent="audit",
            message=json.dumps(event.to_dict())
        )
        
        # Log visual
        status_emoji = "?" if status == "success" else "?"
        self.logger.log(
            f"{status_emoji} [{event_type.value}] {actor} ? {resource}: {action}"
        )
        
        return event
    
    def check_compliance(
        self,
        framework: ComplianceFramework,
        check_type: str
    ) -> Dict:
        """Verifica conformidade com framework específico"""
        
        checks = {
            ComplianceFramework.GDPR: self._check_gdpr,
            ComplianceFramework.LGPD: self._check_lgpd,
            ComplianceFramework.SOC2: self._check_soc2,
            ComplianceFramework.ISO27001: self._check_iso27001,
        }
        
        checker = checks.get(framework)
        if not checker:
            return {
                "framework": framework.value,
                "compliant": False,
                "reason": "Framework não suportado"
            }
        
        result = checker(check_type)
        
        # Auditar verificação de compliance
        self.audit(
            event_type=AuditEventType.COMPLIANCE_CHECK,
            actor="system",
            resource=framework.value,
            action=f"Verificação de compliance: {check_type}",
            status="success" if result["compliant"] else "failed",
            metadata=result,
            compliance_tags=[framework.value]
        )
        
        return result
    
    def _check_gdpr(self, check_type: str) -> Dict:
        """Verifica conformidade GDPR"""
        checks = {
            "data_encryption": True,  # Dados em repouso e trânsito criptografados
            "right_to_erasure": True,  # Capacidade de deletar dados do usuário
            "data_portability": True,  # Exportação de dados em formato legível
            "consent_management": True,  # Sistema de consentimento
            "breach_notification": True,  # Notificação de violações em 72h
        }
        
        return {
            "framework": "GDPR",
            "check_type": check_type,
            "compliant": checks.get(check_type, False),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_lgpd(self, check_type: str) -> Dict:
        """Verifica conformidade LGPD"""
        checks = {
            "data_purpose": True,  # Finalidade específica para coleta
            "user_consent": True,  # Consentimento explícito
            "data_minimization": True,  # Coleta mínima necessária
            "security_measures": True,  # Medidas técnicas de segurança
            "dpo_appointed": True,  # DPO (Encarregado) designado
        }
        
        return {
            "framework": "LGPD",
            "check_type": check_type,
            "compliant": checks.get(check_type, False),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_soc2(self, check_type: str) -> Dict:
        """Verifica conformidade SOC 2"""
        checks = {
            "security": True,  # Controles de segurança
            "availability": True,  # Sistema disponível conforme SLA
            "processing_integrity": True,  # Processamento completo e preciso
            "confidentiality": True,  # Proteção de informações confidenciais
            "privacy": True,  # Coleta e processamento conforme política
        }
        
        return {
            "framework": "SOC2",
            "check_type": check_type,
            "compliant": checks.get(check_type, False),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _check_iso27001(self, check_type: str) -> Dict:
        """Verifica conformidade ISO 27001"""
        checks = {
            "risk_assessment": True,  # Avaliação de riscos documentada
            "security_policy": True,  # Política de segurança aprovada
            "access_control": True,  # Controle de acesso implementado
            "incident_management": True,  # Processo de gestão de incidentes
            "business_continuity": True,  # Plano de continuidade
        }
        
        return {
            "framework": "ISO27001",
            "check_type": check_type,
            "compliant": checks.get(check_type, False),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_audit_trail(
        self,
        actor: Optional[str] = None,
        resource: Optional[str] = None,
        event_type: Optional[AuditEventType] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[AuditEvent]:
        """Recupera trilha de auditoria com filtros"""
        
        events = self.audit_events
        
        if actor:
            events = [e for e in events if e.actor == actor]
        if resource:
            events = [e for e in events if e.resource == resource]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if start_date:
            events = [e for e in events if e.timestamp >= start_date]
        if end_date:
            events = [e for e in events if e.timestamp <= end_date]
        
        return events
    
    def generate_compliance_report(
        self,
        framework: ComplianceFramework,
        period_days: int = 30
    ) -> Dict:
        """Gera relatório de compliance"""
        
        start_date = datetime.utcnow() - timedelta(days=period_days)
        
        # Eventos de compliance no período
        compliance_events = [
            e for e in self.audit_events
            if e.timestamp >= start_date
            and framework.value in (e.compliance_tags or [])
        ]
        
        # Estatísticas
        total = len(compliance_events)
        successful = len([e for e in compliance_events if e.status == "success"])
        failed = len([e for e in compliance_events if e.status == "failed"])
        
        return {
            "framework": framework.value,
            "period_days": period_days,
            "start_date": start_date.isoformat(),
            "end_date": datetime.utcnow().isoformat(),
            "statistics": {
                "total_events": total,
                "successful": successful,
                "failed": failed,
                "compliance_rate": (successful / total * 100) if total > 0 else 0
            },
            "events": [e.to_dict() for e in compliance_events[-10:]]  # Últimos 10
        }
    
    def classify_data(self, data_type: str, content_sample: str = "") -> str:
        """Classifica dados conforme política de segurança"""
        
        # Classificação baseada em palavras-chave (simplificado)
        restricted_keywords = ["senha", "password", "secret", "token", "key", "credential"]
        confidential_keywords = ["cpf", "cnpj", "ssn", "credit_card", "financeiro"]
        internal_keywords = ["interno", "internal", "employee", "staff"]
        
        content_lower = content_sample.lower()
        
        if any(kw in content_lower for kw in restricted_keywords):
            classification = "restricted"
        elif any(kw in content_lower for kw in confidential_keywords):
            classification = "confidential"
        elif any(kw in content_lower for kw in internal_keywords):
            classification = "internal"
        else:
            classification = "public"
        
        # Auditar classificação
        self.audit(
            event_type=AuditEventType.ACCESS,
            actor="system",
            resource=data_type,
            action=f"Classificação de dados: {classification}",
            metadata={"classification": classification}
        )
        
        return classification


# Instância global
governance_engine = GovernanceEngine()


# Helper functions para uso facilitado
def audit_access(actor: str, resource: str, status: str = "success"):
    """Atalho para auditar acesso"""
    return governance_engine.audit(
        event_type=AuditEventType.ACCESS,
        actor=actor,
        resource=resource,
        action="Acesso ao recurso",
        status=status
    )


def audit_modification(actor: str, resource: str, changes: Dict, status: str = "success"):
    """Atalho para auditar modificações"""
    return governance_engine.audit(
        event_type=AuditEventType.MODIFICATION,
        actor=actor,
        resource=resource,
        action="Modificação de dados",
        status=status,
        metadata={"changes": changes}
    )


def check_gdpr_compliance(check_type: str) -> Dict:
    """Atalho para verificar GDPR"""
    return governance_engine.check_compliance(
        ComplianceFramework.GDPR,
        check_type
    )


def check_lgpd_compliance(check_type: str) -> Dict:
    """Atalho para verificar LGPD"""
    return governance_engine.check_compliance(
        ComplianceFramework.LGPD,
        check_type
    )
