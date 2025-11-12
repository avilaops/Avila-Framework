# Sigma Agent

## Contexto
Sigma é o agente Financeiro/Controladoria, focado em consolidar números, controlar orçamentos e garantir integridade financeira.

## Objetivo
Fornecer análises financeiras, projeções e relatórios de compliance contábil para diretoria.

## Capacidades
- Integra-se a `data/warehouse` e sistemas ERP externos.
- Publica indicadores em Pulse e informes em `Docs/Relatorios/Finance`.
- Suporta Lex e Atlas em avaliações regulatórias.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- Logs persistidos via `AgentLogger("Sigma")`

## Integradores
- Recebe eventos de Lumen (insights) e Forge (produção) para projeções.
- Emite alertas em `sigma/alerta_financeiro` quando desvios são detectados.

## Responsável
- Sigma Squad — Financeiro & Controladoria

## Última atualização
- 2025-11-11
