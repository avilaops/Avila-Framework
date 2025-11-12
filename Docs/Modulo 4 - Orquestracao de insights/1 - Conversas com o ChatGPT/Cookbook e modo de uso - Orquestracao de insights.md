# Modulo 4 - Orquestracao de insights e acao

## Visao geral
- Objetivo: transformar datasets curados (Modulos 1-3) em decisoes aplicaveis que geram economia, expandem conhecimento institucional e otimizam infraestrutura e servicos.
- Escopo: analise de valor, motor de recomendacoes, roteamento de iniciativas por categoria (economia, conhecimento, infraestrutura/servidores, experiencia cliente, compliance).
- Responsaveis principais: Conselho de Valor (diretores), Squad de Inteligencia de Negocio, Squad de Operacoes e Squad de Cultura & Conhecimento.

## Arquitetura operacional
- **Camada de input**: datasets curados (`datalake/curated`), indicadores do Modulo 3 (desempenho de agentes), telemetry de custos (Azure Cost Management, finops).
- **Camada semantica**: ontologia enriquecida (dominios, produtos, setores, metas OKR) + embeddings para mapear insights relevantes.
- **Motor de insights**: pipelines analiticas (`analytics/modulo4`) usando notebooks (Python, SQL, PowerBI) e agentes de raciocinio (LangChain/Semantic Kernel) para gerar hipoteses.
- **Camada de decisao**: paines decisorios (PowerBI/Grafana + Obsidian) com matrizes de priorizacao, fluxo RACI e registro de playbooks aprovados.
- **Camada de execucao**: automacoes acionadas (Azure DevOps, GitHub Actions, ServiceNow, Scripts PowerShell) e squads responsaveis.
- **Camada de aprendizagem**: biblioteca de conhecimento (`knowledge-base/modulo4`) e reavaliacao continua dos modelos e regras.

## Taxonomia de categorias
- **Economia**: reducao de custos operacionais, racionalizacao de licencas, finops de nuvem.
- **Aumento de conhecimento**: programas de upskilling, documentacao, trilhas de aprendizagem.
- **Infraestrutura/servidores**: otimizacao de workloads, resiliencia, escalabilidade, migracoes.
- **Experiencia cliente**: NPS, tempo de resposta, personalizacao usando IA.
- **Compliance & risco**: conformidade regulatoria, auditoria, governanca de dados.

## Cookbook de orquestracao

### 0. Preparacao
- Validar atualizacao dos datasets curados (`catalogo_curated.csv`) e dos indicadores operacionais.
- Confirmar objetivos trimestrais (OKRs) e thresholds financeiros/operacionais.
- Atualizar pesos do scorecard em `config/modulo4/score_params.yaml`.

### 1. Mineracao de insights
- Executar notebooks `analytics/modulo4/descoberta_*.ipynb` para gerar candidatos a insight.
- Utilizar tecnicas: analise de Pareto, series temporais, anomaly detection, clustering semantico.
- Registrar cada insight bruto em `insights/backlog_raw.md` com atributos: categoria proposta, impacto estimado, confianca, referencia de dados.

### 2. Refinamento semantico
- Aplicar agentes de linguagem (OpenAI GPT-4.1, Azure OpenAI) com prompts em `prompts/modulo4/refinamento.md` para estruturar insights.
- Normalizar linguagem segundo ontologia (`knowledge-schema.md`) e remover redundancias.
- Submeter amostra para validacao humana (Conselho de Valor) e ajustar criterios.

### 3. Scorecard e priorizacao
- Calcular score `S = 0.35*ImpactoEconomico + 0.25*GanhoConhecimento + 0.2*Urgencia + 0.1*Viabilidade + 0.1*RiscoNegativo`.
- Classificar insights por faixa: A (>=0.8), B (0.6-0.79), C (<0.6).
- Visualizar no dashboard `dashboards/modulo4/scoreboard.pbix` com filtros por categoria.

