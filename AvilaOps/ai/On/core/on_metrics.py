"""
Métricas customizadas para operações multinacionais Ávila
Define KPIs específicos para monitoramento de 70+ países
"""

from on.core.on_telemetry import meter
from opentelemetry.metrics import Counter, Histogram, UpDownCounter

# ===== MÉTRICAS GLOBAIS =====

# Taxa de tarefas processadas globalmente
task_counter = meter.create_counter(
    name="on_tasks_total",
    description="Total de tarefas criadas/processadas",
    unit="tasks"
)

# Turnos de trabalho completados
shift_counter = meter.create_counter(
    name="on_shifts_total",
    description="Turnos de trabalho completados por agente",
    unit="shifts"
)

# Volume de logs gerados
log_counter = meter.create_counter(
    name="on_logs_total",
    description="Total de logs registrados",
    unit="logs"
)

# Heartbeat dos agentes (1 = ativo, 0 = inativo)
agent_heartbeat = meter.create_up_down_counter(
    name="on_agent_heartbeat",
    description="Status de heartbeat dos agentes (1=ativo, 0=inativo)",
    unit="status"
)

# ===== MÉTRICAS DE PERFORMANCE =====

# Latência de processamento
processing_latency = meter.create_histogram(
    name="on_processing_duration_seconds",
    description="Duração de processamento de tarefas",
    unit="seconds"
)

# Taxa de erro
error_counter = meter.create_counter(
    name="on_errors_total",
    description="Total de erros por agente e tipo",
    unit="errors"
)

# ===== MÉTRICAS DE NEGÓCIO (MULTINACIONAL) =====

# Operações por região geográfica
regional_operations = meter.create_counter(
    name="on_regional_operations_total",
    description="Operações processadas por região",
    unit="operations"
)

# Clientes atendidos por país
customers_served = meter.create_up_down_counter(
    name="on_customers_active",
    description="Número de clientes ativos por país",
    unit="customers"
)

# SLA compliance (%)
sla_compliance = meter.create_histogram(
    name="on_sla_compliance_ratio",
    description="Taxa de conformidade com SLA",
    unit="ratio"
)

# ===== MÉTRICAS DE CAPACIDADE =====

# Utilização de recursos
resource_utilization = meter.create_histogram(
    name="on_resource_utilization",
    description="Utilização de recursos (CPU, memória, etc.)",
    unit="percent"
)

# Fila de mensagens
queue_size = meter.create_up_down_counter(
    name="on_queue_size",
    description="Tamanho atual da fila de mensagens",
    unit="messages"
)

# ===== FUNÇÕES AUXILIARES =====

def record_task(agent: str, task_type: str = "generic"):
    """Registra uma nova tarefa processada"""
    task_counter.add(1, {"agent": agent, "type": task_type})

def record_shift_completion(agent: str, duration_minutes: float, success: bool = True):
    """Registra conclusão de um turno de trabalho"""
    shift_counter.add(1, {
        "agent": agent,
        "status": "success" if success else "failed"
    })
    processing_latency.record(duration_minutes * 60, {"agent": agent})

def record_regional_operation(region: str, country: str, operation_type: str):
    """Registra operação por região geográfica"""
    regional_operations.add(1, {
        "region": region,
        "country": country,
        "operation": operation_type
    })

def update_customer_count(country: str, delta: int):
    """Atualiza contagem de clientes ativos"""
    customers_served.add(delta, {"country": country})

def record_error(agent: str, error_type: str, severity: str = "medium"):
    """Registra erro ocorrido"""
    error_counter.add(1, {
        "agent": agent,
        "type": error_type,
        "severity": severity
    })

def update_sla_compliance(agent: str, compliance_ratio: float):
    """Atualiza métrica de conformidade SLA"""
    sla_compliance.record(compliance_ratio, {"agent": agent})
