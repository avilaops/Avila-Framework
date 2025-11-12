# Infra Azure

## Contexto
Repositório de ativos Azure (App Service, Functions, Cosmos DB, Storage, Monitor) utilizados por squads Ávila.

## Objetivo
Organizar IaC, scripts e guias de operação para ambientes provisionados na plataforma Microsoft.

## Estrutura Recomendada
- `iac/` — Bicep/Terraform/ARM templates.
- `scripts/` — PowerShell/CLI para automações (deploy, monitoramento).
- `configs/` — parâmetros de pipelines e environment settings.
- `docs/` — diagramas, SLOs e runbooks de suporte.

## Rotinas Essenciais
- Executar lint/validate antes de deploy (Azure CLI, Bicep).
- Monitorar com Azure Monitor integrado ao stack `devops/monitoring`.
- Garantir compliance com `docs/security_policies` (RG naming, tags).

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
