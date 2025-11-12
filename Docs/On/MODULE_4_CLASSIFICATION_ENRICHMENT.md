# 🧠 MÓDULO 4 - CLASSIFICAÇÃO INTELIGENTE & ENRIQUECIMENTO

## Sistema de Categorização, Insights e Otimização Automática

**Versão:** 1.0
**Data:** 2025-11-10
**Posição no Pipeline:** Após Módulo 3 (Processamento Semântico)

---

## 🎯 OBJETIVO DO MÓDULO

**Transformar dados brutos em conhecimento acionável através de:**

1. **Classificação Multi-Dimensional** - Categorizar documentos em 15+ dimensões
2. **Detecção de Oportunidades** - Identificar economia de custos, otimizações, melhorias
3. **Enriquecimento Contextual** - Adicionar metadados, tags, relacionamentos
4. **Geração de Insights** - Criar recomendações práticas e alertas
5. **Priorização Inteligente** - Ordenar ações por impacto/urgência

---

## 📊 TAXONOMIA DE CLASSIFICAÇÃO

### **Dimensão 1: TIPO DE RECURSO**

```python
RESOURCE_TYPES = {
    "SERVIDOR": {
        "description": "Servidores, VMs, instâncias cloud",
        "subcategorias": [
            "Azure VM",
            "AWS EC2",
            "On-Premise",
            "Container (Docker/K8s)",
            "Serverless (Functions)"
        ],
        "palavras_chave": ["servidor", "vm", "instance", "ec2", "virtual machine"]
    },

    "BANCO_DE_DADOS": {
        "description": "Databases, data warehouses, caches",
        "subcategorias": [
            "SQL (PostgreSQL, MySQL, SQL Server)",
            "NoSQL (MongoDB, Cosmos DB, DynamoDB)",
            "Cache (Redis, Memcached)",
            "Data Warehouse (Snowflake, BigQuery)",
            "Vector DB (Qdrant, Pinecone)"
        ],
        "palavras_chave": ["database", "db", "sql", "nosql", "cache"]
    },

    "ARMAZENAMENTO": {
        "description": "Storage, buckets, file systems",
        "subcategorias": [
            "Blob Storage (Azure/S3)",
            "File Share (NFS/SMB)",
            "Archive (Glacier/Cool tier)",
            "CDN (CloudFront/Azure CDN)"
        ],
        "palavras_chave": ["storage", "bucket", "blob", "s3", "file"]
    },

    "REDE": {
        "description": "VPNs, Load Balancers, DNS, Firewalls",
        "subcategorias": [
            "Load Balancer",
            "VPN Gateway",
            "DNS Zone",
            "Firewall/NSG",
            "CDN"
        ],
        "palavras_chave": ["network", "vpn", "load balancer", "dns", "firewall"]
    },

    "SERVICO_GERENCIADO": {
        "description": "PaaS, SaaS, managed services",
        "subcategorias": [
            "API Management",
            "Logic Apps / Step Functions",
            "Event Hub / EventBridge",
            "AI Services (OpenAI, Cognitive)",
            "Monitoring (App Insights, CloudWatch)"
        ],
        "palavras_chave": ["managed", "paas", "saas", "api", "event"]
    },

    "LICENCA_SOFTWARE": {
        "description": "Licenses, subscriptions, tools",
        "subcategorias": [
            "IDEs (VS Code, IntelliJ)",
            "Collaboration (Slack, Teams, Notion)",
            "Design (Figma, Adobe)",
            "Development (GitHub, GitLab, Jira)",
            "Security (1Password, Okta)"
        ],
        "palavras_chave": ["license", "subscription", "saas", "tool", "software"]
    },

    "CONHECIMENTO": {
        "description": "Docs, tutorials, estudos, research",
        "subcategorias": [
            "Tutorial/How-to",
            "Arquitetura/Design",
            "Pesquisa/Research",
            "Troubleshooting/Debug",
            "Best Practices"
        ],
        "palavras_chave": ["tutorial", "how to", "guide", "documentation", "study"]
    },

    "CODIGO": {
        "description": "Source code, scripts, configs",
        "subcategorias": [
            "Backend (Python, Node, Java)",
            "Frontend (React, Vue, Angular)",
            "Mobile (React Native, Flutter)",
            "Infrastructure (Terraform, CloudFormation)",
            "Scripts (Bash, PowerShell, Python)"
        ],
        "palavras_chave": ["code", "script", "function", "class", "import"]
    }
}
```

---

### **Dimensão 2: OPORTUNIDADES DE ECONOMIA**

