# Dashboards Gerenciais — Operação Ávila Inc

## Visão Geral
Objetivo: monitorar operação ponta a ponta (marketing → vendas → atendimento → financeiro) para garantir redução de custos e aumento de receita dos clientes. Atualização padrão: diária (dados automáticos) + resumo executivo semanal (email).

## Dashboard 1 — Executive Pulse
- Público: direção, coordenador
- Pergunta central: estamos entregando impacto financeiro e mantendo SLAs?
- Seções/visualizações:
  - **Resumo financeiro**: gráfico de barras (semanas) com receita incremental gerada, custos otimizados (R$), margem projetada. Fonte: `sales_targets`, `finance/balancos`.
  - **12 KPIs chave** (cards): CAC, LTV, payback, margem, satisfação (CSAT/NPS), FRT médio, taxa de resolução 24h, leads qualificados, wins, churn, inadimplência, execução 30-60-90.
  - **Alertas**: tabela de exceções (KPI abaixo de meta) com responsável e plano.
- Interação: filtros por região (BR/PT), cliente, segmento.

## Dashboard 2 — Revenue Engine
- Público: equipe comercial e marketing
- Pergunta central: quais regiões/interesses trazem mais receita a melhor custo?
- Visualizações:
  - Heatmap região×interesse (coortes ≥20) destacando volume, qualificação, win-rate.
  - Funil por interesse (leads → qualificados → proposta → win) com tempos médios.
  - CAC vs LTV scatter por campanha (`utm.id`).
  - Tabela de recomendações (canal/mensagem) derivada de `sales_targets`.
- Métricas base: `events_utm`, `sales_targets`, `crm_stages`, custos de campanha.

## Dashboard 3 — Delivery & Service Ops
- Público: operações, atendimento, produto.
- Pergunta central: estamos cumprindo SLAs e extraindo valor dos produtos?
- Visualizações:
  - Tempo de atendimento (FRT, TMA, resolução 24h) por equipe/canal.
  - Volume de tickets por categoria/interesse (WhatsApp tags).
  - Adoção de produto (ON, Geolocation) — gauge com DAU/MAU, TTV, churn/retenção.
  - Checklist 30-60-90 por cliente (status: verde/amarelo/vermelho).
- Fontes: `whatsapp_tags`, `crm_stages`, métricas de produto (`docs/products/on.md`, `geolocation.md`).

## Dados necessários & integrações
- Warehouse central (ex.: PostgreSQL) com camadas staging → analytics.
- Jobs diários (GitHub Actions ou Airflow) para ingestão de:
  - Bancos (Wise/Inter/Nubank)
  - UTMs (site/email/social)
  - WhatsApp tags
  - CRM pipeline
  - Produtos (Geolocation/ON)
- Validações automáticas: checar k-anonimato (k≥20), metas, desvios >10% semanais.

## Métricas meta (baseline 2025)
- CAC ≤ R$ 2.000 por deal ganho
- LTV/CAC ≥ 4x
- Payback ≤ 3 meses
- Margem operacional ≥ 25%
- CSAT ≥ 90 / NPS ≥ 60
- FRT ≤ 4h úteis, resolução padrão ≤ 24h úteis
- Taxa de execução de plano 30-60-90 ≥ 85%

## Operação
- BI tool sugerida: Metabase / Power BI (com row-level security PT/BR)
- Controle de versões do dashboard: specs em repositório + export .pbix/.json
- Auditoria: registrar alterações no dashboard com change log e aprovação do coordenador.
