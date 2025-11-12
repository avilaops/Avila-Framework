# Infra Docker

## Contexto
Central de imagens, Dockerfiles, composes e guidelines para containers utilizados em pipelines, agentes e produtos.

## Objetivo
Garantir templates padronizados, segurança em builds e reprodutibilidade em ambientes locais/CI.

## Estrutura Recomendada
- `dockerfiles/` — imagens base padronizadas.
- `compose/` — stacks de desenvolvimento (observability, banco, etc.).
- `scripts/` — helpers para build/push/scan.
- `docs/` — melhores práticas, matrizes de compatibilidade.

## Rotinas Essenciais
- Executar scans de vulnerabilidades (Trivy, Grype) e registrar resultados.
- Utilizar tags semânticas (`avana/<service>:<version>`).
- Integrar builds com `devops/pipelines` e monitorar via `devops/monitoring`.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
