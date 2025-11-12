#!/usr/bin/env python3
"""
ÁVILA FRAMEWORK - ENVIRONMENT CONFIGURATION MANAGER
=================================================
Gerenciador de configurações usando variáveis de ambiente
Autor: Nicolas Avila - Ávila Framework
Data: 2025-11-11
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv
import json
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DashboardEnvironmentConfig:
    """Configuração do dashboard usando variáveis de ambiente"""
    
    # Email Configuration
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    sender_email: str = ""
    sender_password: str = ""
    
    # Recipients
    email_recipients: List[str] = field(default_factory=list)
    weekly_recipients: List[str] = field(default_factory=list)
    board_recipients: List[str] = field(default_factory=list)
    
    # Company Info
    company_name: str = "Ávila Framework"
    company_logo: str = "https://avatars.githubusercontent.com/avilaops"
    primary_color: str = "#1d1d1f"
    secondary_color: str = "#0066cc"
    accent_color: str = "#007aff"
    
    # Paths
    workspace_path: str = ""
    output_path: str = "./output"
    backup_path: str = "./output/backup"
    
    # Features
    enable_charts: bool = True
    enable_ai_insights: bool = True
    enable_mobile_template: bool = True
    enable_dark_mode: bool = False
    enable_real_time_data: bool = True
    
    # Monitoring
    log_level: str = "INFO"
    alert_on_failure: bool = True
    metrics_collection: bool = True
    
    # Email Settings
    subject_prefix: str = "🏛️ Ávila Framework"
    email_priority: str = "high"
    read_receipt: bool = False
    delivery_notification: bool = True
    
    # Backup
    backup_enabled: bool = True
    retention_days: int = 30
    
    # Timezone
    timezone: str = "America/Sao_Paulo"
    
    # Schedule
    daily_report_time: str = "08:00"
    weekly_summary_time: str = "monday_09:00"
    monthly_analysis_time: str = "first_day_10:00"
    
    def __post_init__(self):
        """Carrega configurações do ambiente após inicialização"""
        self.load_from_env()
    
    def load_from_env(self) -> None:
        """Carrega configurações das variáveis de ambiente"""
        try:
            # Tentar carregar .env file
            env_file = Path(__file__).parent / '.env'
            if env_file.exists():
                load_dotenv(env_file)
                logger.info(f"✅ Arquivo .env carregado: {env_file}")
            else:
                logger.warning(f"⚠️ Arquivo .env não encontrado: {env_file}")
            
            # Email Configuration
            self.smtp_server = os.getenv('SMTP_SERVER', self.smtp_server)
            self.smtp_port = int(os.getenv('SMTP_PORT', str(self.smtp_port)))
            self.sender_email = os.getenv('SENDER_EMAIL', self.sender_email)
            self.sender_password = os.getenv('SENDER_PASSWORD', self.sender_password)
            
            # Recipients (convert comma-separated to list)
            recipients_str = os.getenv('EMAIL_RECIPIENTS', '')
            if recipients_str:
                self.email_recipients = [email.strip() for email in recipients_str.split(',')]
            
            weekly_str = os.getenv('WEEKLY_RECIPIENTS', '')
            if weekly_str:
                self.weekly_recipients = [email.strip() for email in weekly_str.split(',')]
            
            board_str = os.getenv('BOARD_RECIPIENTS', '')
            if board_str:
                self.board_recipients = [email.strip() for email in board_str.split(',')]
            
            # Company Info
            self.company_name = os.getenv('COMPANY_NAME', self.company_name)
            self.company_logo = os.getenv('COMPANY_LOGO', self.company_logo)
            self.primary_color = os.getenv('PRIMARY_COLOR', self.primary_color)
            self.secondary_color = os.getenv('SECONDARY_COLOR', self.secondary_color)
            self.accent_color = os.getenv('ACCENT_COLOR', self.accent_color)
            
            # Paths
            self.workspace_path = os.getenv('WORKSPACE_PATH', self.workspace_path)
            self.output_path = os.getenv('OUTPUT_PATH', self.output_path)
            self.backup_path = os.getenv('BACKUP_PATH', self.backup_path)
            
            # Features (convert string to bool)
            self.enable_charts = self._str_to_bool(os.getenv('ENABLE_CHARTS', str(self.enable_charts)))
            self.enable_ai_insights = self._str_to_bool(os.getenv('ENABLE_AI_INSIGHTS', str(self.enable_ai_insights)))
            self.enable_mobile_template = self._str_to_bool(os.getenv('ENABLE_MOBILE_TEMPLATE', str(self.enable_mobile_template)))
            self.enable_dark_mode = self._str_to_bool(os.getenv('ENABLE_DARK_MODE', str(self.enable_dark_mode)))
            self.enable_real_time_data = self._str_to_bool(os.getenv('ENABLE_REAL_TIME_DATA', str(self.enable_real_time_data)))
            
            # Monitoring
            self.log_level = os.getenv('LOG_LEVEL', self.log_level)
            self.alert_on_failure = self._str_to_bool(os.getenv('ALERT_ON_FAILURE', str(self.alert_on_failure)))
            self.metrics_collection = self._str_to_bool(os.getenv('METRICS_COLLECTION', str(self.metrics_collection)))
            
            # Email Settings
            self.subject_prefix = os.getenv('SUBJECT_PREFIX', self.subject_prefix)
            self.email_priority = os.getenv('EMAIL_PRIORITY', self.email_priority)
            self.read_receipt = self._str_to_bool(os.getenv('READ_RECEIPT', str(self.read_receipt)))
            self.delivery_notification = self._str_to_bool(os.getenv('DELIVERY_NOTIFICATION', str(self.delivery_notification)))
            
            # Backup
            self.backup_enabled = self._str_to_bool(os.getenv('BACKUP_ENABLED', str(self.backup_enabled)))
            self.retention_days = int(os.getenv('RETENTION_DAYS', str(self.retention_days)))
            
            # Timezone
            self.timezone = os.getenv('TIMEZONE', self.timezone)
            
            # Schedule
            self.daily_report_time = os.getenv('DAILY_REPORT_TIME', self.daily_report_time)
            self.weekly_summary_time = os.getenv('WEEKLY_SUMMARY_TIME', self.weekly_summary_time)
            self.monthly_analysis_time = os.getenv('MONTHLY_ANALYSIS_TIME', self.monthly_analysis_time)
            
            # Validar configurações críticas
            self._validate_config()
            
            logger.info("✅ Configurações carregadas das variáveis de ambiente")
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar configurações do ambiente: {e}")
            raise
    
    def _str_to_bool(self, value: str) -> bool:
        """Converte string para boolean"""
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
    
    def _validate_config(self) -> None:
        """Valida configurações críticas"""
        errors = []
        
        if not self.sender_email:
            errors.append("SENDER_EMAIL não configurado")
        
        if not self.email_recipients:
            errors.append("EMAIL_RECIPIENTS não configurado")
        
        if not self.workspace_path:
            errors.append("WORKSPACE_PATH não configurado")
        
        if not Path(self.workspace_path).exists() if self.workspace_path else True:
            errors.append(f"WORKSPACE_PATH não existe: {self.workspace_path}")
        
        if errors:
            error_msg = "Configurações inválidas encontradas:\n" + "\n".join(f"- {error}" for error in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("✅ Configurações validadas com sucesso")
    
    def get_recipients_for_type(self, report_type: str = "daily") -> List[str]:
        """Obtém lista de destinatários baseado no tipo de relatório"""
        if report_type == "weekly":
            return self.weekly_recipients or self.email_recipients
        elif report_type == "board":
            return self.board_recipients or self.email_recipients
        else:
            return self.email_recipients
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário"""
        return {
            'smtp': {
                'server': self.smtp_server,
                'port': self.smtp_port,
                'sender_email': self.sender_email,
                'password_configured': bool(self.sender_password)
            },
            'recipients': {
                'email': self.email_recipients,
                'weekly': self.weekly_recipients,
                'board': self.board_recipients
            },
            'company': {
                'name': self.company_name,
                'logo': self.company_logo,
                'colors': {
                    'primary': self.primary_color,
                    'secondary': self.secondary_color,
                    'accent': self.accent_color
                }
            },
            'paths': {
                'workspace': self.workspace_path,
                'output': self.output_path,
                'backup': self.backup_path
            },
            'features': {
                'charts': self.enable_charts,
                'ai_insights': self.enable_ai_insights,
                'mobile_template': self.enable_mobile_template,
                'dark_mode': self.enable_dark_mode,
                'real_time_data': self.enable_real_time_data
            },
            'monitoring': {
                'log_level': self.log_level,
                'alert_on_failure': self.alert_on_failure,
                'metrics_collection': self.metrics_collection
            },
            'email_settings': {
                'subject_prefix': self.subject_prefix,
                'priority': self.email_priority,
                'read_receipt': self.read_receipt,
                'delivery_notification': self.delivery_notification
            },
            'backup': {
                'enabled': self.backup_enabled,
                'retention_days': self.retention_days
            },
            'schedule': {
                'daily_report_time': self.daily_report_time,
                'weekly_summary_time': self.weekly_summary_time,
                'monthly_analysis_time': self.monthly_analysis_time
            },
            'timezone': self.timezone
        }
    
    def save_to_json(self, filepath: Optional[Path] = None) -> Path:
        """Salva configuração atual em arquivo JSON"""
        if filepath is None:
            filepath = Path(__file__).parent / 'current_config.json'
        
        config_data = self.to_dict()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Configuração salva em: {filepath}")
        return filepath
    
    def print_summary(self) -> None:
        """Imprime resumo das configurações"""
        print("\n🔧 CONFIGURAÇÃO DO DASHBOARD EXECUTIVO")
        print("=" * 50)
        print(f"📧 Email: {self.sender_email}")
        print(f"👥 Destinatários: {len(self.email_recipients)} configurados")
        print(f"🏢 Empresa: {self.company_name}")
        print(f"📁 Workspace: {self.workspace_path}")
        print(f"🎨 Features: Charts={self.enable_charts}, AI={self.enable_ai_insights}")
        print(f"🕒 Timezone: {self.timezone}")
        print(f"📊 Log Level: {self.log_level}")
        print("=" * 50)

def load_dashboard_config() -> DashboardEnvironmentConfig:
    """Carrega configuração do dashboard"""
    try:
        config = DashboardEnvironmentConfig()
        return config
    except Exception as e:
        logger.error(f"❌ Falha ao carregar configuração: {e}")
        raise

def test_configuration() -> None:
    """Testa a configuração atual"""
    print("🧪 TESTE DE CONFIGURAÇÃO")
    print("=" * 30)
    
    try:
        config = load_dashboard_config()
        config.print_summary()
        
        # Salvar configuração de teste
        config.save_to_json()
        
        print("\n✅ Configuração carregada e validada com sucesso!")
        
        # Testar diferentes tipos de destinatários
        print(f"\n📧 DESTINATÁRIOS POR TIPO:")
        print(f"Daily: {config.get_recipients_for_type('daily')}")
        print(f"Weekly: {config.get_recipients_for_type('weekly')}")
        print(f"Board: {config.get_recipients_for_type('board')}")
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_configuration()