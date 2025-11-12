# AvilaOps Product Compliance and Synchronization Plan (2025-11-12)

## Scope
- Consolidate a portfolio view for every product under `products/`
- Map corporate norms from `governance/`, `docs/styleguides/`, `docs/security_policies/`
- Define integration hooks for the On platform (`ai/On`) and Archivus (`ai/📚 Agente Bibliotecario (Archivus)`)

## Corporate Standards Snapshot
- **Governance hub**: `governance/README.md`, `governance/ARCHITECTURE.md`, `governance/PROCEDIMENTO_SETUP_GITHUB.md` establish process ownership, architecture guardrails, and commit discipline
- **Style guides**: `docs/styleguides/README.md` (code/doc/data design baselines) to be cited in every product README and contribution guide
- **Security baseline**: `docs/security_policies/README.md` plus forthcoming `policies/` tree governs retention, classification, incident response; all products must log ownership and data class
- **Observability + self healing**: `ai/On/core/*.py` requires metrics, traces, and heartbeats for any service promoted into production
- **Knowledge lifecycle**: Archivus agent (see `ai/STATUS.md`, `ai/📚 Agente Bibliotecario (Archivus)/README.md`) indexes authoritative docs placed under `ai/📚 Agente Bibliotecario (Archivus)/data`

## Portfolio Overview (2025-11-12)

| Product | Owner | Maturity | Core Stack | Compliance Highlights | On Hooks | Archivus Sync |
| --- | --- | --- | --- | --- | --- | --- |
| ArcSat | Forge Squad (Industria) | Domain foundation | .NET DDD domain layer | Needs tests + policy references | Model domain events for scheduler | Index `products/ArcSat/README.md`
| Barbara | Forge Squad + Atlas | MVP build (30%) | ASP.NET Core, Python AI, Next.js, Babylon.js | Follow style guides, add security baseline ref | Register AI service telemetry in On | Capture README set + roadmap
| Camacho | Forge Squad | Azure web app live | Next.js + Supabase | Ensure LGPD notice + commit policy | Publish deploy events to On bus | Add `docs/` tree to Archivus
| Controle-Roncatin | Forge Squad | Cross platform beta | .NET MAUI + SQLite | Confirm data class (confidential) + backup policy | Expose telemetry to On metrics endpoint | Sync README + manuals
| CoreDesk | Atlas Squad | Documentation only | TBD (service desk) | Must register owner + security contact | Create backlog in On scheduler | Archive README here
| Geolocation | Atlas Squad (Dados) | Production | Rust backend + React frontend + Azure | Already documented; add LGPD handling and secrets policy references | Wire Prometheus scrape into On observability stack | Sync `ARCHITECTURE.md` + deploy notes
| Insight | Lumen Squad | Doc placeholder | Analytics notebooks, front/back TBD | Needs security and data classification notes | Define Insight->On data contract | Add README
| Knowledge | Atlas Squad | Governance note | Knowledge base process document | Formalize location under security policies | Align curriculum with On education | Ingest governance note
| MindLayer | Atlas + Lumen | Platform design | Agents + APIs + orchestration docs | Reference policies for AI lifecycle | Register agent catalog in On/Atlas queue | Sync README
| On Dashboard | Helix Squad | Working prototype | FastAPI + Redis + Prometheus + simple frontend | Add style guide link, note data retention | Emit metrics to On collector (already Prometheus) | Add backend README (create) and current docs
| OpsFlow | Helix Squad | Operational | Workflow engine (docs) | Document auth/monitoring map | Ensure workflows publish events via On | Archive README
| Padaria | Pending | Empty | TBD | Document status + owner | No integration until scoped | Track stub entry only
| Padaria-Vendas | Forge Squad | Dev | Flask + HTML + SQLite | Add security baseline and data classification | Register pilot tasks in On | Sync docs README
| Pulse | Atlas Squad | Operational | Dashboards + collectors planned | Need metrics ownership + update cadence | Feed metrics into On telemetry | Sync README
| Report Framework | Echo + Atlas | GA release | Python reporting framework + GUI | Already references policies; add LGPD section | Use `agents_integration.py` to stream events | Sync README/guide
| Roncav Budget | Sigma Squad | Production-grade MVP | .NET MAUI + SQLite | Add fintech compliance section referencing Lex | Send finance alerts via On bus | Sync README
| Secreta | Forge + Helix | Monorepo skeleton | Next.js + Express monorepo | Add security gating and workspace linting | Connect pipelines to On agent `forge` | Sync README, setup notes
| Shancrys | Forge Squad | Large program (multi modules) | .NET, BIM engine, mobile | Document security boundaries per module | Register milestones with On orchestrator | Sync `specs/` set
| Windows Dev Optimizer | OpsFlow Squad | Production | FastAPI backend + desktop launcher | Ensure security posture documented `validate_governance.ps1` | Maintain On integration module | Sync README + governance scripts