```python
COST_OPPORTUNITIES = {
    "RIGHTSIZING": {
        "description": "Recursos super-dimensionados (muito CPU/RAM/Storage)",
        "impacto_medio": "30-50% economia",
        "deteccao": {
            "servidores": "CPU < 20% por 7+ dias → downsize",
            "storage": "< 50% utilizado por 30+ dias → tier mais barato",
            "database": "IOPS < 30% provisionado → reduzir throughput"
        },
        "exemplo": """
        # Detectado:
        Azure VM: Standard_D8s_v3 (8 vCPUs, 32GB RAM)
        └─ CPU avg: 12% (últimos 30 dias)
        └─ RAM avg: 8GB (25% uso)
        └─ Custo: $280/mês

        # Recomendação:
        Migrar para: Standard_D4s_v3 (4 vCPUs, 16GB RAM)
        └─ Comporta carga atual com folga (50% CPU, 50% RAM)
        └─ Custo: $140/mês
        └─ 💰 Economia: $140/mês = $1,680/ano

        # Confiança: 95% (padrão estável 90 dias)
        # Risco: BAIXO (CPU/RAM sobra 2x)
        # Ação: Agendar migração fora de horário comercial
        """
    },

    "RESERVED_INSTANCES": {
        "description": "Recursos 24/7 sem commitment (pague menos com reserved)",
        "impacto_medio": "30-72% economia",
        "deteccao": {
            "criterio": "Uptime > 80% nos últimos 90 dias",
            "tipos": ["VMs", "Databases", "App Services"]
        },
        "exemplo": """
        # Detectado:
        PostgreSQL Database (General Purpose, 4 vCores)
        └─ Uptime: 99.8% (últimos 90 dias)
        └─ Custo Pay-as-you-go: $250/mês

        # Recomendação:
        Reserved Instance (1 ano, pagamento mensal)
        └─ Custo: $162/mês
        └─ 💰 Economia: $88/mês = $1,056/ano (35% desconto)

        Reserved Instance (3 anos, upfront)
        └─ Custo: $110/mês
        └─ 💰 Economia: $140/mês = $1,680/ano (56% desconto)

        # Recomendação: 1 ano (mais flexível)
        # Risco: BAIXO (workload estável)
        # Payback: Imediato
        """
    },

    "STORAGE_TIERING": {
        "description": "Dados raramente acessados em tier caro (hot storage)",
        "impacto_medio": "50-90% economia em storage",
        "deteccao": {
            "hot_to_cool": "Não acessado por 30+ dias → Cool tier",
            "cool_to_archive": "Não acessado por 90+ dias → Archive tier"
        },
        "exemplo": """
        # Detectado:
        Azure Blob Storage: 2TB em Hot tier
        └─ Análise de acesso (últimos 90 dias):
            - 200GB: acessados semanalmente (manter Hot)
            - 800GB: acessados 1x/mês (mover Cool)
            - 1TB: não acessados (mover Archive)

        # Custos Atuais:
        2TB Hot: $40/TB/mês = $80/mês

        # Custos Otimizados:
        200GB Hot: $40/TB/mês = $8/mês
        800GB Cool: $10/TB/mês = $8/mês
        1TB Archive: $2/TB/mês = $2/mês
        Total: $18/mês

        💰 Economia: $62/mês = $744/ano (77% redução!)

        # Implementação:
        - Lifecycle policy automática (Azure/AWS)
        - Hot → Cool após 30 dias sem acesso
        - Cool → Archive após 90 dias

        # Risco: ZERO (dados não perdidos, apenas latência +ms se acessar)
        """
    },

    "ZOMBIE_RESOURCES": {
        "description": "Recursos inativos/órfãos cobrando desnecessariamente",
        "impacto_medio": "100% economia (remover)",
        "deteccao": {
            "vm_stopped": "VM parada > 30 dias (mas cobrando disk)",
            "disk_unattached": "Discos não conectados a nada",
            "ip_unassigned": "IPs públicos não associados",
            "snapshot_old": "Snapshots > 1 ano"
        },
        "exemplo": """
        # Detectado (scan automático):

        1️⃣ VM "dev-test-old" (parada há 120 dias)
           └─ Disk: 256GB Premium SSD
           └─ Custo: $50/mês (mesmo parada!)
           └─ 💰 Economia: DELETE → $50/mês

        2️⃣ 8x Discos não conectados
           └─ Total: 2TB
           └─ Custo: $200/mês
           └─ 💰 Economia: DELETE → $200/mês

        3️⃣ 12x IPs públicos não associados
           └─ Custo: $36/mês ($3 cada)
           └─ 💰 Economia: RELEASE → $36/mês

        4️⃣ 45x Snapshots > 1 ano (não usados)
           └─ Total: 500GB
           └─ Custo: $25/mês
           └─ 💰 Economia: DELETE → $25/mês

        TOTAL: $311/mês = $3,732/ano 💸

        # Ação:
        1. Notificar owners (7 dias para responder)
        2. Se não responder → auto-delete
        3. Backup metadata antes (recuperável se erro)
        """
    },

    "SPOT_INSTANCES": {
        "description": "Workloads tolerantes a interrupção em instâncias regulares",
        "impacto_medio": "60-90% economia",
        "deteccao": {
            "candidatos": [
                "Batch processing",
                "CI/CD pipelines",
                "Dev/test environments",
                "Data processing (não real-time)"
            ]
        },
        "exemplo": """
        # Detectado:
        Nightly ETL pipeline (roda 2-4h, 1x/dia)
        └─ VM: Standard_D16s_v3
        └─ Custo atual: $600/mês (pay-as-you-go)

        # Recomendação:
        Azure Spot VM (mesma spec)
        └─ Custo: $60-120/mês (80-90% desconto)
        └─ 💰 Economia: ~$500/mês = $6,000/ano

        # Trade-off:
        - Pode ser interrompido (low probability 2-4am)
        - Implementar checkpointing (retomar de onde parou)
        - Fallback: se spot indisponível, usar regular (1 vez/mês)

        # ROI: Mesmo com 10% fallback, economia de 75%
        """
    },

    "LICENCA_SUBUTILIZADA": {
        "description": "Licenças pagas mas não usadas ativamente",
        "impacto_medio": "Economia variável (remove ou downgrade)",
        "deteccao": {
            "criterios": [
                "Último login > 60 dias",
                "Uso < 10% features (ex: Jira só para ver tickets)",
                "Duplicação (mesmo user em 2 tools similares)"
            ]
        },
        "exemplo": """
        # Detectado:

        1️⃣ GitHub Copilot Business (50 licenças)
           └─ Uso ativo: 32 users (últimos 30 dias)
           └─ 18 licenças sem uso
           └─ Custo: $19/user/mês × 18 = $342/mês
           └─ 💰 Economia: Remove 18 → $342/mês

        2️⃣ Jira (100 licenças)
           └─ Análise de uso:
               - 40 users: uso diário (devs)
               - 30 users: 1x/semana (PMs, designers)
               - 30 users: last login > 90 dias
           └─ Custo: $14/user × 30 = $420/mês
           └─ 💰 Economia: Remove 30 → $420/mês

        3️⃣ Figma Professional (duplicado com Adobe XD)
           └─ 5 designers usando ambos
           └─ Consolidar: migrar para Figma (mais usado)
           └─ Cancelar Adobe XD: $55/user × 5 = $275/mês
           └─ 💰 Economia: $275/mês

        TOTAL: $1,037/mês = $12,444/ano

        # Processo:
        1. Email para users inativos (migração/cancelamento)
        2. Offboarding automático (30 dias sem resposta)
        3. Review trimestral de uso
        """
    }
}
```

