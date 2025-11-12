# 🧠 Estratégia de IA para Produtos Ávila
**Data:** 11 de novembro de 2025  
**Objetivo:** Aplicar os 9 agentes do AvilaOps-AI para melhorar produtos ON e Geolocation

---

## 📊 Mapeamento: Agentes → Produtos

### **Produto: ON** (Onboarding & Operações)

| Agente | Aplicação | KPIs Impactados |
|--------|-----------|----------------|
| **Lumen** | Análise preditiva de Time-to-Value (TTV); identificação de padrões de churn em onboarding | TTV, Retenção, DAU/MAU |
| **Vox** | Automação de follow-ups pós-onboarding; qualificação de leads baseada em uso | Tickets de suporte, Recontratação |
| **Atlas** | Consolidação de dashboards executivos com métricas de adoção (30/60/90 dias) | Decisões estratégicas |
| **Helix** | Monitoramento de pipelines de onboarding; automação de provisionamento | Tempo de resolução |
| **Sigma** | *(não documentado, inferido: Analytics Financeiro)* Cálculo de CAC/LTV por coorte de onboarding | ROI, Margem |

### **Produto: Geolocation** (Localização + Interesses → Comercial)

| Agente | Aplicação | KPIs Impactados |
|--------|-----------|----------------|
| **Lumen** | Modelo de classificação de interesse via UTM/Tags; clustering geográfico (geohash) | Acurácia, Conversão |
| **Vox** | Enriquecimento de leads com dados de localização; priorização comercial por região×interesse | Win-rate, CAC |
| **Lex** | Validação de compliance (LGPD/GDPR) em coleta de GPS; auditoria de consentimento | Risco de privacidade |
| **Helix** | Cache local-first para reduzir latência; pseudonimização no ingestion | Latência p95, Custo/1k |
| **Sigma** | Agregação por k-anonimato (k≥20); geração de `sales_targets` por região | Heatmap, CAC/LTV |
| **Echo** | Mensagens personalizadas por coorte interesse×região | Taxa de qualificação |

---

## 🗂️ Estrutura das Pastas Vazias

### **1. `datasets/`** - Dados Estruturados para Treinamento

```
datasets/
├── on/
│   ├── onboarding_events.parquet        # Eventos de uso (DAU/MAU)
│   ├── support_tickets.json             # Tickets + tempo de resolução
│   ├── retention_cohorts.csv            # Análise de retenção 30/60/90d
│   └── README.md                        # Dicionário de dados
├── geolocation/
│   ├── gps_samples.parquet              # Lat/long + acurácia + timestamp
│   ├── interest_taxonomy.json           # Tags UTM → interesse
│   ├── sales_targets.csv                # Região×interesse → conversão
│   └── privacy_consent_log.json         # Registros de consentimento LGPD
└── shared/
    ├── crm_interactions.parquet         # Dados de CRM (HubSpot/Salesforce)
    └── marketing_utm_clicks.json        # Cliques de newsletter/social
```

**Responsável:** Lumen (Analytics) + Helix (Engenharia de dados)

---

### **2. `📚 Agente Bibliotecário ("Archivus")/`** - Sistema RAG

**Propósito:** Indexar documentação de produtos, governance, policies e servir como base de conhecimento para todos os agentes.

```
📚 Agente Bibliotecário ("Archivus")/
├── vector_store/
│   ├── chromadb/                        # Vector DB persistente
│   └── embeddings_cache.pkl             # Cache de embeddings
├── indexed_docs/
│   ├── products/                        # on.md, geolocation.md
│   ├── governance/                      # Políticas LGPD, compliance
│   ├── analytics/                       # Taxonomias, datasources
│   └── architecture/                    # Filosofia Ávila, tech stack
├── archivus_agent.py                    # Agente RAG principal
├── config.yaml                          # Configuração (chunking, embeddings)
└── README.md                            # Guia de uso
```

**Capacidades:**
- **Consulta semântica:** Agentes perguntam "Como coletar GPS com compliance LGPD?" → Archivus retorna trechos relevantes de `geolocation.md` + policies
- **Auditoria de integridade:** Valida se documentação está atualizada
- **Alertas:** Notifica Atlas quando políticas mudam