## Product Deep Dives

### ArcSat
- **Focus**: Domain model for industrial/finance platform; aggregates, value objects, contracts already implemented
- **Assets**: `src/` projects, README with DDD scope
- **Compliance baseline**: Needs explicit link to `docs/styleguides` and `docs/security_policies`; add architecture reference in README
- **Gaps**: Missing services/events tests; no data classification entry
- **On integration**: Expose domain events for scheduling in `ai/On/core/on_bus.py`; record restart policy once application layer exists
- **Archivus**: Copy README and upcoming `docs/` tree into Archivus data for search

### Barbara
- **Focus**: E-commerce with 3D fitting room and AI sizing
- **Assets**: Extensive deployment guides, architecture doc, roadmap
- **Compliance baseline**: Reference governance and security docs in README set; add privacy notice for biometric models per `docs/security_policies`
- **Gaps**: Missing telemetry integration notes, LGPD compliance matrix
- **On integration**: Update AI orchestrator connectors to publish events through On bus and register schedules with `Scheduler`
- **Archivus**: Ensure `README-BARBARA.md`, architecture, deployment guides added to Archivus dataset

### Camacho
- **Focus**: Next.js ordering platform with Supabase backend and Azure deployment pipeline
- **Assets**: `docs/` folder with quickstart, API, deployment
- **Compliance baseline**: Must append style/security references, specify data retention for Supabase tables
- **Gaps**: Privacy policy for customer data; On telemetry not configured
- **On integration**: Configure deploy workflows to emit events to On event bus (`deploy.status`) and register health checks in `on_health`
- **Archivus**: Sync full `docs/` directory

### Controle Roncatin
- **Focus**: Recycling management app using .NET MAUI + Blazor Hybrid
- **Assets**: README, manuals, deployment scripts
- **Compliance baseline**: Add classification (confidential) and backup policy references
- **Gaps**: Data encryption notes, telemetry integration
- **On integration**: Extend existing logging to push metrics via `on_metrics` exporter; schedule nightly backup tasks in On scheduler
- **Archivus**: Include README, user manual, distribution guide in Archivus data

### CoreDesk
- **Focus**: Service desk solution structuring documentation
- **Assets**: README outlines structure
- **Compliance baseline**: Document owners, security, governance references
- **Gaps**: Implementation assets missing; backlog not in On
- **On integration**: Create On tasks for integration with agents (Atlas for governance, Helix for automation)
- **Archivus**: Add README to Archivus so knowledge base surfaces status

### Geolocation
- **Focus**: Production geo/fiscal engine with Rust backend, React frontend, Azure infra
- **Assets**: Extensive README, architecture, deployment scripts
- **Compliance baseline**: Already mature; ensure LGPD compliance and secrets handling documented referencing `docs/security_policies`
- **Gaps**: Document Data Protection Impact Assessment; align logging retention with retention policies
- **On integration**: Connect Prometheus metrics to On observability stack; ensure On scheduler monitors ingestion queues
- **Archivus**: Sync `README.md`, `ARCHITECTURE.md`, `README-DEPLOY.md`