---

### **Dimensão 3: OPORTUNIDADES DE CONHECIMENTO**

```python
KNOWLEDGE_OPPORTUNITIES = {
    "PATTERN_LEARNING": {
        "description": "Identificar padrões recorrentes para criar playbooks",
        "deteccao": {
            "troubleshooting_repetido": "Mesmo erro resolvido 3+ vezes → criar runbook",
            "pergunta_frequente": "Mesma dúvida em 5+ conversas Copilot → FAQ",
            "codigo_duplicado": "Função similar em 3+ repos → criar biblioteca"
        },
        "exemplo": """
        # Detectado (clustering de Copilot history):

        Padrão: "Como conectar Azure SQL com Python?"
        └─ Apareceu em: 12 conversas (últimos 60 dias)
        └─ Time gasto: ~45min/vez (pesquisa + tentativa/erro)
        └─ Custo total: 12 × 45min = 9h desperdiçadas

        # Ação Automática:
        1. GPT-4 gera snippet canônico (melhor das 12 soluções)
        2. Adiciona ao Obsidian: "snippets/azure-sql-python.md"
        3. Indexa no vector DB (alta prioridade)
        4. Próxima vez: Copilot sugere snippet em 5s

        # ROI:
        - Economia: 45min → 5s = 99.8% redução
        - Knowledge compound: outros devs usam snippet
        - Próximo ano: ~50 usos × 45min = 37.5h economizadas
        """
    },

    "SKILL_GAP_DETECTION": {
        "description": "Identificar áreas onde time tem dificuldade",
        "deteccao": {
            "copilot_struggles": "Muitas iterações para resolver tarefa",
            "terminal_errors": "Mesmos erros repetidos",
            "google_searches": "Pesquisas similares recorrentes"
        },
        "exemplo": """
        # Detectado (análise ActivityWatch + Terminal):

        Dev: João Silva
        └─ Comandos Git: 40% taxa de erro
            - "git rebase" → erro (5x esta semana)
            - "git cherry-pick" → erro (3x)
            - Undo/reset: 15 tentativas

        └─ Tempo gasto debugging Git: 4h/semana
        └─ Google: "git rebase conflict", "git undo commit" (recorrente)

        # Insight:
        Skill gap: Git workflows avançados

        # Recomendação Automática:
        📚 Sugerir treinamento:
           - Curso: "Git Pro" (Udemy, 6h)
           - Custo: $20
           - ROI: 4h/semana × 48 semanas = 192h/ano
           - Valor: 192h × $75/h = $14,400
           - Payback: 1 dia

        📄 Criar cheat sheet personalizado:
           - Comandos que João mais usa + erra
           - Obsidian: "git-cheatsheet-joão.md"
           - Pin no VS Code sidebar

        🤖 Copilot auto-suggest:
           - Detecta comando Git → previne erros comuns
           - "⚠️ Cuidado: você está em branch main. Criar feature branch primeiro?"
        """
    },

    "BEST_PRACTICE_EXTRACTION": {
        "description": "Capturar soluções elegantes para reutilizar",
        "deteccao": {
            "code_quality": "Função com alta coesão, baixo acoplamento",
            "performance_win": "Otimização que melhorou 10x+",
            "security_fix": "Correção de vulnerabilidade"
        },
        "exemplo": """
        # Detectado (git diff analysis):

        Commit: "Otimizar query de relatórios - 45s → 2s"
        Author: Ana Costa
        File: reports/analytics.py

        Diff:
        - query = db.query(...).all()  # carregava tudo na RAM
        + query = db.query(...).yield_per(1000)  # streaming

        Impact: -95% latência, -90% RAM

        # Ação Automática:
        1. Extrair padrão: "Use yield_per() para queries grandes"
        2. Criar best practice doc:
           - Antes/depois
           - Quando aplicar (N > 10k rows)
           - Code snippet
        3. Adicionar à knowledge base
        4. Lint rule: detectar .all() em queries grandes → sugerir yield_per()

        # Disseminação:
        - Slack: "💡 Ana otimizou query em 95%! Veja como: [link]"
        - Code review bot: cita best practice quando relevante
        - Onboarding: adicionado a "Python Performance Guide"
        """
    },

    "DEPENDENCY_RISK": {
        "description": "Detectar dependências críticas concentradas em 1 pessoa",
        "deteccao": {
            "single_owner": "1 pessoa fez 90%+ commits em módulo crítico",
            "tribal_knowledge": "Conhecimento não documentado"
        },
        "exemplo": """
        # Detectado (git blame + org chart):

        Módulo: payment_processing/
        └─ Commits: 95% por Carlos (único dev que entende)
        └─ Documentação: 0 READMEs, 0 docstrings
        └─ Criticidade: HIGH (processa $500k/mês)

        Risco: Se Carlos sair/férias → time stuck

        # Ação Automática:
        1. 🚨 Alert para CTO: "Bus factor = 1 em módulo crítico"

        2. 📝 Criar documentação obrigatória:
           - GPT-4 gera draft de README (baseado em código)
           - Carlos revisa/aprova (30min vs 4h manual)
           - Adiciona: arquitetura, flows, edge cases

        3. 👥 Knowledge transfer:
           - Pair programming: Carlos + 2 devs (4h)
           - Gravar walkthrough em vídeo (15min)
           - Indexar no knowledge base

        4. 🔄 Code rotation:
           - Próximas features: outro dev implementa (Carlos revisa)
           - Goal: 3 devs confortáveis em 3 meses

        # Métrica:
        Bus factor: 1 → 3 (risco -66%)
        """
    }
}
```

