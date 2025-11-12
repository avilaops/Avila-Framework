# AI Datasets

## Contexto
Repositório dedicado ao catálogo de datasets utilizados pelos agentes Ávila (especialmente Lumen e Atlas) para treinamento, avaliação e experimentos de IA. Os ativos seguem as políticas de compliance descritas em `governance/` e devem manter versionamento em Git quando compartilhados entre squads.

## Objetivo
Centralizar dados brutos, processados e derivados, garantindo rastreabilidade (metadados, origem, licença) e disponibilidade para pipelines de fine-tuning e RAG.

## Estrutura Recomendada
- `raw/` — dumps originais com manifesto de origem e hash de integridade.
- `processed/` — dados limpos prontos para consumo exploratório.
- `features/` — vetores, embeddings e derivados persistidos pelos agentes.
- `catalog/` — arquivos YAML/JSON descrevendo schema, licença e responsáveis.
- `docs/` — relatórios de qualidade, decisões de curadoria e auditorias.

## Rotinas Essenciais
- Registrar cada dataset em `catalog/` com hash SHA256 e data de ingestão.
- Validar compliance com políticas em `docs/security_policies/` antes de liberar uso.
- Automatizar sincronizações com pipelines definidos em `devops/pipelines/`.

## Responsável
- Lumen Squad — Dados & Analytics

## Última atualização
- 2025-11-11