### Insight
- **Focus**: Analytics platform placeholder
- **Assets**: README with structure
- **Compliance baseline**: Add references to governance, style, security; classify data sources
- **Gaps**: Need data lineage and security requirements
- **On integration**: Define integration with On agents (Lumen for analytics, Helix for pipelines)
- **Archivus**: Add README for discovery

### Knowledge
- **Focus**: Governance of knowledge base
- **Assets**: Process note `Estrutura de dados e governanca.md`
- **Compliance baseline**: Align with Archivus ingestion process and security classification
- **Gaps**: Convert note into actionable SOP under governance
- **On integration**: Provide curriculum inputs for `on_education.py`
- **Archivus**: Already concept; ensure document is ingested for recall

### MindLayer
- **Focus**: Cognitive layer orchestrating agents/APIs
- **Assets**: README with structure
- **Compliance baseline**: Add policies for model lifecycle and monitoring references
- **Gaps**: Missing SLO definitions; On integration plan pending
- **On integration**: Document links between MindLayer agents and On event bus
- **Archivus**: Sync README

### On Dashboard
- **Focus**: FastAPI backend + WebSocket metrics with Prometheus integration
- **Assets**: Backend code, minimal frontend
- **Compliance baseline**: Need README (create) referencing style/security; categorize data sensitivity
- **Gaps**: Document retention and access control; On integration partially done via metrics but not documented
- **On integration**: Register metrics exporter with On observability; configure scheduler for WebSocket health
- **Archivus**: Add backend overview (this plan references location until README is created)

### OpsFlow
- **Focus**: Operational automation platform (workflow engine)
- **Assets**: README describing structure
- **Compliance baseline**: Document SLAs, security, style references
- **Gaps**: Workflows inventory and monitoring not yet captured
- **On integration**: Map On agents executing workflows; ensure events use On bus topics
- **Archivus**: Sync README

### Padaria
- **Focus**: Empty placeholder
- **Actions**: Assign owner, define scope, update README referencing governance before development
- **On integration**: None until charter created
- **Archivus**: Keep stub entry once documentation exists

### Padaria Vendas
- **Focus**: Flask + static frontend for bakery sales
- **Assets**: README with structure and setup
- **Compliance baseline**: Add security/data classification; commit policy references
- **Gaps**: Telemetry, On integration, privacy statement
- **On integration**: Register pilot tasks in On scheduler; log orders to On metrics once backend active
- **Archivus**: Sync docs README

### Pulse
- **Focus**: Executive telemetry hub
- **Assets**: README with structure
- **Compliance baseline**: Add style/security references; ensure dashboards align with data retention policies
- **Gaps**: Collector implementation linking to On watchers
- **On integration**: Bind collectors to On observability; ensure Atlas agent receives updates
- **Archivus**: Sync README

### Report Framework
- **Focus**: Corporate reporting framework with multi channel exporters
- **Assets**: README, integration guide, code
- **Compliance baseline**: Already references policies; ensure LGPD matrix included for report data
- **Gaps**: Automate Archivus validations in pipelines
- **On integration**: Finish `agents_integration.py` hooks so On agents can request reports; instrument metrics
- **Archivus**: Sync README and integration guide for support knowledge

### Roncav Budget
- **Focus**: Personal finance app with MAUI + SQLite
- **Assets**: README, guides
- **Compliance baseline**: Add fintech/regulatory references via Lex; classify dataset as restricted
- **Gaps**: Document encryption, audit trails, On integration
- **On integration**: Publish budget alerts into On bus; schedule backups under On scheduler
- **Archivus**: Sync README and implementation guide

### Secreta
- **Focus**: Gamified metaverse monorepo (Next.js + Express)
- **Assets**: README, instructions, monorepo config
- **Compliance baseline**: Add style/security references, define code ownership per workspace
- **Gaps**: Security gating for shared packages, On integration plan
- **On integration**: Connect pipelines to On orchestrator (Forge) and log release tasks
- **Archivus**: Sync README, setup notes