**Implementação:**
- Vector store: ChromaDB (open-source, local)
- Embeddings: `text-embedding-3-large` (OpenAI)
- Chunking: 500 tokens com overlap de 50
- Retrieval: Top-5 com re-ranking

**Responsável:** Lumen (ML) + Lex (Compliance)

---

### **3. `fine_tuning/`** - Modelos Customizados

**Casos de Uso:**

| Modelo | Propósito | Dataset | Agente Responsável |
|--------|-----------|---------|-------------------|
| `interest_classifier` | Classificar interesse a partir de UTM/Tags | `interest_taxonomy.json` | Lumen |
| `churn_predictor` | Prever churn em onboarding (TTV > 30d) | `retention_cohorts.csv` | Lumen |
| `geolocation_ner` | Extrair entidades geográficas de texto | Anotações customizadas | Vox |
| `compliance_validator` | Validar conformidade de contratos | `security_policies/` | Lex |

**Estrutura:**

```
fine_tuning/
├── datasets_annotated/
│   ├── interest_classification_train.jsonl
│   ├── churn_prediction_train.csv
│   └── ner_geolocation_train.jsonl
├── scripts/
│   ├── train_interest_classifier.py
│   ├── evaluate_churn_model.py
│   └── deploy_to_helix.sh                # CI/CD via Helix
├── models/
│   ├── interest_classifier_v1.pkl
│   └── churn_predictor_v2.onnx
└── README.md
```

**Responsável:** Lumen (treinamento) + Helix (deploy)

---

### **4. `prompts/`** - Biblioteca de Templates Reutilizáveis

**Organização por Agente:**

```
prompts/
├── atlas/
│   ├── executive_summary.md             # Dashboard executivo
│   └── strategic_decision.md            # Template de decisão
├── lumen/
│   ├── data_analysis.md                 # Análise exploratória
│   ├── churn_prediction.md              # Prompt para modelo churn
│   └── clustering_geohash.md            # Agregação geográfica
├── vox/
│   ├── lead_qualification.md            # Qualificação de lead
│   └── followup_automation.md           # Cadência de contato
├── lex/
│   ├── compliance_check.md              # Validação LGPD/GDPR
│   └── contract_review.md               # Análise de contrato
├── helix/
│   ├── pipeline_monitoring.md           # Alerta de pipeline
│   └── incident_response.md             # Resposta a incidentes
├── sigma/
│   ├── financial_forecast.md            # Projeção CAC/LTV
│   └── cohort_analysis.md               # Análise por coorte
└── shared/
    ├── rag_query.md                     # Template para Archivus
    └── telemetry_log.md                 # Estrutura de log
```

**Exemplo - `lumen/churn_prediction.md`:**

```markdown
---
agent: Lumen
use_case: Predição de Churn
model: gpt-4o
temperature: 0.3
---

# Predição de Churn - Onboarding

Você é Lumen, o agente de Analytics da Ávila. Analise os dados de onboarding abaixo e identifique usuários em risco de churn.

## Dados de Entrada:
- **User ID:** {{user_id}}
- **Cadastro:** {{signup_date}}
- **Último acesso:** {{last_login}}
- **Features usadas:** {{features_used}}
- **Tickets abertos:** {{support_tickets}}

## Critérios de Risco:
- TTV > 30 dias sem atividade
- < 3 features usadas
- > 2 tickets críticos

## Saída Esperada:
1. **Risco:** Baixo | Médio | Alto
2. **Justificativa:** [explicação]
3. **Ação recomendada:** [follow-up Vox / tutorial / desconto]
```

**Responsável:** Cada squad de agente mantém seus próprios prompts

---

### **5. `rag/`** - Sistema RAG Compartilhado

**Diferença de Archivus:**
- **Archivus:** RAG focado em documentação interna (policies, produtos)
- **`rag/`:** RAG genérico para knowledge base externa (blogs, papers, integrações)

```
rag/
├── vector_stores/
│   ├── product_docs/                    # ChromaDB para produtos
│   ├── external_apis/                   # Docs de APIs externas (HubSpot, etc.)
│   └── research_papers/                 # Papers de ML/Geolocation
├── embeddings/
│   ├── openai_embeddings.py             # Wrapper OpenAI
│   └── cache_manager.py                 # Cache de embeddings
├── retrieval/
│   ├── semantic_search.py               # Busca vetorial
│   ├── reranker.py                      # Re-ranking com cross-encoder
│   └── query_router.py                  # Roteamento de consultas
├── ingestion/
│   ├── crawlers/
│   │   ├── hubspot_docs_crawler.py
│   │   └── arxiv_papers_crawler.py
│   └── chunking_strategies.py           # Chunking inteligente
└── README.md
```

