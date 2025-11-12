# 🎯 MÓDULO 5 - DECISÃO & AUTOMAÇÃO

## Sistema de Dashboards Interativos + Ações Automatizadas

**Versão:** 1.0
**Data:** 2025-11-10
**Posição no Pipeline:** Camada final (após Módulo 4)

---

## 🎯 OBJETIVO DO MÓDULO

**Transformar insights em AÇÕES através de:**

1. **Dashboards Executivos** - Visualização em tempo real para cada setor
2. **Automação de Ações** - Executar mudanças aprovadas automaticamente
3. **Sistema de Aprovações** - Workflow para mudanças críticas
4. **Alertas Inteligentes** - Notificações contextuais multi-canal
5. **Feedback Loop** - Aprender com resultados e melhorar continuamente

---

## 📊 ARQUITETURA DO MÓDULO 5

```
┌──────────────────────────────────────────────────────────────┐
│                    MÓDULO 5: DECISÃO                          │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   DASHBOARDS    │  │   AUTOMAÇÃO     │  │   ALERTAS    │ │
│  │   (Streamlit)   │  │   (Actions)     │  │  (Multi-ch)  │ │
│  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘ │
│           │                    │                   │          │
│           └────────────────────┼───────────────────┘          │
│                                │                              │
│                    ┌───────────▼──────────┐                   │
│                    │   DECISION ENGINE    │                   │
│                    │   (Regras + ML)      │                   │
│                    └───────────┬──────────┘                   │
│                                │                              │
│           ┌────────────────────┼────────────────────┐         │
│           │                    │                    │         │
│  ┌────────▼────────┐  ┌────────▼────────┐  ┌───────▼──────┐ │
│  │   AUTO EXEC     │  │   APPROVAL      │  │   FEEDBACK   │ │
│  │   (Baixo risco) │  │   (Alto risco)  │  │   LOOP       │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 DASHBOARD 1: VISÃO EXECUTIVA (CEO/CTO)

### **Layout Principal**

```
┌────────────────────────────────────────────────────────────────┐
│  ÁVILA INTELLIGENCE DASHBOARD                    🔴 LIVE      │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 MÉTRICAS PRINCIPAIS (Último mês vs Anterior)               │
│  ┌──────────────┬──────────────┬──────────────┬─────────────┐ │
│  │ 💰 Economia  │ ⏱️ Tempo     │ 🚀 Deploy    │ 🎯 OKRs     │ │
│  │ Identificada │ Economizado  │ Frequency    │ Progress    │ │
│  ├──────────────┼──────────────┼──────────────┼─────────────┤ │
│  │   $38,500    │   127 horas  │   42 deploys │   73%       │ │
│  │   ↑ 22%      │   ↑ 18%      │   ↑ 31%      │   ↑ 8%      │ │
│  └──────────────┴──────────────┴──────────────┴─────────────┘ │
│                                                                 │
│  🚨 ALERTAS CRÍTICOS (P0)                          [Ver 3]     │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ ⚠️  Servidor prod-api-01: CPU 98% há 4h                  │ │
│  │     └─ Ação recomendada: Auto-scale (+2 instances)       │ │
│  │     └─ [APROVAR] [ADIAR 1h] [DETALHES]                   │ │
│  │                                                            │ │
│  │ 🔐 CVE-2025-12345 em dependency "fastapi==0.104.0"       │ │
│  │     └─ Ação: Upgrade para 0.104.1 (patch disponível)    │ │
│  │     └─ [AUTO-FIX] [REVISAR] [SNOOZE]                     │ │
│  │                                                            │ │
│  │ 💸 Custo Azure: $12,300 (orçamento: $10,000)             │ │
│  │     └─ Causa: 8 VMs não desligadas (dev/test)           │ │
│  │     └─ [AUTO-SHUTDOWN] [INVESTIGAR] [AJUSTAR BUDGET]     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  💡 OPORTUNIDADES DE ALTO IMPACTO (Top 5)                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 1. 💰 Reserved Instances: Economia de $4,200/mês         │ │
│  │    └─ 12 VMs com uptime >90% sem commitment              │ │
│  │    └─ ROI: $50,400/ano | Risco: BAIXO | [IMPLEMENTAR]   │ │
│  │                                                            │ │
│  │ 2. 🤖 Chatbot Vendas: +2100% ROI esperado                │ │
│  │    └─ Lead qualification automática (24/7)               │ │
│  │    └─ Setup: 1 semana | Custo: $800 | [PRIORIZAR]       │ │
│  │                                                            │ │
│  │ 3. 📦 Storage Tiering: Economia de $3,600/ano            │ │
│  │    └─ 2TB em Hot tier (50% raramente acessado)           │ │
│  │    └─ Risco: ZERO | Esforço: 15min | [AUTO-EXECUTAR]    │ │
│  │                                                            │ │
│  │ 4. 🧹 Zombie Resources: Economia de $3,732/ano           │ │
│  │    └─ 8 discos, 12 IPs, 45 snapshots não usados          │ │
│  │    └─ [VER LISTA] [DELETAR TODOS] [REVISAR]             │ │
│  │                                                            │ │
│  │ 5. 📚 Runbook "Git Workflows": 6h/mês economizadas       │ │
│  │    └─ Padrão detectado em 8 conversas Copilot            │ │
│  │    └─ [GERAR RUNBOOK] [TREINAR TIME]                     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📈 TENDÊNCIAS (90 dias)                                       │
│  ┌────────────────────────────────────┐                       │
│  │        Economia Acumulada          │                       │
│  │  $                                 │                       │
│  │  50k ┤                         ╭─  │                       │
│  │  40k ┤                   ╭────╯    │                       │
│  │  30k ┤            ╭─────╯          │                       │
│  │  20k ┤      ╭────╯                 │                       │
│  │  10k ┤ ╭───╯                       │                       │
│  │   0  └─────────────────────────    │                       │
│  │      Ago  Set  Out  Nov            │                       │
│  └────────────────────────────────────┘                       │
│                                                                 │
│  🏆 TOP PERFORMERS (Last 30 days)                              │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 👤 Ana Costa: 3 otimizações (economia: $8,200)           │ │
│  │ 👤 João Silva: 5 runbooks criados (60h economizadas)     │ │
│  │ 🤖 AI Auto-actions: 142 execuções (100% sucesso)         │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 DASHBOARD 2: VENDAS & MARKETING

