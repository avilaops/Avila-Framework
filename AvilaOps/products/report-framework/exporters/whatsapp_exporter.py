"""
ÁVILA REPORT FRAMEWORK - EXPORTADOR WHATSAPP
============================================
Sistema de envio de relatórios via WhatsApp
"""

import webbrowser
import urllib.parse
from datetime import datetime
from config import WHATSAPP_CONFIG, get_timestamp
from logger import log_export_action

class WhatsAppExporter:
    """Exportador para WhatsApp"""

    def __init__(self):
        self.phone = WHATSAPP_CONFIG["phone_number"]
        self.api_url = WHATSAPP_CONFIG["api_url"]

    def export(self, data, report_type, format_type="resumo"):
        """Enviar relatório via WhatsApp"""
        try:
            log_export_action("whatsapp", self.phone, "started")

            # Gerar mensagem
            message = self._generate_whatsapp_message(data, report_type, format_type)

            # Enviar via WhatsApp Web
            self._send_whatsapp_message(message)

            log_export_action("whatsapp", self.phone, "completed")
            return f"Mensagem enviada para {self.phone}"

        except Exception as e:
            log_export_action("whatsapp", self.phone, "error")
            raise e

    def _generate_whatsapp_message(self, data, report_type, format_type):
        """Gerar mensagem formatada para WhatsApp"""
        from config import REPORT_TYPES

        report_info = REPORT_TYPES.get(report_type, REPORT_TYPES["custom"])
        timestamp = get_timestamp("br")

        if format_type == "resumo":
            message = self._generate_summary_message(data, report_info, timestamp)
        elif format_type == "detalhado":
            message = self._generate_detailed_message(data, report_info, timestamp)
        else:
            message = self._generate_custom_message(data, report_info, timestamp, format_type)

        return message

    def _generate_summary_message(self, data, report_info, timestamp):
        """Gerar mensagem resumida"""
        message = f"""🏛️ *Ávila Framework - Relatório*

{report_info['icon']} *{report_info['name']}*
📅 {timestamp}

📊 *RESUMO EXECUTIVO*
{data.get('summary', 'Resumo não disponível')}

"""

        # Adicionar métricas principais
        if 'metrics' in data and data['metrics']:
            message += "📈 *MÉTRICAS PRINCIPAIS*\n"
            for metric_name, metric_value in list(data['metrics'].items())[:3]:  # Máximo 3 métricas
                message += f"• {metric_name}: {metric_value}\n"
            message += "\n"

        # Adicionar seção específica por tipo
        if report_info['name'] == "Relatório Financeiro":
            message += f"""💰 *FINANCEIRO*
• Total Receitas: {data.get('receitas_total', 'N/A')}
• Total Despesas: {data.get('despesas_total', 'N/A')}
• Resultado: {data.get('resultado', 'N/A')}

"""
        elif report_info['name'] == "Relatório de Projetos":
            message += f"""🏗️ *PROJETOS*
• Em Andamento: {data.get('projetos_andamento', 'N/A')}
• Concluídos: {data.get('projetos_concluidos', 'N/A')}
• Atrasados: {data.get('projetos_atrasados', 'N/A')}

"""
        elif report_info['name'] == "Relatório de Performance":
            message += f"""🚀 *PERFORMANCE*
• Eficiência: {data.get('score_eficiencia', 'N/A')}
• Qualidade: {data.get('score_qualidade', 'N/A')}
• Produtividade: {data.get('score_produtividade', 'N/A')}

"""

        message += f"""📋 *INFORMAÇÕES*
Sistema: Ávila Report Framework
Responsável: AvilaOps Team

_Relatório gerado automaticamente_"""

        return message

    def _generate_detailed_message(self, data, report_info, timestamp):
        """Gerar mensagem detalhada"""
        message = f"""🏛️ *Ávila Framework - Relatório Detalhado*

{report_info['icon']} *{report_info['name']}*
📅 {timestamp}
🔄 Frequência: {report_info['frequency']}

📊 *RESUMO EXECUTIVO*
{data.get('summary', 'Resumo não disponível')}

📈 *MÉTRICAS COMPLETAS*
"""

        # Todas as métricas
        if 'metrics' in data:
            for metric_name, metric_value in data['metrics'].items():
                message += f"• {metric_name}: {metric_value}\n"

        message += f"""
📋 *DETALHES*
{data.get('details', 'Detalhes não disponíveis')}

🔗 *ACESSO COMPLETO*
Para mais detalhes, acesse:
• Dashboard Obsidian
• Repositório GitHub
• Relatórios Excel/PDF

_Gerado por Ávila Report Framework v1.0_"""

        return message

    def _generate_custom_message(self, data, report_info, timestamp, format_type):
        """Gerar mensagem personalizada"""
        message = f"""🏛️ *Ávila Framework*

{report_info['icon']} *{report_info['name']}*
📅 {timestamp}

{data.get('custom_message', 'Mensagem personalizada')}

_Ávila Report Framework_"""

        return message

    def _send_whatsapp_message(self, message):
        """Enviar mensagem via WhatsApp Web"""
        # Codificar mensagem para URL
        encoded_message = urllib.parse.quote(message)

        # Remover caracteres especiais do número
        clean_phone = self.phone.replace('+', '').replace('-', '').replace(' ', '')

        # URL do WhatsApp Web
        whatsapp_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"

        # Abrir no navegador
        webbrowser.open(whatsapp_url)

        return whatsapp_url

    def send_test_message(self):
        """Enviar mensagem de teste"""
        test_data = {
            'summary': 'Teste de conectividade do Ávila Report Framework',
            'metrics': {
                'Status': '✅ Operacional',
                'Teste': 'Sucesso'
            }
        }

        return self.export(test_data, 'custom', 'resumo')

    def send_quick_alert(self, title, message, urgency="normal"):
        """Enviar alerta rápido"""
        urgency_emojis = {
            "low": "ℹ️",
            "normal": "📢",
            "high": "⚠️",
            "critical": "🚨"
        }

        emoji = urgency_emojis.get(urgency, "📢")
        timestamp = get_timestamp("br")

        alert_message = f"""{emoji} *Ávila Framework - Alerta*

*{title}*

{message}

📅 {timestamp}
🤖 Sistema: Ávila Report Framework"""

        encoded_message = urllib.parse.quote(alert_message)
        clean_phone = self.phone.replace('+', '').replace('-', '').replace(' ', '')
        whatsapp_url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"

        webbrowser.open(whatsapp_url)
        log_export_action("whatsapp_alert", f"{title} - {urgency}", "completed")

        return whatsapp_url
