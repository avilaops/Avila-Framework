# Modulo 2 - Tratamento e classificacao

## Visao geral
- Objetivo: transformar os insumos brutos do Modulo 1 em dados confiaveis e classificados, prontos para ativacao por agentes humanos e IA.
- Escopo: limpeza, normalizacao, rotulacao semantica, enriquecimento contextual e preparacao dos datasets e prompt packs.
- Responsaveis principais: Squad de Dados (orquestra tratativa), Squad de Dominio (valida semantica e regras), Squad de IA (prepara modelos e agentes).

## Arquitetura operacional
- **Camada de staging**: repositorio `OneDrive/Avila/datalake/raw` recebe dumps de ActivityWatch, transcricoes, logs de terminal e CLI.
- **Camada de tratamento**: workflows versionados (`scripts/etl/modulo2`) executam as rotinas de limpeza e transformacao em Python (Pandas, PySpark opcional) ou Azure Data Factory.
- **Camada de classificacao**: taxonomias em `knowledge-schema.md` alimentam pipelines de rotulacao (spaCy, Azure AI Services, OpenAI function calling, ReBAC rules).
- **Camada de armazenamento curado**: datasets validados pousam em `OneDrive/Avila/datalake/curated` + repositorio Obsidian (`.obsidian/datasets`) para consulta rapida.
- **Camada de servico**: APIs internas, notebooks, copilots especializados e dashboards consomem os dados curados.

## Cookbook de tratamento e classificacao

### 0. Preparacao
- Atualizar taxonomias e dicionarios de termos (`knowledge-schema.md`, `glossario.csv`).
- Garantir que o backlog de coleta foi realizado e versionado (`git status` limpo no repositorio de notas sensiveis).
- Definir janela de processamento (ex.: semana corrente).

### 1. Ingestao e staging
- Pegar os dumps brutos do Modulo 1 e mover para `datalake/raw/AAAA-MM-DD`.
- Padronizar nomes de arquivo: `origem_cliente_contexto_timestamp.ext`.
- Registrar metadados em `catalogo_raw.csv` (origem, responsavel, nivel de confidencialidade, checksum).

### 2. Higienizacao
- Aplicar scripts de limpeza (normalizacao de encoding, remocao de PII, filtros de ruido).
- Ferramentas: Python (Pandas), Regex, Presidio (mascaramento), Azure Purview (catalogo de PII).
- Gerar relatorio `logs/limpeza/report.md` com estatisticas: linhas removidas, campos mascarados, erros.

### 3. Normalizacao e enriquecimento
- Converter formatos (ex.: JSON -> Parquet, Markdown -> CSV estruturado via frontmatter).
- Harmonizar unidades, zonas de tempo, IDs de cliente.
- Enriquecer com dados auxiliares (CRM, ERP, SLA). Utilizar merges controlados com chaves unicas.
- Producao de dicionario de dados incremental (`docs/dicionario_mod2.md`).

### 4. Classificacao automatizada
- Rodar pipelines de NER, classificacao de texto e clustering.
- Modelos sugeridos: spaCy pipelines customizadas, Azure Language Studio, OpenAI GPT-4o mini com prompts guiados.
- Estruturar rotulos em taxonomia de 3 niveis (Dominio > Categoria > Etiqueta).
- Registrar confianca do modelo por item.

### 5. Revisao humana e QA
- Usar Obsidian e ferramentas de anotacao (Label Studio) para revisao assistida.
- Realizar amostragem estratificada (pelo menos 10% dos itens ou min 50 instancias por categoria).
- Validar: consistencia dos rotulos, aderencia a definicoes, ausencia de vies.
- Documentar decisoes em `qa/modulo2/YYY-MM-DD.md`.

### 6. Consolidacao e versao curada
- Aprovar conjuntos prontos e mover para `datalake/curated/` com versionamento semantico (`vA.B`).
- Atualizar catalogo mestre `catalogo_curated.csv` com campos: data versao, steward, cobertura, confianca media.
- Publicar visualizacoes (PowerBI, Grafana) e notebooks prontos (`notebooks/mod2/*.ipynb`).

### 7. Preparacao para consumo
- Gerar pacotes de prompts e exemplos (`prompts/mod2/classificacao/*.md`).
- Criar APIs ou endpoints MCP para disponibilizar dados.
- Atualizar checklist de ativacao para Modulo 3 (Deployment e generacao de valor).

## Modo de uso operacional

### Fluxo semanal
- Segunda: sincronizacao squads, definicao de lotes.
- Terca a quinta: execucao do cookbook (ingestao -> QA).
- Sexta: consolidacao, publicacao curada, retro sprint de dados.

### Papeis e responsabilidades
- **Steward de dados**: orquestra fluxos, garante conformidade, assina catalogos.
- **Especialista de dominio**: valida taxonomias, responde duvidas semanticas, aprova rotulos criticos.
- **Engenheiro de IA**: ajusta modelos, monitora metricas (precisao, recall, F1), cuida da reproducibilidade.

### Ferramentas chave
- Python + Pandas/PySpark; Azure Data Factory/Databricks; Label Studio; Obsidian com plugins Dataview e Excalidraw; Git + DVC (para grandes arquivos); Azure Key Vault para segredos.

### KPIs e metricas de controle
- `Precisao_media_classificacao >= 0.92`.
- `Tempo_ciclo_modulo2 <= 5 dias uteis`.
- `Cobertura_taxonomia >= 98%` dos itens sem rotulo pendente.
- `Tickets_reabertos <= 2%`.

### Checklist de liberacao
- Catalogo atualizado e assinado.
- Relatorios de QA arquivados.
- Scripts versionados e testados em ambiente de staging.
- Dados sensiveis mascarados e auditavel via logs.
- Documentacao e prompts publicados no `.obsidian`.

## Playbook de automacao
- CI em GitHub Actions/Azure DevOps executa testes unitarios dos pipelines (pytest, great_expectations).
- Gatilho manual `workflow_dispatch` para processar lotes extras.
- Alertas via Teams/Slack quando metricas caem abaixo de thresholds.
- Uso de DVC ou LakeFS para controle de versao dos datasets volumosos.

## Anexos futuros
- Model cards dos classificadores.
- Prompt library dedicada a revisao humana (macro em Obsidian + extensao VS Code).
- Templates de dashboards para diretores e clientes.