```
┌────────────────────────────────────────────────────────────────┐
│  💼 VENDAS & MARKETING - AI PERFORMANCE                        │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🎯 PIPELINE STATUS                                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  MQL ────→ SQL ────→ Demo ────→ Proposal ────→ Closed    │ │
│  │  450      180       85         45           18            │ │
│  │  (↑12%)   (40%)     (47%)      (53%)        (40%)         │ │
│  │                                                            │ │
│  │  Conversion Rates:                                         │ │
│  │  ▓▓▓▓▓▓▓▓░░ 40% MQL→SQL (target: 35%) ✅                 │ │
│  │  ▓▓▓▓▓▓▓░░░ 47% SQL→Demo (target: 50%) ⚠️                │ │
│  │  ▓▓▓▓▓▓▓▓░░ 53% Demo→Prop (target: 45%) ✅               │ │
│  │  ▓▓▓▓▓▓▓▓░░ 40% Prop→Close (target: 35%) ✅              │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🤖 AI TOOLS PERFORMANCE                                       │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  📧 Email AI (GPT-4 personalization)                      │ │
│  │  ├─ Emails gerados: 1,250 este mês                        │ │
│  │  ├─ Reply rate: 5.2% (vs 2% manual) ⬆️ 160%              │ │
│  │  ├─ Tempo economizado: 28h                                │ │
│  │  └─ ROI: $4,200 (meetings gerados)                        │ │
│  │                                                            │ │
│  │  🤖 Chatbot de Qualificação (RAG)                         │ │
│  │  ├─ Conversas: 380 este mês                               │ │
│  │  ├─ Leads qualificados: 153 (40% conversion)              │ │
│  │  ├─ Demos agendados: 62 (via bot, sem humano)             │ │
│  │  ├─ Disponibilidade: 24/7                                 │ │
│  │  └─ Custo por conversa: $0.12 (vs $15 humano)             │ │
│  │                                                            │ │
│  │  🎯 Lead Scoring (Random Forest)                          │ │
│  │  ├─ Leads scored: 2,840                                   │ │
│  │  ├─ Accuracy: 87% (validado com conversões reais)         │ │
│  │  ├─ Hot leads priorizados: 240 (top 8%)                   │ │
│  │  ├─ Conversion em hot leads: 25% (vs 8% geral)            │ │
│  │  └─ Tempo SDR economizado: 18h/semana (foco nos quentes)  │ │
│  │                                                            │ │
│  │  📝 Content AI (Blog posts automáticos)                   │ │
│  │  ├─ Posts publicados: 32 este mês (vs 8 antes)            │ │
│  │  ├─ SEO traffic: +120% (últimos 6 meses)                  │ │
│  │  ├─ Leads inbound: +80%                                   │ │
│  │  └─ Tempo economizado: 25h/mês (6h → 90min/post)          │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  💰 ECONOMICS                                                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  CAC (Customer Acquisition Cost)                           │ │
│  │  ├─ Antes IA: $2,600                                      │ │
│  │  ├─ Depois IA: $300                                       │ │
│  │  └─ Redução: 88% ✅ ($2,300 economizado/cliente)         │ │
│  │                                                            │ │
│  │  LTV/CAC Ratio                                             │ │
│  │  ├─ Current: 150x                                         │ │
│  │  ├─ Target: >3x                                           │ │
│  │  └─ Status: ✅✅✅ (50x acima do target!)                │ │
│  │                                                            │ │
│  │  Sales Cycle                                               │ │
│  │  ├─ Atual: 18 dias                                        │ │
│  │  ├─ Target: <30 dias                                      │ │
│  │  └─ vs Ano passado: 45 dias (↓60%) 🚀                    │ │
│  │                                                            │ │
│  │  MRR (Monthly Recurring Revenue)                           │ │
│  │  ├─ Atual: $125k                                          │ │
│  │  ├─ Target mês: $150k                                     │ │
│  │  ├─ Progress: ▓▓▓▓▓▓▓▓░░ 83%                             │ │
│  │  └─ Forecast Q4: $180k (95% confidence)                   │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🎯 ACTIONS NEEDED                                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ⚠️  SQL→Demo conversion baixa (47% vs target 50%)       │ │
│  │      └─ Ação: A/B test email follow-up (GPT-4 variants)  │ │
│  │      └─ [IMPLEMENTAR] [ANALISAR PERDAS]                   │ │
│  │                                                            │ │
│  │  💡 3 hot leads sem contato há 48h                        │ │
│  │      └─ Leads: Fintech ABC, SaaS XYZ, E-commerce 123     │ │
│  │      └─ [ENVIAR EMAIL AUTO] [LIGAR AGORA]                │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 📊 DASHBOARD 3: TECNOLOGIA & OPERAÇÕES

```
┌────────────────────────────────────────────────────────────────┐
│  ⚙️ TECNOLOGIA & OPERAÇÕES - PERFORMANCE + CUSTOS              │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  💰 CLOUD SPENDING (Azure - Este mês)                          │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Total: $12,300 / $10,000 (orçado) - ⚠️ 23% over budget  │ │
│  │                                                            │ │
│  │  Por Serviço:                                              │ │
│  │  ▓▓▓▓▓▓▓▓▓▓▓▓ VMs: $4,500 (37%)                          │ │
│  │  ▓▓▓▓▓▓▓▓ Databases: $3,200 (26%)                         │ │
│  │  ▓▓▓▓▓ Storage: $2,100 (17%)                              │ │
│  │  ▓▓▓ Networking: $1,200 (10%)                             │ │
│  │  ▓▓ AI Services: $800 (7%)                                │ │
│  │  ▓ Other: $500 (3%)                                        │ │
│  │                                                            │ │
│  │  Tendência (7 dias): ↗️ +$45/dia                          │ │
│  │  └─ Projeção fim do mês: $13,650 (↗️ $1,350 over)        │ │
│  │                                                            │ │
│  │  🚨 Top Wasters:                                           │ │
│  │  1. dev-vm-old-01: $280/mês (parada há 90 dias) [DELETE] │ │
│  │  2. prod-db-01: $450/mês (CPU 12%) [DOWNSIZE]             │ │
│  │  3. storage-hot-archive: $180/mês (tier wrong) [MIGRATE]  │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  📊 INFRASTRUCTURE HEALTH                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  🖥️  Servers (24 total)                                   │ │
│  │  ├─ ✅ Healthy: 21                                        │ │
│  │  ├─ ⚠️  Warning: 2 (CPU >80%)                             │ │
│  │  └─ 🔴 Critical: 1 (disk 95%)                             │ │
│  │                                                            │ │
│  │  🗄️  Databases (8 total)                                  │ │
│  │  ├─ ✅ Healthy: 7                                         │ │
│  │  ├─ ⚠️  Slow queries: 1 (avg 2.3s)                        │ │
│  │  └─ 🔴 Backup failed: 0                                   │ │
│  │                                                            │ │
│  │  🌐 APIs (12 endpoints)                                    │ │
│  │  ├─ ✅ 200 OK: 11                                         │ │
│  │  ├─ ⚠️  Latency >500ms: 1 (/reports)                      │ │
│  │  └─ 🔴 Down: 0                                            │ │
│  │                                                            │ │
│  │  Uptime (30 dias): 99.87% (target: 99.9%) ⚠️             │ │
│  │  └─ Incidents: 2 (total downtime: 56min)                  │ │
│  │                                                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🚀 DEPLOYMENT STATS (Last 7 days)                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Deploys: 42                                               │ │
│  │  ├─ ✅ Success: 40 (95%)                                  │ │
│  │  ├─ 🔄 Rollback: 2 (5%)                                   │ │
│  │  └─ ❌ Failed: 0                                          │ │
│  │                                                            │ │
│  │  Avg deploy time: 3.2min (target: <5min) ✅              │ │
│  │  Lead time (commit→prod): 18min (target: <30min) ✅      │ │
│  │                                                            │ │
│  │  CI/CD Health:                                             │ │
│  │  ├─ Build time: 2.1min (↓15% vs last week)               │ │
│  │  ├─ Test coverage: 78% (target: 80%) ⚠️                  │ │
│  │  └─ Flaky tests: 3 (need fix)                             │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  🔐 SECURITY ALERTS                                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  🔴 Critical CVEs: 1                                       │ │
│  │     └─ CVE-2025-12345 (fastapi 0.104.0)                   │ │
│  │        [AUTO-PATCH] [CREATE TICKET]                        │ │
│  │                                                            │ │
│  │  ⚠️  High CVEs: 3                                         │ │
│  │     └─ [VIEW LIST] [SCHEDULE PATCHES]                     │ │
│  │                                                            │ │
│  │  Dependencies outdated: 12                                 │ │
│  │     └─ [UPDATE NON-BREAKING] [REVIEW BREAKING]            │ │
│  │                                                            │ │
│  │  Last security scan: 2h ago ✅                            │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
│  💡 OPTIMIZATION OPPORTUNITIES                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  1. Reserved Instances: $4,200/mês economia [IMPLEMENT]   │ │
│  │  2. Spot instances (CI/CD): $600/mês economia [TEST]      │ │
│  │  3. Storage tiering: $300/mês economia [AUTO-EXECUTE]     │ │
│  │  4. Delete zombies: $311/mês economia [REVIEW & DELETE]   │ │
│  │                                                            │ │
│  │  Total potential saving: $5,411/mês = $64,932/ano 💰     │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

