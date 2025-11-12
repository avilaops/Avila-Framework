# AI Prompts

## Contexto
Repositório de prompts corporativos utilizados pelos agentes Ávila em atendimento, governança e personalização (Copilot, Archivus, Atlas, etc.). Agrupa históricos (`*.chatreplay.json`), frameworks e scripts de análise.

## Objetivo
Manter um acervo versionado de prompts, garantir rastreabilidade das iterações e servir como base para treinamento dos agentes de suporte e governança.

## Estrutura Atual
- `analisador_copilot.py` — script de análise de interações.
- `copilot_all_prompts_*.chatreplay.json` — dumps de sessões Copilot.
- `estrategia_personalizacao_avilaops.md` e `framework_analise_personalizacao.md` — guias táticos.
- `relatorio_analise_copilot.json` — métricas consolidadas.
- `output.log` — logs recentes de execuções.

## Rotinas Recomendadas
- Registrar cada sprint de revisão em novo arquivo `relatorio_*.md`.
- Rodar `analisador_copilot.py` após grandes ciclos e anexar resultados.
- Catalogar snippets no snippet manager (`avila-*`) e referenciar aqui.

## Responsável
- Atlas Squad — Estratégia/Corporativo

## Última atualização
- 2025-11-11
