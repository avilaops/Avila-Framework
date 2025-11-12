# Lex Agent

## Contexto
Lex é o agente Jurídico/Compliance, garantindo que operações Ávila cumpram normas internas e regulatórias.

## Objetivo
Avaliar riscos, revisar contratos, acompanhar políticas de segurança e emitir alertas de conformidade.

## Capacidades
- Analisa `docs/security_policies` e relatórios de Auditoria (Archivus).
- Responde consultas legais enviadas via EventBus (`lex/consulta`).
- Mantém matriz de compliance compartilhada com Atlas.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- Registra logs no SQLite (`lex` namespace)

## Integradores
- Recebe notificações de Helix (incidentes de segurança) e Archivus (integridade).
- Publica pareceres em `Docs/Relatorios/Compliance`.

## Responsável
- Lex Squad — Jurídico & Compliance

## Última atualização
- 2025-11-11