---

## 🤖 SISTEMA DE AUTOMAÇÃO

### **Decision Engine - Regras de Auto-Execução**

```python
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

class RiskLevel(Enum):
    ZERO = "ZERO"      # Auto-execute sempre
    LOW = "LOW"        # Auto-execute se $<500 ou tempo<1h
    MEDIUM = "MEDIUM"  # Requer aprovação de Tech Lead
    HIGH = "HIGH"      # Requer aprovação de CTO
    CRITICAL = "CRITICAL"  # Requer aprovação de CEO

class ActionStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"

@dataclass
class AutomationAction:
    """
    Representa uma ação automatizada
    """
    id: str
    type: str  # "cost_optimization", "security_patch", "scaling", etc
    title: str
    description: str
    risk_level: RiskLevel
    impact: Dict  # {"cost_saving": 140, "time_saving": 30, ...}
    prerequisites: List[str]
    execution_steps: List[Dict]
    rollback_steps: List[Dict]
    estimated_duration: int  # minutos
    notification_channels: List[str]
    auto_execute: bool
    approval_required: bool
    approvers: List[str]
    status: ActionStatus
    created_at: datetime
    executed_at: Optional[datetime]
    result: Optional[Dict]

class DecisionEngine:
    """
    Motor de decisão - determina se ação deve ser auto-executada ou requer aprovação
    """

    # Regras de auto-execução
    AUTO_EXECUTE_RULES = {
        "storage_tiering": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda action: True,  # sempre safe
            "reason": "Lifecycle policy não perde dados, apenas move tiers"
        },

        "delete_zombie_snapshot": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda action: action.get('age_days', 0) > 365,
            "reason": "Snapshot >1 ano sem uso, backup metadata mantido"
        },

        "delete_unattached_disk": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda action: action.get('unattached_days', 0) > 90,
            "reason": "Disco não conectado há 90+ dias, notificar owner antes"
        },

        "vm_rightsizing": {
            "risk": RiskLevel.MEDIUM,
            "auto_if": lambda action: (
                action.get('cost_saving', 0) < 500 and
                action.get('downsize_percentage', 0) <= 50
            ),
            "reason": "Downsize <50% com economia <$500 = baixo risco"
        },

        "reserved_instance_purchase": {
            "risk": RiskLevel.MEDIUM,
            "auto_if": lambda action: (
                action.get('uptime_percentage', 0) > 95 and
                action.get('commitment_months', 0) == 12
            ),
            "reason": "Uptime >95% + commitment 1 ano = safe bet"
        },

        "security_patch_minor": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda action: action.get('is_backward_compatible', False),
            "reason": "Patch minor version (backward compatible)"
        },

        "security_patch_critical": {
            "risk": RiskLevel.HIGH,
            "auto_if": lambda action: (
                action.get('cve_severity', '') == 'CRITICAL' and
                action.get('exploit_available', False)
            ),
            "reason": "CVE crítico + exploit público = urgente, mas staging first"
        },

        "auto_scaling": {
            "risk": RiskLevel.LOW,
            "auto_if": lambda action: (
                action.get('cpu_threshold', 0) > 90 and
                action.get('duration_minutes', 0) > 10
            ),
            "reason": "CPU >90% por 10min = add instances"
        },

        "alert_notification": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda action: True,
            "reason": "Notificação não altera infraestrutura"
        },

        "backup_failure_retry": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda action: action.get('retry_count', 0) < 3,
            "reason": "Retry backup automático (<3 tentativas)"
        },

        "runbook_generation": {
            "risk": RiskLevel.ZERO,
            "auto_if": lambda action: True,
            "reason": "Gerar doc não tem risco"
        }
    }

    def should_auto_execute(self, action: AutomationAction) -> Dict:
        """
        Decide se ação deve ser auto-executada

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
            return {
                "auto_execute": False,
                "reason": "Action type not in whitelist",
                "requires_approval": True,
                "approvers": ["tech_lead", "cto"]
            }

        # Verificar se passa na condição
        can_auto = rule['auto_if'](action.impact)

        if can_auto:
            return {
                "auto_execute": True,
                "reason": rule['reason'],
                "requires_approval": False,
                "approvers": []
            }
        else:
            # Não passou = requer aprovação baseada no risco
            approvers = self._get_approvers_for_risk(rule['risk'])
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
        """
        decision = self.should_auto_execute(action)

        if decision['auto_execute']:
            # Auto-execute
            result = self._run_action(action)
            self._send_notification(action, result)
            return result
        else:
            # Enviar para aprovação
            approval_id = self._create_approval_request(action, decision['approvers'])
            self._send_notification(action, {
                "status": "awaiting_approval",
                "approval_id": approval_id,
                "approvers": decision['approvers']
            })
            return {
                "status": "pending_approval",
                "approval_id": approval_id
            }

    def _run_action(self, action: AutomationAction) -> Dict:
        """
        Executa os steps da ação
        """
        action.status = ActionStatus.EXECUTING
        results = []

        try:
            for step in action.execution_steps:
                step_result = self._execute_step(step)
                results.append(step_result)

                if not step_result['success']:
                    # Step falhou = rollback
                    self._rollback(action, results)
                    action.status = ActionStatus.FAILED
                    return {
                        "success": False,
                        "error": step_result['error'],
                        "rollback": "completed"
                    }

            action.status = ActionStatus.COMPLETED
            action.executed_at = datetime.now()
            return {
                "success": True,
                "steps_executed": len(results),
                "impact": action.impact
            }

        except Exception as e:
            self._rollback(action, results)
            action.status = ActionStatus.FAILED
            return {
                "success": False,
                "error": str(e),
                "rollback": "completed"
            }

    def _execute_step(self, step: Dict) -> Dict:
        """
        Executa um step individual
        """
        step_type = step['type']

        if step_type == "azure_cli":
            return self._exec_azure_cli(step['command'])
        elif step_type == "api_call":
            return self._exec_api_call(step['endpoint'], step['method'], step['payload'])
        elif step_type == "script":
            return self._exec_script(step['script_path'], step.get('args', []))
        elif step_type == "notification":
            return self._send_message(step['channel'], step['message'])
        else:
            return {"success": False, "error": f"Unknown step type: {step_type}"}

    def _rollback(self, action: AutomationAction, executed_steps: List[Dict]):
        """
        Reverte ação em caso de falha
        """
        for rollback_step in reversed(action.rollback_steps):
            self._execute_step(rollback_step)

    def _create_approval_request(self, action: AutomationAction, approvers: List[str]) -> str:
        """
        Cria request de aprovação
        """
        # Salvar no DB
        approval_id = f"approval_{action.id}_{datetime.now().timestamp()}"
        # ... salvar no banco ...
        return approval_id

    def _send_notification(self, action: AutomationAction, result: Dict):
        """
        Envia notificação multi-canal
        """
        for channel in action.notification_channels:
            if channel == "slack":
                self._notify_slack(action, result)
            elif channel == "email":
                self._notify_email(action, result)
            elif channel == "dashboard":
                self._update_dashboard(action, result)

    # Métodos auxiliares (implementação específica)
    def _exec_azure_cli(self, command: str) -> Dict:
        """Executa comando Azure CLI"""
        return {"success": True}

    def _exec_api_call(self, endpoint: str, method: str, payload: Dict) -> Dict:
        """Faz chamada API"""
        return {"success": True}

    def _exec_script(self, script_path: str, args: List) -> Dict:
        """Executa script"""
        return {"success": True}

    def _send_message(self, channel: str, message: str) -> Dict:
        """Envia mensagem"""
        return {"success": True}

    def _notify_slack(self, action: AutomationAction, result: Dict):
        """Notifica no Slack"""
        pass

    def _notify_email(self, action: AutomationAction, result: Dict):
        """Notifica por email"""
        pass

    def _update_dashboard(self, action: AutomationAction, result: Dict):
        """Atualiza dashboard"""
        pass
```

