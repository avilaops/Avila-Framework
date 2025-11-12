# Data Warehouse

## Contexto
Camada de armazenamento consolidado (Data Warehouse/Lakehouse) utilizada por dashboards, APIs e modelos de IA corporativos.

## Objetivo
Documentar modelagem dimensional, camadas (bronze, prata, ouro) e processos de governança para consultas críticas.

## Estrutura Recomendada
- `models/` — esquemas dimensionais/fact tables (SQL, dbt).
- `policies/` — regras de acesso, mascaramento, retenção.
- `migrations/` — scripts de evolução de schema.
- `docs/` — diagramas e dicionário de dados.

## Rotinas Essenciais
- Sincronizar catálogos com `governance/` e `docs/security_policies`.
- Registrar alterações estruturais em ADRs (`docs/architecture`).
- Monitorar custos e desempenho via dashboards específicos.

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
