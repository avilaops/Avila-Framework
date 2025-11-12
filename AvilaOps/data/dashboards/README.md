# Data Dashboards

## Contexto
Repositório de painéis analíticos publicados pela área de Dados & Analytics (Power BI, Grafana, Looker Studio). Concentra assets versionáveis, queries e instruções de deploy.

## Objetivo
Garantir rastreabilidade das métricas corporativas e disponibilizar templates padronizados para squads e diretoria.

## Estrutura Recomendada
- `grafana/` — dashboards JSON e datasources.
- `powerbi/` — `.pbix` + scripts de refresh.
- `looker/` — especificações LookML ou exports.
- `docs/` — catálogo com descrição e owners de cada painel.

## Rotinas Essenciais
- Validar consistência com dicionário de dados (`Docs/styleguides`).
- Automatizar deploy via tasks em `devops/pipelines`.
- Registrar auditorias no Archivus (`Docs/Relatorios/Auditorias`).

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
