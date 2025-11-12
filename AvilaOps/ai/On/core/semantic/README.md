# Sistema de Orquestração Inteligente - On Platform

## Contexto
Módulo responsável pela camada semântica e de roteamento inteligente da plataforma On, atuando como base do agente Orchestrator.

## Objetivo
Disponibilizar componentes reutilizáveis (analisador semântico, roteador, gerenciador de conversas, base vetorial e dashboard) para automação de fluxos humanos/IA.

## Responsável
- MindLayer Squad (com apoio Atlas/Helix)

## Última atualização
- 2025-11-11

---

## 🎯 Visão Geral

O **Sistema de Orquestração Inteligente** é uma extensão avançada da plataforma On que implementa análise semântica, roteamento inteligente e gerenciamento automatizado de conversas entre humanos e agentes de IA.

### Características Principais

- 🧠 **Análise Semântica Avançada** - Compreensão profunda de contexto e intenção
- 🎯 **Roteamento Inteligente** - Direcionamento automático para o recurso mais adequado  
- 💬 **Gerenciamento de Conversas** - Coordenação de fluxos de conversa complexos
- 🔍 **Base de Conhecimento Vetorial** - Busca semântica em documentos e conhecimento
- 📊 **Dashboard de Monitoramento** - Interface visual para acompanhamento em tempo real
- 🤖 **Agente Orquestrador** - Maestro central que coordena todas as operações

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    DASHBOARD WEB (Flask)                        │
│  Interface visual para monitoramento e controle do sistema      │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│              SISTEMA DE ORQUESTRAÇÃO CENTRAL                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  OrchestrationSystem - Coordenador Principal            │   │
│  │  • Integra todos os componentes                         │   │
│  │  • Processa solicitações end-to-end                     │   │
│  │  • Gerencia estado global do sistema                    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE COMPONENTES                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│  │  Semantic   │ │ Smart       │ │ Conversation│ │ Vector      │ │
│  │  Analyzer   │ │ Router      │ │ Manager     │ │ Database    │ │
│  │             │ │             │ │             │ │             │ │
│  │ • Entidades │ │ • Estratégias│ │ • Fluxos    │ │ • Embeddings│ │
│  │ • Tópicos   │ │ • Métricas  │ │ • Estados   │ │ • Busca     │ │
│  │ • Sentimentos│ │ • Recursos │ │ • Escalação │ │ • Cache     │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↕️
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTES DA PLATAFORMA ON                     │
│  Atlas • Helix • Sigma • Vox • Lumen • Forge • Lex • Echo       │
│                + Orchestrator (Maestro)                         │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Estrutura do Projeto

```
core/semantic/
├── __init__.py                      # Módulo principal com exports
├── analyzer.py                      # Análise semântica avançada
├── router.py                        # Roteamento inteligente
├── conversation_manager.py          # Gerenciamento de conversas
├── vector_db.py                     # Base de dados vetorial
├── dashboard.py                     # Dashboard web
├── orchestration_integration.py    # Sistema integrado
├── orchestration_example.py        # Exemplos de uso
├── requirements.txt                 # Dependências
└── templates/
    └── dashboard.html              # Template do dashboard

agents/orchestrator/
├── orchestrator_agent.py          # Agente orquestrador principal
├── config.yaml                    # Configuração do agente
└── README.md                      # Documentação do agente
```

## 🚀 Instalação e Configuração

### 1. Dependências

```bash
# Navegue para o diretório do projeto
cd core/semantic

# Instale as dependências
pip install -r requirements.txt
```

### 2. Inicialização Básica

```python
from core.semantic import OrchestrationSystem

# Cria e inicia o sistema
system = OrchestrationSystem(enable_dashboard=True)

if system.start():
    print("Sistema ativo!")
    print("Dashboard: http://localhost:5000")
```

### 3. Execução do Exemplo Completo

```bash
# Executa exemplo com todas as funcionalidades
python core/semantic/orchestration_example.py
```

## 🔧 Componentes Principais

### 1. SemanticAnalyzer

Responsável pela análise semântica profunda de textos.

**Principais funcionalidades:**
- Extração de entidades (emails, telefones, CPF, CNPJ, etc.)
- Identificação de tópicos e categorização
- Análise de sentimento
- Extração de palavras-chave com relevância
- Cálculo de similaridade entre textos

