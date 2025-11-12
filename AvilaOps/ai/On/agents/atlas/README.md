# Atlas Agent

## Contexto
Agente Atlas representa a vertente Estratégia/Corporativo no ecossistema On. Atua como guardião da coerência executiva, alinhando squads aos objetivos da Ávila.

## Objetivo
Priorizar iniciativas, consolidar relatórios executivos, monitorar KPIs estratégicos e orquestrar governança entre áreas.

## Capacidades
- Analisa documentos em `governance/` e `docs/architecture` para propor diretrizes.
- Interage com Atlas Squad para aprovar mudanças críticas.
- Publica comunicados no EventBus (`atlas/alinhamento`, `atlas/alertas`).

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min (`shift_min`)
- Telemetria integrada via `AgentLogger` e `on_telemetry`

## Integradores
- Recebe alertas do Archivus (`archivus_alert`).
- Solicita ações a Helix e Lumen quando decisões exigem execução técnica/analítica.

## Responsável
- Atlas Squad — Estratégia/Corporativo

## Última atualização
- 2025-11-11
