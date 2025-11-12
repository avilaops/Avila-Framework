# DevOps Security

## Contexto
Programas de hardening, scanning e resposta a incidentes conduzidos pela equipe Helix em parceria com Lex (jurídico/compliance).

## Objetivo
Catalogar ferramentas, políticas e playbooks de segurança operacional aplicados aos ambientes Ávila (infra, pipelines, agentes).

## Estrutura Recomendada
- `scans/` — relatórios de SAST/DAST, scripts de varredura.
- `hardening/` — baseline para servers, containers e workstations.
- `iam/` — templates de RBAC, políticas de acesso.
- `incident-response/` — runbooks, checklists e comunicação.

## Rotinas Essenciais
- Executar varreduras mensais e arquivar resultados com Archivus.
- Revisar permissões trimestralmente com Atlas/Lex.
- Integrar alertas críticos com `devops/monitoring`.

## Responsável
- Helix Squad — Engenharia & DevOps (com suporte Lex)

## Última atualização
- 2025-11-11