---

### **Dimensão 4: TIPO DE INSIGHT**

```python
INSIGHT_TYPES = {
    "ALERTA_URGENTE": {
        "prioridade": "P0 - Ação imediata",
        "sla_resposta": "24h",
        "exemplos": [
            "Servidor com 95%+ CPU por 6h+ (risco de crash)",
            "CVE crítico detectado em dependência (exploitable)",
            "Custo mensal 50%+ acima do orçado (leak de recursos)",
            "Backup falhou 3+ dias consecutivos (risco de perda)"
        ],
        "notificacao": ["Email", "Slack", "SMS", "PagerDuty"]
    },

    "OPORTUNIDADE_ALTO_IMPACTO": {
        "prioridade": "P1 - Agendar esta semana",
        "sla_resposta": "7 dias",
        "exemplos": [
            "Economia potencial > $1k/mês (rightsizing, reserved)",
            "Automação que economiza 10h+/semana",
            "Security fix (não crítico mas importante)",
            "Performance win > 50% (user experience)"
        ],
        "notificacao": ["Email", "Slack", "Dashboard"]
    },

    "MELHORIA_CONTINUA": {
        "prioridade": "P2 - Incluir no próximo sprint",
        "sla_resposta": "30 dias",
        "exemplos": [
            "Refactoring (reduzir technical debt)",
            "Documentação faltando",
            "Test coverage < 70%",
            "Dependency update (non-breaking)"
        ],
        "notificacao": ["Dashboard", "Weekly digest"]
    },

    "APRENDIZADO": {
        "prioridade": "P3 - Knowledge sharing",
        "sla_resposta": "Contínuo",
        "exemplos": [
            "Padrão interessante descoberto",
            "Nova tecnologia/lib útil",
            "Case study de sucesso",
            "Erro comum + solução"
        ],
        "notificacao": ["Slack #learnings", "Monthly newsletter"]
    }
}
```

---

## 🔧 IMPLEMENTAÇÃO TÉCNICA

### **Pipeline de Classificação**

