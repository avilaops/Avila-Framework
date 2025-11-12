"""
Orchestrator Agent - Maestro da Análise Semântica e Roteamento Inteligente
Responsável por analisar, classificar e rotear conversas/tarefas de forma inteligente
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

# Adiciona core ao path
CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from _bootstrap import ensure_on_namespace

ensure_on_namespace()

from on.core.on_logger import AgentLogger
from on.core.on_message import Message, MessageType, MessagePriority
from on.core.on_storage import log as storage_log


class IntentType(Enum):
    """Tipos de intenção identificados"""
    QUESTION = "pergunta"
    TASK_REQUEST = "solicitacao_tarefa"
    INFORMATION = "informacao"
    ESCALATION = "escalacao"
    FEEDBACK = "feedback"
    EMERGENCY = "emergencia"
    ANALYSIS_REQUEST = "solicitacao_analise"
    DECISION_NEEDED = "decisao_necessaria"
    UNKNOWN = "desconhecido"


class UrgencyLevel(Enum):
    """Níveis de urgência"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class ContextType(Enum):
    """Tipos de contexto conversacional"""
    BUSINESS = "negocio"
    TECHNICAL = "tecnico"
    FINANCIAL = "financeiro"
    LEGAL = "juridico"
    STRATEGIC = "estrategico"
    OPERATIONAL = "operacional"
    PERSONAL = "pessoal"
    MIXED = "misto"


@dataclass
class SemanticAnalysis:
    """Resultado da análise semântica"""
    intent: IntentType
    urgency: UrgencyLevel
    context_type: ContextType
    entities: List[str]
    keywords: List[str]
    sentiment: str  # positive, negative, neutral
    confidence: float
    summary: str
    recommended_agent: Optional[str] = None
    requires_human: bool = False
    metadata: Dict[str, Any] = None

    def to_dict(self) -> Dict:
        data = asdict(self)
        data['intent'] = self.intent.value
        data['urgency'] = self.urgency.value
        data['context_type'] = self.context_type.value
        return data


