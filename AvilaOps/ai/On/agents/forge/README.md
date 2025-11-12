# Forge Agent

## Contexto
Forge é o agente responsável por Produção/Indústria, garantindo excelência operacional em produtos físicos/digitais.

## Objetivo
Orquestrar rotinas de manufatura digital, acompanhar SLAs de produção e coordenar logística junto a demais agentes.

## Capacidades
- Consulta dados industriais em `data/` e integra com Pulse.
- Dispara workflows em OpsFlow para execução de tarefas.
- Gera relatórios de capacidade e consumo para Atlas.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- Telemetria: integra com `on_telemetry` e dashboards Grafana.

## Integradores
- Recebe ordens de Atlas e Sigma (planejamento/orçamento).
- Publica status em `forge/status_producao`.

## Responsável
- Forge Squad — Produção & Indústria

## Última atualização
- 2025-11-11
