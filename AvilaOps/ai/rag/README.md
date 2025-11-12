# AI RAG

## Contexto
Área dedicada a pipelines de Retrieval-Augmented Generation (RAG) empregados pelos agentes (Atlas, Archivus, Lumen) para consulta contextual a bases internas.

## Objetivo
Manter infraestrutura de ingestão, indexação e consulta (vectordb, chunking, prompts) garantindo consistência com políticas de segurança Ávila.

## Estrutura Recomendada
- `pipelines/` — scripts de ingestão e atualização de índices.
- `configs/` — YAML de provedores (OpenAI, Azure AI Search, Pinecone, etc.).
- `evaluations/` — resultados de testes de precisão/recall.
- `docs/` — decisões arquiteturais e playbooks de rollout.

## Rotinas Essenciais
- Automatizar atualização de índices via `devops/pipelines` (cron semanal).
- Versionar configs sensíveis usando `Shared/templates` + secrets externos.
- Integrar métricas com `ai/On/observability` para rastrear latência e relevância.

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
