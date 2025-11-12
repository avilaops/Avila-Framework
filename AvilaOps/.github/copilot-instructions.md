# AvilaOps Copilot Instructions

**Version:** 1.0  
**Last Updated:** 2025-11-10  
**Scope:** AvilaOps engineering workspace

## Overview

AvilaOps is a multi-agent AI platform with distinct specialized agents coordinating via event bus and shared storage. This document guides AI coding agents on the actual architecture, patterns, and workflows discovered in the codebase.

---

## Architecture: The "On" Platform

### Core System (`ai/On/core/`)

The **On** platform is the runtime foundation for all agents:

- **`on_core.py`** (Facade): Boots agents, discovers configs, manages agent shifts, handles SIGINT/SIGTERM
- **`on_bus.py`** (Pub/Sub): Thread-safe EventBus with topic-based subscriptions for inter-agent communication
- **`on_storage.py`** (Persistence): SQLite with tables for logs, tasks, shifts, heartbeats, restarts
- **`on_logger.py`** (Structured Logging): Writes to SQLite + stdout (for Promtail collection → Loki)
- **`on_scheduler.py`** (Self-Healing): CoreScheduler monitors agents every 60s, auto-restarts on failure, 2-min heartbeat timeout
- **`on_health.py`** (Health Monitoring): Heartbeat emission and status checks
- **`on_telemetry.py`** (Observability): OpenTelemetry traces → Tempo, metrics → Prometheus, logs → Loki
- **`on_message.py`** (Message Primitives): Standardized message format for EventBus
- **`on_education.py`** (Curriculum): Agent learning/memory system (referenced but not yet detailed)
- **`on_supervisor.py`** (CLI): Interactive supervision dashboard without coding

### Agent Architecture (`ai/On/agents/{atlas,helix,echo,forge,lex,lumen,sigma,vox}/`)

Each agent has:
- **`config.yaml`**: Declares agent_name, area, significado, shift_min, permissions, model (gpt-4o)
- **`README.md`**: Functional description
- **`{agent_name}_agent.py`**: Implementation (helix example exists; others are scaffolding)

**Agent Responsibilities** (from `setup_agents.py`):
- Atlas: Strategy/Corporate (base of operations)
- Helix: Engineering/DevOps (technical DNA)
- Sigma: Finance/Accounting (math & precision)
- Vox: Sales/CRM (company voice)
- Lumen: Research & Applied AI (clarity, insight)
- Forge: Production/Manufacturing (creation)
- Lex: Legal/Compliance (law & standardization)
- Echo: Communications/Branding (brand message relay)

### Data & Registry (`ai/On/data/`, `ai/On/registry/`)

- **`exchange/`**: Inter-agent data sharing (implementation TBD)
- **`metrics/`**: Exported metrics from agents
- **`reports/`**: Generated reports
- **`on_core.db`**: SQLite auto-created on first run
- **`memory/`**: Agent curricula/knowledge persistence
- **`tasks/`**: Persisted task queue

### Observability Stack (`ai/On/observability/`)

Docker Compose deployment with:
- OpenTelemetry Collector (OTLP receiver on :4317)
- Prometheus (metrics scraping on :9090)
- Loki (log aggregation)
- Tempo (distributed tracing)
- Grafana (visualization on :3000, admin/admin)

---

## Governance & Curation: Archivus Agent

**Purpose**: Institutional librarian ensuring compliance, integrity, and documentation governance.

### Monitored Structure
```
Docs/Relatorios/{Conversas, Analises, Auditorias, Comparacoes, Diagnosticos, Performance}
Logs/{Daily, Alerts, Archive}
Scripts/{Backup, Maintenance, Verify}
Shared/{backups/archivus, scripts, templates}
```

### Automated Routines
- **Daily (02:00)**: Structure validation, log rotation (>30 days → Archive), metrics collection, audit report generation
- **Weekly (Sunday 03:00)**: Backup Scripts/ to ZIP, SHA256 integrity verification, manifest update
- **Monthly (1st, 04:00)**: Deep archival, log compression, cleanup old backups

### Key Files
- **`integrity_manifest.json`**: SHA256 hashes of all scripts with timestamps
- **`AUDITORIA_ARCHIVUS_YYYY-MM-DD.md`**: Daily compliance report

### Integration Points
- Atlas receives daily compliance reports; alerts on integrity divergence
- Helix receives backup failure alerts; notified of script modifications

---

## Project-Specific Patterns & Conventions

### 1. **Config-Driven Discovery**
Agents are NOT hardcoded. On-Core scans `agents/` folder, reads each `config.yaml`, and dynamically registers agents with their declared shift_min (default 60 min).