```python
import openai
import json
from typing import Dict, List
from datetime import datetime, timedelta

class Module4Classifier:
    """
    Classificador inteligente multi-dimensional
    """

    def __init__(self, config):
        self.config = config
        self.openai_client = openai.Client(api_key=config['openai_api_key'])

    def classify_document(self, doc: Dict) -> Dict:
        """
        Classifica documento em todas as dimensões
        """
        classifications = {
            "resource_type": self._classify_resource_type(doc),
            "cost_opportunities": self._detect_cost_opportunities(doc),
            "knowledge_opportunities": self._detect_knowledge_opportunities(doc),
            "insights": self._generate_insights(doc),
            "enrichments": self._enrich_metadata(doc),
            "priority_score": 0  # calculado depois
        }

        # Calcular prioridade final
        classifications['priority_score'] = self._calculate_priority(classifications)

        return classifications

    def _classify_resource_type(self, doc: Dict) -> List[str]:
        """
        Detecta tipo de recurso via GPT-4 + keywords
        """
        # 1. Tentativa rápida: keyword matching
        content_lower = doc['content'].lower()

        matched_types = []
        for resource_type, config in RESOURCE_TYPES.items():
            for keyword in config['palavras_chave']:
                if keyword in content_lower:
                    matched_types.append(resource_type)
                    break

        # 2. Se ambíguo ou vazio: usar GPT-4
        if len(matched_types) != 1:
            prompt = f"""
Classifique este documento em UMA categoria principal:

Categorias: {', '.join(RESOURCE_TYPES.keys())}

Documento:
---
{doc['content'][:1000]}
---

Retorne apenas o nome da categoria (ex: "SERVIDOR").
"""
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )

            gpt_category = response.choices[0].message.content.strip()
            matched_types = [gpt_category] if gpt_category in RESOURCE_TYPES else matched_types

        return matched_types

    def _detect_cost_opportunities(self, doc: Dict) -> List[Dict]:
        """
        Detecta oportunidades de economia de custos
        """
        opportunities = []

        # 1. RIGHTSIZING (baixa utilização de recursos)
        if self._is_azure_resource(doc):
            metrics = self._extract_metrics(doc)

            if metrics.get('cpu_avg') and metrics['cpu_avg'] < 20:
                saving = self._calculate_rightsizing_saving(metrics)
                opportunities.append({
                    "type": "RIGHTSIZING",
                    "current_cost": metrics.get('monthly_cost', 0),
                    "potential_saving": saving,
                    "confidence": 0.95 if self._has_stable_pattern(metrics) else 0.70,
                    "action": f"Downsize de {metrics['current_sku']} para {metrics['recommended_sku']}",
                    "risk": "BAIXO" if saving['percentage'] < 50 else "MÉDIO"
                })

        # 2. RESERVED INSTANCES (uptime alto)
        if self._has_high_uptime(doc):
            ri_saving = self._calculate_reserved_saving(doc)
            opportunities.append({
                "type": "RESERVED_INSTANCES",
                "current_cost": ri_saving['payg_cost'],
                "potential_saving": ri_saving['saving'],
                "confidence": 0.90,
                "action": f"Comprar Reserved Instance ({ri_saving['term']})",
                "risk": "BAIXO"
            })

        # 3. ZOMBIE RESOURCES (inativos)
        if self._is_zombie_resource(doc):
            opportunities.append({
                "type": "ZOMBIE_RESOURCES",
                "current_cost": doc.get('monthly_cost', 50),
                "potential_saving": {"amount": doc.get('monthly_cost', 50), "percentage": 100},
                "confidence": 0.99,
                "action": "DELETE (recurso inativo há 90+ dias)",
                "risk": "ZERO"
            })

        # 4. STORAGE TIERING
        if doc.get('resource_type') == 'ARMAZENAMENTO':
            tiering = self._analyze_storage_access_pattern(doc)
            if tiering['saving']['amount'] > 10:
                opportunities.append({
                    "type": "STORAGE_TIERING",
                    "current_cost": tiering['current_cost'],
                    "potential_saving": tiering['saving'],
                    "confidence": 0.85,
                    "action": f"Mover {tiering['gb_to_cool']}GB para Cool, {tiering['gb_to_archive']}GB para Archive",
                    "risk": "ZERO"
                })

        return opportunities

    def _detect_knowledge_opportunities(self, doc: Dict) -> List[Dict]:
        """
        Detecta oportunidades de aprendizado e otimização
        """
        opportunities = []

        # 1. PADRÕES REPETIDOS (criar playbook)
        if self._is_troubleshooting_doc(doc):
            similar_docs = self._find_similar_issues(doc)

            if len(similar_docs) >= 3:
                opportunities.append({
                    "type": "PATTERN_LEARNING",
                    "pattern": doc.get('issue_title', 'Unknown'),
                    "occurrences": len(similar_docs),
                    "time_wasted": len(similar_docs) * 45,  # minutos
                    "action": "Criar runbook automático",
                    "impact": "HIGH"
                })

        # 2. SKILL GAPS (treinar time)
        if self._has_error_pattern(doc):
            skill_gap = self._analyze_skill_gap(doc)
            opportunities.append({
                "type": "SKILL_GAP_DETECTION",
                "skill": skill_gap['skill_name'],
                "developer": skill_gap['developer'],
                "error_rate": skill_gap['error_rate'],
                "time_wasted_weekly": skill_gap['hours_wasted'],
                "recommended_training": skill_gap['training_suggestions'],
                "impact": "MEDIUM"
            })

        # 3. BEST PRACTICES (documentar e disseminar)
        if self._is_performance_improvement(doc):
            opportunities.append({
                "type": "BEST_PRACTICE_EXTRACTION",
                "improvement": doc.get('title'),
                "impact_metrics": doc.get('metrics', {}),
                "author": doc.get('author'),
                "action": "Documentar e compartilhar com time",
                "impact": "HIGH"
            })

        # 4. DEPENDENCY RISK (bus factor)
        if self._has_single_point_of_knowledge(doc):
            opportunities.append({
                "type": "DEPENDENCY_RISK",
                "module": doc.get('module_name'),
                "owner": doc.get('primary_author'),
                "commit_percentage": doc.get('ownership_percentage', 0),
                "criticality": doc.get('business_criticality', 'MEDIUM'),
                "action": "Knowledge transfer + documentação",
                "impact": "HIGH"
            })

        return opportunities

    def _enrich_metadata(self, doc: Dict) -> Dict:
        """
        Adiciona metadados enriquecidos ao documento
        """
        enrichments = {
            "tags_auto": [],
            "relacionamentos": [],
            "contexto_business": {},
            "metricas_tecnicas": {},
            "owner_sugerido": None,
            "expiration_date": None
        }

        # Tags automáticas (via NER + keywords)
        enrichments['tags_auto'] = self._extract_tags(doc)

        # Relacionamentos (documentos similares)
        enrichments['relacionamentos'] = self._find_related_docs(doc)

        # Contexto de negócio (qual setor/projeto)
        enrichments['contexto_business'] = self._infer_business_context(doc)

        # Métricas técnicas (custo, performance, etc)
        enrichments['metricas_tecnicas'] = self._extract_metrics(doc)

        # Owner sugerido (quem deve cuidar disso?)
        enrichments['owner_sugerido'] = self._suggest_owner(doc)

        # Data de expiração (doc temporário?)
        if self._is_temporary_doc(doc):
            enrichments['expiration_date'] = self._calculate_expiration(doc)

        return enrichments

    def _generate_insights(self, doc: Dict) -> List[Dict]:
        """
        Gera insights acionáveis via GPT-4
        """
        # Preparar contexto para GPT-4
        context = {
            "doc_title": doc.get('title'),
            "doc_type": doc.get('type'),
            "resource_types": self._classify_resource_type(doc),
            "cost_opportunities": self._detect_cost_opportunities(doc),
            "knowledge_opportunities": self._detect_knowledge_opportunities(doc),
            "metrics": self._extract_metrics(doc)
        }

        prompt = f"""
Você é um consultor de TI analisando documentos de uma empresa.

Documento: {doc.get('title')}
Tipo: {doc.get('type')}
Conteúdo (preview): {doc['content'][:500]}

Contexto adicional:
{json.dumps(context, indent=2)}

Gere 3-5 INSIGHTS ACIONÁVEIS:
1. Cada insight deve ter: título, descrição, ação recomendada, impacto (LOW/MEDIUM/HIGH)
2. Focar em: economia de custos, otimização, segurança, conhecimento
3. Ser específico e prático (não genérico)

Formato JSON:
[
  {{
    "titulo": "...",
    "descricao": "...",
    "acao": "...",
    "impacto": "HIGH|MEDIUM|LOW",
    "prioridade": "P0|P1|P2|P3"
  }}
]
"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        insights = json.loads(response.choices[0].message.content)
        return insights.get('insights', [])

    def _calculate_priority(self, classifications: Dict) -> float:
        """
        Calcula score de prioridade (0-100)
        """
        score = 0

        # Peso 1: Economia de custos (0-40 pontos)
        total_saving = sum([
            opp.get('potential_saving', {}).get('amount', 0)
            for opp in classifications.get('cost_opportunities', [])
        ])
        score += min(40, total_saving / 100)  # $100 saving = 1 ponto

        # Peso 2: Insights de alto impacto (0-30 pontos)
        high_impact_insights = [
            ins for ins in classifications.get('insights', [])
            if ins.get('impacto') == 'HIGH'
        ]
        score += len(high_impact_insights) * 10

        # Peso 3: Urgência (0-30 pontos)
        if self._has_p0_alert(classifications):
            score += 30
        elif self._has_p1_opportunity(classifications):
            score += 20

        return min(100, score)

    # Métodos auxiliares (detecção)

    def _is_azure_resource(self, doc: Dict) -> bool:
        keywords = ['azure', 'vm', 'app service', 'sql database']
        return any(k in doc['content'].lower() for k in keywords)

    def _extract_metrics(self, doc: Dict) -> Dict:
        """Extrai métricas via regex ou API calls"""
        # Implementação depende da fonte (Azure Monitor, AWS CloudWatch, etc)
        return {}

    def _has_stable_pattern(self, metrics: Dict) -> bool:
        """Verifica se padrão de uso é estável (90 dias)"""
        return metrics.get('days_monitored', 0) >= 90

    def _calculate_rightsizing_saving(self, metrics: Dict) -> Dict:
        """Calcula economia de downsize"""
        # Lógica de pricing Azure/AWS
        return {"amount": 140, "percentage": 50}

    def _has_high_uptime(self, doc: Dict) -> bool:
        """Detecta se recurso tem uptime alto (candidato a reserved)"""
        return doc.get('uptime_percentage', 0) > 80

    def _is_zombie_resource(self, doc: Dict) -> bool:
        """Detecta recurso inativo"""
        last_activity = doc.get('last_activity_days', 0)
        return last_activity > 90

    def _is_troubleshooting_doc(self, doc: Dict) -> bool:
        keywords = ['error', 'fix', 'troubleshoot', 'debug', 'resolved']
        return any(k in doc['title'].lower() for k in keywords)

    def _find_similar_issues(self, doc: Dict) -> List[Dict]:
        """Busca documentos similares no vector DB"""
        # Query vector DB com embedding do doc
        return []

    def _has_error_pattern(self, doc: Dict) -> bool:
        """Detecta padrão de erros repetidos"""
        return 'error' in doc.get('type', '').lower()

    def _analyze_skill_gap(self, doc: Dict) -> Dict:
        """Analisa gap de conhecimento"""
        return {
            "skill_name": "Git Advanced",
            "developer": doc.get('author'),
            "error_rate": 0.40,
            "hours_wasted": 4,
            "training_suggestions": ["Git Pro course (Udemy)"]
        }

    def _is_performance_improvement(self, doc: Dict) -> bool:
        keywords = ['optimize', 'improve', 'faster', '10x', 'performance']
        return any(k in doc['content'].lower() for k in keywords)

    def _has_single_point_of_knowledge(self, doc: Dict) -> bool:
        """Detecta conhecimento concentrado (bus factor 1)"""
        return doc.get('ownership_percentage', 0) > 90

    def _extract_tags(self, doc: Dict) -> List[str]:
        """Extrai tags via NER"""
        return []

    def _find_related_docs(self, doc: Dict) -> List[str]:
        """Busca docs relacionados"""
        return []

    def _infer_business_context(self, doc: Dict) -> Dict:
        """Infere contexto de negócio (setor, projeto)"""
        return {"setor": "Tecnologia", "projeto": "Plataforma"}

    def _suggest_owner(self, doc: Dict) -> str:
        """Sugere responsável"""
        return doc.get('author', 'Unassigned')

    def _is_temporary_doc(self, doc: Dict) -> bool:
        """Detecta se doc é temporário"""
        temp_keywords = ['temp', 'draft', 'wip', 'test']
        return any(k in doc['title'].lower() for k in temp_keywords)

    def _calculate_expiration(self, doc: Dict) -> str:
        """Calcula data de expiração sugerida"""
        return (datetime.now() + timedelta(days=30)).isoformat()

    def _has_p0_alert(self, classifications: Dict) -> bool:
        return any(
            ins.get('prioridade') == 'P0'
            for ins in classifications.get('insights', [])
        )

    def _has_p1_opportunity(self, classifications: Dict) -> bool:
        return any(
            ins.get('prioridade') == 'P1'
            for ins in classifications.get('insights', [])
        )
```