**Fluxo:**
1. Agente faz pergunta → `query_router` decide qual vector store usar
2. `semantic_search` retorna top-10
3. `reranker` reordena por relevância → top-3
4. Contexto injetado no prompt do agente

**Responsável:** Lumen (ML) + Helix (infra)

---

## 🎯 Roadmap de Implementação

### **Fase 1: Fundação (Semanas 1-2)**
- [x] Documentar estratégia (este arquivo)
- [ ] Criar estrutura de pastas `datasets/`, `prompts/`, `rag/`, `fine_tuning/`
- [ ] Implementar Archivus com ChromaDB
- [ ] Migrar documentação existente para Archivus (`products/`, `governance/`)

### **Fase 2: Dados (Semanas 3-4)**
- [ ] Coletar datasets de ON (onboarding, tickets, retenção)
- [ ] Coletar datasets de Geolocation (GPS samples, taxonomia de interesse)
- [ ] Criar dicionários de dados em cada `README.md`
- [ ] Validar compliance com Lex

### **Fase 3: Prompts (Semana 5)**
- [ ] Criar biblioteca de prompts para 6 agentes prioritários (Lumen, Vox, Atlas, Lex, Helix, Sigma)
- [ ] Testar prompts com dados reais
- [ ] Versionamento no Git

### **Fase 4: RAG (Semanas 6-7)**
- [ ] Implementar `rag/` com ChromaDB
- [ ] Crawlers para docs externas (HubSpot, Salesforce)
- [ ] Integrar retrieval com On.Core

### **Fase 5: Fine-Tuning (Semanas 8-10)**
- [ ] Anotar datasets para `interest_classifier` e `churn_predictor`
- [ ] Treinar modelos com Lumen
- [ ] Deploy via Helix em `ai/fine_tuning/models/`

### **Fase 6: Integração (Semanas 11-12)**
- [ ] Conectar agentes aos produtos (ON + Geolocation)
- [ ] Dashboards em Grafana com métricas de produtos
- [ ] Testes A/B com pilotos

---

## 📈 Métricas de Sucesso

### **ON (Onboarding)**
| Métrica | Baseline | Meta 3 meses | Agente |
|---------|----------|--------------|--------|
| TTV médio | ? | -30% | Lumen |
| Taxa de retenção 30d | ? | +15% | Vox |
| Tickets/usuário | ? | -25% | Helix |

### **Geolocation**
| Métrica | Baseline | Meta 3 meses | Agente |
|---------|----------|--------------|--------|
| Acurácia de classificação de interesse | ? | >85% | Lumen |
| Win-rate por região×interesse | ? | +20% | Vox + Sigma |
| Latência p95 geocoding | ? | <200ms | Helix |
| Custo/1k consultas | ? | -40% | Helix |

---

## 🔐 Compliance & Governança

### **LGPD/GDPR (Responsável: Lex)**
- ✅ Todos os datasets em `geolocation/` possuem log de consentimento
- ✅ Pseudonimização obrigatória antes de análise
- ✅ Agregação por k-anonimato (k≥20)
- ✅ Retenção máxima: 90 dias (justificar se > 90d)
- ✅ DPIA obrigatória para GPS em larga escala

### **Auditoria (Responsável: Archivus + Lex)**
- Logs de acesso a datasets sensíveis
- Versionamento de políticas em Archivus
- Alertas automáticos quando compliance muda

---

## 🚀 Próximos Passos Imediatos

1. **Criar estrutura de pastas** (hoje)
2. **Implementar Archivus** com docs existentes (2 dias)
3. **Coletar 1º dataset de ON** (onboarding_events) (3 dias)
4. **Testar 1º prompt com Lumen** (churn_prediction) (1 dia)
5. **Configurar RAG básico** para consultas a produtos (3 dias)

---

**Autor:** GitHub Copilot + Nicolas (Ávila)  
**Revisão:** Atlas Squad (estratégia) + Lumen Squad (IA)  
**Status:** 🚧 Em construção