---

## 🔔 SISTEMA DE ALERTAS INTELIGENTES

### **Multi-Channel Notifications**

```python
from typing import Dict, List
from enum import Enum

class NotificationChannel(Enum):
    SLACK = "slack"
    EMAIL = "email"
    SMS = "sms"
    TEAMS = "teams"
    PAGERDUTY = "pagerduty"
    DASHBOARD = "dashboard"

class NotificationPriority(Enum):
    P0_CRITICAL = "P0"  # 🔴 Immediato (SMS + call)
    P1_HIGH = "P1"      # 🟠 <1h (Slack + Email)
    P2_MEDIUM = "P2"    # 🟡 <24h (Email + Dashboard)
    P3_LOW = "P3"       # 🟢 Weekly digest

class IntelligentAlerting:
    """
    Sistema de alertas contextuais e inteligentes
    """

    # Regras de roteamento baseadas em contexto
    ROUTING_RULES = {
        "cost_spike": {
            "priority": NotificationPriority.P1_HIGH,
            "channels": [NotificationChannel.SLACK, NotificationChannel.EMAIL],
            "recipients": {
                "if_amount": {
                    "> 1000": ["cto", "cfo"],
                    "> 500": ["engineering_manager"],
                    "> 100": ["tech_lead"]
                }
            },
            "throttle": "1/hour",  # max 1 por hora (evitar spam)
            "smart_group": True    # agrupar alertas similares
        },

        "performance_degradation": {
            "priority": NotificationPriority.P1_HIGH,
            "channels": [NotificationChannel.SLACK, NotificationChannel.PAGERDUTY],
            "recipients": ["on_call_engineer"],
            "escalation": {
                "if_not_ack_15min": ["engineering_manager"],
                "if_not_resolved_1h": ["cto"]
            },
            "throttle": "1/15min"
        },

        "security_vulnerability": {
            "priority": NotificationPriority.P0_CRITICAL,
            "channels": [
                NotificationChannel.SLACK,
                NotificationChannel.EMAIL,
                NotificationChannel.PAGERDUTY
            ],
            "recipients": {
                "if_severity": {
                    "CRITICAL": ["cto", "security_team", "ceo"],
                    "HIGH": ["security_team", "tech_lead"],
                    "MEDIUM": ["security_team"]
                }
            },
            "throttle": None,  # nunca throttle (sempre enviar)
            "require_ack": True
        },

        "opportunity_detected": {
            "priority": NotificationPriority.P2_MEDIUM,
            "channels": [NotificationChannel.SLACK, NotificationChannel.DASHBOARD],
            "recipients": {
                "if_impact": {
                    "> 5000": ["cto", "cfo"],  # economia >$5k
                    "> 1000": ["engineering_manager"],
                    "> 0": ["tech_lead"]
                }
            },
            "throttle": "1/day",
            "smart_group": True,
            "digest": "daily_10am"  # agrupar em digest diário 10am
        },

        "knowledge_pattern": {
            "priority": NotificationPriority.P3_LOW,
            "channels": [NotificationChannel.SLACK],
            "recipients": ["#engineering-learnings"],  # canal, não pessoa
            "throttle": "1/week",
            "digest": "weekly_friday"
        }
    }

    def send_alert(self, alert_type: str, context: Dict):
        """
        Envia alerta inteligente baseado em contexto
        """
        rule = self.ROUTING_RULES.get(alert_type)

        if not rule:
            # Tipo desconhecido = rota padrão
            rule = self._default_routing(context)

        # 1. Determinar recipientes baseado em contexto
        recipients = self._resolve_recipients(rule, context)

        # 2. Verificar throttling (evitar spam)
        if self._is_throttled(alert_type, rule['throttle']):
            return {"sent": False, "reason": "throttled"}

        # 3. Smart grouping (agrupar alertas similares)
        if rule.get('smart_group', False):
            if self._should_group(alert_type, context):
                self._add_to_group(alert_type, context)
                return {"sent": False, "reason": "grouped_for_digest"}

        # 4. Formatar mensagem (personalizada por canal)
        messages = {
            channel: self._format_message(channel, alert_type, context)
            for channel in rule['channels']
        }

        # 5. Enviar para cada canal
        results = []
        for channel in rule['channels']:
            for recipient in recipients:
                result = self._send_to_channel(
                    channel=channel,
                    recipient=recipient,
                    message=messages[channel],
                    priority=rule['priority']
                )
                results.append(result)

        # 6. Setup de escalação (se configurado)
        if 'escalation' in rule:
            self._setup_escalation(alert_type, context, rule['escalation'])

        return {"sent": True, "channels": rule['channels'], "recipients": recipients}

    def _resolve_recipients(self, rule: Dict, context: Dict) -> List[str]:
        """
        Resolve destinatários baseado em regras condicionais
        """
        recipients_config = rule['recipients']

        # Se é dict com condições
        if isinstance(recipients_config, dict):
            for condition_key, conditions in recipients_config.items():
                if condition_key == "if_amount":
                    amount = context.get('amount', 0)
                    for threshold, recips in conditions.items():
                        if eval(f"{amount} {threshold}"):
                            return recips

                elif condition_key == "if_severity":
                    severity = context.get('severity', '')
                    return conditions.get(severity, [])

                elif condition_key == "if_impact":
                    impact = context.get('impact', 0)
                    for threshold, recips in conditions.items():
                        if eval(f"{impact} {threshold}"):
                            return recips

        # Se é lista simples
        return recipients_config

    def _is_throttled(self, alert_type: str, throttle_rule: str) -> bool:
        """
        Verifica se alerta deve ser throttled (evitar spam)
        """
        if not throttle_rule:
            return False

        # Parse regra: "1/hour" = max 1 por hora
        # ... implementar lógica de throttling ...
        return False

    def _should_group(self, alert_type: str, context: Dict) -> bool:
        """
        Decide se alerta deve ser agrupado em digest
        """
        # Exemplo: agrupar se já houve similar nas últimas 2h
        return False

    def _add_to_group(self, alert_type: str, context: Dict):
        """
        Adiciona alerta ao grupo para digest posterior
        """
        pass

    def _format_message(self, channel: NotificationChannel, alert_type: str, context: Dict) -> str:
        """
        Formata mensagem específica para cada canal
        """
        if channel == NotificationChannel.SLACK:
            return self._format_slack(alert_type, context)
        elif channel == NotificationChannel.EMAIL:
            return self._format_email(alert_type, context)
        elif channel == NotificationChannel.SMS:
            return self._format_sms(alert_type, context)
        else:
            return str(context)

    def _format_slack(self, alert_type: str, context: Dict) -> str:
        """
        Formata para Slack (markdown + blocks)
        """
        if alert_type == "cost_spike":
            return f"""
🚨 *Cost Alert*: Spending spike detected

💰 *Amount*: ${context['amount']} (↑{context['percentage_increase']}% vs last week)
📊 *Service*: {context['service']}
⏰ *Period*: {context['period']}

*Top contributors:*
{chr(10).join([f"  • {item['name']}: ${item['cost']}" for item in context['top_items'][:3]])}

*Recommended actions:*
  1. {context['recommendations'][0]}
  2. {context['recommendations'][1]}

<{context['dashboard_url']}|View Dashboard> | <{context['action_url']}|Take Action>
"""

        elif alert_type == "opportunity_detected":
            return f"""
💡 *Optimization Opportunity*

*Title*: {context['title']}
💰 *Potential Saving*: ${context['saving']}/month (${context['saving']*12}/year)
📈 *Impact*: {context['impact']}
⚖️  *Risk*: {context['risk']}

*Action*: {context['action']}
⏱️  *Effort*: {context['estimated_effort']}

<{context['details_url']}|View Details> | <{context['implement_url']}|Implement Now>
"""

        return str(context)

    def _format_email(self, alert_type: str, context: Dict) -> str:
        """
        Formata para Email (HTML)
        """
        # ... HTML template ...
        return f"<html>...</html>"

    def _format_sms(self, alert_type: str, context: Dict) -> str:
        """
        Formata para SMS (curto, <160 chars)
        """
        if alert_type == "cost_spike":
            return f"AVILA ALERT: ${context['amount']} spike in {context['service']}. Check dashboard."
        return "AVILA: New alert. Check dashboard."

    def _send_to_channel(self, channel: NotificationChannel, recipient: str,
                         message: str, priority: NotificationPriority) -> Dict:
        """
        Envia mensagem para canal específico
        """
        # Implementação específica por canal
        if channel == NotificationChannel.SLACK:
            return self._send_slack(recipient, message)
        elif channel == NotificationChannel.EMAIL:
            return self._send_email(recipient, message)
        # ... outros canais ...

        return {"success": True}

    def _setup_escalation(self, alert_type: str, context: Dict, escalation_rules: Dict):
        """
        Configura escalação automática se não houver ack/resolução
        """
        # Agendar checagem futura
        # Se não resolvido em X tempo → notificar próximo nível
        pass

    def _send_slack(self, recipient: str, message: str) -> Dict:
        """Envia para Slack"""
        return {"success": True}

    def _send_email(self, recipient: str, message: str) -> Dict:
        """Envia email"""
        return {"success": True}

    def _default_routing(self, context: Dict) -> Dict:
        """Roteamento padrão para alertas desconhecidos"""
        return {
            "priority": NotificationPriority.P2_MEDIUM,
            "channels": [NotificationChannel.SLACK, NotificationChannel.DASHBOARD],
            "recipients": ["tech_lead"],
            "throttle": "1/hour"
        }
```

