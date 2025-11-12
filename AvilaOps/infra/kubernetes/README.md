# Infra Kubernetes

## Contexto
Ambiente Kubernetes (EKS, AKS, Hetzner) utilizado para hospedar serviços críticos, agentes On e pipelines.

## Objetivo
Versionar manifests, Helm charts e operadores customizados necessários para a operação.

## Estrutura Recomendada
- `clusters/` — manifests de criação/configuração de clusters.
- `workloads/` — deployments, services, ingress.
- `helm/` — charts padronizados.
- `policies/` — OPA/Gatekeeper, PodSecurity, RBAC.
- `docs/` — runbooks (rollouts, upgrades, incidentes).

## Rotinas Essenciais
- Validar manifests com `kubectl diff` e linters (kubeval, datree).
- Manter observabilidade via `devops/monitoring` e logs centralizados.
- Registrar upgrades de cluster e dependências em `governance/`.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
