# Products Portfolio Compliance Sync (2025-11-12)

## Purpose
- Single source of truth for product ownership, maturity, and compliance status
- Align On agents with tasks defined in `docs/products/PORTFOLIO_COMPLIANCE_SYNC.md`
- Ensure Archivus knowledge base remains in sync with portfolio changes

## Key Standards
- Governance: `governance/README.md`, `governance/ARCHITECTURE.md`
- Commit discipline: `governance/PROCEDIMENTO_SETUP_GITHUB.md`
- Style guides: `docs/styleguides/README.md`
- Security baseline: `docs/security_policies/README.md`

## Agent Responsibilities
- **Atlas**: track owner assignments, escalate governance gaps, update executive dashboards
- **Helix**: instrument telemetry for Geolocation, Windows Dev Optimizer, Report Framework; update CI/CD pipelines
- **Sigma**: review financial compliance for Roncav Budget and Report Framework
- **Lumen**: supervise analytics/AI programs (Insight, MindLayer, Barbara AI stack)
- **Forge**: coordinate large builds (ArcSat, Shancrys, Secreta) and feed orchestrator schedule
- **Vox**: prepare stakeholder messaging using compliance plan highlights
- **Lex**: deliver LGPD/security reviews for consumer products (Camacho, Barbara, Roncav Budget)
- **Echo**: document progress and push updates to Archivus
- **Orchestrator**: maintain cross product timeline and dependencies

## Immediate Actions (Nov 2025)
1. Atlas + Helix create On tasks for telemetry and governance by 2025-11-13
2. Archivus reindex after plan publication (`python index_all_docs.py`) by 2025-11-15
3. Lex issues compliance addenda for Camacho, Barbara, Roncav Budget by 2025-11-20
4. Forge publishes integrated roadmap for ArcSat, Shancrys, Secreta by 2025-12-05

## Product Highlights
- **Geolocation**: production hardened; ensure LGPD documentation and Prometheus feed into On metrics
- **Barbara**: MVP in progress; add biometric privacy notes and On telemetry for AI pipelines
- **Camacho**: live Azure deployment; enforce privacy notice and publish deploy events to On bus
- **Controle Roncatin**: requires data classification and backup tasks scheduled in On
- **Roncav Budget**: mark data as restricted; integrate finance alerts with On
- **Report Framework**: finalize agents integration to allow automated report requests
- **Shancrys**: document module boundaries; register milestones with On orchestrator
- **Windows Dev Optimizer**: validate governance script references; keep On integration module current

## Archivus Sync Checklist
- `docs/products/PORTFOLIO_COMPLIANCE_SYNC.md`
- `ai/📚 Agente Bibliotecario (Archivus)/data/Portfolio-Compliance-Sync.md`
- All product readmes and specs listed in the plan

## Monitoring
- Telemetry endpoints must export Prometheus metrics readable by `ai/On/core/on_metrics.py`
- Health checks registered in On scheduler for services with uptime requirements
- Archivus status tracked via `ai/STATUS.md`

## Change Control
- Update this file and the master plan whenever product ownership, maturity, or compliance posture changes
- Notify Archivus via `index_all_docs.py` run and log change in governance meeting notes