```python
from core.semantic import SemanticAnalyzer

analyzer = SemanticAnalyzer()

# Análise completa
entities = analyzer.extract_entities(texto)
topics = analyzer.identify_topics(texto)
keywords = analyzer.extract_keywords(texto)
sentiment = analyzer.analyze_sentiment(texto)
```

### 2. SmartRouter

Sistema de roteamento inteligente que direciona solicitações para os recursos mais adequados.

**Estratégias disponíveis:**
- `BEST_MATCH` - Melhor correspondência semântica
- `LOAD_BALANCE` - Balanceamento de carga
- `ROUND_ROBIN` - Alternância circular
- `PRIORITY_BASED` - Baseado em prioridade da solicitação
- `EXPERTISE_LEVEL` - Nível de especialização do recurso

```python
from core.semantic import SmartRouter, RoutingRequest

router = SmartRouter()

# Cria solicitação de roteamento
request = RoutingRequest(
    content="Preciso de análise financeira urgente",
    sender="user_123",
    priority=4,
    required_capabilities=["financial", "analysis"]
)

# Executa roteamento
decision = router.route_request(request)
print(f"Roteado para: {decision.selected_resource}")
```

### 3. ConversationManager

Gerencia fluxos de conversa entre humanos e agentes IA.

**Funcionalidades:**
- Criação e gerenciamento de conversas
- Análise de fluxo conversacional
- Escalação automática baseada em condições
- Métricas de satisfação e resolução
- Roteamento dinâmico durante a conversa

```python
from core.semantic import ConversationManager, ConversationType

manager = ConversationManager()

# Inicia nova conversa
conversation = manager.start_conversation(
    initial_message="Como resolver problema X?",
    user_id="user_123",
    conversation_type=ConversationType.TROUBLESHOOTING,
    priority=3
)

# Adiciona mensagem à conversa
manager.add_message(
    conversation.id,
    "Aqui está a solução...",
    "agent_helix",
    MessageRole.AGENT
)
```

### 4. VectorDatabase

Base de conhecimento vetorial para busca semântica.

**Características:**
- Armazenamento de embeddings em SQLite
- Busca por similaridade vetorial (coseno)
- Cache inteligente para performance
- Suporte a coleções e categorização
- Indexação automática de metadados

```python
from core.semantic import VectorDatabase

vector_db = VectorDatabase()

# Adiciona documentos
doc_id = vector_db.add_document(
    content="Como resolver problemas de API...",
    category="troubleshooting",
    tags=["api", "performance"]
)

# Busca semântica
results = vector_db.search(
    query="problemas de performance",
    limit=5,
    min_similarity=0.3
)

for result in results:
    print(f"{result.similarity_score:.1%} - {result.document.content}")
```

### 5. Dashboard de Orquestração

Interface web para monitoramento e controle do sistema.

**Recursos do Dashboard:**
- Métricas em tempo real
- Visualização de conversas ativas
- Status dos recursos (agentes)
- Teste de componentes (análise semântica, roteamento, busca)
- API RESTful para integração

**Endpoints principais:**
```
GET  /                           # Interface principal
GET  /api/metrics/overview       # Métricas gerais
GET  /api/conversations/recent   # Conversas recentes
GET  /api/resources/status       # Status dos recursos
POST /api/semantic/analyze       # Análise semântica
POST /api/routing/simulate       # Simulação de roteamento
POST /api/search                 # Busca na base de conhecimento
```

## 💡 Casos de Uso

### 1. Atendimento Automatizado

```python
# Sistema analisa mensagem do cliente
response = system.process_request(
    content="Preciso cancelar minha assinatura urgentemente",
    sender="cliente_123",
    priority=3,
    context={"channel": "chat", "customer_type": "premium"}
)

# Resultado:
# - Análise: intent=task_request, urgency=high, context=commercial
# - Roteamento: vox_agent (especialista comercial)
# - Conversa: criada automaticamente com prioridade alta
```

### 2. Suporte Técnico Inteligente

