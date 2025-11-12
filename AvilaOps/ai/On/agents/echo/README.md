# Echo Agent

## Contexto
Echo é o agente de Comunicação/Branding que garante coerência da narrativa Ávila em todos os canais.

## Objetivo
Gerar comunicados, revisar materiais públicos e alinhar tom/mensagem com as diretrizes de branding.

## Capacidades
- Consome guias em `docs/styleguides` e `research/insights`.
- Suporta Atlas na divulgação de decisões estratégicas.
- Monitora menções e consolida relatórios para Pulse.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- EventBus: tópicos `echo/comunicado`, `echo/brand_alert`

## Integradores
- Trabalha com Atlas (aprovação) e Echo Squad (roteiros).
- Publica resumos em `Docs/Relatorios/Comunicados`.

## Responsável
- Echo Squad — Comunicação & Branding

## Última atualização
- 2025-11-11
