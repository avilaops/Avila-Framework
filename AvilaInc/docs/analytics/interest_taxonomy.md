# Interest Taxonomy

Authoritative list of interest slugs used in `utm.term` and content front-matter.

Format: slug | description | category | example signals

## Core Financial Outcomes
- reduzir_custos | iniciativas para diminuir despesas operacionais | financeiro | cliques em guias de otimização de custos
- aumento_receita | crescimento de faturamento e expansão comercial | comercial | leitura de case aumento de ticket
- margem_operacional | melhorar margem bruta ou líquida | financeiro | engajamento em análise de margem

## Operational & Process
- eficiencia_processos | automação e melhoria contínua | operações | interesse em workflow simplification
- compliance_privacidade | LGPD/GDPR e segurança de dados | compliance | cliques em política de privacidade

## Marketing & Growth
- marketing_performance | otimização de canais e CAC | marketing | uso de UTMs em campanhas
- conteudo_estrategico | estratégia de conteúdo e autoridade | marketing | leitura de bastidores/guia editorial

## Product & Delivery
- produto_adocao | adoção de funcionalidades e onboarding | produto | engajamento em tutoriais
- produto_valor | medir impacto do produto em KPIs | produto | cliques em métricas de valor

Governance rules:
- One primary slug per asset → `utm.term`
- Secondary interests listed in front-matter `interests: []`
- New slugs require PR with justification (impact esperado + definição clara)
