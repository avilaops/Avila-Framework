"""
ÁVILA - Decision Engine & Automation System

Sistema de decisão automática e execução de ações baseado em risco.

Features:
- Auto-executa ações de baixo risco
- Requer aprovação para ações de alto risco
- Execução com rollback automático em caso de falha
- Notificações multi-canal
- Logging completo de todas as ações

Uso:
    from decision_engine import DecisionEngine, AutomationAction, RiskLevel

    engine = DecisionEngine(config)
    action = AutomationAction(...)
    result = engine.execute_action(action)
"""

from enum import Enum
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging
import subprocess
import requests
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Níveis de risco para ações automatizadas"""
    ZERO = "ZERO"          # Auto-execute sempre
    LOW = "LOW"            # Auto-execute se $<500 ou tempo<1h
    MEDIUM = "MEDIUM"      # Requer aprovação de Tech Lead
    HIGH = "HIGH"          # Requer aprovação de CTO
    CRITICAL = "CRITICAL"  # Requer aprovação de CEO


class ActionStatus(Enum):
    """Status de execução de ações"""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"


class NotificationChannel(Enum):
    """Canais de notificação"""
    SLACK = "slack"
    EMAIL = "email"
    SMS = "sms"
    DASHBOARD = "dashboard"
    PAGERDUTY = "pagerduty"


@dataclass
class ExecutionStep:
    """Representa um passo de execução"""
    type: str  # "azure_cli", "api_call", "script", "notification"
    description: str
    command: Optional[str] = None
    endpoint: Optional[str] = None
    method: Optional[str] = None
    payload: Optional[Dict] = None
    script_path: Optional[str] = None
    args: List[str] = field(default_factory=list)
    timeout: int = 300  # segundos
    retry_count: int = 0
    success_criteria: Optional[Callable] = None


@dataclass
class AutomationAction:
    """
    Representa uma ação automatizada completa
    """
    id: str
    type: str  # "cost_optimization", "security_patch", "scaling", etc
    title: str
    description: str
    risk_level: RiskLevel
    impact: Dict  # {"cost_saving": 140, "time_saving": 30, ...}
    prerequisites: List[str] = field(default_factory=list)
    execution_steps: List[ExecutionStep] = field(default_factory=list)
    rollback_steps: List[ExecutionStep] = field(default_factory=list)
    estimated_duration: int = 0  # minutos
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    auto_execute: bool = False
    approval_required: bool = True
    approvers: List[str] = field(default_factory=list)
    status: ActionStatus = ActionStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    metadata: Dict = field(default_factory=dict)


class DecisionEngine:
    """
    Motor de decisão - determina se ação deve ser auto-executada ou requer aprovação
    """

    # Regras de auto-execução por tipo de ação
    AUTO_EXECUTE_RULES = {
        "storage_tiering": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda impact: True,
            "reason": "Lifecycle policy não perde dados, apenas move tiers"
        },

        "delete_zombie_snapshot": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda impact: impact.get('age_days', 0) > 365,
            "reason": "Snapshot >1 ano sem uso, backup metadata mantido"
        },

        "delete_unattached_disk": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda impact: impact.get('unattached_days', 0) > 90,
            "reason": "Disco não conectado há 90+ dias, notificar owner antes"
        },

        "vm_rightsizing": {
            "risk": RiskLevel.MEDIUM,
            "auto_if": lambda impact: (
                impact.get('cost_saving', 0) < 500 and
                impact.get('downsize_percentage', 0) <= 50
            ),
            "reason": "Downsize <50% com economia <$500 = baixo risco"
        },

        "reserved_instance_purchase": {
            "risk": RiskLevel.MEDIUM,
            "auto_if": lambda impact: (
                impact.get('uptime_percentage', 0) > 95 and
                impact.get('commitment_months', 0) == 12
            ),
            "reason": "Uptime >95% + commitment 1 ano = safe bet"
        },

        "security_patch_minor": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda impact: impact.get('is_backward_compatible', False),
            "reason": "Patch minor version (backward compatible)"
        },

        "security_patch_critical": {
            "risk": RiskLevel.HIGH,
            "auto_if": lambda impact: False,  # sempre requer aprovação
            "reason": "CVE crítico requer validação humana antes de aplicar"
        },

        "auto_scaling": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda impact: (
                impact.get('cpu_threshold', 0) > 90 and
                impact.get('duration_minutes', 0) > 10
            ),
            "reason": "CPU >90% por 10min = add instances"
        }
    }

    def __init__(self, config: Dict):
        """
        Inicializa o Decision Engine

        Args:
            config: Configuração com credenciais, endpoints, etc
        """
        self.config = config
        self.approval_db = {}  # Em produção, usar DB real
        self.execution_history = []

        logger.info("DecisionEngine initialized")

    def should_auto_execute(self, action: AutomationAction) -> Dict:
        """
        Decide se ação deve ser auto-executada

        Args:
            action: Ação a avaliar

        Returns:
            {
                "auto_execute": bool,
                "reason": str,
                "requires_approval": bool,
                "approvers": List[str]
            }
        """
        rule = self.AUTO_EXECUTE_RULES.get(action.type)

        if not rule:
            # Tipo desconhecido = requer aprovação manual
            logger.warning(f"Unknown action type: {action.type}")
            return {
                "auto_execute": False,
                "reason": "Action type not in whitelist",
                "requires_approval": True,
                "approvers": ["tech_lead", "cto"]
            }

        # Verificar se passa na condição
        try:
            can_auto = rule['auto_if'](action.impact)
        except Exception as e:
            logger.error(f"Error evaluating auto_if condition: {e}")
            can_auto = False

        if can_auto:
            logger.info(f"Action {action.id} approved for auto-execution: {rule['reason']}")
            return {
                "auto_execute": True,
                "reason": rule['reason'],
                "requires_approval": False,
                "approvers": []
            }
        else:
            # Não passou = requer aprovação baseada no risco
            approvers = self._get_approvers_for_risk(rule['risk'])
            logger.info(f"Action {action.id} requires approval from: {approvers}")
            return {
                "auto_execute": False,
                "reason": f"Requires approval: {rule['risk'].value} risk",
                "requires_approval": True,
                "approvers": approvers
            }

    def _get_approvers_for_risk(self, risk: RiskLevel) -> List[str]:
        """
        Retorna lista de aprovadores baseado no nível de risco
        """
        approvers_map = {
            RiskLevel.ZERO: [],
            RiskLevel.LOW: ["tech_lead"],
            RiskLevel.MEDIUM: ["tech_lead", "engineering_manager"],
            RiskLevel.HIGH: ["cto"],
            RiskLevel.CRITICAL: ["cto", "ceo"]
        }
        return approvers_map.get(risk, ["cto"])

    def execute_action(self, action: AutomationAction) -> Dict:
        """
        Executa ação (ou envia para aprovação)

        Args:
            action: Ação a executar

        Returns:
            Resultado da execução ou status de aprovação
        """
        decision = self.should_auto_execute(action)

        if decision['auto_execute']:
            # Auto-execute
            logger.info(f"Auto-executing action {action.id}: {action.title}")
            result = self._run_action(action)
            self._send_notifications(action, result)
            return result
        else:
            # Enviar para aprovação
            logger.info(f"Creating approval request for action {action.id}")
            approval_id = self._create_approval_request(action, decision['approvers'])
            self._send_notifications(action, {
                "status": "awaiting_approval",
                "approval_id": approval_id,
                "approvers": decision['approvers']
            })
            return {
                "status": "pending_approval",
                "approval_id": approval_id,
                "approvers": decision['approvers']
            }

    def _run_action(self, action: AutomationAction) -> Dict:
        """
        Executa os steps da ação

        Args:
            action: Ação a executar

        Returns:
            Resultado da execução
        """
        action.status = ActionStatus.EXECUTING
        action.executed_at = datetime.now()
        results = []

        try:
            # Verificar prerequisites
            if not self._check_prerequisites(action.prerequisites):
                raise Exception("Prerequisites not met")

            # Executar cada step
            for i, step in enumerate(action.execution_steps):
                logger.info(f"Executing step {i+1}/{len(action.execution_steps)}: {step.description}")
                step_result = self._execute_step(step)
                results.append(step_result)

                if not step_result.get('success', False):
                    # Step falhou = rollback
                    logger.error(f"Step {i+1} failed: {step_result.get('error')}")
                    self._rollback(action, results)
                    action.status = ActionStatus.ROLLED_BACK
                    return {
                        "success": False,
                        "error": step_result.get('error'),
                        "failed_step": i + 1,
                        "rollback": "completed"
                    }

            # Sucesso!
            action.status = ActionStatus.COMPLETED
            action.completed_at = datetime.now()
            action.result = {
                "success": True,
                "steps_executed": len(results),
                "impact": action.impact,
                "duration_seconds": (action.completed_at - action.executed_at).total_seconds()
            }

            logger.info(f"Action {action.id} completed successfully")

            # Salvar histórico
            self.execution_history.append({
                "action_id": action.id,
                "type": action.type,
                "result": action.result,
                "timestamp": action.completed_at
            })

            return action.result

        except Exception as e:
            logger.error(f"Action {action.id} failed with exception: {e}")
            self._rollback(action, results)
            action.status = ActionStatus.FAILED
            return {
                "success": False,
                "error": str(e),
                "rollback": "completed"
            }

    def _check_prerequisites(self, prerequisites: List[str]) -> bool:
        """Verifica se prerequisites foram atendidos"""
        # Implementação depende do tipo de prerequisite
        # Exemplo: "backup_completed", "staging_validated", etc
        return True

    def _execute_step(self, step: ExecutionStep) -> Dict:
        """
        Executa um step individual

        Args:
            step: Step a executar

        Returns:
            Resultado do step
        """
        try:
            if step.type == "azure_cli":
                return self._exec_azure_cli(step.command, step.timeout)

            elif step.type == "api_call":
                return self._exec_api_call(
                    step.endpoint,
                    step.method,
                    step.payload,
                    step.timeout
                )

            elif step.type == "script":
                return self._exec_script(step.script_path, step.args, step.timeout)

            elif step.type == "notification":
                return self._send_message(step.payload.get('channel'), step.payload.get('message'))

            else:
                return {"success": False, "error": f"Unknown step type: {step.type}"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _exec_azure_cli(self, command: str, timeout: int) -> Dict:
        """
        Executa comando Azure CLI

        Args:
            command: Comando az a executar
            timeout: Timeout em segundos

        Returns:
            Resultado da execução
        """
        try:
            logger.info(f"Executing Azure CLI: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "command": command
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "command": command
                }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _exec_api_call(self, endpoint: str, method: str, payload: Dict, timeout: int) -> Dict:
        """
        Faz chamada API

        Args:
            endpoint: URL do endpoint
            method: GET, POST, PUT, DELETE
            payload: Dados a enviar
            timeout: Timeout em segundos

        Returns:
            Resultado da chamada
        """
        try:
            logger.info(f"API Call: {method} {endpoint}")

            response = requests.request(
                method=method,
                url=endpoint,
                json=payload,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code < 400:
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "response": response.json() if response.text else {}
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _exec_script(self, script_path: str, args: List[str], timeout: int) -> Dict:
        """
        Executa script Python/Bash

        Args:
            script_path: Caminho do script
            args: Argumentos
            timeout: Timeout em segundos

        Returns:
            Resultado da execução
        """
        try:
            logger.info(f"Executing script: {script_path} {' '.join(args)}")

            # Determinar interpretador
            if script_path.endswith('.py'):
                cmd = ['python', script_path] + args
            elif script_path.endswith('.sh'):
                cmd = ['bash', script_path] + args
            else:
                cmd = [script_path] + args

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "script": script_path
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "script": script_path
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _send_message(self, channel: str, message: str) -> Dict:
        """Envia mensagem (placeholder)"""
        logger.info(f"Sending notification to {channel}: {message}")
        return {"success": True}

    def _rollback(self, action: AutomationAction, executed_steps: List[Dict]):
        """
        Reverte ação em caso de falha

        Args:
            action: Ação a reverter
            executed_steps: Steps já executados
        """
        logger.warning(f"Rolling back action {action.id}")

        for rollback_step in reversed(action.rollback_steps):
            logger.info(f"Rollback step: {rollback_step.description}")
            result = self._execute_step(rollback_step)
            if not result.get('success'):
                logger.error(f"Rollback step failed: {result.get('error')}")

    def _create_approval_request(self, action: AutomationAction, approvers: List[str]) -> str:
        """
        Cria request de aprovação

        Args:
            action: Ação a aprovar
            approvers: Lista de aprovadores

        Returns:
            ID da aprovação
        """
        approval_id = f"approval_{action.id}_{int(datetime.now().timestamp())}"

        self.approval_db[approval_id] = {
            "action": action,
            "approvers": approvers,
            "status": "pending",
            "created_at": datetime.now(),
            "approved_by": []
        }

        logger.info(f"Created approval request {approval_id} for {approvers}")

        return approval_id

    def approve_action(self, approval_id: str, approver: str) -> Dict:
        """
        Aprova uma ação pendente

        Args:
            approval_id: ID da aprovação
            approver: Quem aprovou

        Returns:
            Resultado da aprovação
        """
        if approval_id not in self.approval_db:
            return {"success": False, "error": "Approval not found"}

        approval = self.approval_db[approval_id]

        if approver not in approval['approvers']:
            return {"success": False, "error": "Not authorized to approve"}

        approval['approved_by'].append(approver)
        approval['status'] = "approved"

        logger.info(f"Approval {approval_id} approved by {approver}")

        # Se todos aprovaram, executar
        if set(approval['approved_by']) == set(approval['approvers']):
            action = approval['action']
            action.status = ActionStatus.APPROVED
            result = self._run_action(action)
            self._send_notifications(action, result)
            return result
        else:
            return {
                "success": True,
                "status": "partially_approved",
                "pending": list(set(approval['approvers']) - set(approval['approved_by']))
            }

    def _send_notifications(self, action: AutomationAction, result: Dict):
        """
        Envia notificações multi-canal

        Args:
            action: Ação executada
            result: Resultado da execução
        """
        for channel in action.notification_channels:
            if channel == NotificationChannel.SLACK:
                self._notify_slack(action, result)
            elif channel == NotificationChannel.EMAIL:
                self._notify_email(action, result)
            elif channel == NotificationChannel.DASHBOARD:
                self._update_dashboard(action, result)

    def _notify_slack(self, action: AutomationAction, result: Dict):
        """Notifica no Slack (placeholder)"""
        logger.info(f"Slack notification: Action {action.id} - {result.get('status', 'completed')}")

    def _notify_email(self, action: AutomationAction, result: Dict):
        """Notifica por email (placeholder)"""
        logger.info(f"Email notification: Action {action.id} - {result.get('status', 'completed')}")

    def _update_dashboard(self, action: AutomationAction, result: Dict):
        """Atualiza dashboard (placeholder)"""
        logger.info(f"Dashboard update: Action {action.id} - {result.get('status', 'completed')}")


# ====== EXEMPLO DE USO ======

if __name__ == "__main__":
    # Configuração
    config = {
        "azure_subscription_id": "your-subscription-id",
        "slack_webhook": "https://hooks.slack.com/...",
        "email_smtp": "smtp.gmail.com"
    }

    # Inicializar engine
    engine = DecisionEngine(config)

    # Exemplo 1: Storage Tiering (auto-execute)
    action1 = AutomationAction(
        id="action_001",
        type="storage_tiering",
        title="Mover 800GB para Cool tier",
        description="Dados não acessados há 30+ dias",
        risk_level=RiskLevel.ZERO,
        impact={"cost_saving": 62, "data_moved_gb": 800},
        execution_steps=[
            ExecutionStep(
                type="azure_cli",
                description="Set lifecycle policy",
                command="az storage account management-policy create ..."
            )
        ],
        notification_channels=[NotificationChannel.SLACK, NotificationChannel.DASHBOARD]
    )

    result1 = engine.execute_action(action1)
    print(f"Action 1 result: {json.dumps(result1, indent=2)}")

    # Exemplo 2: VM Rightsizing (requer aprovação)
    action2 = AutomationAction(
        id="action_002",
        type="vm_rightsizing",
        title="Downsize VM prod-api-01",
        description="D8s_v3 → D4s_v3 (CPU avg 12%)",
        risk_level=RiskLevel.MEDIUM,
        impact={
            "cost_saving": 140,
            "downsize_percentage": 50,
            "cpu_avg": 12
        },
        execution_steps=[
            ExecutionStep(
                type="azure_cli",
                description="Resize VM",
                command="az vm resize --resource-group prod --name prod-api-01 --size Standard_D4s_v3"
            )
        ],
        rollback_steps=[
            ExecutionStep(
                type="azure_cli",
                description="Restore original size",
                command="az vm resize --resource-group prod --name prod-api-01 --size Standard_D8s_v3"
            )
        ],
        notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
    )

    result2 = engine.execute_action(action2)
    print(f"Action 2 result: {json.dumps(result2, indent=2)}")

    # Se requer aprovação, aprovar
    if result2.get('status') == 'pending_approval':
        approval_result = engine.approve_action(result2['approval_id'], "tech_lead")
        print(f"Approval result: {json.dumps(approval_result, indent=2)}")
