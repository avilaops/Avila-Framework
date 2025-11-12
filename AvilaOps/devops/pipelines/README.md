# DevOps Pipelines

## Contexto
Pipelines CI/CD utilizados por produtos Ávila e agentes On. Inclui GitHub Actions, Azure Pipelines, scripts PowerShell e tasks de automação.

## Objetivo
Manter catálogo versionado de fluxos de build, teste, deploy e verificação de compliance.

## Estrutura Recomendada
- `github-actions/` — workflows `.yml` reutilizáveis.
- `azure-pipelines/` — templates e variáveis.
- `tasks/` — scripts PowerShell/Bash para tarefas auxiliares.
- `docs/` — matrizes de ambientes, approvals e SLAs.

## Rotinas Essenciais
- Validar pipelines com Helix antes de produção.
- Garantir integração com Archivus para logs de deploy.
- Documentar dependências externas (Azure, AWS) em `infra/` correspondentes.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