---

## 🔄 FEEDBACK LOOP (Aprendizado Contínuo)

```python
class FeedbackLoop:
    """
    Sistema de aprendizado contínuo baseado em resultados
    """

    def record_action_result(self, action_id: str, result: Dict):
        """
        Registra resultado de ação para aprendizado
        """
        feedback = {
            "action_id": action_id,
            "success": result['success'],
            "actual_impact": result.get('actual_impact', {}),
            "predicted_impact": result.get('predicted_impact', {}),
            "user_satisfaction": None,  # será coletado depois
            "timestamp": datetime.now()
        }

        # Salvar no banco
        self._save_feedback(feedback)

        # Analisar desvios (predição vs realidade)
        self._analyze_prediction_accuracy(feedback)

        # Ajustar modelos se necessário
        if self._should_retrain():
            self._retrain_models()

    def collect_user_feedback(self, action_id: str, satisfaction: int, comments: str):
        """
        Coleta feedback do usuário (1-5 stars)
        """
        self._update_feedback(action_id, {
            "user_satisfaction": satisfaction,
            "user_comments": comments
        })

        # Se feedback ruim (1-2 stars), investigar
        if satisfaction <= 2:
            self._investigate_negative_feedback(action_id)

    def _analyze_prediction_accuracy(self, feedback: Dict):
        """
        Analisa precisão das predições
        """
        predicted = feedback['predicted_impact']
        actual = feedback['actual_impact']

        # Calcular erro
        if 'cost_saving' in predicted and 'cost_saving' in actual:
            error_percentage = abs(predicted['cost_saving'] - actual['cost_saving']) / predicted['cost_saving']

            # Se erro >20%, ajustar modelo
            if error_percentage > 0.20:
                self._flag_for_model_adjustment("cost_prediction", error_percentage)

    def _should_retrain(self) -> bool:
        """
        Decide se deve retreinar modelos
        """
        # Retreinar se:
        # - Acumulou 100+ novos feedbacks
        # - Accuracy caiu >5%
        # - Última treino foi há >30 dias
        return False

    def _retrain_models(self):
        """
        Retreina modelos de ML com novos dados
        """
        # Lead scoring
        # Cost prediction
        # etc
        pass

    def _save_feedback(self, feedback: Dict):
        """Salva no banco"""
        pass

    def _update_feedback(self, action_id: str, updates: Dict):
        """Atualiza feedback"""
        pass

    def _investigate_negative_feedback(self, action_id: str):
        """Investiga feedback negativo"""
        pass

    def _flag_for_model_adjustment(self, model_name: str, error: float):
        """Flag modelo para ajuste"""
        pass
```

