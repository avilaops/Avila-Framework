"""
Smart Router - Sistema Inteligente de Roteamento
Responsável por direcionar conversas/tarefas para os recursos mais adequados
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

from analyzer import SemanticAnalyzer, Entity, Topic

class ResourceType(Enum):
    """Tipos de recursos disponíveis"""
    AGENT = "agent"
    HUMAN = "human"
    SYSTEM = "system"
    EXTERNAL = "external"

class RoutingStrategy(Enum):
    """Estratégias de roteamento"""
    BEST_MATCH = "best_match"          # Melhor correspondência
    LOAD_BALANCE = "load_balance"      # Balanceamento de carga
    ROUND_ROBIN = "round_robin"        # Alternância circular
    PRIORITY_BASED = "priority_based"   # Baseado em prioridade
    EXPERTISE_LEVEL = "expertise_level" # Nível de especialização

@dataclass
class Resource:
    """Recurso disponível para roteamento"""
    id: str
    name: str
    type: ResourceType
    capabilities: List[str]
    expertise_level: float  # 0.0 - 1.0
    current_load: int
    max_load: int
    availability: bool
    response_time_avg: float  # em minutos
    success_rate: float  # 0.0 - 1.0
    specializations: List[str]
    metadata: Dict[str, Any]

@dataclass
class RoutingDecision:
    """Decisão de roteamento tomada"""
    request_id: str
    timestamp: datetime
    selected_resource: str
    strategy_used: RoutingStrategy
    confidence: float
    reasoning: str
    alternatives: List[str]
    estimated_response_time: float
    metadata: Dict[str, Any]

@dataclass
class RoutingRequest:
    """Solicitação de roteamento"""
    id: str
    content: str
    sender: str
    priority: int  # 1-5, sendo 5 crítico
    required_capabilities: List[str]
    preferred_type: Optional[ResourceType]
    max_wait_time: Optional[float]  # em minutos
    context: Dict[str, Any]
    timestamp: datetime

class SmartRouter:
    """Roteador Inteligente"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.semantic_analyzer = SemanticAnalyzer()
        self.resources: Dict[str, Resource] = {}
        self.routing_history: List[RoutingDecision] = []
        self.performance_metrics: Dict[str, Dict[str, float]] = {}
        
        # Carrega configuração
        self.config = self._load_config(config_path)
        self._initialize_resources()
        
    def register_resource(self, resource: Resource) -> bool:
        """Registra um novo recurso no roteador"""
        if resource.id in self.resources:
            return False  # Já existe
            
        self.resources[resource.id] = resource
        self.performance_metrics[resource.id] = {
            'requests_handled': 0,
            'avg_response_time': resource.response_time_avg,
            'success_rate': resource.success_rate,
            'last_updated': datetime.now().timestamp()
        }
        return True
    
    def update_resource_status(self, resource_id: str, **kwargs) -> bool:
        """Atualiza status de um recurso"""
        if resource_id not in self.resources:
            return False
            
        resource = self.resources[resource_id]
        for key, value in kwargs.items():
            if hasattr(resource, key):
                setattr(resource, key, value)
        
        return True
    
    def route_request(self, request: RoutingRequest, strategy: RoutingStrategy = RoutingStrategy.BEST_MATCH) -> RoutingDecision:
        """Roteia uma solicitação usando a estratégia especificada"""
        
        # Análise semântica do conteúdo
        semantic_analysis = self._analyze_request_semantics(request)
        
        # Filtra recursos elegíveis
        eligible_resources = self._filter_eligible_resources(request, semantic_analysis)
        
        if not eligible_resources:
            return self._create_fallback_decision(request, "Nenhum recurso elegível encontrado")
        
        # Aplica estratégia de roteamento
        selected_resource = self._apply_routing_strategy(request, eligible_resources, strategy, semantic_analysis)
        
        # Cria decisão de roteamento
        decision = self._create_routing_decision(request, selected_resource, strategy, eligible_resources, semantic_analysis)
        
        # Atualiza métricas e histórico
        self._update_metrics(decision)
        self.routing_history.append(decision)
        
        return decision
    
    def get_resource_recommendations(self, request: RoutingRequest, top_n: int = 3) -> List[Tuple[str, float, str]]:
        """Retorna recomendações de recursos com scores"""
        semantic_analysis = self._analyze_request_semantics(request)
        eligible_resources = self._filter_eligible_resources(request, semantic_analysis)
        
        recommendations = []
        for resource_id in eligible_resources:
            score = self._calculate_resource_score(request, resource_id, semantic_analysis)
            reason = self._explain_recommendation(request, resource_id, semantic_analysis)
            recommendations.append((resource_id, score, reason))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:top_n]
    
    def analyze_routing_patterns(self, days: int = 7) -> Dict[str, Any]:
        """Analisa padrões de roteamento dos últimos dias"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_decisions = [d for d in self.routing_history if d.timestamp > cutoff_date]
        
        if not recent_decisions:
            return {"message": "Dados insuficientes para análise"}
        
        # Estatísticas por recurso
        resource_stats = {}
        for decision in recent_decisions:
            resource_id = decision.selected_resource
            if resource_id not in resource_stats:
                resource_stats[resource_id] = {
                    'count': 0,
                    'avg_confidence': 0,
                    'strategies_used': {}
                }
            
            stats = resource_stats[resource_id]
            stats['count'] += 1
            stats['avg_confidence'] = (stats['avg_confidence'] * (stats['count'] - 1) + decision.confidence) / stats['count']
            
            strategy = decision.strategy_used.value
            stats['strategies_used'][strategy] = stats['strategies_used'].get(strategy, 0) + 1
        
        # Estratégias mais usadas
        strategy_usage = {}
        for decision in recent_decisions:
            strategy = decision.strategy_used.value
            strategy_usage[strategy] = strategy_usage.get(strategy, 0) + 1
        
        return {
            'period_days': days,
            'total_decisions': len(recent_decisions),
            'resource_usage': resource_stats,
            'strategy_usage': strategy_usage,
            'avg_confidence': sum(d.confidence for d in recent_decisions) / len(recent_decisions),
            'avg_response_time': sum(d.estimated_response_time for d in recent_decisions) / len(recent_decisions)
        }
    
    def _analyze_request_semantics(self, request: RoutingRequest) -> Dict[str, Any]:
        """Analisa semanticamente a solicitação"""
        entities = self.semantic_analyzer.extract_entities(request.content)
        topics = self.semantic_analyzer.identify_topics(request.content)
        keywords = self.semantic_analyzer.extract_keywords(request.content)
        sentiment = self.semantic_analyzer.analyze_sentiment(request.content)
        
        return {
            'entities': entities,
            'topics': topics,
            'keywords': keywords,
            'sentiment': sentiment,
            'complexity': self._assess_complexity(request.content),
            'domain': self._identify_domain(topics, keywords)
        }
    
    def _filter_eligible_resources(self, request: RoutingRequest, semantic_analysis: Dict) -> List[str]:
        """Filtra recursos elegíveis para a solicitação"""
        eligible = []
        
        for resource_id, resource in self.resources.items():
            if not resource.availability:
                continue
            
            if resource.current_load >= resource.max_load:
                continue
            
            # Verifica capacidades requeridas
            if request.required_capabilities:
                if not all(cap in resource.capabilities for cap in request.required_capabilities):
                    continue
            
            # Verifica tipo preferido
            if request.preferred_type and resource.type != request.preferred_type:
                continue
            
            # Verifica especialização com base na análise semântica
            domain = semantic_analysis.get('domain', '')
            if domain and domain not in resource.specializations and resource.specializations:
                # Se tem especializações mas não inclui o domínio, reduz prioridade mas não elimina
                pass
            
            eligible.append(resource_id)
        
        return eligible
    
    def _apply_routing_strategy(self, request: RoutingRequest, eligible_resources: List[str], 
                              strategy: RoutingStrategy, semantic_analysis: Dict) -> str:
        """Aplica a estratégia de roteamento selecionada"""
        
        if strategy == RoutingStrategy.BEST_MATCH:
            return self._best_match_strategy(request, eligible_resources, semantic_analysis)
        elif strategy == RoutingStrategy.LOAD_BALANCE:
            return self._load_balance_strategy(eligible_resources)
        elif strategy == RoutingStrategy.ROUND_ROBIN:
            return self._round_robin_strategy(eligible_resources)
        elif strategy == RoutingStrategy.PRIORITY_BASED:
            return self._priority_based_strategy(request, eligible_resources)
        elif strategy == RoutingStrategy.EXPERTISE_LEVEL:
            return self._expertise_level_strategy(request, eligible_resources, semantic_analysis)
        else:
            return eligible_resources[0]  # Fallback
    
    def _best_match_strategy(self, request: RoutingRequest, eligible_resources: List[str], semantic_analysis: Dict) -> str:
        """Estratégia de melhor correspondência"""
        best_resource = None
        best_score = -1
        
        for resource_id in eligible_resources:
            score = self._calculate_resource_score(request, resource_id, semantic_analysis)
            if score > best_score:
                best_score = score
                best_resource = resource_id
        
        return best_resource or eligible_resources[0]
    
    def _load_balance_strategy(self, eligible_resources: List[str]) -> str:
        """Estratégia de balanceamento de carga"""
        min_load = float('inf')
        best_resource = None
        
        for resource_id in eligible_resources:
            resource = self.resources[resource_id]
            load_ratio = resource.current_load / resource.max_load if resource.max_load > 0 else 0
            
            if load_ratio < min_load:
                min_load = load_ratio
                best_resource = resource_id
        
        return best_resource or eligible_resources[0]
    
    def _round_robin_strategy(self, eligible_resources: List[str]) -> str:
        """Estratégia de alternância circular"""
        if not hasattr(self, '_round_robin_index'):
            self._round_robin_index = 0
        
        if eligible_resources:
            selected = eligible_resources[self._round_robin_index % len(eligible_resources)]
            self._round_robin_index += 1
            return selected
        
        return eligible_resources[0] if eligible_resources else None
    
    def _priority_based_strategy(self, request: RoutingRequest, eligible_resources: List[str]) -> str:
        """Estratégia baseada em prioridade"""
        if request.priority >= 4:  # Alta prioridade
            # Escolhe recurso com melhor tempo de resposta
            best_resource = min(eligible_resources, 
                              key=lambda r: self.resources[r].response_time_avg)
            return best_resource
        else:
            # Usa balanceamento de carga para prioridade normal
            return self._load_balance_strategy(eligible_resources)
    
    def _expertise_level_strategy(self, request: RoutingRequest, eligible_resources: List[str], semantic_analysis: Dict) -> str:
        """Estratégia baseada no nível de expertise"""
        domain = semantic_analysis.get('domain', '')
        complexity = semantic_analysis.get('complexity', 0.5)
        
        best_resource = None
        best_score = -1
        
        for resource_id in eligible_resources:
            resource = self.resources[resource_id]
            
            # Score baseado em expertise e especialização
            score = resource.expertise_level
            
            if domain in resource.specializations:
                score += 0.3  # Bonus por especialização
            
            # Ajusta pela complexidade da tarefa
            if complexity > 0.7 and resource.expertise_level > 0.8:
                score += 0.2  # Especialista para tarefas complexas
            
            if score > best_score:
                best_score = score
                best_resource = resource_id
        
        return best_resource or eligible_resources[0]
    
    def _calculate_resource_score(self, request: RoutingRequest, resource_id: str, semantic_analysis: Dict) -> float:
        """Calcula score de adequação de um recurso para a solicitação"""
        resource = self.resources[resource_id]
        score = 0.0
        
        # Score base por disponibilidade e carga
        load_factor = 1.0 - (resource.current_load / resource.max_load) if resource.max_load > 0 else 1.0
        score += load_factor * 0.2
        
        # Score por capabilities match
        if request.required_capabilities:
            capability_match = len([cap for cap in request.required_capabilities if cap in resource.capabilities])
            capability_ratio = capability_match / len(request.required_capabilities)
            score += capability_ratio * 0.3
        
        # Score por especialização
        domain = semantic_analysis.get('domain', '')
        if domain and domain in resource.specializations:
            score += 0.25
        
        # Score por performance histórica
        performance = self.performance_metrics.get(resource_id, {})
        success_rate = performance.get('success_rate', resource.success_rate)
        score += success_rate * 0.15
        
        # Score por tempo de resposta
        response_time = performance.get('avg_response_time', resource.response_time_avg)
        response_score = max(0, 1.0 - (response_time / 60.0))  # Normaliza por hora
        score += response_score * 0.1
        
        return min(score, 1.0)
    
    def _assess_complexity(self, content: str) -> float:
        """Avalia complexidade do conteúdo (0.0 - 1.0)"""
        complexity_indicators = [
            'analise', 'complexo', 'detalhado', 'profundo', 'estrategico',
            'tecnico', 'especializado', 'avancado', 'critico'
        ]
        
        content_lower = content.lower()
        matches = sum(1 for indicator in complexity_indicators if indicator in content_lower)
        
        # Também considera tamanho do texto
        length_factor = min(len(content) / 1000.0, 1.0)
        
        return min((matches / len(complexity_indicators)) + length_factor * 0.3, 1.0)
    
    def _identify_domain(self, topics: List[Topic], keywords: List[Dict]) -> str:
        """Identifica domínio principal baseado em tópicos e keywords"""
        if topics:
            return topics[0].name  # Tópico com maior confiança
        
        # Fallback: analisa keywords
        domain_keywords = {
            'tecnologia': ['sistema', 'software', 'api', 'codigo', 'tecnologia'],
            'financeiro': ['dinheiro', 'orcamento', 'custo', 'financeiro', 'pagamento'],
            'vendas': ['cliente', 'venda', 'produto', 'comercial', 'mercado'],
            'juridico': ['contrato', 'legal', 'juridico', 'compliance', 'lei'],
            'estrategico': ['estrategia', 'planejamento', 'meta', 'objetivo'],
            'operacional': ['processo', 'operacao', 'producao', 'qualidade']
        }
        
        keyword_texts = [kw['word'] for kw in keywords[:5]]  # Top 5 keywords
        
        for domain, domain_kws in domain_keywords.items():
            if any(kw in keyword_texts for kw in domain_kws):
                return domain
        
        return 'geral'
    
    def _create_routing_decision(self, request: RoutingRequest, selected_resource: str, 
                                strategy: RoutingStrategy, eligible_resources: List[str], 
                                semantic_analysis: Dict) -> RoutingDecision:
        """Cria objeto de decisão de roteamento"""
        
        resource = self.resources[selected_resource]
        confidence = self._calculate_resource_score(request, selected_resource, semantic_analysis)
        
        # Reasoning
        domain = semantic_analysis.get('domain', 'geral')
        reasoning = f"Selecionado {resource.name} para domínio '{domain}' usando estratégia {strategy.value}"
        
        if domain in resource.specializations:
            reasoning += f" (especialização em {domain})"
        
        # Alternativas (outros recursos elegíveis)
        alternatives = [r for r in eligible_resources if r != selected_resource][:3]
        
        return RoutingDecision(
            request_id=request.id,
            timestamp=datetime.now(),
            selected_resource=selected_resource,
            strategy_used=strategy,
            confidence=confidence,
            reasoning=reasoning,
            alternatives=alternatives,
            estimated_response_time=resource.response_time_avg,
            metadata={
                'domain': domain,
                'complexity': semantic_analysis.get('complexity', 0),
                'sentiment': semantic_analysis.get('sentiment', {}),
                'total_eligible': len(eligible_resources)
            }
        )
    
    def _create_fallback_decision(self, request: RoutingRequest, reason: str) -> RoutingDecision:
        """Cria decisão de fallback quando não há recursos elegíveis"""
        return RoutingDecision(
            request_id=request.id,
            timestamp=datetime.now(),
            selected_resource="human_supervisor",
            strategy_used=RoutingStrategy.BEST_MATCH,
            confidence=0.1,
            reasoning=f"Fallback para supervisor humano: {reason}",
            alternatives=[],
            estimated_response_time=30.0,  # 30 minutos para humano
            metadata={'fallback': True, 'reason': reason}
        )
    
    def _explain_recommendation(self, request: RoutingRequest, resource_id: str, semantic_analysis: Dict) -> str:
        """Explica por que um recurso foi recomendado"""
        resource = self.resources[resource_id]
        explanations = []
        
        # Especialização
        domain = semantic_analysis.get('domain', '')
        if domain in resource.specializations:
            explanations.append(f"especializado em {domain}")
        
        # Carga
        load_ratio = resource.current_load / resource.max_load if resource.max_load > 0 else 0
        if load_ratio < 0.5:
            explanations.append("baixa carga atual")
        
        # Performance
        if resource.success_rate > 0.8:
            explanations.append(f"alta taxa de sucesso ({resource.success_rate:.1%})")
        
        if resource.response_time_avg < 15:
            explanations.append("tempo de resposta rápido")
        
        return "Recomendado por: " + ", ".join(explanations) if explanations else "Recurso disponível"
    
    def _update_metrics(self, decision: RoutingDecision):
        """Atualiza métricas de performance"""
        resource_id = decision.selected_resource
        if resource_id in self.performance_metrics:
            metrics = self.performance_metrics[resource_id]
            metrics['requests_handled'] += 1
            metrics['last_updated'] = datetime.now().timestamp()
    
    def _initialize_resources(self):
        """Inicializa recursos padrão do sistema On"""
        default_resources = [
            Resource(
                id="atlas", name="Atlas Agent", type=ResourceType.AGENT,
                capabilities=["knowledge", "strategy", "analysis"], expertise_level=0.9,
                current_load=0, max_load=10, availability=True, response_time_avg=5.0,
                success_rate=0.95, specializations=["estrategico", "corporativo", "dados"],
                metadata={"description": "Especialista em estratégia e conhecimento"}
            ),
            Resource(
                id="helix", name="Helix Agent", type=ResourceType.AGENT,
                capabilities=["technical", "devops", "automation"], expertise_level=0.95,
                current_load=0, max_load=15, availability=True, response_time_avg=3.0,
                success_rate=0.98, specializations=["tecnologia", "engenharia", "devops"],
                metadata={"description": "Especialista técnico e DevOps"}
            ),
            Resource(
                id="sigma", name="Sigma Agent", type=ResourceType.AGENT,
                capabilities=["financial", "analysis", "math"], expertise_level=0.92,
                current_load=0, max_load=8, availability=True, response_time_avg=7.0,
                success_rate=0.96, specializations=["financeiro", "controladoria", "analise"],
                metadata={"description": "Especialista financeiro e analítico"}
            ),
            Resource(
                id="vox", name="Vox Agent", type=ResourceType.AGENT,
                capabilities=["sales", "communication", "crm"], expertise_level=0.88,
                current_load=0, max_load=12, availability=True, response_time_avg=4.0,
                success_rate=0.92, specializations=["vendas", "comercial", "comunicacao"],
                metadata={"description": "Especialista em vendas e CRM"}
            ),
            Resource(
                id="human_supervisor", name="Human Supervisor", type=ResourceType.HUMAN,
                capabilities=["decision_making", "escalation", "complex_analysis"], expertise_level=1.0,
                current_load=0, max_load=3, availability=True, response_time_avg=30.0,
                success_rate=0.99, specializations=["geral"], 
                metadata={"description": "Supervisão humana para casos complexos"}
            )
        ]
        
        for resource in default_resources:
            self.register_resource(resource)
    
    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Carrega configuração do roteador"""
        default_config = {
            "default_strategy": "best_match",
            "max_routing_history": 1000,
            "enable_learning": True,
            "performance_window_hours": 24
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception:
                pass  # Usa configuração padrão
        
        return default_config


# Exemplo de uso
if __name__ == "__main__":
    router = SmartRouter()
    
    # Exemplo de solicitação
    request = RoutingRequest(
        id="req_001",
        content="Preciso de uma análise técnica urgente sobre o problema de performance na API. O sistema está com latência alta e precisamos identificar o gargalo.",
        sender="user_dev",
        priority=4,  # Alta prioridade
        required_capabilities=["technical", "analysis"],
        preferred_type=ResourceType.AGENT,
        max_wait_time=15.0,
        context={"department": "engineering"},
        timestamp=datetime.now()
    )
    
    # Roteamento
    decision = router.route_request(request)
    
    print("=== DECISÃO DE ROTEAMENTO ===")
    print(f"Recurso selecionado: {decision.selected_resource}")
    print(f"Estratégia: {decision.strategy_used.value}")
    print(f"Confiança: {decision.confidence:.1%}")
    print(f"Razão: {decision.reasoning}")
    print(f"Tempo estimado: {decision.estimated_response_time:.1f} min")
    
    # Recomendações
    recommendations = router.get_resource_recommendations(request)
    print(f"\n=== RECOMENDAÇÕES ===")
    for resource_id, score, reason in recommendations:
        print(f"• {resource_id}: {score:.1%} - {reason}")