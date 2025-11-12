# Data Ingestion

## Contexto
Pipelines de ingestão responsáveis por trazer dados de ERPs, CRMs, APIs externas e sensores industriais para o lake corporativo.

## Objetivo
Manter scripts, configs e documentação dos fluxos ELT/ETL utilizados em produção, garantindo sla de ingestão e qualidade.

## Estrutura Recomendada
- `sources/` — connectors (PowerShell, Python, Airbyte, Fivetran configs).
- `schedules/` — cron jobs, orchestrators (Airflow, Prefect).
- `schemas/` — contratos de dados (JSON/YAML) para validação.
- `tests/` — suites de qualidade (Great Expectations, Soda).

## Rotinas Essenciais
- Registrar cada integração em `docs/catalogo_ingestao.md` (a criar).
- Automatizar validação em pipelines `devops/pipelines`.
- Reportar status diário em dashboards de ingestão (`data/dashboards`).

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
