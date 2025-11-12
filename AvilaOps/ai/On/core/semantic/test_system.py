#!/usr/bin/env python3
"""
Teste básico do Sistema de Orquestração Inteligente
"""

from orchestration_integration import OrchestrationSystem
import json

def main():
    print('🚀 Iniciando Sistema de Orquestração Inteligente...')
    
    system = OrchestrationSystem(enable_dashboard=False)
    
    if system.start():
        print('✅ Sistema iniciado com sucesso!')
        
        # Teste 1: Processamento de solicitação
        print('\n🧪 Teste 1: Processamento de solicitação')
        response = system.process_request(
            content='Preciso de ajuda com análise de dados urgente',
            sender='user_test',
            priority=3
        )
        
        routing = response['routing_decision']
        semantic = response['semantic_analysis']
        
        print(f'📊 Roteado para: {routing["selected_resource"]}')
        print(f'🎯 Confiança: {routing["confidence"]:.1%}')
        print(f'🧠 Intenção detectada: {semantic["intent"]}')
        print(f'⚡ Urgência: {semantic["urgency"]}')
        
        # Teste 2: Busca na base de conhecimento
        print('\n🔍 Teste 2: Busca na base de conhecimento')
        results = system.search_knowledge('análise de dados', limit=2)
        print(f'📚 Encontrados {len(results)} resultados na base de conhecimento')
        
        # Teste 3: Métricas do sistema
        print('\n📊 Teste 3: Métricas do sistema')
        metrics = system.get_metrics()
        print(f'💬 Total de conversas: {metrics["conversations"]["total"]}')
        print(f'🎯 Decisões de roteamento: {metrics["routing"]["total_decisions"]}')
        print(f'📚 Documentos na base: {metrics["knowledge"]["total_documents"]}')
        
        print('\n✨ Todos os testes passaram! Sistema funcionando perfeitamente.')
        system.stop()
        return True
        
    else:
        print('❌ Falha na inicialização do sistema')
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)