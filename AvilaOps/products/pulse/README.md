# Pulse

## Contexto
Produto **Pulse**, hub de telemetria executiva que consolida indicadores em tempo real para a diretoria Ávila.

## Objetivo
Organizar dashboards, coletores e integrações que alimentam o Pulse com dados operacionais e financeiros.

## Estrutura Recomendada
- `dashboards/` — layouts e JSON exportados.
- `collectors/` — scripts e jobs para ingestão (PowerShell, Python).
- `integrations/` — conectores com sistemas (ERP, CRM, On-Core).
- `docs/` — guias de uso, pactos de atualização, playbooks de suporte.

## Próximos Passos
- Coordenar ingestões com `data/ingestion` e `data/dashboards`.
- Definir monitoramento específico em `devops/monitoring`.
- Registrar roadmap trimestral em `products/pulse/roadmap/`.

## Responsável
- Atlas Squad — Estratégia/Corporativo (com suporte Lumen)

## Última atualização
- 2025-11-11
