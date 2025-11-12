"""
ÁVILA REPORT FRAMEWORK - SISTEMA DE LOGS
========================================
Sistema unificado de logging com integração Sentry
"""

import logging
import logging.handlers
import os
from datetime import datetime
from config import LOG_CONFIG, SENTRY_CONFIG
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

class AvilaLogger:
    """Sistema de logging personalizado para Ávila Framework"""

    def __init__(self):
        self.logger = logging.getLogger("AvilaReports")
        self.setup_logger()
        self.setup_sentry()

    def setup_logger(self):
        """Configurar logging básico"""
        self.logger.setLevel(getattr(logging, LOG_CONFIG["level"]))

        # Limpar handlers existentes
        self.logger.handlers.clear()

        # Formatter
        formatter = logging.Formatter(LOG_CONFIG["format"])

        # File handler com rotação
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_CONFIG["file"],
            maxBytes=LOG_CONFIG["max_size_mb"] * 1024 * 1024,
            backupCount=LOG_CONFIG["backup_count"],
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def setup_sentry(self):
        """Configurar Sentry para monitoramento de erros"""
        if not SENTRY_CONFIG["enabled"]:
            return

        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )

        try:
            sentry_sdk.init(
                dsn=SENTRY_CONFIG["dsn"],
                integrations=[sentry_logging],
                environment=SENTRY_CONFIG["environment"],
                release=SENTRY_CONFIG["release"],
                traces_sample_rate=0.1
            )
            self.logger.info("✅ Sentry inicializado com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️ Falha ao inicializar Sentry: {e}")

    def info(self, message, extra=None):
        """Log de informação"""
        self.logger.info(message, extra=extra)

    def success(self, message, extra=None):
        """Log de sucesso"""
        self.logger.info(f"✅ {message}", extra=extra)

    def warning(self, message, extra=None):
        """Log de aviso"""
        self.logger.warning(f"⚠️ {message}", extra=extra)

    def error(self, message, extra=None):
        """Log de erro"""
        self.logger.error(f"❌ {message}", extra=extra)

    def critical(self, message, extra=None):
        """Log crítico"""
        self.logger.critical(f"🚨 {message}", extra=extra)

    def report_action(self, action, report_type, format_type, status="started"):
        """Log específico para ações de relatório"""
        emoji = "🚀" if status == "started" else "✅" if status == "completed" else "❌"
        message = f"{emoji} Relatório {action}: {report_type} ({format_type}) - {status}"

        extra = {
            "action": action,
            "report_type": report_type,
            "format_type": format_type,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

        if status == "error":
            self.error(message, extra=extra)
        else:
            self.info(message, extra=extra)

    def export_action(self, export_type, destination, status="started"):
        """Log específico para exportações"""
        emoji = "📤" if status == "started" else "✅" if status == "completed" else "❌"
        message = f"{emoji} Exportação {export_type}: {destination} - {status}"

        extra = {
            "export_type": export_type,
            "destination": destination,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

        if status == "error":
            self.error(message, extra=extra)
        else:
            self.info(message, extra=extra)

    def get_recent_logs(self, lines=100):
        """Retorna logs recentes para visualização na GUI"""
        try:
            with open(LOG_CONFIG["file"], 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        except Exception as e:
            return f"Erro ao ler logs: {e}"

    def clear_old_logs(self, days_to_keep=30):
        """Remove logs antigos"""
        try:
            import glob
            log_dir = os.path.dirname(LOG_CONFIG["file"])
            pattern = os.path.join(log_dir, "avila_reports_*.log*")

            cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)

            for log_file in glob.glob(pattern):
                if os.path.getmtime(log_file) < cutoff_time:
                    os.remove(log_file)
                    self.info(f"🗑️ Log antigo removido: {log_file}")

        except Exception as e:
            self.error(f"Erro ao limpar logs antigos: {e}")

# Instância global do logger
logger = AvilaLogger()

# Funções de conveniência
def log_info(message, extra=None):
    logger.info(message, extra)

def log_success(message, extra=None):
    logger.success(message, extra)

def log_warning(message, extra=None):
    logger.warning(message, extra)

def log_error(message, extra=None):
    logger.error(message, extra)

def log_critical(message, extra=None):
    logger.critical(message, extra)

def log_report_action(action, report_type, format_type, status="started"):
    logger.report_action(action, report_type, format_type, status)

def log_export_action(export_type, destination, status="started"):
    logger.export_action(export_type, destination, status)

# Log inicial
log_success("Sistema de logging inicializado")