**Pattern**: When adding new agents, ensure:
```yaml
agent_name: {name}
area: {category}
significado: {metaphor}
shift_min: 60
model: gpt-4o
permissions:
  read: [paths]
  write: [paths]
  sync: true
```

### 2. **Event-Driven Inter-Agent Communication**
Agents communicate via topic-based pub/sub on EventBus, NOT via direct calls.

**Pattern**:
```python
# Agent A publishes:
message = Message(topic="data_analysis_complete", payload={"result": ...})
event_bus.publish(message)

# Agent B subscribes:
event_bus.subscribe("data_analysis_complete", handle_analysis)
```

### 3. **Structured Logging & Persistence**
All logging goes through `AgentLogger`, which writes to:
- SQLite `logs` table (queryable)
- stdout in structured format (Promtail → Loki)

**Pattern**:
```python
from on.core.on_logger import AgentLogger
logger = AgentLogger("AgentName")
logger.log("Action completed")  # Stored + streamed
```

### 4. **Health & Auto-Recovery**
Agents MUST emit heartbeats via `on_health.py`. CoreScheduler polls every 60s; >2 min silence = restart.

**Pattern**:
```python
from on.core.on_health import emit_heartbeat
# In agent loop:
emit_heartbeat("agent_name")
```

### 5. **Observability First**
Telemetry is not optional. Agents should instrument with:
- **Traces** (via OpenTelemetry): Mark spans for latency analysis
- **Metrics** (Counter, Gauge, Histogram): Track operations
- **Logs** (structured, JSON-compatible): Debug & audit

**Pattern** (from helix example):
```python
from on.core.on_telemetry import tracer, meter
with tracer.start_as_current_span("operation_name") as span:
    span.set_attribute("key", "value")
    # operation
```

### 6. **Markdown Docs + YAML Configs**
All significant components must have:
- `README.md`: Purpose, function, configuration
- `config.yaml`: Declarative settings (versioning, permissions, routing)

**File Encoding**: UTF-8 (no BOM)  
**Indentation**: YAML & JSON = 2 spaces, Python = 4 spaces

### 7. **Shift-Based Task Execution**
Agents don't run continuously; they work in declared shifts (e.g., 60 min). Scheduler awakens, agent executes, scheduler logs completion.

**Pattern**: Define `shift_min` in config.yaml; On-Core manages lifecycle.

---

## Critical Developer Workflows

### 1. **Bootstrap & Namespace**
`_bootstrap.py` ensures Python can import `on.*` packages even when running from different directories.

**Always ensure** imports use `ensure_on_namespace()` before importing `on` modules:
```python
from on.core._bootstrap import ensure_on_namespace
ensure_on_namespace()
from on.core.on_core import OnCoreApp
```

### 2. **Running On-Core (Service Mode)**
```bash
cd c:\Users\nicol\OneDrive\Avila\AvilaOps\ai\On
python -m on.core.on_core
```
Boots agents, starts shifts, runs forever (Ctrl+C to stop).

### 3. **Running Single Agent**
```bash
cd c:\Users\nicol\OneDrive\Avila\AvilaOps\ai\On
python -m agents.helix.helix_agent
```

### 4. **Observability Stack**
```bash
cd c:\Users\nicol\OneDrive\Avila\AvilaOps\ai\On\observability
docker-compose up -d
# Access Grafana: http://localhost:3000
```

### 5. **Querying Logs & Metrics**
```python
from on.core.on_storage import get_db
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM logs WHERE agent='agent_name' ORDER BY timestamp DESC LIMIT 10")
for row in cursor:
    print(row)
```

### 6. **Checking Agent Health**
Via Grafana dashboard (`grafana-dashboards/on-core-overview.json`) or:
```sql
SELECT agent, MAX(timestamp) as last_heartbeat FROM agent_heartbeats GROUP BY agent;
```

---

## Cross-Component Integration Points

### **OnCore → Agents**
1. Discovers agents in `agents/` folder (config-driven)
2. Creates Scheduler for each agent
3. Scheduler manages shift lifecycle (startup → run → log → sleep)
4. EventBus pub/sub available globally

### **Agents → Storage**
All persistent state flows through SQLite (`on_storage.py`):
- Logs (for audit)
- Tasks (for queue)
- Shifts (for history)
- Heartbeats (for health)
- Restarts (for diagnostics)

