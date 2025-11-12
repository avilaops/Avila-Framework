# Archivus - Agente Bibliotecário

Sistema RAG (Retrieval-Augmented Generation) para indexação e consulta semântica da documentação Ávila.

## 🎯 Propósito

Archivus é o **guardião do conhecimento** da Ávila. Ele indexa toda a documentação (produtos, governance, analytics, arquitetura) e permite consultas semânticas para os outros agentes.

## 🧠 Capacidades

- **Indexação automática:** Processa Markdown, TXT, JSON
- **Busca semântica:** Consultas em linguagem natural
- **Chunking inteligente:** Divide documentos em segmentos de 500 chars com overlap
- **Vector store persistente:** ChromaDB local
- **Embeddings:** OpenAI `text-embedding-3-large` (com fallback local `all-MiniLM-L6-v2`)
- **Context injection:** Retorna contexto formatado para prompts de agentes

## 📂 Estrutura

```
📚 Agente Bibliotecário (Archivus)/
├── archivus_agent.py            # Agente principal
├── config.yaml                  # Configuração
├── vector_store/
│   └── chromadb/                # Vector DB persistente
└── indexed_docs/                # Docs a serem indexados
    ├── products/                # on.md, geolocation.md
    ├── governance/              # Políticas, compliance
    ├── analytics/               # Taxonomias, datasources
    └── architecture/            # Filosofia Ávila
```

## 🚀 Instalação

```bash
# Instalar dependências básicas
pip install chromadb sentence-transformers

# (Opcional) habilitar embeddings OpenAI
pip install openai
export OPENAI_API_KEY="sua-chave-aqui"
```

## 💻 Uso

### Indexação

```python
from archivus_agent import ArchivusAgent

archivus = ArchivusAgent(db_path="./vector_store/chromadb")

# Indexar diretório de produtos
archivus.index_directory(
    dir_path=Path("docs/products"),
    category="products"
)

# Indexar arquivo individual
archivus.index_file(
    file_path=Path("docs/AVILA_PHILOSOPHY.md"),
    category="architecture"
)
```

### Consulta

```python
# Consulta simples
results = archivus.query(
    question="Como coletar GPS com compliance LGPD?",
    top_k=5,
    category_filter="products"  # opcional
)

for result in results:
    print(f"📄 {result['metadata']['filename']}")
    print(result['content'])
    print(f"Relevância: {result['distance']}\n")
```

### Context Injection para Agentes

```python
# Obter contexto formatado para prompt
context = archivus.get_context_for_agent(
    question="Quais KPIs rastrear para onboarding?",
    max_tokens=2000
)

# Usar em prompt do agente Lumen
prompt = f"""
{context}

Com base no contexto acima, responda:
Quais KPIs devo rastrear para o produto ON?
"""
```

## 🔄 Integração com Agentes

| Agente | Caso de Uso |
|--------|------------|
| **Lumen** | Consulta best practices de analytics/ML |
| **Vox** | Busca templates de mensagem comercial |
| **Lex** | Valida compliance contra políticas |
| **Atlas** | Revisa filosofia e alinhamento estratégico |
| **Helix** | Consulta procedimentos DevOps |

### Exemplo - Lumen usa Archivus

```python
# Lumen quer saber sobre classificação de interesse
context = archivus.get_context_for_agent(
    "Como classificar interesses a partir de UTM e tags?"
)

# Context retorna trechos de:
# - docs/analytics/interest_taxonomy.md
# - docs/products/geolocation.md
# - docs/analytics/datasources.md

# Lumen injeta context no prompt e gera resposta
```

## 📊 Estatísticas

```python
stats = archivus.stats()
# {
#   "total_documents": 127,
#   "db_path": "./vector_store/chromadb",
#   "embedding_model": "text-embedding-3-large"
# }
```

## 🔐 Privacidade

- **Dados sensíveis:** Não indexar PIIs ou secrets
- **Local-first:** ChromaDB roda localmente, não envia dados para cloud
- **Embeddings:** Preferencialmente enviados para OpenAI (`text-embedding-3-large`). Sem chave, utiliza local `sentence-transformers` (`all-MiniLM-L6-v2`).

## 🛠️ Manutenção

### Re-indexação

```python
# Apagar índice existente
archivus.collection.delete()

# Re-indexar tudo
archivus.index_directory(Path("docs/products"), "products")
archivus.index_directory(Path("docs/governance"), "governance")
```

### Backup

```bash
# Backup do vector store
tar -czf archivus_backup_$(date +%Y%m%d).tar.gz vector_store/
```

## 🤝 Responsáveis

- **Lumen Squad:** Manutenção do agente e embeddings
- **Lex Squad:** Compliance e validação de documentos
- **Atlas Squad:** Governança da base de conhecimento

## 📖 Próximas Funcionalidades

- [ ] Re-ranking com cross-encoder
- [ ] Query router (decidir qual collection consultar)
- [ ] Versionamento de documentos
- [ ] Alertas quando docs ficam desatualizados
- [ ] Integração com On.Core EventBus (`archivus/query`)

---

**Última atualização:** 2025-11-11  
**Versionamento:** v1.0  
**Status:** 🚧 Funcional, aguardando indexação completa
