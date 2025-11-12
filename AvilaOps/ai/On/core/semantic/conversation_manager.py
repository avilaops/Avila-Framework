"""
Conversation Manager - Gerenciador Inteligente de Conversas
Responsável por gerenciar fluxos de conversa entre humanos e IA
"""

import json
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
import uuid

from analyzer import SemanticAnalyzer
from router import SmartRouter, RoutingRequest, ResourceType

class ConversationState(Enum):
    """Estados possíveis de uma conversa"""
    ACTIVE = "active"
    WAITING = "waiting"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    ARCHIVED = "archived"
    FAILED = "failed"

class MessageRole(Enum):
    """Papéis dos participantes"""
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    SUPERVISOR = "supervisor"

class ConversationType(Enum):
    """Tipos de conversa"""
    QUESTION_ANSWER = "question_answer"
    TASK_REQUEST = "task_request"
    TROUBLESHOOTING = "troubleshooting"
    CONSULTATION = "consultation"
    ESCALATION = "escalation"
    FOLLOW_UP = "follow_up"

@dataclass
class ConversationMessage:
    """Mensagem individual em uma conversa"""
    id: str
    conversation_id: str
    sender_id: str
    sender_role: MessageRole
    content: str
    timestamp: datetime
    metadata: Dict[str, Any]
    attachments: List[str] = None
    semantic_analysis: Dict[str, Any] = None
    routing_decision: Dict[str, Any] = None

@dataclass
class Conversation:
    """Conversa completa entre participantes"""
    id: str
    title: str
    type: ConversationType
    state: ConversationState
    priority: int  # 1-5
    participants: List[str]  # IDs dos participantes
    messages: List[ConversationMessage]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    assigned_to: Optional[str]  # ID do responsável atual
    tags: List[str]
    summary: str
    context: Dict[str, Any]
    satisfaction_score: Optional[float] = None
    resolution_time: Optional[float] = None  # em minutos

@dataclass
class ConversationFlow:
    """Fluxo de conversa com regras de roteamento"""
    id: str
    name: str
    description: str
    trigger_conditions: Dict[str, Any]
    routing_rules: List[Dict[str, Any]]
    escalation_rules: Dict[str, Any]
    auto_responses: Dict[str, str]
    success_criteria: List[str]
    active: bool

