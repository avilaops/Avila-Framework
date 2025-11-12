#!/usr/bin/env python3
"""
DEMO - ÁVILA EXECUTIVE DASHBOARD
===============================
Script de demonstração do sistema de dashboards executivos
Autor: Nicolas Avila - Ávila Framework
Data: 2025-11-11
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

from config_manager import load_dashboard_config

async def demo_dashboard():
    """Demonstração completa do sistema de dashboard"""
    print("🏛️ ÁVILA EXECUTIVE DASHBOARD - DEMONSTRAÇÃO")
    print("=" * 60)
    print(f"⏰ Iniciando demonstração em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    try:
        # Configuração do dashboard
        print("⚙️ Configurando dashboard...")
        config = DashboardConfig(
            company_name="Ávila Framework",
            email_recipients=["nicolas@avila.inc"],
            sender_email="reports@avilaops.com"
        )
        
        # Criar instância do dashboard
        dashboard = AvilaExecutiveDashboard(config)
        print("✅ Dashboard configurado com sucesso!")
        print()
        
        # Gerar dados do dashboard
        print("📊 Gerando dados do dashboard...")
        dashboard_data = await dashboard.generate_full_dashboard()
        print("✅ Dados gerados com sucesso!")
        print()
        
        # Mostrar resumo dos dados
        print("📈 RESUMO EXECUTIVO:")
        summary = dashboard_data['executive_summary']
        print(f"   🚀 Produtos Ativos: {summary['total_products']}")
        print(f"   📈 Crescimento: {summary['revenue_growth']}%")
        print(f"   ⭐ Satisfação: {summary['customer_satisfaction']}")
        print(f"   👥 Equipe: {summary['team_size']} membros")
        print()
        
        # Gerar HTML
        print("🎨 Gerando relatório HTML...")
        html_content = dashboard.generate_html_report(dashboard_data)
        print("✅ HTML gerado com sucesso!")
        print()
        
        # Salvar arquivo
        print("💾 Salvando relatório...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"demo_dashboard_{timestamp}.html"
        filepath = await dashboard.save_report(html_content, filename)
        print(f"✅ Arquivo salvo: {filepath}")
        print()
        
        # Opção para envio por email
        print("📧 Deseja enviar o relatório por email? (s/n): ", end="")
        choice = input().strip().lower()
        
        if choice in ['s', 'sim', 'y', 'yes']:
            print("📨 Enviando relatório por email...")
            # Nota: vai pedir a senha do email
            success = await dashboard.send_email_report(html_content)
            
            if success:
                print("✅ Email enviado com sucesso!")
            else:
                print("⚠️ Falha no envio do email (normal sem credenciais)")
        else:
            print("📄 Relatório salvo apenas localmente.")
        
        print()
        print("🎯 PRINCIPAIS CONQUISTAS:")
        for achievement in summary['key_achievements']:
            print(f"   {achievement}")
        
        print()
        print("⚠️ ALERTAS CRÍTICOS:")
        for alert in summary['critical_alerts']:
            print(f"   {alert}")
        
        print()
        print("💰 MÉTRICAS FINANCEIRAS:")
        financial = dashboard_data['financial_overview']
        print(f"   💵 Receita Atual: R$ {financial['revenue']['current_month']:,.2f}")
        print(f"   📊 Crescimento: {financial['revenue']['growth_rate']}%")
        print(f"   📈 Margem Bruta: {financial['profitability']['gross_margin']}%")
        print(f"   💎 Margem Líquida: {financial['profitability']['net_margin']}%")
        
        print()
        print("👥 PERFORMANCE DAS EQUIPES:")
        team_data = dashboard_data['team_productivity']
        for squad, data in team_data['squads'].items():
            print(f"   {squad}: {data['productivity_score']}% ({data['members']} membros)")
        
        print()
        print("🔧 MÉTRICAS TÉCNICAS:")
        tech = dashboard_data['technical_metrics']
        print(f"   🧪 Cobertura de Testes: {tech['code_quality']['test_coverage']}%")
        print(f"   📊 Uptime: {tech['infrastructure']['uptime_percentage']}%")
        print(f"   ⚡ Tempo de Resposta: {tech['infrastructure']['response_time_p95']}")
        print(f"   🔄 Deploy Frequency: {tech['deployment_metrics']['deployment_frequency']}")
        
        print()
        print("🧠 INSIGHTS DE CRESCIMENTO:")
        growth = dashboard_data['growth_insights']
        print("   📈 Oportunidades:")
        for opportunity in growth['opportunities'][:2]:
            print(f"      {opportunity}")
        
        print("   ⚠️ Riscos:")
        for risk in growth['risks'][:2]:
            print(f"      {risk}")
        
        print("   💡 Recomendações:")
        for recommendation in growth['recommendations'][:2]:
            print(f"      {recommendation}")
        
        print()
        print("✨ TEMPLATES DISPONÍVEIS:")
        print("   📧 Executive Template - Design premium responsivo")
        print("   📱 Mobile Template - Otimizado para smartphones")
        print("   🎨 Customizável - Cores e branding personalizáveis")
        
        print()
        print("🚀 SISTEMA DE AUTOMAÇÃO:")
        print("   📅 Relatórios Diários: 8h00 (operacional)")
        print("   📊 Resumo Semanal: Segundas 9h00 (executivo)")
        print("   📈 Análise Mensal: Dia 1º 10h00 (board)")
        
        print()
        print("🏆 DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📄 Arquivo HTML gerado: {filename}")
        print("🎯 Sistema pronto para uso em produção!")
        
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        return False
    
    return True

def show_features():
    """Mostra as funcionalidades do sistema"""
    print("🚀 FUNCIONALIDADES DO ÁVILA EXECUTIVE DASHBOARD")
    print("=" * 60)
    
    features = [
        "📊 Dashboard Executivo Completo",
        "📧 Templates HTML Premium",
        "🤖 Automação Inteligente",
        "📈 Gráficos Interativos (Plotly)",
        "👥 Análise de Equipes",
        "💰 Métricas Financeiras",
        "🔧 Indicadores Técnicos",
        "🧠 AI Insights",
        "📱 Design Responsivo",
        "⏰ Agendamento Automático",
        "🔐 Segurança e Compliance",
        "📄 Múltiplos Formatos",
        "🎨 Branding Personalizado",
        "📊 KPIs Executivos",
        "⚡ Performance Otimizada"
    ]
    
    for i, feature in enumerate(features, 1):
        print(f"   {i:2d}. {feature}")
    
    print()
    print("🏛️ Desenvolvido por Nicolas Avila - Ávila Framework")
    print("✨ Padrão de excelência em analytics executivos")

async def main():
    """Função principal"""
    print()
    show_features()
    print()
    
    # Menu de demonstração
    while True:
        print("📋 MENU DE DEMONSTRAÇÃO:")
        print("1. 🚀 Executar demonstração completa")
        print("2. 📊 Mostrar funcionalidades")
        print("3. 📄 Ver documentação")
        print("4. ❌ Sair")
        print()
        
        choice = input("Escolha uma opção (1-4): ").strip()
        
        if choice == "1":
            print()
            success = await demo_dashboard()
            if success:
                print("\n🎉 Demonstração executada com sucesso!")
            else:
                print("\n❌ Falha na demonstração")
            print()
        
        elif choice == "2":
            print()
            show_features()
            print()
        
        elif choice == "3":
            readme_path = Path(__file__).parent / "README.md"
            if readme_path.exists():
                print(f"\n📖 Documentação disponível em: {readme_path}")
                print("🔗 Abra o arquivo README.md para ver a documentação completa")
            else:
                print("\n📖 README.md não encontrado")
            print()
        
        elif choice == "4":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    asyncio.run(main())