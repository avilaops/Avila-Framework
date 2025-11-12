# Copilot Instructions for Ávila Inc

## Project Overview
Ávila Inc is a Brazilian business consulting firm focused on **reducing costs and increasing revenue** for clients through practical, measurable, and ethical consulting. We operate with **100% human service** (AI assists but never replaces human judgment) and maintain governance-first organizational structure with bilingual operations targeting Brazilian and Portuguese markets.

## Core Values & Operational Principles

### Mission-Critical Values (Non-negotiable)
1. **Client First**: All decisions must drive real financial impact (cost reduction + revenue increase)
2. **Human Excellence**: Clear, respectful, and resolution-focused service with empathy + action
3. **Ethics & Transparency**: No questionable shortcuts; declare conflicts of interest
4. **Privacy-First**: Minimal collection, explicit purpose, short retention, anonymization by default
5. **Analytical Rigor**: Testable hypotheses, verifiable metrics, continuous learning
6. **AI Responsibility**: AI assistive with human oversight; **FORBIDDEN** to train models with client data
7. **Operational Discipline**: Versioned processes, auditing, continuous improvement
8. **Results Over Vanity**: Prefer P&L and cash flow over social media metrics

### Mandatory Workflow Philosophy
- **Problem → Hypothesis → Experiment → Result**: Short cycles, solid evidence
- **Content and operations as code**: Everything versioned in repositories; changes via PR only
- **Operational simplicity**: Minimum viable before sophisticated
- **Local-first when possible**: Keep sensitive data away from third parties
- **Human-in-the-loop**: Any critical automation requires human review

## Privacy & Data Compliance (LGPD/GDPR)

### Strict Data Rules
- **Collection**: Only what's necessary for declared purpose
- **Legal basis**: Documented; registered consent when applicable
- **Classification**: Public / Internal / Confidential / Restricted
- **Secrets**: Vault storage only; minimum access + 24h revocation
- **PII Protection**: FORBIDDEN in open chats, public issues, or unredacted screenshots
- **LLM Training**: FORBIDDEN with client data; inference only with pseudonymization under contract

### Development Data Handling
- Never commit credentials or PII to repositories
- Use environment variables or secure vaults for secrets
- Anonymize/pseudonymize all sample data
- Client data exports require explicit contracts and risk assessment

## Service Standards (100% Human)

### Response Times (SLA)
- **Initial Response (FRT)**: 4 business hours maximum
- **Standard Resolution**: 24 business hours with action plan for complex cases
- **Communication**: One response with next steps, timeline, and responsible party
- **Documentation**: Every relevant contact becomes client dossier note

### Customer Lifecycle Integration
Complete end-to-end flow: Lead acquisition → Service → Proposal → Contract → Billing → Payment → Post-sale
- **WhatsApp Business**: Primary touchpoint with versioned scripts, no sensitive data, explicit opt-in
- **CRM Pipeline**: Lead → Qualification → Proposal → Closing → Implementation → Support
- **Project Standards**: SMART objectives, financial baseline, 30-60-90 plans, executive reports

### Core Business Areas
- `governance_framework/`: Central governance with 10 specialized subdirectories
- `finance/`: Financial operations, metrics, and multi-currency management (BRL/EUR)
- `legal/`: Contract templates, compliance, and cross-border legal framework
- `marketing/`: Multi-platform content strategy with automated publishing
- `docs/`: Corporate documentation and institutional knowledge

### Governance Framework Pattern
Each governance subdirectory follows a consistent structure:
- `filosofia/`: Core principles and business philosophy
- `procedimentos/`: Standard operating procedures (see `plano_coordenador_avila_inc.md`)
- `parametros/`: Configuration and business parameters
- `funcoes/`: Role definitions and responsibilities
- `tecnicas/`: Technical methodologies and approaches
- `versoes/`: Version control for governance artifacts
- `revisao/`: Review and audit processes
- `capturas/`: Screenshots and visual documentation
- `_anexos/` & `_modelos/`: Templates and attachments (underscore prefix for metadata)

## Development Workflows

## Architecture & Structure

### Core Business Areas
- `governance_framework/`: Central governance with 10 specialized subdirectories
- `finance/`: Financial operations, metrics, and multi-currency management (BRL/EUR)
- `legal/`: Contract templates, compliance, and cross-border legal framework
- `marketing/`: Multi-platform content strategy with automated publishing
- `docs/`: Corporate documentation and institutional knowledge

### Governance Framework Pattern
Each governance subdirectory follows a consistent structure:
- `filosofia/`: Core principles and business philosophy (see mission/values document)
- `procedimentos/`: Standard operating procedures (see `plano_coordenador_avila_inc.md`)
- `parametros/`: Configuration and business parameters
- `funcoes/`: Role definitions and responsibilities
- `tecnicas/`: Technical methodologies and approaches
- `versoes/`: Version control for governance artifacts
- `revisao/`: Review and audit processes
- `capturas/`: Screenshots and visual documentation
- `_anexos/` & `_modelos/`: Templates and attachments (underscore prefix for metadata)

## Development Workflows

### Content Management (Nothing published without PR approval)
- **Source of truth**: Markdown files in respective directories with front-matter metadata
- **Publishing flow**: `marketing/` → GitHub Actions → Website + Social Media
- **Content calendar**: Weekly editorial calendar with 3 posts/week (case studies, product updates, behind-the-scenes)
- **Release integration**: GitHub releases automatically generate news content
- **Quality gate**: Double review + approved PR required before any public material