---

## 📈 MÉTRICAS DE SUCESSO DO MÓDULO 5

```python
KPIs_MODULE_5 = {
    "DASHBOARDS": {
        "Uptime": "> 99.9%",
        "Load Time": "< 2s",
        "User Adoption": "> 80% do time usa diariamente",
        "Data Freshness": "< 5min lag"
    },

    "AUTOMACAO": {
        "Actions Executed": "> 100/mês",
        "Success Rate": "> 95%",
        "Time Saved": "> 50h/mês",
        "Cost Saved": "> $10k/mês"
    },

    "ALERTAS": {
        "False Positive Rate": "< 10%",
        "Time to Acknowledge": "< 5min (P0), < 1h (P1)",
        "Time to Resolution": "< 1h (P0), < 24h (P1)",
        "Alert Fatigue Score": "< 20%"  # % de alertas ignorados
    },

    "FEEDBACK_LOOP": {
        "Prediction Accuracy": "> 85%",
        "User Satisfaction": "> 4.2/5",
        "Model Improvement Rate": "> 5%/quarter"
    }
}
```

---

## 🎓 RESUMO EXECUTIVO

**Módulo 5 = "Interface de Ação" do Sistema**

**Componentes:**
1. **3 Dashboards Principais** (Executivo, Vendas, Tech/Ops)
2. **Decision Engine** (auto-executa ou requer aprovação baseado em risco)
3. **Sistema de Automação** (142 ações/mês, 95% sucesso)
4. **Alertas Inteligentes** (multi-canal, contextuais, anti-spam)
5. **Feedback Loop** (aprendizado contínuo, melhoria de modelos)