```python
# Problema técnico é categorizado e roteado
response = system.process_request(
    content="API retornando erro 500 em produção",
    sender="dev_team",
    priority=4,
    context={"environment": "production", "severity": "high"}
)

# Resultado:
# - Análise: intent=emergency, urgency=critical, context=technical
# - Roteamento: helix_agent (especialista técnico)
# - Escalação: automática para supervisor se não resolvido em 30min
```

### 3. Consulta à Base de Conhecimento

```python
# Busca informações relevantes automaticamente
knowledge_results = system.search_knowledge(
    query="processo de aprovação de orçamento",
    limit=3
)

# Resultado: documentos mais relevantes sobre o processo
for result in knowledge_results:
    print(f"Relevância: {result['similarity']:.1%}")
    print(f"Conteúdo: {result['content']}")
```

## 📊 Métricas e Monitoramento

O sistema coleta métricas abrangentes para análise de performance:

### Métricas de Conversas
- Total de conversas por período
- Tempo médio de resolução
- Taxa de escalação
- Distribuição por tipo e estado
- Score de satisfação

### Métricas de Roteamento  
- Decisões de roteamento por período
- Confiança média das decisões
- Estratégias mais utilizadas
- Performance por recurso

### Métricas da Base de Conhecimento
- Total de documentos indexados
- Eficiência do cache
- Queries de busca mais frequentes
- Taxa de acerto nas buscas

## 🔒 Considerações de Segurança

### Recomendações Implementadas
- Validação de entrada em todas as APIs
- Sanitização de conteúdo antes do processamento
- Cache limitado para evitar vazamentos de memória
- Logs estruturados para auditoria

### Melhorias Sugeridas
- Autenticação e autorização nas APIs
- Criptografia de dados sensíveis
- Rate limiting para prevenir abuso
- Backup automático da base de conhecimento

## 🚧 Roadmap de Desenvolvimento

### Fase 1 ✅ (Implementada)
- [x] Análise semântica básica
- [x] Roteamento inteligente
- [x] Gerenciamento de conversas
- [x] Base de conhecimento vetorial
- [x] Dashboard de monitoramento

### Fase 2 🔄 (Em andamento)
- [ ] Integração com OpenAI para embeddings reais
- [ ] Análise de sentimento mais avançada
- [ ] Métricas de negócio personalizadas
- [ ] API de integração externa

### Fase 3 🔮 (Planejada)
- [ ] Machine Learning para otimização de roteamento
- [ ] Análise preditiva de escalações
- [ ] Integração com sistemas de ticketing
- [ ] Suporte multiidioma

## 🤝 Como Contribuir

### Estrutura para Novos Componentes

1. **Crie módulo específico** em `core/semantic/`
2. **Implemente interface padrão** com métodos `initialize()`, `process()`, `get_metrics()`
3. **Adicione testes** com exemplos de uso
4. **Documente API** seguindo padrão estabelecido
5. **Integre com sistema principal** via `OrchestrationSystem`

### Padrões de Código

- Use **type hints** em todas as funções
- Implemente **dataclasses** para estruturas de dados
- Utilize **logging estruturado** para debugging
- Siga **convenções de nomenclatura** estabelecidas

## 📚 Exemplos Avançados

Veja o arquivo `orchestration_example.py` para exemplos completos de:

- Inicialização do sistema
- Processamento de solicitações complexas
- Integração com base de conhecimento
- Monitoramento em tempo real
- Casos de uso específicos por área de negócio

## 🆘 Suporte e Troubleshooting

### Logs do Sistema

O sistema gera logs estruturados em vários níveis:

```python
# Para ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Problemas Comuns

**Erro: "Vector database não inicializada"**
- Solução: Chamar `system.initialize()` antes de usar

**Dashboard não carrega**
- Verificar se Flask está instalado: `pip install flask`
- Verificar se porta 5000 está livre

**Embeddings não funcionam**
- Para embeddings reais: configurar OpenAI API key
- Sistema funciona com embeddings simulados por padrão

### Contato

Para suporte técnico ou dúvidas sobre implementação, consulte:
- Documentação da plataforma On principal
- Logs do sistema em `logs/`
- API de status do sistema: `/api/system/health`

---

**Sistema de Orquestração Inteligente - On Platform v1.0**  
*Transformando conversas em ações inteligentes* 🎯🤖✨