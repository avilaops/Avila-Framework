# Lumen Agent

## Contexto
Lumen é o agente de Pesquisa & IA Aplicada, responsável por gerar insights, treinar modelos e apoiar decisões baseadas em dados.

## Objetivo
Transformar dados em inteligência acionável e alimentar produtos/quadros executivos com análises.

## Capacidades
- Consome datasets (`ai/datasets`), notebooks, pipelines de `ai/fine_tuning`.
- Publica relatórios em `Docs/Relatorios/Analises` e painéis `data/dashboards`.
- Colabora com MindLayer para servir modelos.

## Configuração
- Arquivo: `config.yaml`
- Modelo: GPT-4o
- Turno padrão: 60 min
- Exporta telemetria via `on_telemetry`

## Integradores
- Recebe demandas de Atlas (estratégia) e Helix (execução técnica).
- Fornece dados para Pulse e Insight.

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
