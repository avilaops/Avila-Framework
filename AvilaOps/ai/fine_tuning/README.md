# AI Fine-Tuning

## Contexto
Espaço reservado para experimentos de ajuste fino de modelos fundacionais utilizados pelos agentes do ecossistema Ávila. Reúne scripts, configs e relatórios de execuções conduzidas pela célula de pesquisa aplicada.

## Objetivo
Documentar pipelines de fine-tuning (datasets usados, hiperparâmetros, métricas) e manter reprodutibilidade das execuções para homologação via Helix/DevOps.

## Estrutura Recomendada
- `configs/` — YAML com hiperparâmetros e seeds.
- `scripts/` — notebooks ou jobs Python/PowerShell para disparo dos treinos.
- `checkpoints/` — artefatos resultantes (com manifesto de tamanho e hash).
- `reports/` — métricas comparativas e decisões de promoção.
- `datasets/` — links ou referências para `ai/datasets`.

## Rotinas Essenciais
- Versionar configs e resultados relevantes (git + Archivus manifesto).
- Registrar cada execução em `reports/` com data, autor e status.
- Integrar pipelines com `devops/pipelines` antes de liberar produção.

## Responsável
- Lumen Squad — Pesquisa & IA Aplicada

## Última atualização
- 2025-11-11