class OrchestratorAgent:
    """Agente Orquestrador - Maestro da Análise Semântica"""
    
    def __init__(self, message_bus=None):
        self.name = "Orchestrator"
        self.logger = AgentLogger(self.name)
        self.bus = message_bus
        
        # Integração com sistema semântico
        self.semantic_system = None
        self._try_semantic_integration()
        
        # Configuração de agentes disponíveis
        self.agent_capabilities = {
            "atlas": ["estrategia", "corporativo", "dados", "conhecimento"],
            "helix": ["engenharia", "devops", "tecnico", "automacao"],
            "sigma": ["financeiro", "controladoria", "matematica", "analise"],
            "vox": ["comercial", "crm", "vendas", "cliente"],
            "lumen": ["pesquisa", "ia", "insights", "inovacao"],
            "forge": ["producao", "industria", "manufatura", "processos"],
            "lex": ["juridico", "compliance", "legal", "regulamentacao"],
            "echo": ["comunicacao", "branding", "marketing", "mensagem"]
        }
        
        # Palavras-chave para identificação de contexto
        self.context_keywords = {
            ContextType.BUSINESS: ["negocio", "empresa", "mercado", "cliente", "vendas", "receita"],
            ContextType.TECHNICAL: ["codigo", "sistema", "api", "bug", "deploy", "infraestrutura"],
            ContextType.FINANCIAL: ["dinheiro", "custo", "orcamento", "lucro", "investimento", "financeiro"],
            ContextType.LEGAL: ["contrato", "legal", "compliance", "regulamentacao", "lei"],
            ContextType.STRATEGIC: ["estrategia", "planejamento", "visao", "objetivos", "metas"],
            ContextType.OPERATIONAL: ["processo", "operacao", "fluxo", "procedimento", "execucao"]
        }
        
        # Palavras de urgência
        self.urgency_keywords = {
            UrgencyLevel.CRITICAL: ["urgente", "critico", "emergencia", "imediato", "agora", "parou"],
            UrgencyLevel.HIGH: ["importante", "prioritario", "rapido", "breve", "logo"],
            UrgencyLevel.MEDIUM: ["quando possivel", "conveniente", "normal"],
            UrgencyLevel.LOW: ["eventual", "futuro", "quando der", "sem pressa"]
        }
        
        if self.bus:
            self.node = self.bus.register_agent(self.name, self.handle_message)
            
        self.logger.log("Orchestrator Agent inicializado - Maestro semântico ativo")

    def configure_semantic_integration(self, semantic_system):
        """Configura integração com sistema semântico (chamado externamente)"""
        self.semantic_system = semantic_system
        self.logger.log("🧠 Integração semântica avançada configurada")

    def _try_semantic_integration(self):
        """Prepara para integração semântica (será configurada externamente)"""
        # Não inicializa sistema automático para evitar dependência circular
        # A integração será feita pelo OrchestrationSystem externamente
        self.semantic_system = None
        self.logger.log("🧠 Integração semântica preparada para configuração externa")

    def analyze_semantics_advanced(self, content: str, context: Dict = None) -> SemanticAnalysis:
        """Análise semântica usando sistema avançado se disponível"""
        
        if self.semantic_system:
            try:
                # Usa sistema semântico avançado
                response = self.semantic_system.process_request(
                    content=content,
                    sender="orchestrator",
                    priority=2,
                    context=context
                )
                
                if "error" not in response:
                    # Converte resposta para formato interno
                    sem_analysis = response["semantic_analysis"]
                    return SemanticAnalysis(
                        intent=IntentType(sem_analysis["intent"]),
                        urgency=UrgencyLevel(4 if sem_analysis["urgency"] == "high" else 3 if sem_analysis["urgency"] == "medium" else 2),
                        context_type=ContextType(sem_analysis["context_type"]),
                        entities=[], # Simplificado
                        keywords=[],
                        sentiment=response.get("sentiment", "neutral"),
                        confidence=sem_analysis["confidence"],
                        summary=sem_analysis["summary"],
                        recommended_agent=response["routing"]["selected_resource"],
                        requires_human=response["routing"]["selected_resource"] == "human_supervisor"
                    )
            except Exception as e:
                self.logger.log(f"⚠️ Erro no sistema semântico avançado: {e}")
        
        # Fallback para análise básica
        return self.analyze_semantics(content, context)

    def analyze_semantics(self, content: str, context: Dict = None) -> SemanticAnalysis:
        """Realiza análise semântica completa do conteúdo"""
        
        # 1. Detectar intenção
        intent = self._detect_intent(content)
        
        # 2. Avaliar urgência
        urgency = self._assess_urgency(content)
        
        # 3. Identificar contexto
        context_type = self._identify_context(content)
        
        # 4. Extrair entidades e keywords
        entities = self._extract_entities(content)
        keywords = self._extract_keywords(content)
        
        # 5. Análise de sentimento
        sentiment = self._analyze_sentiment(content)
        
        # 6. Calcular confiança
        confidence = self._calculate_confidence(content, intent, context_type)
        
        # 7. Gerar resumo
        summary = self._generate_summary(content, intent, context_type)
        
        # 8. Recomendar agente
        recommended_agent = self._recommend_agent(context_type, keywords, intent)
        
        # 9. Verificar se requer humano
        requires_human = self._requires_human_intervention(urgency, intent, confidence)
        
        analysis = SemanticAnalysis(
            intent=intent,
            urgency=urgency,
            context_type=context_type,
            entities=entities,
            keywords=keywords,
            sentiment=sentiment,
            confidence=confidence,
            summary=summary,
            recommended_agent=recommended_agent,
            requires_human=requires_human,
            metadata=context or {}
        )
        
        self.logger.log(f"Análise semântica concluída: {intent.value} | {urgency.value} | {context_type.value}")
        return analysis

    def route_conversation(self, content: str, sender: str, analysis: SemanticAnalysis = None) -> Dict[str, Any]:
        """Roteia conversa baseado na análise semântica"""
        
        if not analysis:
            analysis = self.analyze_semantics(content)
        
        routing_decision = {
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "analysis": analysis.to_dict(),
            "routing": {}
        }
        
        # Decisão de roteamento
        if analysis.requires_human:
            routing_decision["routing"] = {
                "target": "human_supervisor",
                "reason": "Requer intervenção humana",
                "priority": analysis.urgency.value
            }
        elif analysis.recommended_agent:
            routing_decision["routing"] = {
                "target": analysis.recommended_agent,
                "reason": f"Especialização em {analysis.context_type.value}",
                "priority": analysis.urgency.value
            }
        else:
            routing_decision["routing"] = {
                "target": "atlas",  # Default para Atlas (conhecimento geral)
                "reason": "Análise geral de conhecimento",
                "priority": analysis.urgency.value
            }
        
        # Executar roteamento
        self._execute_routing(routing_decision)
        
        return routing_decision

    def handle_message(self, message: Message):
        """Processa mensagens recebidas pelo Orchestrator"""
        
        self.logger.log(f"Recebida mensagem de {message.sender}: {message.message_type.value}")
        
        try:
            # Análise semântica da mensagem
            analysis = self.analyze_semantics(message.content, message.metadata)
            
            # Roteamento inteligente
            routing = self.route_conversation(message.content, message.sender, analysis)
            
            # Resposta ao remetente com análise
            response = self._generate_routing_response(analysis, routing)
            
            if self.bus and hasattr(self, 'node'):
                self.node.reply(message, response)
            
            # Log da decisão
            storage_log(self.name, f"Roteamento: {routing['routing']['target']} | Razão: {routing['routing']['reason']}")
            
        except Exception as e:
            self.logger.log(f"Erro no processamento: {e}")
            if self.bus and hasattr(self, 'node'):
                self.node.reply(message, "Erro interno no processamento. Escalando para supervisor.")

    def _detect_intent(self, content: str) -> IntentType:
        """Detecta a intenção do conteúdo"""
        content_lower = content.lower()
        
        # Patterns de intenção
        if any(word in content_lower for word in ["?", "como", "quando", "onde", "por que", "qual"]):
            return IntentType.QUESTION
        elif any(word in content_lower for word in ["preciso", "quero", "solicito", "tarefa", "fazer"]):
            return IntentType.TASK_REQUEST
        elif any(word in content_lower for word in ["urgente", "emergencia", "critico", "parou"]):
            return IntentType.EMERGENCY
        elif any(word in content_lower for word in ["analisar", "avaliar", "estudar", "investigar"]):
            return IntentType.ANALYSIS_REQUEST
        elif any(word in content_lower for word in ["decidir", "escolher", "aprovar", "autorizar"]):
            return IntentType.DECISION_NEEDED
        elif any(word in content_lower for word in ["feedback", "opiniao", "sugestao", "melhoria"]):
            return IntentType.FEEDBACK
        elif any(word in content_lower for word in ["escalar", "supervisor", "gerente", "ajuda"]):
            return IntentType.ESCALATION
        elif any(word in content_lower for word in ["informo", "comunico", "atualizacao", "status"]):
            return IntentType.INFORMATION
        
        return IntentType.UNKNOWN

    def _assess_urgency(self, content: str) -> UrgencyLevel:
        """Avalia o nível de urgência"""
        content_lower = content.lower()
        
        for level, keywords in self.urgency_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                return level
        
        return UrgencyLevel.MEDIUM  # Default

    def _identify_context(self, content: str) -> ContextType:
        """Identifica o tipo de contexto"""
        content_lower = content.lower()
        context_scores = {}
        
        for context_type, keywords in self.context_keywords.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                context_scores[context_type] = score
        
        if not context_scores:
            return ContextType.MIXED
        
        return max(context_scores.keys(), key=lambda x: context_scores[x])

    def _extract_entities(self, content: str) -> List[str]:
        """Extrai entidades nomeadas (simplificado)"""
        # Busca por padrões de email, números, datas, etc.
        entities = []
        
        # Emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities.extend(re.findall(email_pattern, content))
        
        # Números importantes (valores, percentuais)
        number_pattern = r'\b\d+(?:[.,]\d+)?%?\b'
        entities.extend(re.findall(number_pattern, content))
        
        return entities

    def _extract_keywords(self, content: str) -> List[str]:
        """Extrai palavras-chave importantes"""
        # Simplificado: palavras com mais de 4 caracteres, excluindo stopwords
        stopwords = {"para", "com", "por", "sobre", "como", "quando", "onde", "que", "uma", "dos", "das"}
        words = re.findall(r'\b\w{4,}\b', content.lower())
        return [word for word in set(words) if word not in stopwords][:10]

    def _analyze_sentiment(self, content: str) -> str:
        """Análise básica de sentimento"""
        positive_words = ["bom", "otimo", "excelente", "satisfeito", "obrigado", "parabens"]
        negative_words = ["ruim", "pessimo", "problema", "erro", "falha", "insatisfeito"]
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

    def _calculate_confidence(self, content: str, intent: IntentType, context_type: ContextType) -> float:
        """Calcula confiança na análise"""
        confidence = 0.5  # Base
        
        # Aumenta confiança baseado em indicadores claros
        if intent != IntentType.UNKNOWN:
            confidence += 0.2
        if context_type != ContextType.MIXED:
            confidence += 0.2
        if len(content) > 50:  # Mais contexto = mais confiança
            confidence += 0.1
        
        return min(confidence, 1.0)

    def _generate_summary(self, content: str, intent: IntentType, context_type: ContextType) -> str:
        """Gera resumo da análise"""
        return f"{intent.value.title()} sobre {context_type.value} ({len(content)} chars)"

    def _recommend_agent(self, context_type: ContextType, keywords: List[str], intent: IntentType) -> Optional[str]:
        """Recomenda agente baseado no contexto e keywords"""
        
        # Mapeamento de contexto para agente
        context_to_agent = {
            ContextType.BUSINESS: "vox",
            ContextType.TECHNICAL: "helix",
            ContextType.FINANCIAL: "sigma",
            ContextType.LEGAL: "lex",
            ContextType.STRATEGIC: "atlas",
            ContextType.OPERATIONAL: "forge"
        }
        
        # Primeiro, tenta pelo contexto
        recommended = context_to_agent.get(context_type)
        
        if not recommended:
            # Se não encontrou pelo contexto, analisa keywords
            for agent, capabilities in self.agent_capabilities.items():
                if any(keyword in keywords for keyword in capabilities):
                    recommended = agent
                    break
        
        return recommended

    def _requires_human_intervention(self, urgency: UrgencyLevel, intent: IntentType, confidence: float) -> bool:
        """Determina se requer intervenção humana"""
        
        # Cenários que sempre requerem humano
        if urgency == UrgencyLevel.CRITICAL:
            return True
        if intent == IntentType.EMERGENCY:
            return True
        if intent == IntentType.ESCALATION:
            return True
        if confidence < 0.6:  # Baixa confiança na análise
            return True
            
        return False

    def _execute_routing(self, routing_decision: Dict):
        """Executa o roteamento decidido"""
        target = routing_decision["routing"]["target"]
        
        if target == "human_supervisor":
            self.logger.log("🚨 Escalando para supervisor humano")
            # Aqui seria integrado com sistema de notificação humana
        else:
            self.logger.log(f"📤 Roteando para agente: {target}")
            # Aqui seria enviada mensagem para o agente target
            if self.bus and hasattr(self, 'node'):
                routing_msg = f"Nova tarefa roteada: {routing_decision['analysis']['summary']}"
                self.node.send(
                    recipient=target,
                    content=routing_msg,
                    message_type=MessageType.REQUEST,
                    priority=MessagePriority.NORMAL
                )

    def _generate_routing_response(self, analysis: SemanticAnalysis, routing: Dict) -> str:
        """Gera resposta sobre a decisão de roteamento"""
        target = routing["routing"]["target"]
        reason = routing["routing"]["reason"]
        
        response = f"📊 Análise concluída:\n"
        response += f"• Intenção: {analysis.intent.value}\n"
        response += f"• Contexto: {analysis.context_type.value}\n"
        response += f"• Urgência: {analysis.urgency.value}\n"
        response += f"• Confiança: {analysis.confidence:.1%}\n\n"
        response += f"🎯 Roteamento: {target}\n"
        response += f"💡 Razão: {reason}"
        
        return response


# Exemplo de uso standalone
if __name__ == "__main__":
    from on.core.on_message import MessageBus
    from pathlib import Path
    
    # Inicializa bus de mensagens
    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    bus = MessageBus(logs_dir)
    
    # Cria Orchestrator
    orchestrator = OrchestratorAgent(bus)
    
    # Testa análise semântica
    test_content = "Preciso urgentemente analisar os custos do projeto. Há um problema crítico no orçamento."
    
    analysis = orchestrator.analyze_semantics(test_content)
    print("=== ANÁLISE SEMÂNTICA ===")
    print(f"Intenção: {analysis.intent.value}")
    print(f"Urgência: {analysis.urgency.value}")
    print(f"Contexto: {analysis.context_type.value}")
    print(f"Agente recomendado: {analysis.recommended_agent}")
    print(f"Requer humano: {analysis.requires_human}")
    print(f"Confiança: {analysis.confidence:.1%}")
    
    # Testa roteamento
    routing = orchestrator.route_conversation(test_content, "user_test", analysis)
    print(f"\n=== ROTEAMENTO ===")
    print(f"Target: {routing['routing']['target']}")
    print(f"Razão: {routing['routing']['reason']}")