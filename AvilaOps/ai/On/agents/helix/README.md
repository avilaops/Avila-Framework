# Helix Agent

## Contexto
Helix é o agente de Engenharia/DevOps ("DNA técnico e automação") responsável por manter operações confiáveis para todo o ecossistema Ávila.

## Objetivo
Automatizar pipelines, monitoramento, segurança operacional e provisionamento de infraestrutura.

## Capacidades
- Executa scripts em `devops/` e `infra/` conforme solicitações do EventBus.
- Publica métricas em `ai/On/observability` (traces/metrics/logs).
- Interage com Archivus para validar backups e integridade.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- Logs: `AgentLogger("Helix")`
- Heartbeat emitido a cada ciclo para `on_scheduler`

## Integradores
- Recebe pedidos de Atlas (`atlas/execucao`), Lumen (`lumen/deploy`) e Archivus.
- Publica estado de pipelines em `helix/pipeline_status`.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
