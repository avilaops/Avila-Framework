# Infra AWS

## Contexto
Centro de artefatos relacionados à infraestrutura AWS utilizada pelos produtos Ávila (segreta, opsflow, etc.).

## Objetivo
Documentar arquiteturas, IaC, runbooks e playbooks de operação na nuvem AWS.

## Estrutura Recomendada
- `iac/` — Terraform/CloudFormation.
- `runbooks/` — respostas a incidentes e rotinas.
- `configs/` — parâmetros (SSM, Secrets Manager) sem segredos.
- `diagrams/` — topologias e fluxos de rede.

## Rotinas Essenciais
- Validar IaC via pipelines (`devops/pipelines`) antes de aplicar.
- Registrar incidentes e postmortems em `Docs/Relatorios/Diagnosticos`.
- Manter inventário de contas, roles e políticas atualizado.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
