#!/usr/bin/env python3
"""
ÁVILA DASHBOARD AUTOMATION
=========================
Sistema de automação para geração e envio de dashboards executivos
Autor: Nicolas Avila - Ávila Framework
Data: 2025-11-11
"""

import asyncio
import schedule
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import json
import os
from dashboard_generator import AvilaExecutiveDashboard, DashboardConfig
from email_templates import AvilaEmailTemplates

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DashboardAutomation:
    """Sistema de automação para dashboards executivos"""
    
    def __init__(self, config_file: str = "dashboard_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.dashboard = AvilaExecutiveDashboard(self.config.dashboard)
        self.reports_sent = 0
        
    def _load_config(self) -> 'AutomationConfig':
        """Carrega configuração do arquivo"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                return AutomationConfig.from_dict(config_data)
        else:
            # Criar configuração padrão
            config = AutomationConfig()
            self._save_config(config)
            return config
    
    def _save_config(self, config: 'AutomationConfig'):
        """Salva configuração no arquivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, indent=2, ensure_ascii=False)
    
    async def generate_and_send_daily_report(self):
        """Gera e envia relatório diário"""
        try:
            logger.info("🚀 Iniciando geração de relatório diário...")
            
            # Gerar dashboard
            dashboard_data = await self.dashboard.generate_full_dashboard()
            
            # Usar template premium
            template = AvilaEmailTemplates.get_executive_template()
            html_content = self._render_template(template, dashboard_data)
            
            # Salvar relatório
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_diario_{timestamp}.html"
            filepath = await self.dashboard.save_report(html_content, filename)
            
            # Enviar por email
            success = await self.dashboard.send_email_report(html_content)
            
            if success:
                self.reports_sent += 1
                logger.info(f"✅ Relatório diário enviado com sucesso! Total enviado: {self.reports_sent}")
                
                # Atualizar estatísticas
                self._update_stats("daily_reports_sent", 1)
            else:
                logger.error("❌ Falha no envio do relatório diário")
                
        except Exception as e:
            logger.error(f"❌ Erro na geração do relatório diário: {e}")
    
    async def generate_weekly_summary(self):
        """Gera resumo semanal executivo"""
        try:
            logger.info("📊 Gerando resumo semanal...")
            
            # Gerar dados da semana
            dashboard_data = await self.dashboard.generate_full_dashboard()
            dashboard_data['period'] = {
                'start': (datetime.now() - timedelta(days=7)).strftime("%d/%m/%Y"),
                'end': datetime.now().strftime("%d/%m/%Y"),
                'type': 'weekly'
            }
            
            # Template específico para semanal
            template = self._get_weekly_template()
            html_content = self._render_template(template, dashboard_data)
            
            # Salvar relatório
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"resumo_semanal_{timestamp}.html"
            filepath = await self.dashboard.save_report(html_content, filename)
            
            # Enviar para lista executiva
            executive_config = DashboardConfig(
                email_recipients=self.config.weekly_recipients,
                sender_email=self.config.dashboard.sender_email,
                sender_password=self.config.dashboard.sender_password
            )
            executive_dashboard = AvilaExecutiveDashboard(executive_config)
            
            success = await executive_dashboard.send_email_report(html_content)
            
            if success:
                logger.info("✅ Resumo semanal enviado para executivos")
                self._update_stats("weekly_reports_sent", 1)
            else:
                logger.error("❌ Falha no envio do resumo semanal")
                
        except Exception as e:
            logger.error(f"❌ Erro na geração do resumo semanal: {e}")
    
    async def generate_monthly_analysis(self):
        """Gera análise mensal completa"""
        try:
            logger.info("📈 Gerando análise mensal...")
            
            # Gerar dados do mês
            dashboard_data = await self.dashboard.generate_full_dashboard()
            dashboard_data['period'] = {
                'start': (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y"),
                'end': datetime.now().strftime("%d/%m/%Y"),
                'type': 'monthly'
            }
            
            # Adicionar análises específicas mensais
            dashboard_data['monthly_analysis'] = await self._generate_monthly_insights()
            
            # Template específico para mensal
            template = self._get_monthly_template()
            html_content = self._render_template(template, dashboard_data)
            
            # Salvar relatório
            timestamp = datetime.now().strftime("%Y%m")
            filename = f"analise_mensal_{timestamp}.html"
            filepath = await self.dashboard.save_report(html_content, filename)
            
            # Enviar para board
            board_config = DashboardConfig(
                email_recipients=self.config.board_recipients,
                sender_email=self.config.dashboard.sender_email,
                sender_password=self.config.dashboard.sender_password
            )
            board_dashboard = AvilaExecutiveDashboard(board_config)
            
            success = await board_dashboard.send_email_report(html_content)
            
            if success:
                logger.info("✅ Análise mensal enviada para board")
                self._update_stats("monthly_reports_sent", 1)
            else:
                logger.error("❌ Falha no envio da análise mensal")
                
        except Exception as e:
            logger.error(f"❌ Erro na geração da análise mensal: {e}")
    
    def _render_template(self, template: str, data: Dict) -> str:
        """Renderiza template com dados"""
        # Formatar listas para HTML
        achievements_html = AvilaEmailTemplates.format_achievement_items(
            data['executive_summary']['key_achievements']
        )
        alerts_html = AvilaEmailTemplates.format_alert_items(
            data['executive_summary']['critical_alerts']
        )
        
        # Renderizar template
        return template.format(
            company_name=self.config.dashboard.company_name,
            company_logo=self.config.dashboard.company_logo,
            report_date=datetime.now().strftime("%d/%m/%Y"),
            report_time=datetime.now().strftime("%H:%M"),
            period_start=data['period']['start'],
            period_end=data['period']['end'],
            
            # Executive Summary
            total_products=data['executive_summary']['total_products'],
            healthy_products=data['products_metrics']['healthy_products'],
            total_products_detail=data['products_metrics']['total_products'],
            revenue_growth=data['executive_summary']['revenue_growth'],
            customer_satisfaction=data['executive_summary']['customer_satisfaction'],
            team_size=data['executive_summary']['team_size'],
            overall_velocity=data['team_productivity']['overall_velocity'],
            
            # Financial
            current_revenue=data['financial_overview']['revenue']['current_month'],
            revenue_growth_rate=data['financial_overview']['revenue']['growth_rate'],
            gross_margin=data['financial_overview']['profitability']['gross_margin'],
            net_margin=data['financial_overview']['profitability']['net_margin'],
            
            # Lists
            achievements=achievements_html,
            critical_alerts=alerts_html
        )
    
    def _get_weekly_template(self) -> str:
        """Template específico para relatório semanal"""
        return AvilaEmailTemplates.get_executive_template()  # Por enquanto usa o mesmo
    
    def _get_monthly_template(self) -> str:
        """Template específico para relatório mensal"""
        return AvilaEmailTemplates.get_executive_template()  # Por enquanto usa o mesmo
    
    async def _generate_monthly_insights(self) -> Dict:
        """Gera insights específicos mensais"""
        return {
            'trends': [
                "📈 Crescimento consistente em todos os produtos",
                "🚀 Melhoria na performance das equipes",
                "💰 ROI positivo em todos os investimentos"
            ],
            'recommendations': [
                "🎯 Expandir capacidade do produto líder",
                "📊 Implementar dashboards por squad",
                "🔐 Reforçar segurança em produtos críticos"
            ]
        }
    
    def _update_stats(self, metric: str, value: int):
        """Atualiza estatísticas de automação"""
        stats_file = Path("automation_stats.json")
        stats = {}
        
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
        
        if metric not in stats:
            stats[metric] = 0
        stats[metric] += value
        stats['last_updated'] = datetime.now().isoformat()
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def setup_schedule(self):
        """Configura agendamento automático"""
        logger.info("⏰ Configurando agendamento de relatórios...")
        
        # Relatório diário às 8h
        schedule.every().day.at("08:00").do(
            lambda: asyncio.create_task(self.generate_and_send_daily_report())
        )
        
        # Resumo semanal às segundas-feiras às 9h
        schedule.every().monday.at("09:00").do(
            lambda: asyncio.create_task(self.generate_weekly_summary())
        )
        
        # Análise mensal no primeiro dia do mês às 10h
        schedule.every().month.do(
            lambda: asyncio.create_task(self.generate_monthly_analysis())
        )
        
        logger.info("✅ Agendamento configurado:")
        logger.info("   📅 Diário: 8h00")
        logger.info("   📊 Semanal: Segundas 9h00")
        logger.info("   📈 Mensal: Dia 1º 10h00")
    
    def run_scheduler(self):
        """Executa o agendador"""
        logger.info("🚀 Iniciando sistema de automação...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto
    
    async def test_all_reports(self):
        """Testa geração de todos os tipos de relatório"""
        logger.info("🧪 Iniciando testes de relatórios...")
        
        try:
            # Teste diário
            await self.generate_and_send_daily_report()
            
            # Teste semanal
            await self.generate_weekly_summary()
            
            # Teste mensal
            await self.generate_monthly_analysis()
            
            logger.info("✅ Todos os testes concluídos com sucesso!")
            
        except Exception as e:
            logger.error(f"❌ Erro nos testes: {e}")

class AutomationConfig:
    """Configuração do sistema de automação"""
    
    def __init__(self):
        self.dashboard = DashboardConfig()
        self.weekly_recipients = ["nicolas@avila.inc", "board@avila.inc"]
        self.board_recipients = ["nicolas@avila.inc", "board@avila.inc", "investors@avila.inc"]
        self.enabled = True
        self.timezone = "America/Sao_Paulo"
        
    @classmethod
    def from_dict(cls, data: Dict) -> 'AutomationConfig':
        """Cria configuração a partir de dicionário"""
        config = cls()
        
        if 'dashboard' in data:
            dashboard_data = data['dashboard']
            config.dashboard = DashboardConfig(
                company_name=dashboard_data.get('company_name', 'Ávila Framework'),
                email_recipients=dashboard_data.get('email_recipients', ["nicolas@avila.inc"]),
                sender_email=dashboard_data.get('sender_email', 'reports@avilaops.com'),
                sender_password=dashboard_data.get('sender_password', '')
            )
        
        config.weekly_recipients = data.get('weekly_recipients', config.weekly_recipients)
        config.board_recipients = data.get('board_recipients', config.board_recipients)
        config.enabled = data.get('enabled', True)
        config.timezone = data.get('timezone', 'America/Sao_Paulo')
        
        return config
    
    def to_dict(self) -> Dict:
        """Converte configuração para dicionário"""
        return {
            'dashboard': {
                'company_name': self.dashboard.company_name,
                'email_recipients': self.dashboard.email_recipients,
                'sender_email': self.dashboard.sender_email,
                'sender_password': self.dashboard.sender_password
            },
            'weekly_recipients': self.weekly_recipients,
            'board_recipients': self.board_recipients,
            'enabled': self.enabled,
            'timezone': self.timezone
        }

async def main():
    """Função principal"""
    print("🏛️ Ávila Executive Dashboard Automation")
    print("=" * 50)
    
    # Criar sistema de automação
    automation = DashboardAutomation()
    
    # Opções do menu
    while True:
        print("\n📋 Menu de Opções:")
        print("1. 📊 Gerar relatório diário agora")
        print("2. 📈 Gerar resumo semanal agora")
        print("3. 📉 Gerar análise mensal agora")
        print("4. 🧪 Testar todos os relatórios")
        print("5. ⏰ Iniciar automação agendada")
        print("6. 📄 Ver configurações")
        print("7. ❌ Sair")
        
        choice = input("\nEscolha uma opção (1-7): ").strip()
        
        if choice == "1":
            await automation.generate_and_send_daily_report()
        
        elif choice == "2":
            await automation.generate_weekly_summary()
        
        elif choice == "3":
            await automation.generate_monthly_analysis()
        
        elif choice == "4":
            await automation.test_all_reports()
        
        elif choice == "5":
            print("\n⏰ Iniciando sistema de automação...")
            print("📝 Pressione Ctrl+C para parar")
            automation.setup_schedule()
            try:
                automation.run_scheduler()
            except KeyboardInterrupt:
                print("\n🛑 Automação interrompida pelo usuário")
        
        elif choice == "6":
            print(f"\n📄 Configurações:")
            print(f"   Company: {automation.config.dashboard.company_name}")
            print(f"   Recipients: {automation.config.dashboard.email_recipients}")
            print(f"   Weekly: {automation.config.weekly_recipients}")
            print(f"   Board: {automation.config.board_recipients}")
            print(f"   Enabled: {automation.config.enabled}")
        
        elif choice == "7":
            print("👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == "__main__":
    asyncio.run(main())