### Shancrys
- **Focus**: Construction 4D platform with multiple modules (engine, frontend, mobile)
- **Assets**: Specs, engine docs, frontend technical foundation
- **Compliance baseline**: Need explicit security boundaries, retention per module, style references
- **Gaps**: Integration tasks not documented; On orchestrator plan missing
- **On integration**: Register module roadmaps with On orchestrator agent; ensure telemetry exported per module
- **Archivus**: Sync `specs/` and module readmes

### Windows Dev Optimizer
- **Focus**: Windows optimization suite with FastAPI backend and desktop shell
- **Assets**: README, governance validation scripts, modules
- **Compliance baseline**: `validate_governance.ps1` needs to point to current policies; ensure privacy of telemetry
- **Gaps**: Document data retention, On integration health checks
- **On integration**: Maintain `framework/core/on_integration.py`; ensure scheduler handles update cadences
- **Archivus**: Sync README and governance scripts for support knowledge

## On Synchronization Workplan
- **Atlas** (`ai/On/agents/atlas`): Load `ai/On/data/knowledge_base/products_portfolio_compliance.md`, track owner assignments, raise governance alerts via `atlas/alinhamento`
- **Helix** (`ai/On/agents/helix`): Derive automation backlog (deploy pipelines, telemetry hookups) from the plan; register tasks in On scheduler and observability stack
- **Sigma** (`ai/On/agents/sigma`): Monitor financial/compliance heavy products (Roncav Budget, Report Framework) and ensure cost and regulatory metrics align with policies
- **Lumen** (`ai/On/agents/lumen`): Prioritize analytics/AI integration tasks (Insight, MindLayer, Barbara AI services) and deliver ML governance updates
- **Forge** (`ai/On/agents/forge`): Coordinate heavy build programs (ArcSat, Shancrys, Secreta) and keep orchestrator informed on release cadence
- **Vox** (`ai/On/agents/vox`): Prepare communication packages referencing this plan for stakeholders; ensure CRM narratives updated
- **Lex** (`ai/On/agents/lex`): Validate compliance with `docs/security_policies` and LGPD for customer facing products; file findings in governance log
- **Echo** (`ai/On/agents/echo`): Produce documentation updates and meeting notes referencing this plan for Archivus ingestion
- **Orchestrator** (`ai/On/agents/orchestrator`): Register master timeline, map cross product dependencies, and surface blockers to On core metrics

## Archivus Synchronization Steps
1. Copy this plan into `ai/📚 Agente Bibliotecario (Archivus)/data/Portfolio-Compliance-Sync.md` (done in this change)
2. Verify Archivus dataset indexing:
   - `pwsh> cd ai`
   - `pwsh> python archivus_hotfix.py` (temporary) or execute `python index_all_docs.py`
3. Confirm Archivus search returns portfolio entries (query "Portfolio compliance plan")
4. Ensure future product docs are duplicated into Archivus `data/` prior to publishing roadmaps so the RAG layer remains updated

## Milestones and Next Actions
- **2025-11-13**: Atlas + Helix validate owner assignments and create On tasks
- **2025-11-15**: Archivus reindex completed, search tested, plan linked in dashboards
- **2025-11-20**: Lex delivers compliance review addenda (LGPD, security) for Camacho, Barbara, Roncav Budget
- **2025-11-25**: Helix finishes instrumentation backlog for Geolocation, Windows Dev Optimizer, Report Framework
- **2025-12-05**: Forge publishes integrated roadmap for ArcSat, Shancrys, Secreta referencing On orchestrator schedule

## Traceability
- Source standards: `governance/` hub, `docs/styleguides/`, `docs/security_policies/`
- On platform integration references: `ai/On/core/*`, agent readmes under `ai/On/agents/`
- Archivus integration references: `ai/STATUS.md`, `ai/index_all_docs.py`, `ai/📚 Agente Bibliotecario (Archivus)/README.md`