---

## 📊 OUTPUT DO MÓDULO 4

### **Exemplo de Documento Classificado**

```json
{
  "document_id": "doc_12345",
  "original": {
    "title": "Azure VM Performance Analysis - Oct 2025",
    "source": "Obsidian Vault/Modulo 1/Azure CLI outputs",
    "created_at": "2025-10-15T10:30:00Z",
    "author": "João Silva"
  },

  "classifications": {
    "resource_type": ["SERVIDOR"],
    "sub_types": ["Azure VM", "Windows Server 2022"],

    "cost_opportunities": [
      {
        "type": "RIGHTSIZING",
        "current_cost": 280,
        "potential_saving": {
          "amount": 140,
          "percentage": 50
        },
        "confidence": 0.95,
        "action": "Downsize de Standard_D8s_v3 para Standard_D4s_v3",
        "risk": "BAIXO",
        "implementation_time": "30min",
        "payback_period": "Imediato"
      },
      {
        "type": "RESERVED_INSTANCES",
        "current_cost": 140,
        "potential_saving": {
          "amount": 49,
          "percentage": 35
        },
        "confidence": 0.90,
        "action": "Comprar Reserved Instance (1 ano)",
        "risk": "BAIXO",
        "implementation_time": "5min"
      }
    ],

    "knowledge_opportunities": [
      {
        "type": "PATTERN_LEARNING",
        "pattern": "CPU utilization monitoring setup",
        "occurrences": 8,
        "time_wasted": 360,
        "action": "Criar runbook: Azure VM monitoring setup",
        "impact": "MEDIUM",
        "estimated_saving": "6h/mês"
      }
    ],

    "insights": [
      {
        "titulo": "Economia de $189/mês combinando rightsizing + reserved",
        "descricao": "VM está 50% subutilizada. Após downsize, comprar reserved instance resulta em economia total de 67%.",
        "acao": "1) Agendar downsize (sábado 2am), 2) Comprar RI após validação (1 semana)",
        "impacto": "HIGH",
        "prioridade": "P1",
        "estimated_roi": "$2,268/ano"
      },
      {
        "titulo": "Documentar processo de monitoring setup",
        "descricao": "Time configurou Azure Monitor 8x em VMs diferentes (mesmo processo). Criar template/runbook economiza 45min/vez.",
        "acao": "João (autor original) cria runbook com GPT-4 assist (15min)",
        "impacto": "MEDIUM",
        "prioridade": "P2",
        "estimated_roi": "6h/ano economizadas"
      }
    ],

    "enrichments": {
      "tags_auto": [
        "azure",
        "virtual-machine",
        "windows-server",
        "performance-monitoring",
        "cost-optimization"
      ],

      "relacionamentos": [
        {
          "doc_id": "doc_98765",
          "title": "Azure Cost Report - Oct 2025",
          "similarity": 0.87,
          "relationship": "Este VM aparece no cost report como top 3 gastos"
        },
        {
          "doc_id": "doc_45678",
          "title": "Windows Server Patching Guide",
          "similarity": 0.72,
          "relationship": "Mesmo OS version, patching process aplicável"
        }
      ],

      "contexto_business": {
        "setor": "Tecnologia",
        "projeto": "Production API Backend",
        "criticality": "HIGH",
        "sla": "99.9% uptime"
      },

      "metricas_tecnicas": {
        "cpu_avg_30d": 12,
        "ram_avg_30d": 25,
        "disk_io_avg": "low",
        "network_throughput": "medium",
        "uptime_90d": 99.8,
        "incident_count_90d": 0
      },

      "owner_sugerido": "João Silva (Infrastructure Team)",
      "expiration_date": null
    },

    "priority_score": 78
  },

  "next_actions": [
    {
      "action": "Agendar downsize VM",
      "owner": "João Silva",
      "due_date": "2025-11-17",
      "estimated_effort": "30min",
      "dependencies": ["Aprovar com stakeholders", "Backup antes"]
    },
    {
      "action": "Comprar Reserved Instance",
      "owner": "João Silva",
      "due_date": "2025-11-24",
      "estimated_effort": "5min",
      "dependencies": ["Validar downsize funcionou"]
    },
    {
      "action": "Criar runbook de monitoring",
      "owner": "João Silva",
      "due_date": "2025-11-30",
      "estimated_effort": "15min",
      "dependencies": []
    }
  ]
}
```