**Fluxo Completo:**
```
Insight detectado (Módulo 4)
↓
Decision Engine avalia risco
↓
├─ Risco ZERO/LOW → Auto-executa → Notifica resultado
└─ Risco MEDIUM/HIGH → Cria approval → Notifica stakeholders
   ↓
   Aprovador revisa no dashboard
   ↓
   ├─ Aprova → Executa → Notifica resultado
   └─ Rejeita → Registra motivo → Aprende
↓
Coleta feedback (satisfação 1-5)
↓
Ajusta modelos (se necessário)
↓
Melhoria contínua ♻️
```

**ROI do Módulo 5:**
- ⚡ **Velocidade:** Decisões em segundos (vs horas/dias)
- 🤖 **Automação:** 70% de ações sem intervenção humana
- 💰 **Economia:** $10-50k/mês executada automaticamente
- ⏱️ **Tempo:** 50-100h/mês economizadas (time foca no estratégico)
- 📊 **Visibilidade:** 100% das operações rastreáveis em tempo real

**Stack Tecnológico:**
- **Frontend:** Streamlit (dashboards interativos)
- **Backend:** Python (FastAPI)
- **DB:** PostgreSQL (actions, approvals, feedback)
- **Queue:** Redis (task queue para execuções)
- **Monitoring:** Prometheus + Grafana
- **Notifications:** Slack API, SendGrid, Twilio

---

## 🔗 INTEGRAÇÃO COM MÓDULOS ANTERIORES

```
Módulo 1: COLETA
├─ Obsidian, ActivityWatch, Azure CLI, Copilot
↓
Módulo 2: AGREGAÇÃO
├─ ETL, Data Lake, Normalização
↓
Módulo 3: PROCESSAMENTO SEMÂNTICO
├─ Embeddings, Clustering, Knowledge Graph
↓
Módulo 4: CLASSIFICAÇÃO & ENRIQUECIMENTO
├─ 8 tipos recursos, 10 tipos oportunidades
├─ Insights GPT-4, Priorização
↓
Módulo 5: DECISÃO & AUTOMAÇÃO ⭐
├─ Dashboards (visualização)
├─ Decision Engine (auto-execute ou aprova)
├─ Automation (execução)
├─ Alerts (notificação inteligente)
└─ Feedback Loop (aprendizado)
```

---

**Pipeline Completo Ávila = 5 Módulos Funcionando em Harmonia! 🚀**

*Última Atualização: 2025-11-10*
