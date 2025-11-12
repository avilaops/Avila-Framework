# On.Core - Arquitetura de Observabilidade Corporativa

## Contexto
Infraestrutura oficial de observabilidade que suporta agentes On e produtos Ávila, baseada em OpenTelemetry e stack Grafana Labs.

## Objetivo
Fornecer telemetria unificada (logs, métricas, traces) com dashboards, alertas e playbooks para operação 24/7.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11

---

Este diretório contém toda a infraestrutura de observabilidade da plataforma On, seguindo as melhores práticas de empresas como Google, Azure e Tesla.

## 📊 Stack de Observabilidade

### Componentes

1. **OpenTelemetry Collector** - Gateway central para telemetria
2. **Prometheus** - Armazenamento e consulta de métricas
3. **Loki** - Agregação de logs
4. **Tempo** - Backend de traces distribuídos
5. **Grafana** - Visualização e dashboards
6. **Promtail** - Coleta de logs (opcional)

## 🚀 Início Rápido

### 1. Subir a Stack

```bash
cd observability
docker-compose up -d
```

### 2. Verificar Serviços

```bash
docker-compose ps
```

Todos os serviços devem estar "Up".

### 3. Acessar Interfaces

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Tempo**: http://localhost:3200

### 4. Executar Agente Instrumentado

```bash
cd ..
python -m agents.helix.helix_agent
```

## 📈 Dashboards Disponíveis

### On.Core - Visão Geral
- Tarefas por minuto (por agente)
- Status de heartbeat dos agentes
- Logs recentes
- Turnos completados
- Volume de logs

Para acessar: Grafana → Dashboards → On Core - Visão Geral

## 🔍 Como Funciona

### Fluxo de Telemetria

```
┌──────────────┐
│ Agente       │
│  (Python)    │
└──────┬───────┘
       │ OpenTelemetry SDK
       ▼
┌──────────────┐
│ OTel         │
│ Collector    │ :4317 (gRPC)
└──┬───┬───┬───┘
   │   │   │
   │   │   └──────────────┐
   │   │                  │
   ▼   ▼                  ▼
┌─────┐ ┌─────┐      ┌─────┐
│Prom │ │Loki │      │Tempo│
│9090 │ │3100 │      │3200 │
└──┬──┘ └──┬──┘      └──┬──┘
   │       │            │
   └───────┴────────────┘
           │
           ▼
      ┌─────────┐
      │ Grafana │ :3000
      └─────────┘
```

### Tipos de Telemetria

#### 1. **Traces** (Tempo)
- Rastreamento de requisições end-to-end
- Correlação entre serviços
- Análise de latência

#### 2. **Métricas** (Prometheus)
- `on_tasks_total` - Tarefas criadas
- `on_shifts_total` - Turnos completados
- `on_logs_total` - Volume de logs
- `on_agent_heartbeat` - Status dos agentes
- Métricas customizadas por agente

#### 3. **Logs** (Loki)
- Logs estruturados com contexto
- Filtragem por agente
- Correlação com traces

## 🛠️ Configuração

### Variáveis de Ambiente

Os agentes podem ser configurados via variáveis:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
export OTEL_SERVICE_NAME="avilaops-on"
```

### Customização de Dashboards

1. Acesse Grafana
2. Navegue até o dashboard
3. Clique em "Settings" → "JSON Model"
4. Edite e salve

Os dashboards também podem ser editados em:
`grafana-dashboards/*.json`

## 📊 Queries Úteis

### Prometheus

```promql
# Taxa de tarefas por agente
rate(on_tasks_total[5m])

# Agentes com heartbeat ativo
on_agent_heartbeat == 1

# Tempo médio de processamento (Helix)
rate(helix_processing_duration_seconds_sum[5m]) / 
rate(helix_processing_duration_seconds_count[5m])
```

### Loki

```logql
# Todos os logs do Helix
{job="on-core"} |= "Helix"

# Erros nos últimos 5 minutos
{job="on-core"} |= "ERROR" | __error__=""

# Logs por nível
{job="on-core"} | json | level="ERROR"
```

### Tempo

As queries são feitas automaticamente quando você:
1. Vai em Grafana → Explore
2. Seleciona "Tempo" como datasource
3. Busca por trace ID ou service name

## 🔔 Alertas

### Configurar Alertmanager

1. Adicione ao `docker-compose.yaml`:

```yaml
alertmanager:
  image: prom/alertmanager:latest
  ports:
    - "9093:9093"
  volumes:
    - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
```

2. Crie regras de alerta em `prometheus.yml`:

```yaml
rule_files:
  - "alerts.yml"
```

3. Exemplo de alerta (`alerts.yml`):

```yaml
groups:
  - name: on_core_alerts
    interval: 30s
    rules:
      - alert: AgentDown
        expr: on_agent_heartbeat == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent }} is down"
```

## 🧪 Testando a Stack

### 1. Gerar Métricas de Teste

```bash
python -c "
from on.core.on_core import OnCore
from on.core.on_telemetry import task_counter

core = OnCore()
for i in range(100):
    task_counter.add(1, {'agent': 'test'})
print('Métricas enviadas!')
"
```

### 2. Verificar no Prometheus

1. Acesse http://localhost:9090
2. Query: `on_tasks_total`
3. Deve aparecer a métrica com valor ~100

### 3. Verificar Logs no Grafana

1. Grafana → Explore
2. Selecione "Loki"
3. Query: `{job="on-core"}`

## 🐛 Troubleshooting

### Collector não recebe métricas

```bash
# Verificar logs do collector
docker logs on-otel-collector

# Verificar se porta está aberta
curl http://localhost:4317
```

### Grafana não mostra dados

```bash
# Verificar datasources
# Grafana → Configuration → Data Sources

# Testar conexão
# Cada datasource tem botão "Test"
```

### Métricas não aparecem no Prometheus

```bash
# Verificar targets
# http://localhost:9090/targets

# Deve mostrar otel-collector como UP
```

## 📚 Recursos

- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Query Examples](https://prometheus.io/docs/prometheus/latest/querying/examples/)
- [Loki LogQL](https://grafana.com/docs/loki/latest/logql/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)

## 🎯 Próximos Passos

1. **Fase 1** ✅ - Stack básica configurada
2. **Fase 2** 🔄 - Instrumentar todos os agentes
3. **Fase 3** - Adicionar alertas personalizados
4. **Fase 4** - Integrar com Alertmanager (email/Telegram)
5. **Fase 5** - Métricas de negócio (vendas, notas, etc)

## 💡 Dicas

- Use tags/labels consistentes em todas as métricas
- Nomeie métricas seguindo convenção: `<namespace>_<name>_<unit>`
- Logs estruturados facilitam queries no Loki
- Traces ajudam a debugar problemas de performance
- Dashboards devem contar uma história
