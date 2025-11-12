"""
ÁVILA REPORT FRAMEWORK - CONFIGURAÇÕES
=====================================
Configurações centralizadas para o sistema de relatórios
"""

import os
from datetime import datetime

# =============================================================================
# CONFIGURAÇÕES BÁSICAS
# =============================================================================
APP_NAME = "Ávila Report Framework"
APP_VERSION = "1.0.0"
APP_AUTHOR = "AvilaOps Team"

# Diretórios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Criar diretórios se não existirem
for directory in [LOGS_DIR, REPORTS_DIR, EXPORTS_DIR, ASSETS_DIR]:
    os.makedirs(directory, exist_ok=True)

# =============================================================================
# CONFIGURAÇÕES DE COMUNICAÇÃO
# =============================================================================

# WhatsApp
WHATSAPP_CONFIG = {
    "enabled": True,
    "phone_number": "+5517997811471",
    "api_url": "https://api.whatsapp.com/send",  # Pode ser substituído por API do WhatsApp Business
    "message_template": "🏛️ *Ávila Framework - Relatório*\n\n{content}\n\n📊 Gerado em: {timestamp}"
}

# Email
EMAIL_CONFIG = {
    "enabled": True,
    "smtp_server": "smtp.gmail.com",  # Configurar conforme provedor
    "smtp_port": 587,
    "from_email": "reports@avilaops.com",  # Email remetente
    "to_email": "nicolas@avila.inc",
    "password": "",  # Será solicitada na primeira execução
    "subject_template": "[Ávila Framework] Relatório - {report_type} - {timestamp}",
    "body_template": """
    Olá Nicolas,

    Segue em anexo o relatório solicitado:

    📊 Tipo: {report_type}
    📅 Data/Hora: {timestamp}
    📁 Formato: {format}

    {summary}

    Atenciosamente,
    Ávila Report Framework
    """
}

# =============================================================================
# MONITORAMENTO E LOGS
# =============================================================================

# Sentry
SENTRY_CONFIG = {
    "enabled": True,
    "dsn": "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",
    "environment": "production",
    "release": APP_VERSION
}

# Logs
LOG_CONFIG = {
    "level": "INFO",
    "format": "[%(asctime)s] [%(levelname)s] %(message)s",
    "file": os.path.join(LOGS_DIR, f"avila_reports_{datetime.now().strftime('%Y%m%d')}.log"),
    "max_size_mb": 10,
    "backup_count": 5
}

# =============================================================================
# TIPOS DE RELATÓRIOS
# =============================================================================

REPORT_TYPES = {
    "daily": {
        "name": "Relatório Diário",
        "description": "Resumo das atividades do dia",
        "icon": "📅",
        "frequency": "Diário"
    },
    "weekly": {
        "name": "Relatório Semanal",
        "description": "Consolidado da semana",
        "icon": "📊",
        "frequency": "Semanal"
    },
    "monthly": {
        "name": "Relatório Mensal",
        "description": "Análise mensal completa",
        "icon": "📈",
        "frequency": "Mensal"
    },
    "projects": {
        "name": "Relatório de Projetos",
        "description": "Status dos projetos ativos",
        "icon": "🏗️",
        "frequency": "Sob demanda"
    },
    "financial": {
        "name": "Relatório Financeiro",
        "description": "Análise financeira",
        "icon": "💰",
        "frequency": "Mensal"
    },
    "performance": {
        "name": "Relatório de Performance",
        "description": "Métricas de desempenho",
        "icon": "🚀",
        "frequency": "Semanal"
    },
    "governance": {
        "name": "Relatório de Governança",
        "description": "Compliance e governança",
        "icon": "🏛️",
        "frequency": "Trimestral"
    },
    "custom": {
        "name": "Relatório Personalizado",
        "description": "Relatório customizado",
        "icon": "⚙️",
        "frequency": "Sob demanda"
    }
}

# =============================================================================
# FORMATOS DE EXPORTAÇÃO
# =============================================================================

EXPORT_FORMATS = {
    "markdown": {
        "name": "Markdown",
        "extension": ".md",
        "mime_type": "text/markdown",
        "icon": "📝"
    },
    "excel": {
        "name": "Excel",
        "extension": ".xlsx",
        "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "icon": "📊"
    },
    "pdf": {
        "name": "PDF",
        "extension": ".pdf",
        "mime_type": "application/pdf",
        "icon": "📄"
    },
    "html": {
        "name": "HTML",
        "extension": ".html",
        "mime_type": "text/html",
        "icon": "🌐"
    }
}

# =============================================================================
# CONFIGURAÇÕES DA GUI
# =============================================================================

GUI_CONFIG = {
    "title": f"{APP_NAME} v{APP_VERSION}",
    "geometry": "1200x800",
    "min_size": (800, 600),
    "icon_path": os.path.join(ASSETS_DIR, "avila_icon.ico"),
    "theme": {
        "bg_primary": "#2E3440",
        "bg_secondary": "#3B4252",
        "fg_primary": "#ECEFF4",
        "fg_secondary": "#D8DEE9",
        "accent": "#5E81AC",
        "success": "#A3BE8C",
        "warning": "#EBCB8B",
        "error": "#BF616A"
    }
}

# =============================================================================
# FUNÇÕES UTILITÁRIAS
# =============================================================================

def get_timestamp(format_type="full"):
    """Retorna timestamp formatado"""
    now = datetime.now()

    formats = {
        "full": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "filename": now.strftime("%Y%m%d_%H%M%S"),
        "br": now.strftime("%d/%m/%Y %H:%M:%S")
    }

    return formats.get(format_type, formats["full"])

def get_report_filename(report_type, format_ext, timestamp=None):
    """Gera nome do arquivo de relatório"""
    if not timestamp:
        timestamp = get_timestamp("filename")

    return f"avila_report_{report_type}_{timestamp}{format_ext}"

def validate_config():
    """Valida configurações essenciais"""
    errors = []

    # Validar email
    if EMAIL_CONFIG["enabled"] and not EMAIL_CONFIG["to_email"]:
        errors.append("Email de destino não configurado")

    # Validar WhatsApp
    if WHATSAPP_CONFIG["enabled"] and not WHATSAPP_CONFIG["phone_number"]:
        errors.append("Número do WhatsApp não configurado")

    return errors

# Executar validação na importação
config_errors = validate_config()
if config_errors:
    print("⚠️ Avisos de configuração:")
    for error in config_errors:
        print(f"   - {error}")
