"""
Orchestration System Integration - Sistema Completo de Orquestração
Integra todos os componentes do sistema de orquestração inteligente
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import threading
import time
import signal

# Adiciona core ao path
CORE_DIR = Path(__file__).resolve().parents[1]
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

# Importa componentes do sistema
from on.core.on_logger import AgentLogger
from on.core.on_message import Message, MessageType, MessagePriority
from on.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
    IntentType,
    UrgencyLevel,
    ContextType,
    SemanticAnalysis as OrchestratorSemanticAnalysis,
)
from analyzer import SemanticAnalyzer, SemanticAnalysis as CoreSemanticAnalysis
from router import SmartRouter, RoutingRequest, ResourceType
from conversation_manager import ConversationManager, ConversationType, MessageRole
from vector_db import VectorDatabase, populate_with_on_project_data
from dashboard import OrchestrationDashboard, create_dashboard_template

class OrchestrationSystem:
    """Sistema Completo de Orquestração Inteligente"""
    
    def __init__(self, project_root: Optional[Path] = None, enable_dashboard: bool = True):
        self.project_root = project_root or Path(__file__).resolve().parents[2]
        self.enable_dashboard = enable_dashboard
        self.logger = AgentLogger("OrchestrationSystem")
        
        # Estado do sistema
        self.running = False
        self.components_initialized = False
        
        # Componentes principais
        self.semantic_analyzer: Optional[SemanticAnalyzer] = None
        self.router: Optional[SmartRouter] = None
        self.conversation_manager: Optional[ConversationManager] = None
        self.vector_db: Optional[VectorDatabase] = None
        self.orchestrator_agent: Optional[OrchestratorAgent] = None
        self.dashboard: Optional[OrchestrationDashboard] = None
        
        # Threads de background
        self.dashboard_thread: Optional[threading.Thread] = None
        
        self.logger.log("Sistema de Orquestração inicializado")
    
    def initialize(self, populate_knowledge: bool = True) -> bool:
        """Inicializa todos os componentes do sistema"""
        
        try:
            self.logger.log("🚀 Inicializando componentes do sistema...")
            
            # 1. Analisador Semântico
            self.logger.log("📊 Inicializando Semantic Analyzer...")
            self.semantic_analyzer = SemanticAnalyzer()
            
            # 2. Sistema de Roteamento
            self.logger.log("🎯 Inicializando Smart Router...")
            self.router = SmartRouter()
            
            # 3. Gerenciador de Conversas
            self.logger.log("💬 Inicializando Conversation Manager...")
            self.conversation_manager = ConversationManager()
            
            # 4. Base de Dados Vetorial
            self.logger.log("🔍 Inicializando Vector Database...")
            self.vector_db = VectorDatabase()
            
            # 5. Popula base de conhecimento se solicitado
            if populate_knowledge:
                self.logger.log("📚 Populando base de conhecimento...")
                self._populate_knowledge_base()
            
            # 6. Agente Orquestrador
            self.logger.log("🎭 Inicializando Orchestrator Agent...")
            self.orchestrator_agent = OrchestratorAgent()
            
            # Configura integração bidirecional com agente orquestrador
            if hasattr(self.orchestrator_agent, 'configure_semantic_integration'):
                self.orchestrator_agent.configure_semantic_integration(self)
            
            # 7. Dashboard (se habilitado)
            if self.enable_dashboard:
                self.logger.log("🖥️ Inicializando Dashboard...")
                create_dashboard_template()
                self.dashboard = OrchestrationDashboard()
            
            self.components_initialized = True
            self.logger.log("✅ Todos os componentes inicializados com sucesso!")
            
            return True
            
        except Exception as e:
            self.logger.log(f"❌ Erro na inicialização: {e}")
            return False
    
    def start(self) -> bool:
        """Inicia o sistema de orquestração"""
        
        if not self.components_initialized:
            if not self.initialize():
                return False
        
        try:
            self.running = True
            self.logger.log("🎯 Sistema de Orquestração ATIVO")
            
            # Inicia dashboard em thread separada se habilitado
            if self.enable_dashboard and self.dashboard:
                self.dashboard_thread = threading.Thread(
                    target=self._run_dashboard,
                    daemon=True
                )
                self.dashboard_thread.start()
                self.logger.log("🖥️ Dashboard iniciado em http://localhost:5000")
            
            # Exibe estatísticas iniciais
            self._show_system_statistics()
            
            return True
            
        except Exception as e:
            self.logger.log(f"❌ Erro ao iniciar sistema: {e}")
            return False
    
    def stop(self):
        """Para o sistema de orquestração"""
        self.running = False
        
        if self.dashboard:
            self.dashboard.stop()
        
        self.logger.log("🛑 Sistema de Orquestração PARADO")
    
    def process_request(self, content: str, sender: str = "user", 
                       priority: int = 2, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa uma solicitação completa através do sistema"""
        
        if not self.running:
            return {"error": "Sistema não está ativo"}
        
        try:
            request_id = f"req_{int(datetime.now().timestamp())}"
            self.logger.log(f"📥 Processando solicitação {request_id}: {content[:50]}...")
            
            # 1. Análise semântica
            semantic_analysis = self.semantic_analyzer.analyze_semantics(content, context)
            
            # 2. Busca na base de conhecimento para contexto adicional
            search_results = self.vector_db.search(content, limit=3, min_similarity=0.4)
            knowledge_context = [
                {"content": result.document.content, "similarity": result.similarity_score}
                for result in search_results
            ]
            
            # 3. Roteamento inteligente
            routing_request = RoutingRequest(
                id=request_id,
                content=content,
                sender=sender,
                priority=priority,
                required_capabilities=self._extract_capabilities(semantic_analysis),
                preferred_type=ResourceType.AGENT,
                max_wait_time=30.0,
                context=context or {},
                timestamp=datetime.now()
            )
            
            routing_decision = self.router.route_request(routing_request)
            
            # 4. Inicia conversa
            conversation = self.conversation_manager.start_conversation(
                initial_message=content,
                user_id=sender,
                conversation_type=self._determine_conversation_type(semantic_analysis),
                priority=priority,
                context={
                    **(context or {}),
                    "semantic_analysis": semantic_analysis.__dict__ if hasattr(semantic_analysis, '__dict__') else semantic_analysis,
                    "routing_decision": routing_decision.__dict__ if hasattr(routing_decision, '__dict__') else routing_decision,
                    "knowledge_context": knowledge_context
                }
            )
            
            # 5. Resposta estruturada
            response = {
                "request_id": request_id,
                "conversation_id": conversation.id,
                "semantic_analysis": {
                    "intent": semantic_analysis.intent.value,
                    "urgency": semantic_analysis.urgency.value,
                    "context_type": semantic_analysis.context_type.value,
                    "confidence": semantic_analysis.confidence,
                    "summary": semantic_analysis.summary
                },
                "routing": {
                    "selected_resource": routing_decision.selected_resource,
                    "strategy": routing_decision.strategy_used.value,
                    "confidence": routing_decision.confidence,
                    "reasoning": routing_decision.reasoning,
                    "estimated_response_time": routing_decision.estimated_response_time
                },
                "conversation": {
                    "id": conversation.id,
                    "title": conversation.title,
                    "type": conversation.type.value,
                    "assigned_to": conversation.assigned_to,
                    "state": conversation.state.value
                },
                "knowledge_context": knowledge_context,
                "timestamp": datetime.now().isoformat(),
                "status": "processed"
            }
            
            self.logger.log(f"✅ Solicitação {request_id} processada com sucesso")
            return response
            
        except Exception as e:
            self.logger.log(f"❌ Erro ao processar solicitação: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "status": "failed"
            }
    
    def add_knowledge(self, content: str, category: str = "general", 
                     tags: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        """Adiciona conhecimento à base vetorial"""
        
        if not self.vector_db:
            raise RuntimeError("Vector database não inicializada")
        
        doc_id = self.vector_db.add_document(
            content=content,
            category=category,
            tags=tags or [],
            metadata=metadata or {},
            source="manual_input"
        )
        
        self.logger.log(f"📚 Conhecimento adicionado: {doc_id}")
        return doc_id
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Busca na base de conhecimento"""
        
        if not self.vector_db:
            raise RuntimeError("Vector database não inicializada")
        
        results = self.vector_db.search(query, limit=limit)
        
        return [
            {
                "document_id": result.document.id,
                "content": result.document.content,
                "similarity": result.similarity_score,
                "category": result.document.category,
                "tags": result.document.tags,
                "matched_terms": result.matched_terms
            }
            for result in results
        ]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtém status completo do sistema"""
        
        if not self.components_initialized:
            return {"status": "not_initialized"}
        
        # Status dos componentes
        components_status = {
            "semantic_analyzer": "active" if self.semantic_analyzer else "inactive",
            "router": "active" if self.router else "inactive",
            "conversation_manager": "active" if self.conversation_manager else "inactive",
            "vector_db": "active" if self.vector_db else "inactive",
            "orchestrator_agent": "active" if self.orchestrator_agent else "inactive",
            "dashboard": "active" if self.dashboard and self.enable_dashboard else "inactive"
        }
        
        # Estatísticas dos componentes
        statistics = {}
        
        if self.conversation_manager:
            conv_analytics = self.conversation_manager.get_conversation_analytics()
            statistics["conversations"] = conv_analytics
        
        if self.router:
            routing_analytics = self.router.analyze_routing_patterns()
            statistics["routing"] = routing_analytics
        
        if self.vector_db:
            vector_stats = self.vector_db.get_statistics()
            statistics["knowledge_base"] = vector_stats
        
        return {
            "status": "active" if self.running else "stopped",
            "components": components_status,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        }
    
    def _populate_knowledge_base(self):
        """Popula base de conhecimento com dados do projeto"""
        try:
            doc_ids = populate_with_on_project_data(self.vector_db, self.project_root)
            self.logger.log(f"📚 Base de conhecimento populada com {len(doc_ids)} documentos")
        except Exception as e:
            self.logger.log(f"⚠️ Aviso: Não foi possível popular base de conhecimento: {e}")
    
    def _extract_capabilities(self, semantic_analysis) -> List[str]:
        """Extrai capacidades requeridas da análise semântica"""
        capabilities = []
        
        # Mapeia contexto para capacidades
        context_type = semantic_analysis.context_type.value
        if context_type == "tecnologia":
            capabilities.extend(["technical", "analysis"])
        elif context_type == "financeiro":
            capabilities.extend(["financial", "analysis"])
        elif context_type == "vendas":
            capabilities.extend(["sales", "communication"])
        elif context_type == "juridico":
            capabilities.extend(["legal", "analysis"])
        else:
            capabilities.append("general")
        
        # Adiciona capacidades baseadas na urgência
        if semantic_analysis.urgency.value >= 3:
            capabilities.append("escalation")
        
        return capabilities
    
    def _determine_conversation_type(self, semantic_analysis) -> ConversationType:
        """Determina tipo de conversa baseado na análise semântica"""
        intent = semantic_analysis.intent.value
        
        mapping = {
            "pergunta": ConversationType.QUESTION_ANSWER,
            "solicitacao_tarefa": ConversationType.TASK_REQUEST,
            "emergencia": ConversationType.ESCALATION,
            "solicitacao_analise": ConversationType.CONSULTATION,
            "escalacao": ConversationType.ESCALATION
        }
        
        return mapping.get(intent, ConversationType.QUESTION_ANSWER)
    
    def _run_dashboard(self):
        """Executa dashboard em thread separada"""
        if self.dashboard:
            self.dashboard.run(debug=False)
    
    def _show_system_statistics(self):
        """Exibe estatísticas iniciais do sistema"""
        status = self.get_system_status()
        
        self.logger.log("📈 ESTATÍSTICAS DO SISTEMA:")
        self.logger.log(f"   • Status: {status['status']}")
        
        components = status['components']
        active_components = sum(1 for comp_status in components.values() if comp_status == "active")
        self.logger.log(f"   • Componentes ativos: {active_components}/{len(components)}")
        
        if "knowledge_base" in status['statistics']:
            kb_stats = status['statistics']['knowledge_base']
            self.logger.log(f"   • Documentos na base: {kb_stats['total_documents']}")
        
        self.logger.log("✨ Sistema pronto para receber solicitações!")

    def _convert_semantic_analysis(
        self,
        analysis: CoreSemanticAnalysis,
        original_content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> OrchestratorSemanticAnalysis:
        """Converte análise do motor semântico para formato do Orchestrator"""

        intent_map = {
            "question": IntentType.QUESTION,
            "request": IntentType.TASK_REQUEST,
            "task_request": IntentType.TASK_REQUEST,
            "information": IntentType.INFORMATION,
            "complaint": IntentType.FEEDBACK,
            "emergency": IntentType.EMERGENCY,
            "analysis": IntentType.ANALYSIS_REQUEST,
            "general": IntentType.ANALYSIS_REQUEST,
        }

        urgency_map = {
            "critical": UrgencyLevel.CRITICAL,
            "high": UrgencyLevel.HIGH,
            "medium": UrgencyLevel.MEDIUM,
            "low": UrgencyLevel.LOW,
        }

        context_map = {
            "business": ContextType.BUSINESS,
            "technical": ContextType.TECHNICAL,
            "support": ContextType.OPERATIONAL,
            "personal": ContextType.PERSONAL,
            "education": ContextType.STRATEGIC,
            "health": ContextType.PERSONAL,
            "financial": ContextType.FINANCIAL,
            "legal": ContextType.LEGAL,
            "general": ContextType.MIXED,
        }

        intent = intent_map.get(analysis.intent, IntentType.UNKNOWN)
        urgency = urgency_map.get(analysis.urgency, UrgencyLevel.LOW)
        context_type = context_map.get(analysis.context, ContextType.MIXED)

        keywords = [kw["word"] for kw in analysis.keywords if isinstance(kw, dict) and kw.get("word")]
        entities = []
        for entity_list in analysis.entities.values():
            for entity in entity_list:
                text = entity.get("text") if isinstance(entity, dict) else None
                if text:
                    entities.append(text)

        sentiment_label = analysis.sentiment.overall if analysis.sentiment else "neutral"
        summary = self._generate_summary_from_content(original_content, intent, context_type)
        recommended_agent = self._suggest_agent_for_context(context_type)
        requires_human = self._should_require_human(urgency, sentiment_label)

        metadata = {
            "raw_entities": analysis.entities,
            "topics": [topic.name for topic in analysis.topics],
            "language": analysis.language,
            "detected_context": analysis.context,
            "provided_context": context or {},
            "sentiment_scores": getattr(analysis.sentiment, "scores", {}),
        }

        return OrchestratorSemanticAnalysis(
            intent=intent,
            urgency=urgency,
            context_type=context_type,
            entities=entities,
            keywords=keywords,
            sentiment=sentiment_label,
            confidence=analysis.confidence,
            summary=summary,
            recommended_agent=recommended_agent,
            requires_human=requires_human,
            metadata=metadata,
        )

    def _suggest_agent_for_context(self, context_type: ContextType) -> Optional[str]:
        """Sugere agente baseado no contexto identificado"""
        mapping = {
            ContextType.BUSINESS: "atlas",
            ContextType.STRATEGIC: "atlas",
            ContextType.TECHNICAL: "helix",
            ContextType.FINANCIAL: "sigma",
            ContextType.LEGAL: "lex",
            ContextType.OPERATIONAL: "forge",
            ContextType.PERSONAL: "vox",
            ContextType.MIXED: "atlas",
        }
        return mapping.get(context_type, "atlas")

    def _generate_summary_from_content(
        self,
        content: str,
        intent: IntentType,
        context_type: ContextType,
        max_length: int = 180
    ) -> str:
        """Gera resumo compacto do conteúdo"""
        sanitized = " ".join(content.strip().split())
        if len(sanitized) > max_length:
            sanitized = sanitized[: max_length - 3] + "..."
        return f"{intent.value} | {context_type.value} | {sanitized}"

    def _should_require_human(self, urgency: UrgencyLevel, sentiment: str) -> bool:
        """Decide se a solicitação deve ser escalada para humano"""
        if urgency == UrgencyLevel.CRITICAL:
            return True
        if urgency == UrgencyLevel.HIGH and sentiment == "negative":
            return True
        return False


def create_integration_example():
    """Cria arquivo de exemplo de uso do sistema"""
    
    example_code = '''#!/usr/bin/env python3
"""
Exemplo de Uso - Sistema de Orquestração Inteligente
Demonstra como utilizar o sistema completo de orquestração
"""

from pathlib import Path
import time
import signal
import sys

# Importa o sistema de orquestração
from orchestration_integration import OrchestrationSystem

def main():
    """Exemplo principal de uso"""
    
    # Inicializa sistema
    print("🚀 Inicializando Sistema de Orquestração...")
    system = OrchestrationSystem(enable_dashboard=True)
    
    # Configura handler para interrupção
    def signal_handler(sig, frame):
        print("\\n🛑 Parando sistema...")
        system.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Inicia sistema
    if not system.start():
        print("❌ Falha ao iniciar sistema")
        return
    
    print("\\n✅ Sistema ativo! Exemplos de uso:")
    print("   • Dashboard: http://localhost:5000")
    
    # Exemplos de solicitações
    test_requests = [
        {
            "content": "Preciso de uma análise financeira urgente do projeto X. O orçamento está estourando.",
            "sender": "gerente_projeto",
            "priority": 4,
            "context": {"department": "finance", "project": "X"}
        },
        {
            "content": "Como resolver problemas de performance na API? O sistema está lento.",
            "sender": "dev_team",
            "priority": 3,
            "context": {"department": "engineering", "issue_type": "performance"}
        },
        {
            "content": "Quais são os agentes disponíveis no sistema On?",
            "sender": "usuario_teste",
            "priority": 1,
            "context": {"type": "information_request"}
        }
    ]
    
    print("\\n🧪 Processando solicitações de exemplo...")
    
    for i, request in enumerate(test_requests, 1):
        print(f"\\n--- Solicitação {i} ---")
        print(f"📝 Conteúdo: {request['content']}")
        
        # Processa solicitação
        response = system.process_request(**request)
        
        if "error" in response:
            print(f"❌ Erro: {response['error']}")
        else:
            print(f"✅ Processada com sucesso!")
            print(f"   • ID Conversa: {response['conversation_id']}")
            print(f"   • Intenção detectada: {response['semantic_analysis']['intent']}")
            print(f"   • Roteado para: {response['routing']['selected_resource']}")
            print(f"   • Confiança: {response['routing']['confidence']:.1%}")
            print(f"   • Tempo estimado: {response['routing']['estimated_response_time']:.1f}min")
        
        time.sleep(1)  # Pausa entre requests
    
    # Adiciona conhecimento personalizado
    print("\\n📚 Adicionando conhecimento personalizado...")
    
    custom_knowledge = [
        {
            "content": "Para resolver problemas de latência na API, primeiro verificar cache Redis, depois analisar queries do banco de dados e por último revisar configurações de load balancer.",
            "category": "troubleshooting",
            "tags": ["api", "performance", "troubleshooting"],
            "metadata": {"priority": "high", "department": "engineering"}
        },
        {
            "content": "O processo de aprovação de orçamento requer: 1) Análise preliminar do Sigma, 2) Revisão estratégica do Atlas, 3) Aprovação final do supervisor humano.",
            "category": "procedures",
            "tags": ["orcamento", "aprovacao", "processo"],
            "metadata": {"department": "finance"}
        }
    ]
    
    for knowledge in custom_knowledge:
        doc_id = system.add_knowledge(**knowledge)
        print(f"   • Adicionado: {doc_id}")
    
    # Demonstra busca na base de conhecimento
    print("\\n🔍 Testando busca na base de conhecimento...")
    
    search_queries = [
        "Como resolver problemas de performance?",
        "Processo de aprovação de orçamento",
        "Atlas agent funcionalidades"
    ]
    
    for query in search_queries:
        print(f"\\n🔎 Busca: {query}")
        results = system.search_knowledge(query, limit=2)
        
        for result in results:
            print(f"   • {result['similarity']:.1%} - {result['content'][:80]}...")
    
    # Status do sistema
    print("\\n📊 Status do Sistema:")
    status = system.get_system_status()
    print(f"   • Status: {status['status']}")
    
    components = status['components']
    for comp_name, comp_status in components.items():
        icon = "✅" if comp_status == "active" else "❌"
        print(f"   • {comp_name}: {icon} {comp_status}")
    
    print("\\n🎯 Sistema em execução...")
    print("   • Pressione Ctrl+C para parar")
    print("   • Acesse http://localhost:5000 para o dashboard")
    
    # Mantém sistema rodando
    try:
        while True:
            time.sleep(30)
            print(f"⏰ Sistema ativo - {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
'''
    
    example_file = Path(__file__).parent / "orchestration_example.py"
    example_file.write_text(example_code, encoding='utf-8')
    
    return example_file


# Função principal para facilitar uso
def main():
    """Função principal para executar sistema"""
    system = OrchestrationSystem()
    
    try:
        if system.start():
            print("\\n🎯 Sistema de Orquestração ativo!")
            print("   • Dashboard: http://localhost:5000")
            print("   • Pressione Ctrl+C para parar")
            
            # Mantém sistema rodando
            while True:
                time.sleep(60)
        else:
            print("❌ Falha ao iniciar sistema")
            
    except KeyboardInterrupt:
        print("\\n🛑 Parando sistema...")
        system.stop()


if __name__ == "__main__":
    # Cria arquivo de exemplo
    create_integration_example()
    
    # Executa sistema
    main()