### Email & Marketing Templates (usage and locations)
- **Locations**:
	- Email templates: `marketing/templates/email/` (e.g., `outreach.md`, `followup.md`, `newsletter.md`)
	- Social templates: `marketing/templates/social/` (e.g., `facebook.md`, `linkedin.md`)
	- Brand assets: `marketing/brand/` (tone, voice, colors, typography)
	- Campaign plans: `marketing/campaigns/`
- **Front-matter required**: `title`, `audience`, `goal`, `cta`, `channels`, `date`, `utm`
- **Compliance**: Opt-in only; include unsubscribe/opt-out instructions where applicable; never include PII beyond the minimum necessary
- **UTM conventions**: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` defined per campaign in `marketing/templates/utm-conventions.md`
- **PR rule**: Nothing goes live without double review and an approved PR

### Financial Operations
- **Multi-currency**: BRL (Brazil) + EUR (Portugal) with segregated cost centers
- **Banking integration**: Daily CSV/API imports from Wise, Inter, Nubank → `bank_tx` datastore
- **KPI tracking**: Weekly financial metrics (MRR/ARR, margin, cash flow, DSO)
- **Compliance**: Separate fiscal reporting for BR and PT operations

### Customer Lifecycle
Complete end-to-end flow: Lead acquisition → Service → Proposal → Contract → Billing → Payment → Post-sale
- **WhatsApp Business**: Primary customer touchpoint with standardized labels and SLA
- **CRM Pipeline**: Lead → Qualification → Proposal → Closing → Implementation → Support
- **Contract management**: Template-based with unique numbering and electronic signatures

## Project Conventions

### File Organization
- **README pattern**: Each directory has a Portuguese README explaining its purpose and scope
- **Metadata prefix**: Underscore (`_`) for supporting files (templates, attachments)
- **Naming**: Portuguese directory names, bilingual content support

### Documentation Standards
- **Language**: Portuguese for internal docs, bilingual for external-facing content
- **Front-matter**: Use structured metadata in Markdown files for automation
- **Versioning**: Governance documents maintain version history in `versoes/`

### Automation Integration
- **GitHub Actions**: Deploy site, generate content, collect banking data
- **Data synchronization**: Daily financial data ingestion with reconciliation
- **Content publishing**: Single PR triggers multi-platform content distribution

## Critical Integration Points

### Banking & Finance
- **Multi-bank aggregation**: Wise (international), Inter/Nubank (Brazil)
- **Payment processing**: PIX/Boleto (BR), SEPA/IBAN (PT), Stripe (optional)
- **Reconciliation**: Automatic matching of `payments` to `bank_tx` records

### Marketing Automation
- **Repository**: `marketing/` with structured content workflow
- **UTM tracking**: Standardized campaign tracking across all channels
- **Social media**: Facebook integration via GitHub CI/CD

### Product study tracks: Geolocation and "ON"
- **Purpose**: These products are core tools for analysis and experimentation; treat them as workstreams with clear hypotheses, metrics, and data boundaries.
- **Study framework (apply to both)**: Problem → Hypothesis → Experiment → Result; keep cycles short with measurable outcomes.
- **Documentation**: `docs/products/geolocation.md` and `docs/products/on.md` for scope, KPIs, datasets, risks, and decisions.
- **KPIs examples**:
	- Geolocation: coverage %, geocoding accuracy, latency, cost per 1k lookups, privacy risk score
	- ON: adoption/usage rate, time-to-value, support tickets, churn/retention impact
- **Data boundaries**:
	- Collect only what is necessary; prefer aggregated or coarse-grained location where possible
	- Explicit consent required for any precise location; no raw GPS stored without legal basis and retention limits
	- Pseudonymize at ingestion; segregate BR/PT data per jurisdiction

### WhatsApp Business Operations
- **Current**: Manual Business App with labels and quick responses
- **Target**: Cloud API with webhooks, catalog sync, and automatic CRM integration
- **Escalation**: Tiered support (attendant → coordinator → management)

### Key Business Rules

### Portugal Expansion Strategy
- **Pricing**: EUR conversion with margin targeting and rounding policies
- **Legal structure**: Separate Portuguese entity with local compliance
- **Banking**: Wise IBAN preferred for SEPA/international payments (no cash mixing between jurisdictions)
- **Tax**: Local accounting integration when PT entity is active
- **Language**: PT-BR and PT-PT adapted content and references

### Critical Success Metrics
- **Client Impact**: Cost reduction %, revenue increase %, payback period, margin improvement
- **Ávila Performance**: CSAT/NPS, delivery punctuality, recontraction rate, delinquency
- **Operations**: FRT, average handling time, first-contact resolution, 30-60-90 compliance

### Prohibited Actions
- Publishing material without double review and approved PR
- Exporting client data to tools without contracts and risk assessment
- Using shared credentials (individual access only)
- Training external LLMs with client data
- Putting PII in open chats, public issues, or unredacted screenshots

## Development Priorities (90-day roadmap)
1. **Days 1-30**: WhatsApp setup, CRM pipeline, content calendar, basic metrics
2. **Days 31-60**: Banking integration, marketing funnels, service playbooks
3. **Days 61-90**: WhatsApp Cloud API, billing automation, executive dashboards

## Ethics & Compliance Requirements
- Declare relevant commercial relationships and potential commissions
- Refuse projects requiring unethical or anti-privacy practices
- Security before speed when client data risk exists
- Individual credentials only - no shared access

When working on this codebase:
- **Human service first**: AI assists but never replaces human judgment
- Follow Portuguese naming conventions for internal systems
- Maintain bilingual capability for external-facing features  
- Respect the governance framework hierarchy and approval workflows
- Prioritize automation and integration over manual processes
- Consider multi-currency and cross-border compliance requirements
- **Always maintain client financial impact focus**: every feature should tie to cost reduction or revenue increase