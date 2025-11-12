"""
Sistema Semântico de Orquestração - Módulo Principal
Facilita importação dos componentes principais do sistema
"""

# Componentes principais
from .analyzer import SemanticAnalyzer, Entity, Topic, SemanticVector
from .router import SmartRouter, RoutingRequest, RoutingDecision, Resource, ResourceType, RoutingStrategy
from .conversation_manager import ConversationManager, Conversation, ConversationMessage, ConversationType, ConversationState, MessageRole
from .vector_db import VectorDatabase, VectorDocument, SearchResult, populate_with_on_project_data
from .dashboard import OrchestrationDashboard, create_dashboard_template
from .orchestration_integration import OrchestrationSystem

# Versão do módulo
__version__ = "1.0.0"

# Exports principais
__all__ = [
    # Análise Semântica
    "SemanticAnalyzer",
    "Entity", 
    "Topic", 
    "SemanticVector",
    
    # Roteamento
    "SmartRouter",
    "RoutingRequest", 
    "RoutingDecision", 
    "Resource", 
    "ResourceType", 
    "RoutingStrategy",
    
    # Gerenciamento de Conversas
    "ConversationManager",
    "Conversation", 
    "ConversationMessage", 
    "ConversationType", 
    "ConversationState", 
    "MessageRole",
    
    # Base de Dados Vetorial
    "VectorDatabase",
    "VectorDocument", 
    "SearchResult", 
    "populate_with_on_project_data",
    
    # Dashboard
    "OrchestrationDashboard",
    "create_dashboard_template",
    
    # Sistema Integrado
    "OrchestrationSystem"
]

# Funções de conveniência
def create_orchestration_system(**kwargs):
    """Cria uma instância do sistema de orquestração com configurações padrão"""
    return OrchestrationSystem(**kwargs)

def quick_semantic_analysis(text: str):
    """Análise semântica rápida de um texto"""
    analyzer = SemanticAnalyzer()
    return {
        'entities': analyzer.extract_entities(text),
        'topics': analyzer.identify_topics(text),
        'keywords': analyzer.extract_keywords(text, max_keywords=5),
        'sentiment': analyzer.analyze_sentiment(text)
    }

def quick_search(query: str, vector_db: VectorDatabase = None):
    """Busca rápida na base de conhecimento"""
    if vector_db is None:
        vector_db = VectorDatabase()
    
    results = vector_db.search(query, limit=5)
    return [
        {
            'content': result.document.content,
            'similarity': result.similarity_score,
            'category': result.document.category,
            'tags': result.document.tags
        }
        for result in results
    ]

# Configurações padrão
DEFAULT_CONFIG = {
    'semantic_analyzer': {
        'cache_enabled': True,
        'embedding_model': 'text-embedding-3-large',
        'max_keywords': 10
    },
    'router': {
        'default_strategy': 'best_match',
        'max_routing_history': 1000,
        'performance_window_hours': 24
    },
    'conversation_manager': {
        'auto_escalation': True,
        'max_conversation_time_hours': 24,
        'enable_sentiment_monitoring': True
    },
    'vector_db': {
        'cache_size': 1000,
        'min_similarity_threshold': 0.3,
        'max_search_results': 50
    },
    'dashboard': {
        'enable_realtime_updates': True,
        'metrics_update_interval_seconds': 30,
        'host': 'localhost',
        'port': 5000
    }
}