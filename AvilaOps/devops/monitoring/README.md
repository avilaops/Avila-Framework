# DevOps Monitoring

## Contexto
Stack de observabilidade (Prometheus, Grafana, Loki, Tempo, OpenTelemetry) mantida pela equipe Helix para suportar agentes e produtos Ávila.

## Objetivo
Versionar dashboards, exporters, alertas e documentação das rotinas de monitoramento.

## Estrutura Recomendada
- `dashboards/` — JSON/YAML dos painéis Grafana.
- `alerting/` — regras de alerta (Prometheus Alertmanager, Grafana Loki).
- `exporters/` — scripts e configs de coleta customizada.
- `docs/` — runbooks de incidentes e SLOs.

## Rotinas Essenciais
- Revisar alertas trimestralmente com Atlas (governança).
- Sincronizar configs com `ai/On/observability` para agentes.
- Registrar incidentes e postmortems em `Docs/Relatorios/Diagnosticos`.

## Responsável
- Helix Squad — Engenharia & DevOps

## Última atualização
- 2025-11-11