### 4. Planejamento de acao
- Para cada insight A/B, criar plano em `planos/YYY-MM-DD_nome.md` com campos: objetivo, squad responsavel, milestones, automacoes, indicadores esperados.
- Linkar playbooks existentes ou criar novos em `playbooks/*.md`.
- Validar com Operacoes e Finops para garantir capacidade de execucao.

### 5. Execucao monitorada
- Disparar automacoes (scripts, pipelines) conforme plano aprovado.
- Utilizar Kanban `boards/modulo4` para acompanhar status (Backlog, Em execucao, Validacao, Concluido).
- Registrar logs de execucao em `logs/modulo4/execucao_*.md` com metrica real vs prevista.

### 6. Aprendizagem e retroalimentacao
- Medir resultados com lag definidos (30, 60, 90 dias) e comparar com baseline.
- Atualizar knowledge base (`knowledge-base/modulo4/casos_de_sucesso.md`) e matriz de competencias.
- Recalibrar scorecard com dados reais (ajuste de pesos e thresholds).

### 7. Publicacao de valor
- Criar relatórios executivos (`relatorios/OKR_modulo4_Q*.md`), newsletters internas e comunicados para clientes quando aplicavel.
- Atualizar bibliotecas de prompts e agentes com novos exemplos de alto valor.
- Feed integração com Modulo 1 (coleta de feedback e novas demandas) e Modulo 3 (ajuste de agentes produtivos).

## Modo de uso operacional

### Ritmo de cadencia
- **Semanal**: triagem de novos insights e atualizacao de Kanban.
- **Mensal**: reuniao do Conselho de Valor para priorizar e liberar recursos.
- **Trimestral**: revisao de OKRs, scorecard e publicacao de resultados.

### Papeis e responsabilidades
- **Conselho de Valor**: decide prioridades, aprova investimentos, monitora ROI.
- **Squad de BI/Finops**: mantem pipelines analiticos, calcula impactos economicos.
- **Squad de Conhecimento**: transforma insights em trilhas educacionais e playbooks.
- **Squad de Operacoes/Infra**: executa ajustes tecnicos, monitora workloads.
- **PMO/Agile Coach**: garante cadencia, remove impedimentos, coleta feedback.

## Ferramentas e tecnologias
- PowerBI, Grafana, Azure Data Explorer/Kusto, dbt para models analiticos.
- Azure Machine Learning/Databricks para modelos probabilisticos de ROI.
- LangSmith ou PromptFlow para monitoria de agentes de recomendacao.
- ServiceNow/Jira para governar execucao e change management.
- Obsidian para documentação narrativa e storytelling dos casos de uso.

## KPIs modulo 4
- `ROI_iniciativas >= 1.5` (retorno sobre investimento médio por insight executado).
- `Taxa_execucao_insights_A >= 85%` dentro do trimestre.
- `Ganho_horas_equivalentes` em economia operacional > meta anual.
- `Indice_uplift_conhecimento` medido por quiz interno >= 0.25 incremento.
- `Tempo_medio_implantacao` (aprovacao -> execucao) <= 30 dias.

## Governanca e compliance
- Utilizar matriz de criticalidade para verificar necessidade de aprovacao adicional (seguranca, juridico).
- Garantir rastreabilidade: cada insight vinculado a dados fonte e decisor.
- Auditorias semestrais de fairness e vies nos modelos de recomendacao.
- Politicas de comunicacao interna para evitar overload de iniciativas.

## Playbook de automacao
- Jobs agendados no Azure Data Factory/SQL para alimentar dashboards.
- GitHub Actions para rodar notebooks de descoberta e publicar resultados no repositorio.
- Webhooks para atualizar boards e enviar notificacoes Teams/Slack quando um insight muda de fase.

## Anexos futuros
- Biblioteca de modelos financeiros (payback, NPV, TCO).
- Templates de comunicados e workshops de compartilhamento de conhecimento.
- Lista priorizada de otimizações de nuvem (reservas, rightsizing, spot instances).
