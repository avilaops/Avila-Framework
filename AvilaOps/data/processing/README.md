# Data Processing

## Contexto
Transformações analíticas realizadas após ingestão para padronização, enriquecimento e criação de features.

## Objetivo
Concentrar pipelines de processamento (dbt, Spark, Python, SQL) garantindo versionamento, testes automatizados e documentação técnica.

## Estrutura Recomendada
- `dbt/` — modelos, seeds, macros.
- `spark/` — jobs distribuídos.
- `python/` — scripts Pandas/Polars.
- `tests/` — validações unitárias/integradas.
- `docs/` — catálogo de modelos e SLAs.

## Rotinas Essenciais
- Executar `dbt test` ou equivalentes antes de liberar merges.
- Integrar com dashboards de qualidade (`data/dashboards`).
- Documentar dependências cruzadas com `data/warehouse`.

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
