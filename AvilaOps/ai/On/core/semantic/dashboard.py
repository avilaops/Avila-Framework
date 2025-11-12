"""
Orchestration Dashboard - Interface Visual para Monitoramento e Controle
Dashboard web para visualizar e controlar o sistema de orquestração
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
from pathlib import Path
import threading
import time

# Importa componentes do sistema
from analyzer import SemanticAnalyzer
from router import SmartRouter, RoutingRequest, ResourceType
from conversation_manager import ConversationManager, ConversationType, MessageRole
from vector_db import VectorDatabase

class OrchestrationDashboard:
    """Dashboard de Orquestração - Interface Web"""
    
    def __init__(self, host: str = "localhost", port: int = 5000):
        self.app = Flask(__name__, template_folder="templates", static_folder="static")
        self.host = host
        self.port = port
        
        # Componentes do sistema
        self.semantic_analyzer = SemanticAnalyzer()
        self.router = SmartRouter()
        self.conversation_manager = ConversationManager()
        self.vector_db = VectorDatabase()
        
        # Métricas em tempo real
        self.realtime_metrics = {
            'active_conversations': 0,
            'total_requests_today': 0,
            'avg_response_time': 0.0,
            'system_health': 'healthy',
            'last_updated': datetime.now()
        }
        
        # Thread para atualização de métricas
        self.metrics_thread = None
        self.running = False
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura rotas do Flask"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/metrics/overview')
        def metrics_overview():
            """Métricas gerais do sistema"""
            try:
                # Conversas
                conv_analytics = self.conversation_manager.get_conversation_analytics(days=1)
                
                # Router
                routing_analytics = self.router.analyze_routing_patterns(days=1)
                
                # Vector DB
                vector_stats = self.vector_db.get_statistics()
                
                # Recursos
                resources_status = self._get_resources_status()
                
                overview = {
                    'conversations': {
                        'total_today': conv_analytics.get('total_conversations', 0),
                        'active': conv_analytics.get('active_conversations', 0),
                        'avg_resolution_time': conv_analytics.get('avg_resolution_time_minutes', 0),
                        'escalation_rate': conv_analytics.get('escalation_rate', 0)
                    },
                    'routing': {
                        'total_decisions': routing_analytics.get('total_decisions', 0),
                        'avg_confidence': routing_analytics.get('avg_confidence', 0),
                        'most_used_strategy': self._get_most_used_strategy(routing_analytics)
                    },
                    'knowledge': {
                        'total_documents': vector_stats.get('total_documents', 0),
                        'collections': vector_stats.get('total_collections', 0),
                        'cache_efficiency': vector_stats.get('cache_size', 0)
                    },
                    'resources': resources_status,
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify(overview)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/conversations/recent')
        def recent_conversations():
            """Conversas recentes"""
            try:
                conversations = self.conversation_manager.list_conversations(limit=20)
                
                result = []
                for conv in conversations:
                    result.append({
                        'id': conv.id,
                        'title': conv.title,
                        'type': conv.type.value,
                        'state': conv.state.value,
                        'priority': conv.priority,
                        'participants': conv.participants,
                        'message_count': len(conv.messages),
                        'created_at': conv.created_at.isoformat(),
                        'updated_at': conv.updated_at.isoformat(),
                        'assigned_to': conv.assigned_to,
                        'tags': conv.tags,
                        'summary': conv.summary
                    })
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/conversations/<conv_id>')
        def get_conversation(conv_id):
            """Detalhes de uma conversa específica"""
            try:
                conv = self.conversation_manager.get_conversation(conv_id)
                if not conv:
                    return jsonify({'error': 'Conversa não encontrada'}), 404
                
                messages = []
                for msg in conv.messages:
                    messages.append({
                        'id': msg.id,
                        'sender_id': msg.sender_id,
                        'sender_role': msg.sender_role.value,
                        'content': msg.content,
                        'timestamp': msg.timestamp.isoformat(),
                        'semantic_analysis': msg.semantic_analysis,
                        'routing_decision': msg.routing_decision
                    })
                
                result = {
                    'id': conv.id,
                    'title': conv.title,
                    'type': conv.type.value,
                    'state': conv.state.value,
                    'priority': conv.priority,
                    'participants': conv.participants,
                    'created_at': conv.created_at.isoformat(),
                    'updated_at': conv.updated_at.isoformat(),
                    'resolved_at': conv.resolved_at.isoformat() if conv.resolved_at else None,
                    'assigned_to': conv.assigned_to,
                    'tags': conv.tags,
                    'summary': conv.summary,
                    'context': conv.context,
                    'satisfaction_score': conv.satisfaction_score,
                    'resolution_time': conv.resolution_time,
                    'messages': messages
                }
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/resources/status')
        def resources_status():
            """Status dos recursos do sistema"""
            try:
                resources = []
                for resource_id, resource in self.router.resources.items():
                    resources.append({
                        'id': resource.id,
                        'name': resource.name,
                        'type': resource.type.value,
                        'capabilities': resource.capabilities,
                        'expertise_level': resource.expertise_level,
                        'current_load': resource.current_load,
                        'max_load': resource.max_load,
                        'availability': resource.availability,
                        'response_time_avg': resource.response_time_avg,
                        'success_rate': resource.success_rate,
                        'specializations': resource.specializations,
                        'load_percentage': (resource.current_load / resource.max_load * 100) if resource.max_load > 0 else 0
                    })
                
                return jsonify(resources)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/semantic/analyze', methods=['POST'])
        def analyze_text():
            """Análise semântica de texto"""
            try:
                data = request.get_json()
                if not data or 'text' not in data:
                    return jsonify({'error': 'Texto não fornecido'}), 400
                
                text = data['text']
                
                # Análise completa
                entities = self.semantic_analyzer.extract_entities(text)
                topics = self.semantic_analyzer.identify_topics(text)
                keywords = self.semantic_analyzer.extract_keywords(text)
                sentiment = self.semantic_analyzer.analyze_sentiment(text)
                
                result = {
                    'text': text,
                    'analysis': {
                        'entities': [
                            {
                                'text': e.text,
                                'type': e.type,
                                'confidence': e.confidence,
                                'context': e.context
                            }
                            for e in entities
                        ],
                        'topics': [
                            {
                                'name': t.name,
                                'confidence': t.confidence,
                                'keywords': t.keywords,
                                'description': t.description
                            }
                            for t in topics
                        ],
                        'keywords': keywords,
                        'sentiment': sentiment
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/routing/simulate', methods=['POST'])
        def simulate_routing():
            """Simula decisão de roteamento"""
            try:
                data = request.get_json()
                if not data or 'content' not in data:
                    return jsonify({'error': 'Conteúdo não fornecido'}), 400
                
                # Cria request simulado
                routing_request = RoutingRequest(
                    id=f"sim_{int(datetime.now().timestamp())}",
                    content=data['content'],
                    sender=data.get('sender', 'dashboard_user'),
                    priority=data.get('priority', 2),
                    required_capabilities=data.get('capabilities', []),
                    preferred_type=ResourceType.AGENT,
                    max_wait_time=30.0,
                    context=data.get('context', {}),
                    timestamp=datetime.now()
                )
                
                # Executa roteamento
                decision = self.router.route_request(routing_request)
                
                # Obtém recomendações alternativas
                recommendations = self.router.get_resource_recommendations(routing_request)
                
                result = {
                    'decision': {
                        'selected_resource': decision.selected_resource,
                        'strategy_used': decision.strategy_used.value,
                        'confidence': decision.confidence,
                        'reasoning': decision.reasoning,
                        'alternatives': decision.alternatives,
                        'estimated_response_time': decision.estimated_response_time,
                        'metadata': decision.metadata
                    },
                    'recommendations': [
                        {
                            'resource_id': rec[0],
                            'score': rec[1],
                            'reason': rec[2]
                        }
                        for rec in recommendations
                    ],
                    'timestamp': datetime.now().isoformat()
                }
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/search', methods=['POST'])
        def search_knowledge():
            """Busca na base de conhecimento"""
            try:
                data = request.get_json()
                if not data or 'query' not in data:
                    return jsonify({'error': 'Query não fornecida'}), 400
                
                query = data['query']
                limit = data.get('limit', 10)
                category = data.get('category')
                min_similarity = data.get('min_similarity', 0.3)
                
                results = self.vector_db.search(
                    query=query,
                    limit=limit,
                    category=category,
                    min_similarity=min_similarity
                )
                
                search_results = []
                for result in results:
                    search_results.append({
                        'document_id': result.document.id,
                        'content': result.document.content,
                        'similarity_score': result.similarity_score,
                        'rank': result.rank,
                        'matched_terms': result.matched_terms,
                        'category': result.document.category,
                        'tags': result.document.tags,
                        'metadata': result.document.metadata,
                        'created_at': result.document.created_at.isoformat()
                    })
                
                return jsonify({
                    'query': query,
                    'total_results': len(search_results),
                    'results': search_results,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/conversations/start', methods=['POST'])
        def start_conversation():
            """Inicia nova conversa"""
            try:
                data = request.get_json()
                if not data or 'message' not in data:
                    return jsonify({'error': 'Mensagem não fornecida'}), 400
                
                conversation = self.conversation_manager.start_conversation(
                    initial_message=data['message'],
                    user_id=data.get('user_id', 'dashboard_user'),
                    conversation_type=ConversationType(data.get('type', 'question_answer')),
                    priority=data.get('priority', 2),
                    context=data.get('context', {})
                )
                
                result = {
                    'id': conversation.id,
                    'title': conversation.title,
                    'type': conversation.type.value,
                    'state': conversation.state.value,
                    'assigned_to': conversation.assigned_to,
                    'created_at': conversation.created_at.isoformat()
                }
                
                return jsonify(result)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/system/health')
        def system_health():
            """Status de saúde do sistema"""
            try:
                health_status = {
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'components': {
                        'semantic_analyzer': {'status': 'up', 'response_time_ms': 5},
                        'router': {'status': 'up', 'active_resources': len(self.router.resources)},
                        'conversation_manager': {'status': 'up', 'active_conversations': len(self.conversation_manager.active_conversations)},
                        'vector_database': {'status': 'up', 'documents_count': self.vector_db.get_statistics()['total_documents']}
                    },
                    'metrics': self.realtime_metrics
                }
                
                return jsonify(health_status)
            except Exception as e:
                return jsonify({
                    'status': 'unhealthy',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500
    
    def _get_resources_status(self) -> Dict[str, Any]:
        """Obtém status resumido dos recursos"""
        total_resources = len(self.router.resources)
        available_resources = sum(1 for r in self.router.resources.values() if r.availability)
        total_load = sum(r.current_load for r in self.router.resources.values())
        total_capacity = sum(r.max_load for r in self.router.resources.values())
        
        return {
            'total': total_resources,
            'available': available_resources,
            'utilization': (total_load / total_capacity * 100) if total_capacity > 0 else 0,
            'avg_response_time': sum(r.response_time_avg for r in self.router.resources.values()) / total_resources if total_resources > 0 else 0
        }
    
    def _get_most_used_strategy(self, routing_analytics: Dict) -> str:
        """Obtém estratégia de roteamento mais usada"""
        strategy_usage = routing_analytics.get('strategy_usage', {})
        if not strategy_usage:
            return 'N/A'
        
        return max(strategy_usage.keys(), key=lambda x: strategy_usage[x])
    
    def _update_metrics_loop(self):
        """Loop de atualização de métricas em background"""
        while self.running:
            try:
                # Atualiza métricas em tempo real
                self.realtime_metrics.update({
                    'active_conversations': len(self.conversation_manager.active_conversations),
                    'total_requests_today': self._count_today_requests(),
                    'avg_response_time': self._calculate_avg_response_time(),
                    'system_health': self._assess_system_health(),
                    'last_updated': datetime.now()
                })
                
                time.sleep(30)  # Atualiza a cada 30 segundos
            except Exception as e:
                print(f"Erro ao atualizar métricas: {e}")
                time.sleep(60)
    
    def _count_today_requests(self) -> int:
        """Conta requests do dia atual"""
        today = datetime.now().date()
        count = 0
        
        for conv in self.conversation_manager.active_conversations.values():
            if conv.created_at.date() == today:
                count += len(conv.messages)
        
        return count
    
    def _calculate_avg_response_time(self) -> float:
        """Calcula tempo médio de resposta"""
        response_times = []
        
        for resource in self.router.resources.values():
            if resource.availability:
                response_times.append(resource.response_time_avg)
        
        return sum(response_times) / len(response_times) if response_times else 0.0
    
    def _assess_system_health(self) -> str:
        """Avalia saúde geral do sistema"""
        try:
            # Verifica se componentes principais estão funcionando
            available_resources = sum(1 for r in self.router.resources.values() if r.availability)
            total_resources = len(self.router.resources)
            
            if available_resources / total_resources < 0.5:
                return 'degraded'
            elif available_resources == total_resources:
                return 'healthy'
            else:
                return 'warning'
        except Exception:
            return 'unhealthy'
    
    def run(self, debug: bool = False):
        """Inicia o dashboard"""
        print(f"🚀 Iniciando Dashboard de Orquestração em http://{self.host}:{self.port}")
        
        # Inicia thread de métricas
        self.running = True
        self.metrics_thread = threading.Thread(target=self._update_metrics_loop, daemon=True)
        self.metrics_thread.start()
        
        # Inicia servidor Flask
        self.app.run(host=self.host, port=self.port, debug=debug)
    
    def stop(self):
        """Para o dashboard"""
        self.running = False
        if self.metrics_thread:
            self.metrics_thread.join(timeout=5)


# Cria template HTML básico
def create_dashboard_template():
    """Cria template HTML para o dashboard"""
    template_dir = Path(__file__).parent / "templates"
    template_dir.mkdir(exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard de Orquestração - Sistema On</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f7; }
        .header { background: #1d1d1f; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; font-weight: 600; }
        .main { padding: 2rem; max-width: 1200px; margin: 0 auto; }
        .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .card h3 { color: #1d1d1f; margin-bottom: 1rem; font-size: 1.1rem; }
        .metric { display: flex; justify-content: space-between; margin-bottom: 0.5rem; }
        .metric-label { color: #666; }
        .metric-value { font-weight: 600; color: #1d1d1f; }
        .status-indicator { width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px; }
        .status-healthy { background: #34c759; }
        .status-warning { background: #ff9500; }
        .status-error { background: #ff3b30; }
        .conversation-item { border-bottom: 1px solid #f0f0f0; padding: 0.75rem 0; }
        .conversation-item:last-child { border-bottom: none; }
        .conversation-title { font-weight: 600; color: #1d1d1f; margin-bottom: 0.25rem; }
        .conversation-meta { color: #666; font-size: 0.875rem; }
        .test-section { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test-input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 1rem; font-size: 1rem; }
        .test-button { background: #007aff; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-size: 1rem; }
        .test-button:hover { background: #0056b3; }
        .result-container { background: #f8f9fa; border-radius: 8px; padding: 1rem; margin-top: 1rem; font-family: monospace; font-size: 0.875rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Dashboard de Orquestração - Sistema On</h1>
    </div>
    
    <div class="main">
        <!-- Métricas principais -->
        <div class="cards">
            <div class="card">
                <h3>📊 Visão Geral</h3>
                <div class="metric">
                    <span class="metric-label">Status do Sistema</span>
                    <span class="metric-value">
                        <span class="status-indicator status-healthy"></span>
                        Saudável
                    </span>
                </div>
                <div class="metric">
                    <span class="metric-label">Conversas Ativas</span>
                    <span class="metric-value" id="active-conversations">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Requests Hoje</span>
                    <span class="metric-value" id="requests-today">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tempo Médio Resposta</span>
                    <span class="metric-value" id="avg-response-time">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 Recursos</h3>
                <div class="metric">
                    <span class="metric-label">Total de Agentes</span>
                    <span class="metric-value" id="total-resources">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Disponíveis</span>
                    <span class="metric-value" id="available-resources">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Utilização</span>
                    <span class="metric-value" id="resource-utilization">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>💬 Conversas Recentes</h3>
                <div id="recent-conversations">
                    Carregando...
                </div>
            </div>
        </div>
        
        <!-- Seção de Testes -->
        <div class="test-section">
            <h3>🧪 Teste de Análise Semântica</h3>
            <textarea class="test-input" id="semantic-text" placeholder="Digite um texto para análise semântica..." rows="3"></textarea>
            <button class="test-button" onclick="testSemanticAnalysis()">Analisar Texto</button>
            <div id="semantic-result" class="result-container" style="display: none;"></div>
        </div>
        
        <div class="test-section">
            <h3>🎯 Simulador de Roteamento</h3>
            <textarea class="test-input" id="routing-text" placeholder="Digite uma mensagem para simular roteamento..." rows="3"></textarea>
            <button class="test-button" onclick="testRouting()">Simular Roteamento</button>
            <div id="routing-result" class="result-container" style="display: none;"></div>
        </div>
        
        <div class="test-section">
            <h3>🔍 Busca na Base de Conhecimento</h3>
            <input class="test-input" id="search-query" placeholder="Digite sua busca..." />
            <button class="test-button" onclick="testSearch()">Buscar</button>
            <div id="search-result" class="result-container" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        // Atualiza métricas principais
        async function updateMetrics() {
            try {
                const response = await fetch('/api/metrics/overview');
                const data = await response.json();
                
                document.getElementById('active-conversations').textContent = data.conversations.active;
                document.getElementById('requests-today').textContent = data.conversations.total_today;
                document.getElementById('avg-response-time').textContent = data.resources.avg_response_time.toFixed(1) + 'min';
                document.getElementById('total-resources').textContent = data.resources.total;
                document.getElementById('available-resources').textContent = data.resources.available;
                document.getElementById('resource-utilization').textContent = data.resources.utilization.toFixed(1) + '%';
            } catch (error) {
                console.error('Erro ao atualizar métricas:', error);
            }
        }
        
        // Atualiza conversas recentes
        async function updateConversations() {
            try {
                const response = await fetch('/api/conversations/recent');
                const conversations = await response.json();
                
                const container = document.getElementById('recent-conversations');
                container.innerHTML = '';
                
                conversations.slice(0, 5).forEach(conv => {
                    const item = document.createElement('div');
                    item.className = 'conversation-item';
                    item.innerHTML = `
                        <div class="conversation-title">${conv.title}</div>
                        <div class="conversation-meta">
                            ${conv.type} • ${conv.state} • ${conv.message_count} mensagens
                        </div>
                    `;
                    container.appendChild(item);
                });
            } catch (error) {
                console.error('Erro ao atualizar conversas:', error);
            }
        }
        
        // Teste de análise semântica
        async function testSemanticAnalysis() {
            const text = document.getElementById('semantic-text').value;
            if (!text.trim()) return;
            
            try {
                const response = await fetch('/api/semantic/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const result = await response.json();
                const container = document.getElementById('semantic-result');
                container.style.display = 'block';
                container.innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                console.error('Erro na análise semântica:', error);
            }
        }
        
        // Teste de roteamento
        async function testRouting() {
            const text = document.getElementById('routing-text').value;
            if (!text.trim()) return;
            
            try {
                const response = await fetch('/api/routing/simulate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({content: text})
                });
                
                const result = await response.json();
                const container = document.getElementById('routing-result');
                container.style.display = 'block';
                container.innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                console.error('Erro no roteamento:', error);
            }
        }
        
        // Teste de busca
        async function testSearch() {
            const query = document.getElementById('search-query').value;
            if (!query.trim()) return;
            
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query, limit: 5})
                });
                
                const result = await response.json();
                const container = document.getElementById('search-result');
                container.style.display = 'block';
                container.innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                console.error('Erro na busca:', error);
            }
        }
        
        // Inicializa dashboard
        document.addEventListener('DOMContentLoaded', function() {
            updateMetrics();
            updateConversations();
            
            // Atualiza a cada 30 segundos
            setInterval(() => {
                updateMetrics();
                updateConversations();
            }, 30000);
        });
    </script>
</body>
</html>'''
    
    template_file = template_dir / "dashboard.html"
    template_file.write_text(html_content, encoding='utf-8')
    
    return template_file


# Exemplo de uso
if __name__ == "__main__":
    # Cria template se não existir
    create_dashboard_template()
    
    # Inicia dashboard
    dashboard = OrchestrationDashboard(host="localhost", port=5000)
    
    try:
        dashboard.run(debug=True)
    except KeyboardInterrupt:
        print("\n🛑 Parando Dashboard...")
        dashboard.stop()
    except Exception as e:
        print(f"❌ Erro no Dashboard: {e}")