class ConversationManager:
    """Gerenciador Inteligente de Conversas"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Componentes principais
        self.semantic_analyzer = SemanticAnalyzer()
        self.router = SmartRouter()
        
        # Estado interno
        self.active_conversations: Dict[str, Conversation] = {}
        self.conversation_flows: Dict[str, ConversationFlow] = {}
        self.participants: Dict[str, Dict[str, Any]] = {}
        
        # Métricas
        self.metrics = {
            'total_conversations': 0,
            'avg_resolution_time': 0.0,
            'satisfaction_avg': 0.0,
            'escalation_rate': 0.0
        }
        
        # Inicialização
        self._load_conversation_flows()
        self._load_active_conversations()
        self._register_default_participants()
    
    def start_conversation(self, initial_message: str, user_id: str, 
                          conversation_type: ConversationType = ConversationType.QUESTION_ANSWER,
                          priority: int = 2, context: Dict[str, Any] = None) -> Conversation:
        """Inicia nova conversa"""
        
        conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        
        # Análise semântica da mensagem inicial
        semantic_analysis = self._analyze_message_semantics(initial_message)
        
        # Determina título automaticamente
        title = self._generate_conversation_title(initial_message, semantic_analysis)
        
        # Roteamento inicial
        routing_request = RoutingRequest(
            id=f"route_{uuid.uuid4().hex[:8]}",
            content=initial_message,
            sender=user_id,
            priority=priority,
            required_capabilities=self._extract_required_capabilities(semantic_analysis),
            preferred_type=ResourceType.AGENT,
            max_wait_time=30.0,
            context=context or {},
            timestamp=datetime.now()
        )
        
        routing_decision = self.router.route_request(routing_request)
        
        # Cria mensagem inicial
        initial_msg = ConversationMessage(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            conversation_id=conversation_id,
            sender_id=user_id,
            sender_role=MessageRole.USER,
            content=initial_message,
            timestamp=datetime.now(),
            metadata=context or {},
            semantic_analysis=semantic_analysis,
            routing_decision=asdict(routing_decision)
        )
        
        # Cria conversa
        conversation = Conversation(
            id=conversation_id,
            title=title,
            type=conversation_type,
            state=ConversationState.ACTIVE,
            priority=priority,
            participants=[user_id, routing_decision.selected_resource],
            messages=[initial_msg],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            resolved_at=None,
            assigned_to=routing_decision.selected_resource,
            tags=self._extract_tags(semantic_analysis),
            summary="Conversa iniciada",
            context=context or {}
        )
        
        self.active_conversations[conversation_id] = conversation
        
        # Gera resposta automática se configurada
        auto_response = self._check_auto_response(conversation, initial_msg)
        if auto_response:
            self.add_message(conversation_id, auto_response, 
                           routing_decision.selected_resource, MessageRole.AGENT)
        
        self._save_conversation(conversation)
        self.metrics['total_conversations'] += 1
        
        return conversation
    
    def add_message(self, conversation_id: str, content: str, sender_id: str, 
                   sender_role: MessageRole, metadata: Dict[str, Any] = None) -> ConversationMessage:
        """Adiciona mensagem a uma conversa existente"""
        
        if conversation_id not in self.active_conversations:
            raise ValueError(f"Conversa {conversation_id} não encontrada")
        
        conversation = self.active_conversations[conversation_id]
        
        # Análise semântica da mensagem
        semantic_analysis = self._analyze_message_semantics(content)
        
        # Verifica necessidade de reroteamento
        routing_decision = None
        if sender_role == MessageRole.USER:
            routing_decision = self._check_rerouting(conversation, content, semantic_analysis)
        
        # Cria mensagem
        message = ConversationMessage(
            id=f"msg_{uuid.uuid4().hex[:8]}",
            conversation_id=conversation_id,
            sender_id=sender_id,
            sender_role=sender_role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {},
            semantic_analysis=semantic_analysis,
            routing_decision=asdict(routing_decision) if routing_decision else None
        )
        
        # Adiciona à conversa
        conversation.messages.append(message)
        conversation.updated_at = datetime.now()
        
        # Atualiza participantes se necessário
        if sender_id not in conversation.participants:
            conversation.participants.append(sender_id)
        
        # Atualiza responsável se houve reroteamento
        if routing_decision and routing_decision.selected_resource != conversation.assigned_to:
            conversation.assigned_to = routing_decision.selected_resource
            if routing_decision.selected_resource not in conversation.participants:
                conversation.participants.append(routing_decision.selected_resource)
        
        # Verifica condições de escalação
        self._check_escalation_conditions(conversation)
        
        # Atualiza resumo
        conversation.summary = self._update_conversation_summary(conversation)
        
        self._save_conversation(conversation)
        
        return message
    
    def resolve_conversation(self, conversation_id: str, resolver_id: str, 
                           resolution_note: str = "", satisfaction_score: Optional[float] = None) -> bool:
        """Resolve uma conversa"""
        
        if conversation_id not in self.active_conversations:
            return False
        
        conversation = self.active_conversations[conversation_id]
        conversation.state = ConversationState.RESOLVED
        conversation.resolved_at = datetime.now()
        conversation.satisfaction_score = satisfaction_score
        
        # Calcula tempo de resolução
        resolution_time = (conversation.resolved_at - conversation.created_at).total_seconds() / 60
        conversation.resolution_time = resolution_time
        
        # Adiciona nota de resolução
        if resolution_note:
            self.add_message(conversation_id, f"Conversa resolvida: {resolution_note}", 
                           resolver_id, MessageRole.SYSTEM)
        
        # Remove das conversas ativas
        resolved_conversation = self.active_conversations.pop(conversation_id)
        
        # Atualiza métricas
        self._update_metrics(resolved_conversation)
        
        # Arquiva
        self._archive_conversation(resolved_conversation)
        
        return True
    
    def escalate_conversation(self, conversation_id: str, escalator_id: str, 
                            reason: str, target_supervisor: Optional[str] = None) -> bool:
        """Escala conversa para supervisor"""
        
        if conversation_id not in self.active_conversations:
            return False
        
        conversation = self.active_conversations[conversation_id]
        conversation.state = ConversationState.ESCALATED
        conversation.priority = min(conversation.priority + 1, 5)  # Aumenta prioridade
        
        # Determina supervisor se não especificado
        if not target_supervisor:
            target_supervisor = "human_supervisor"
        
        conversation.assigned_to = target_supervisor
        if target_supervisor not in conversation.participants:
            conversation.participants.append(target_supervisor)
        
        # Adiciona mensagem de escalação
        escalation_msg = f"Conversa escalada por {escalator_id}. Razão: {reason}"
        self.add_message(conversation_id, escalation_msg, "system", MessageRole.SYSTEM)
        
        # Adiciona tag de escalação
        if "escalated" not in conversation.tags:
            conversation.tags.append("escalated")
        
        self._save_conversation(conversation)
        
        return True
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Obtém conversa por ID"""
        return self.active_conversations.get(conversation_id)
    
    def list_conversations(self, filters: Dict[str, Any] = None, limit: int = 50) -> List[Conversation]:
        """Lista conversas com filtros opcionais"""
        conversations = list(self.active_conversations.values())
        
        if filters:
            # Filtra por estado
            if 'state' in filters:
                conversations = [c for c in conversations if c.state == filters['state']]
            
            # Filtra por tipo
            if 'type' in filters:
                conversations = [c for c in conversations if c.type == filters['type']]
            
            # Filtra por prioridade
            if 'priority' in filters:
                conversations = [c for c in conversations if c.priority >= filters['priority']]
            
            # Filtra por participante
            if 'participant' in filters:
                conversations = [c for c in conversations if filters['participant'] in c.participants]
            
            # Filtra por tag
            if 'tag' in filters:
                conversations = [c for c in conversations if filters['tag'] in c.tags]
        
        # Ordena por última atualização (mais recentes primeiro)
        conversations.sort(key=lambda x: x.updated_at, reverse=True)
        
        return conversations[:limit]
    
    def search_conversations(self, query: str, limit: int = 20) -> List[Tuple[Conversation, float]]:
        """Busca conversas por conteúdo semântico"""
        results = []
        
        for conversation in self.active_conversations.values():
            # Constrói texto da conversa
            conversation_text = f"{conversation.title} {conversation.summary} "
            conversation_text += " ".join([msg.content for msg in conversation.messages[-5:]])  # Últimas 5 mensagens
            
            # Calcula similaridade
            similarity = self.semantic_analyzer.calculate_similarity(query, conversation_text)
            
            if similarity > 0.3:  # Threshold mínimo
                results.append((conversation, similarity))
        
        # Ordena por relevância
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:limit]
    
    def get_conversation_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Obtém analytics de conversas dos últimos dias"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filtra conversas do período
        recent_conversations = [
            c for c in self.active_conversations.values() 
            if c.created_at > cutoff_date
        ]
        
        if not recent_conversations:
            return {"message": "Nenhuma conversa no período especificado"}
        
        # Análises
        total_conversations = len(recent_conversations)
        
        # Por tipo
        type_distribution = {}
        for conv in recent_conversations:
            type_name = conv.type.value
            type_distribution[type_name] = type_distribution.get(type_name, 0) + 1
        
        # Por estado
        state_distribution = {}
        for conv in recent_conversations:
            state_name = conv.state.value
            state_distribution[state_name] = state_distribution.get(state_name, 0) + 1
        
        # Tempo médio de resolução (conversas resolvidas)
        resolved_conversations = [c for c in recent_conversations if c.resolution_time is not None]
        avg_resolution_time = (
            sum(c.resolution_time for c in resolved_conversations) / len(resolved_conversations)
            if resolved_conversations else 0
        )
        
        # Taxa de escalação
        escalated_count = len([c for c in recent_conversations if "escalated" in c.tags])
        escalation_rate = escalated_count / total_conversations if total_conversations > 0 else 0
        
        # Satisfação média
        satisfaction_scores = [c.satisfaction_score for c in recent_conversations if c.satisfaction_score is not None]
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else None
        
        return {
            'period_days': days,
            'total_conversations': total_conversations,
            'type_distribution': type_distribution,
            'state_distribution': state_distribution,
            'avg_resolution_time_minutes': avg_resolution_time,
            'escalation_rate': escalation_rate,
            'avg_satisfaction': avg_satisfaction,
            'active_conversations': len([c for c in recent_conversations if c.state == ConversationState.ACTIVE])
        }
    
    def _analyze_message_semantics(self, content: str) -> Dict[str, Any]:
        """Analisa semanticamente uma mensagem"""
        return {
            'entities': self.semantic_analyzer.extract_entities(content),
            'topics': self.semantic_analyzer.identify_topics(content),
            'keywords': self.semantic_analyzer.extract_keywords(content),
            'sentiment': self.semantic_analyzer.analyze_sentiment(content)
        }
    
    def _generate_conversation_title(self, initial_message: str, semantic_analysis: Dict) -> str:
        """Gera título para a conversa baseado na mensagem inicial"""
        keywords = semantic_analysis.get('keywords', [])
        topics = semantic_analysis.get('topics', [])
        
        if topics:
            topic = topics[0].name
            if keywords:
                main_keyword = keywords[0]['word']
                return f"{topic.title()}: {main_keyword}"
            else:
                return f"{topic.title()}"
        elif keywords:
            return f"Conversa: {keywords[0]['word']}"
        else:
            # Fallback: primeiras palavras da mensagem
            words = initial_message.split()[:4]
            return " ".join(words) + "..."
    
    def _extract_required_capabilities(self, semantic_analysis: Dict) -> List[str]:
        """Extrai capacidades requeridas baseado na análise semântica"""
        capabilities = []
        
        topics = semantic_analysis.get('topics', [])
        for topic in topics:
            if topic.name == 'tecnologia':
                capabilities.append('technical')
            elif topic.name == 'financeiro':
                capabilities.append('financial')
            elif topic.name == 'vendas':
                capabilities.append('sales')
            elif topic.name == 'juridico':
                capabilities.append('legal')
        
        keywords = semantic_analysis.get('keywords', [])
        keyword_texts = [kw['word'] for kw in keywords]
        
        if any(kw in keyword_texts for kw in ['analise', 'avaliar', 'estudar']):
            capabilities.append('analysis')
        if any(kw in keyword_texts for kw in ['urgente', 'critico', 'emergencia']):
            capabilities.append('escalation')
        
        return capabilities or ['general']
    
    def _extract_tags(self, semantic_analysis: Dict) -> List[str]:
        """Extrai tags baseado na análise semântica"""
        tags = []
        
        sentiment = semantic_analysis.get('sentiment', {})
        if sentiment.get('overall') == 'negative':
            tags.append('negative_sentiment')
        elif sentiment.get('overall') == 'positive':
            tags.append('positive_sentiment')
        
        topics = semantic_analysis.get('topics', [])
        for topic in topics:
            tags.append(topic.name)
        
        return tags
    
    def _check_auto_response(self, conversation: Conversation, message: ConversationMessage) -> Optional[str]:
        """Verifica se deve enviar resposta automática"""
        # Busca por fluxos aplicáveis
        for flow in self.conversation_flows.values():
            if not flow.active:
                continue
            
            # Verifica condições do trigger
            if self._match_trigger_conditions(conversation, message, flow.trigger_conditions):
                auto_responses = flow.auto_responses
                
                # Retorna resposta baseada no tipo de conversa
                response_key = conversation.type.value
                if response_key in auto_responses:
                    return auto_responses[response_key]
                elif 'default' in auto_responses:
                    return auto_responses['default']
        
        return None
    
    def _check_rerouting(self, conversation: Conversation, content: str, semantic_analysis: Dict) -> Optional[Any]:
        """Verifica se é necessário rerotear a conversa"""
        # Simples: reroteia se tópico mudou significativamente
        current_topics = {topic.name for topic in semantic_analysis.get('topics', [])}
        
        # Obtém tópicos das mensagens anteriores
        previous_topics = set()
        for msg in conversation.messages[-3:]:  # Últimas 3 mensagens
            if msg.semantic_analysis:
                msg_topics = msg.semantic_analysis.get('topics', [])
                previous_topics.update(topic.name if hasattr(topic, 'name') else topic.get('name', '') 
                                     for topic in msg_topics)
        
        # Se mudou significativamente, reroteia
        if current_topics and not current_topics.intersection(previous_topics):
            routing_request = RoutingRequest(
                id=f"reroute_{uuid.uuid4().hex[:8]}",
                content=content,
                sender=conversation.participants[0],  # Usuário original
                priority=conversation.priority,
                required_capabilities=self._extract_required_capabilities(semantic_analysis),
                preferred_type=ResourceType.AGENT,
                max_wait_time=15.0,
                context=conversation.context,
                timestamp=datetime.now()
            )
            
            return self.router.route_request(routing_request)
        
        return None
    
    def _check_escalation_conditions(self, conversation: Conversation):
        """Verifica condições de escalação automática"""
        # Escalação por tempo (mais de 2 horas sem resolução e prioridade alta)
        if conversation.priority >= 4:
            time_diff = (datetime.now() - conversation.created_at).total_seconds() / 3600
            if time_diff > 2:  # 2 horas
                self.escalate_conversation(conversation.id, "system", 
                                         "Escalação automática por tempo (prioridade alta)")
                return
        
        # Escalação por número de mensagens (mais de 15 mensagens sem resolução)
        if len(conversation.messages) > 15:
            self.escalate_conversation(conversation.id, "system", 
                                     "Escalação automática por número de mensagens")
            return
        
        # Escalação por sentimento negativo persistente
        recent_messages = conversation.messages[-3:]
        negative_count = 0
        for msg in recent_messages:
            if msg.sender_role == MessageRole.USER and msg.semantic_analysis:
                sentiment = msg.semantic_analysis.get('sentiment', {})
                if sentiment.get('overall') == 'negative':
                    negative_count += 1
        
        if negative_count >= 2:  # 2 das últimas 3 mensagens são negativas
            self.escalate_conversation(conversation.id, "system", 
                                     "Escalação automática por sentimento negativo persistente")
    
    def _update_conversation_summary(self, conversation: Conversation) -> str:
        """Atualiza resumo da conversa"""
        if len(conversation.messages) <= 1:
            return "Conversa iniciada"
        
        # Analisa últimas mensagens para gerar resumo
        recent_content = " ".join([msg.content for msg in conversation.messages[-3:]])
        keywords = self.semantic_analyzer.extract_keywords(recent_content, max_keywords=3)
        
        if keywords:
            key_terms = [kw['word'] for kw in keywords]
            return f"Discussão sobre: {', '.join(key_terms)}"
        else:
            return f"{len(conversation.messages)} mensagens trocadas"
    
    def _match_trigger_conditions(self, conversation: Conversation, message: ConversationMessage, 
                                 conditions: Dict[str, Any]) -> bool:
        """Verifica se as condições do trigger são atendidas"""
        # Implementação simplificada
        if 'message_contains' in conditions:
            keywords = conditions['message_contains']
            content_lower = message.content.lower()
            return any(keyword.lower() in content_lower for keyword in keywords)
        
        return False
    
    def _update_metrics(self, resolved_conversation: Conversation):
        """Atualiza métricas globais"""
        # Tempo médio de resolução
        if resolved_conversation.resolution_time:
            current_avg = self.metrics['avg_resolution_time']
            total_resolved = self.metrics.get('total_resolved', 0) + 1
            new_avg = (current_avg * (total_resolved - 1) + resolved_conversation.resolution_time) / total_resolved
            self.metrics['avg_resolution_time'] = new_avg
            self.metrics['total_resolved'] = total_resolved
        
        # Satisfação média
        if resolved_conversation.satisfaction_score:
            current_avg = self.metrics['satisfaction_avg']
            total_with_rating = self.metrics.get('total_with_rating', 0) + 1
            new_avg = (current_avg * (total_with_rating - 1) + resolved_conversation.satisfaction_score) / total_with_rating
            self.metrics['satisfaction_avg'] = new_avg
            self.metrics['total_with_rating'] = total_with_rating
        
        # Taxa de escalação
        total_conversations = self.metrics['total_conversations']
        total_escalated = self.metrics.get('total_escalated', 0)
        if "escalated" in resolved_conversation.tags:
            total_escalated += 1
            self.metrics['total_escalated'] = total_escalated
        
        if total_conversations > 0:
            self.metrics['escalation_rate'] = total_escalated / total_conversations
    
    def _load_conversation_flows(self):
        """Carrega fluxos de conversa padrão"""
        default_flows = [
            ConversationFlow(
                id="welcome_flow",
                name="Fluxo de Boas-vindas",
                description="Resposta automática inicial",
                trigger_conditions={"message_contains": ["ola", "oi", "bom dia"]},
                routing_rules=[],
                escalation_rules={},
                auto_responses={
                    "default": "Olá! Sou o assistente do sistema On. Como posso ajudá-lo hoje?"
                },
                success_criteria=[],
                active=True
            )
        ]
        
        for flow in default_flows:
            self.conversation_flows[flow.id] = flow
    
    def _load_active_conversations(self):
        """Carrega conversas ativas do disco (placeholder)"""
        # Em produção, carregaria do banco de dados
        pass
    
    def _register_default_participants(self):
        """Registra participantes padrão do sistema"""
        participants = [
            {"id": "system", "name": "Sistema", "type": "system"},
            {"id": "human_supervisor", "name": "Supervisor Humano", "type": "human"},
            {"id": "atlas", "name": "Atlas Agent", "type": "agent"},
            {"id": "helix", "name": "Helix Agent", "type": "agent"},
            {"id": "sigma", "name": "Sigma Agent", "type": "agent"},
            {"id": "vox", "name": "Vox Agent", "type": "agent"}
        ]
        
        for participant in participants:
            self.participants[participant["id"]] = participant
    
    def _save_conversation(self, conversation: Conversation):
        """Salva conversa no disco (placeholder)"""
        # Em produção, salvaria no banco de dados
        pass
    
    def _archive_conversation(self, conversation: Conversation):
        """Arquiva conversa resolvida (placeholder)"""
        # Em produção, moveria para arquivo/backup
        pass