### **Agents → Observability**
On-Telemetry exports:
- Traces to Tempo (http://localhost:4317 via OTLP gRPC)
- Metrics to Prometheus (scraped from agents)
- Logs to stdout (Promtail → Loki)

### **Archivus → Other Agents**
- Publishes daily audit reports to `Docs/Relatorios/Auditorias/`
- Publishes alerts to EventBus topic `archivus_alert` for Atlas & Helix
- Manifests maintained in `integrity_manifest.json`

---

## Key Files & Their Roles

| File | Purpose | Editor Should Know |
|------|---------|-------------------|
| `ai/On/setup_agents.py` | Agent scaffolding generator | Modify to add new agent types; auto-creates config.yaml + README |
| `ai/On/core/on_core.py` | Service bootstrap | Entry point; discovery + shift management; never directly invoke agents |
| `ai/On/core/on_bus.py` | Event pub/sub | Lightweight (no external broker); topics are strings; errors logged but don't crash |
| `ai/On/core/on_storage.py` | SQLite schema | Tables auto-created; context manager for safe connections |
| `ai/On/core/config.yaml` | Global On config | vault_path, language_model, agents_path, permissions |
| `Agente Bibliotecario (Archivus)/archivus_main.py` | Daily compliance | Runs independently; produces audit logs + manifests |
| `governance/ARCHITECTURE.md` | System reference | High-level overview of On platform; reference for new features |

---

## Do's & Don'ts

### Do's
- ✅ Read agent `config.yaml` before modifying agent behavior
- ✅ Use EventBus for inter-agent communication (publish messages, subscribe to topics)
- ✅ Call `AgentLogger` for all logging (not print())
- ✅ Emit heartbeats from long-running agents
- ✅ Instrument with OpenTelemetry for production readiness
- ✅ Validate configs with YAML schema before deploying
- ✅ Test agents in isolation before integrating with On-Core
- ✅ Keep shifts short & focused (60 min default; adjust as needed)

### Don'ts
- ❌ Hardcode agent discovery (use filesystem scanning + config.yaml)
- ❌ Use direct inter-agent function calls (use EventBus)
- ❌ Print logs instead of using AgentLogger
- ❌ Assume agents run continuously (they run in shifts)
- ❌ Ignore heartbeat monitoring (CoreScheduler restarts on silence)
- ❌ Deploy agents without observability instrumentation
- ❌ Modify On-Core bootstrap without understanding import namespacing
- ❌ Create files outside `Docs/`, `Logs/`, `Scripts/`, `Shared/` (Archivus will flag as non-compliant)

---

## Common Modifications & Examples

### Adding a New Agent
1. Create folder: `ai/On/agents/{new_agent}/`
2. Create `config.yaml` with agent_name, area, significado, shift_min, model
3. Create `README.md` describing function
4. Implement `{new_agent}_agent.py` with:
   - Import bootstrap
   - AgentLogger for logging
   - EventBus subscriptions/publishes
   - Heartbeat emission
   - Telemetry instrumentation
5. On-Core auto-discovers on next boot

### Publishing Inter-Agent Message
```python
from on.core.on_bus import EventBus
from on.core.on_message import Message

bus = EventBus()
msg = Message(topic="helix_deployment_ready", payload={"service": "api", "version": "1.2.3"})
bus.publish(msg)
```

### Querying Agent Logs
```python
from on.core.on_storage import get_db
conn = get_db()
cursor = conn.cursor()
cursor.execute("SELECT * FROM logs WHERE agent=? ORDER BY timestamp DESC LIMIT 20", ("helix",))
for row in cursor.fetchall():
    print(f"{row[0]}: {row[2]}")  # timestamp + message
```

### Checking Agent Heartbeats
```sql
SELECT agent, MAX(timestamp) as last_heartbeat, 
       CAST((julianday('now') - julianday(MAX(timestamp))) * 1440 AS INTEGER) as minutes_ago
FROM agent_heartbeats 
GROUP BY agent;
```

---

## Notes for Future Development

- **`on_education.py`**: Curriculum system referenced but not yet implemented. Future agents may learn from execution history.
- **`exchange/` data sharing**: Inter-agent data exchange is planned but currently under development.
- **Vox agent**: Commercial/CRM agent exists in scaffolding; full implementation pending.
- **Orchestrator**: Central orchestration agent exists but details TBD.

---

## Questions to Ask Before Modifying Core

1. **Is this an agent change or core platform change?**
   - Agent: Modify in `agents/{agent}/`
   - Core: Coordinate with On-Core maintainer; impacts all agents

2. **Does this require inter-agent communication?**
   - Yes: Use EventBus with a new topic (document in README)
   - No: Keep in agent-local storage

3. **Will this impact observability?**
   - Yes: Update telemetry setup; test with docker-compose observability stack
   - No: Still should add basic instrumentation

4. **Is this a new persistent state?**
   - Yes: Add table to on_storage.py schema; run migration
   - No: Use EventBus or in-memory state (won't persist across restarts)

---

**For questions or updates, reference `governance/ARCHITECTURE.md` and review the Archivus audit logs in `Docs/Relatorios/Auditorias/`.**