---

## 🚀 INTEGRAÇÃO COM MÓDULOS ANTERIORES

```
Módulo 1: COLETA
↓
Documentos brutos
↓
Módulo 2: AGREGAÇÃO
↓
Dados normalizados
↓
Módulo 3: PROCESSAMENTO SEMÂNTICO
↓
Embeddings + Clusters + Knowledge Graph
↓
Módulo 4: CLASSIFICAÇÃO & ENRIQUECIMENTO ⭐
↓
├─ Classificações multi-dimensionais
├─ Oportunidades de economia
├─ Oportunidades de conhecimento
├─ Insights acionáveis
├─ Metadados enriquecidos
└─ Priorização inteligente
↓
Módulo 5: DECISÃO (próximo)
↓
Ações automáticas + Dashboards
```

---

## 📈 MÉTRICAS DE SUCESSO DO MÓDULO 4

```python
KPIs = {
    "CLASSIFICACAO": {
        "Accuracy": "> 90%",  # classificação correta de resource type
        "Coverage": "> 95%",  # % docs classificados (não "unknown")
        "Latency": "< 5s/doc"  # tempo de processamento
    },

    "DETECCAO_OPORTUNIDADES": {
        "Precision": "> 80%",  # oportunidades sugeridas são válidas
        "Recall": "> 70%",  # captura maioria das oportunidades reais
        "False Positive Rate": "< 15%"  # não sugerir mudanças desnecessárias
    },

    "IMPACTO_BUSINESS": {
        "Economia Identificada": "> $10k/mês",
        "Tempo Economizado": "> 40h/mês",
        "Incidents Prevenidos": "> 5/mês"
    },

    "QUALIDADE_INSIGHTS": {
        "Actionability": "> 85%",  # insights levam a ações concretas
        "User Satisfaction": "> 4.2/5",  # feedback do time
        "Time to Value": "< 7 dias"  # da detecção à implementação
    }
}
```

---

## 🎓 RESUMO EXECUTIVO

**Módulo 4 = "Cérebro" do Sistema**

**Entrada:**
- Documentos processados (embeddings, clusters, grafos)

**Processamento:**
- Classificação multi-dimensional (8 tipos de recursos)
- Detecção de 6 tipos de oportunidades de custo
- Detecção de 4 tipos de oportunidades de conhecimento
- Geração de insights via GPT-4
- Enriquecimento de metadados
- Priorização inteligente (score 0-100)

**Saída:**
- Documentos enriquecidos com classificações, tags, relacionamentos
- Lista priorizada de oportunidades (economia + conhecimento)
- Insights acionáveis (P0/P1/P2/P3)
- Next actions com owners e deadlines

**ROI Esperado:**
- 🎯 **Economia:** $10-50k/mês identificados automaticamente
- ⏱️ **Tempo:** 40-100h/mês economizadas (automação + best practices)
- 📚 **Conhecimento:** Redução de 70% em "tempo para resolver problemas repetidos"
- 🚨 **Prevenção:** 5-15 incidents/mês evitados (alertas proativos)

**Próximo Passo:**
→ **Módulo 5: DECISÃO** (dashboards + automação de ações)

---

*Última Atualização: 2025-11-10*