# Exemplo de uso
if __name__ == "__main__":
    manager = ConversationManager()
    
    # Inicia nova conversa
    conversation = manager.start_conversation(
        initial_message="Preciso de ajuda com um problema técnico urgente na API",
        user_id="user_123",
        conversation_type=ConversationType.TROUBLESHOOTING,
        priority=4,
        context={"department": "engineering"}
    )
    
    print("=== NOVA CONVERSA ===")
    print(f"ID: {conversation.id}")
    print(f"Título: {conversation.title}")
    print(f"Tipo: {conversation.type.value}")
    print(f"Responsável: {conversation.assigned_to}")
    print(f"Tags: {conversation.tags}")
    
    # Adiciona resposta do agente
    manager.add_message(
        conversation.id,
        "Entendi o problema. Pode me descrever mais detalhes sobre o erro?",
        conversation.assigned_to,
        MessageRole.AGENT
    )
    
    # Adiciona resposta do usuário
    manager.add_message(
        conversation.id,
        "O erro acontece quando fazemos mais de 100 requests por minuto. Recebemos timeout.",
        "user_123",
        MessageRole.USER
    )
    
    print(f"\n=== CONVERSA ATUALIZADA ===")
    print(f"Mensagens: {len(conversation.messages)}")
    print(f"Resumo: {conversation.summary}")
    print(f"Estado: {conversation.state.value}")
    
    # Analytics
    analytics = manager.get_conversation_analytics()
    print(f"\n=== ANALYTICS ===")
    print(f"Total de conversas: {analytics['total_conversations']}")
    print(f"Distribuição por tipo: {analytics['type_distribution']}")
    print(f"Conversas ativas: {analytics['active_conversations']}")