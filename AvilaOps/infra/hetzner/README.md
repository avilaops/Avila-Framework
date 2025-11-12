# Infra Hetzner

## Contexto
Infraestrutura bare-metal e VPS Hetzner utilizada para workloads específicos (build runners, staging, jobs batch).

## Objetivo
Manter documentação de provisionamento, automação e manutenção dos recursos Hetzner.

## Estrutura Recomendada
- `terraform/` — IaC para criação de servidores, redes e volumes.
- `ansible/` — playbooks de configuração inicial.
- `monitoring/` — scripts de telemetria customizada.
- `docs/` — inventário de hosts, custos e políticas de acesso.

## Rotinas Essenciais
- Garantir compliance com `docs/security_policies` (hardening, backups).
- Sincronizar inventário com Archivus e dashboards operacionais.
- Registrar mudanças relevantes em `governance/` e `infra/kubernetes` quando aplicável.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
