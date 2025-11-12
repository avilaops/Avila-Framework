# AI Notebooks

## Contexto
Repositório de notebooks exploratórios, protótipos rápidos e estudos conduzidos pelos agentes técnicos (Lumen, Helix e Atlas). Os arquivos funcionam como laboratório antes de se tornarem pipelines oficiais.

## Objetivo
Garantir que experimentos tenham rastreabilidade (dataset, propósito, conclusão) e possam ser promovidos para `ai/fine_tuning` ou `data/processing` quando consolidados.

## Diretrizes
- Cada notebook deve iniciar com bloco de metadados (objetivo, autor, dataset).
- Utilizar kernels registrados em `.vscode/` e manter dependências listadas em `requirements.txt` local.
- Salvar saídas relevantes em `reports/` ou anexar no repositório somente quando necessário.

## Estrutura Recomendada
- `exploration/` — análises ad-hoc.
- `experiments/` — POCs estruturadas com versão.
- `templates/` — modelos padronizados (snippets `avila-notebook`).

## Responsável
- Lumen Squad — Pesquisa & IA Aplicada

## Última atualização
- 2025-11-11
