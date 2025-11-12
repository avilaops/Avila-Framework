"""
ÁVILA REPORT FRAMEWORK
======================
Framework completo de relatórios corporativos com múltiplas saídas

Desenvolvido por: AvilaOps Team
Versão: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "AvilaOps Team"
__email__ = "nicolas@avila.inc"

# Importações principais
from .config import *
from .logger import logger

# Exportadores
from .exporters.markdown_exporter import MarkdownExporter
from .exporters.excel_exporter import ExcelExporter
from .exporters.whatsapp_exporter import WhatsAppExporter
from .exporters.email_exporter import EmailExporter

__all__ = [
    'MarkdownExporter',
    'ExcelExporter',
    'WhatsAppExporter',
    'EmailExporter',
    'logger'
]
