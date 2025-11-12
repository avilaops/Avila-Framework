# On Platform - Arquitetura Completa

## 📁 Estrutura Final

```
On/
├── on/                          # Pacote Python principal
│   ├── __init__.py
│   └── core/                    # Núcleo da plataforma
│       ├── __init__.py
│       ├── on_core.py          # Facade principal
│       ├── on_bus.py           # Event bus (pub/sub)
│       ├── on_message.py       # Primitivas de mensagem
│       ├── on_logger.py        # Logging estruturado → Loki
│       ├── on_education.py     # Sistema de curriculo
│       ├── on_scheduler.py     # Scheduler + Self-healing
│       ├── on_storage.py       # Persistência SQLite
│       ├── on_health.py        # Health checks + heartbeats
│       ├── on_telemetry.py     # OpenTelemetry (traces + métricas)
│       └── on_supervisor.py    # CLI de supervisão
│
├── agents/                      # Agentes do ecossistema
│   ├── atlas/
│   ├── echo/
│   ├── forge/
│   ├── helix/                   # ✅ Exemplo instrumentado
│   │   ├── config.yaml
│   │   ├── README.md
│   │   ├── README_OBSERVABILITY.md
│   │   └── helix_agent.py       # Agente completo com telemetria
│   ├── lex/
│   ├── lumen/
│   ├── sigma/
│   └── vox/
│
├── observability/               # Stack de observabilidade
│   ├── docker-compose.yaml      # OTel + Prometheus + Loki + Tempo + Grafana
│   ├── otel-collector-config.yaml
│   ├── prometheus.yml
│   ├── tempo.yaml
│   ├── promtail-config.yaml
│   ├── grafana-datasources.yaml
│   ├── grafana-dashboards/
│   │   ├── dashboards.yaml
│   │   └── on-core-overview.json  # Dashboard pronto
│   └── README.md                # Documentação completa
│
├── data/                        # Dados em tempo de execução
│   ├── exchange/               # Troca de dados entre agentes
│   ├── metrics/                # Métricas exportadas
│   └── reports/                # Relatórios gerados
│
├── registry/                    # Estado persistente
│   ├── on_core.db              # SQLite (auto-criado)
│   ├── memory/                 # Currículos dos agentes
│   └── tasks/                  # Tarefas persistidas
│
├── logs/                        # Logs locais (backup)
│
├── scripts/                     # Utilitários
│   └── setup_agents.py
│
├── config.yaml                  # Configuração global
└── requirements.txt             # Dependências Python
```

## ✅ O Que Foi Implementado

### 1. **Persistência Real (SQLite)**
- ✅ `on_storage.py` com tabelas:
  - `logs` - Histórico de logs
  - `tasks` - Tarefas dos agentes
  - `shifts` - Turnos trabalhados
  - `agent_heartbeats` - Status de saúde
  - `agent_restarts` - Histórico de reinícios

### 2. **Telemetria Unificada (OpenTelemetry)**
- ✅ `on_telemetry.py` exportando para:
  - **Traces** → Tempo (análise de latência)
  - **Métricas** → Prometheus (monitoramento)
  - **Logs** → Loki (agregação)

### 3. **Logging Estruturado**
- ✅ `on_logger.py` com saída para:
  - SQLite (persistência local)
  - stdout (coleta por Promtail)
  - Formato estruturado para Loki

### 4. **Health Monitoring**
- ✅ `on_health.py` com:
  - Heartbeats automáticos
  - Verificação de status
  - Integração com métricas

### 5. **Self-Healing**
- ✅ `on_scheduler.py` com:
  - CoreScheduler que monitora agentes a cada 60s
  - Detecção de falhas (sem heartbeat > 2 min)
  - Restart automático via handlers
  - Registro de eventos

### 6. **Painel de Supervisão**
- ✅ `on_supervisor.py` - CLI interativo
- ✅ Grafana dashboards prontos
- ✅ Acesso sem programação (SQL queries visuais)

### 7. **Agente Exemplo (Helix)**
- ✅ Totalmente instrumentado
- ✅ Traces, métricas e logs
- ✅ Health monitoring
- ✅ Integração completa

## 🚀 Como Usar

### Iniciar Stack de Observabilidade
```bash
cd observability
docker-compose up -d
```

### Executar Supervisor CLI
```bash
python -m on.core.on_supervisor
```

### Executar Agente Helix
```bash
python -m agents.helix.helix_agent
```

### Acessar Grafana
http://localhost:3000 (admin/admin)

## 📊 Métricas Disponíveis

- `on_tasks_total{agent="..."}` - Tarefas criadas
- `on_shifts_total{agent="..."}` - Turnos completados
- `on_logs_total{agent="..."}` - Volume de logs
- `on_agent_heartbeat{agent="..."}` - Status (1=vivo, 0=morto)
- `helix_requests_total` - Requisições do Helix
- `helix_processing_duration_seconds` - Latência

## 🎯 Padrão Enterprise

Esta arquitetura segue os mesmos princípios usados por:
- **Google** (Borg, Kubernetes)
- **Azure** (Application Insights)
- **Tesla** (Factory OS)

Tudo integrado, observável e auto-recuperável.
