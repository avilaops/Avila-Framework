"""
ÁVILA REPORT FRAMEWORK - EXPORTADOR EMAIL
==========================================
Sistema de envio de relatórios via email
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import EMAIL_CONFIG, get_timestamp, REPORT_TYPES
from logger import log_export_action

class EmailExporter:
    """Exportador para Email"""

    def __init__(self):
        self.smtp_server = EMAIL_CONFIG["smtp_server"]
        self.smtp_port = EMAIL_CONFIG["smtp_port"]
        self.from_email = EMAIL_CONFIG["from_email"]
        self.to_email = EMAIL_CONFIG["to_email"]
        self.password = EMAIL_CONFIG.get("password", "")

    def export(self, data, report_type, attachments=None, format_type="html"):
        """Enviar relatório via email"""
        try:
            log_export_action("email", self.to_email, "started")

            # Verificar senha
            if not self.password:
                self.password = self._get_email_password()

            # Gerar conteúdo do email
            subject = self._generate_subject(report_type)
            body = self._generate_body(data, report_type, format_type)

            # Criar mensagem
            msg = self._create_message(subject, body, format_type)

            # Adicionar anexos
            if attachments:
                self._add_attachments(msg, attachments)

            # Enviar email
            self._send_email(msg)

            log_export_action("email", self.to_email, "completed")
            return f"Email enviado para {self.to_email}"

        except Exception as e:
            log_export_action("email", self.to_email, "error")
            raise e

    def _get_email_password(self):
        """Obter senha do email (pode ser melhorado com keyring)"""
        # Por segurança, não armazenar senha no código
        # Em produção, usar variáveis de ambiente ou keyring
        import getpass
        return getpass.getpass("Digite a senha do email: ")

    def _generate_subject(self, report_type):
        """Gerar assunto do email"""
        report_info = REPORT_TYPES.get(report_type, REPORT_TYPES["custom"])
        timestamp = get_timestamp("date")

        return EMAIL_CONFIG["subject_template"].format(
            report_type=report_info['name'],
            timestamp=timestamp
        )

    def _generate_body(self, data, report_type, format_type):
        """Gerar corpo do email"""
        if format_type == "html":
            return self._generate_html_body(data, report_type)
        else:
            return self._generate_text_body(data, report_type)

    def _generate_html_body(self, data, report_type):
        """Gerar corpo HTML do email"""
        report_info = REPORT_TYPES.get(report_type, REPORT_TYPES["custom"])
        timestamp = get_timestamp("br")

        # Gerar resumo das métricas
        metrics_html = ""
        if 'metrics' in data and data['metrics']:
            metrics_html = "<h3>📈 Métricas Principais</h3><ul>"
            for metric_name, metric_value in data['metrics'].items():
                metrics_html += f"<li><strong>{metric_name}:</strong> {metric_value}</li>"
            metrics_html += "</ul>"

        # Conteúdo específico por tipo de relatório
        specific_content = ""
        if report_type == "financial":
            specific_content = self._generate_financial_html_content(data)
        elif report_type == "projects":
            specific_content = self._generate_projects_html_content(data)
        elif report_type == "performance":
            specific_content = self._generate_performance_html_content(data)

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Ávila Framework - Relatório</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #2E3440, #5E81AC);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .info-box {{
            background: #f8f9fa;
            border-left: 4px solid #5E81AC;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .metrics {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }}
        .footer {{
            background: #f1f3f4;
            padding: 15px;
            text-align: center;
            border-radius: 8px;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏛️ Ávila Framework</h1>
        <h2>{report_info['icon']} {report_info['name']}</h2>
        <p>📅 {timestamp}</p>
    </div>

    <div class="info-box">
        <h3>📊 Resumo Executivo</h3>
        <p>{data.get('summary', 'Resumo não disponível')}</p>
    </div>

    <div class="metrics">
        {metrics_html}
    </div>

    {specific_content}

    <div class="info-box">
        <h3>📋 Detalhes</h3>
        <p>{data.get('details', 'Detalhes não disponíveis')}</p>
    </div>

    <div class="footer">
        <p><strong>Ávila Report Framework v1.0</strong></p>
        <p>AvilaOps Team | nicolas@avila.inc</p>
        <p>🔗 <a href="https://github.com/avilaops/Avila-Framework">GitHub Repository</a></p>
        <p><em>Relatório gerado automaticamente em {timestamp}</em></p>
    </div>
</body>
</html>"""

        return html_body

    def _generate_financial_html_content(self, data):
        """Gerar conteúdo HTML específico para relatório financeiro"""
        return f"""
    <div class="info-box">
        <h3>💰 Análise Financeira</h3>
        <table>
            <tr><th>Item</th><th>Valor</th></tr>
            <tr><td>Total Receitas</td><td>{data.get('receitas_total', 'N/A')}</td></tr>
            <tr><td>Total Despesas</td><td>{data.get('despesas_total', 'N/A')}</td></tr>
            <tr><td>Resultado Líquido</td><td>{data.get('resultado', 'N/A')}</td></tr>
            <tr><td>Margem de Lucro</td><td>{data.get('margem', 'N/A')}</td></tr>
        </table>
    </div>"""

    def _generate_projects_html_content(self, data):
        """Gerar conteúdo HTML específico para relatório de projetos"""
        return f"""
    <div class="info-box">
        <h3>🏗️ Status dos Projetos</h3>
        <table>
            <tr><th>Status</th><th>Quantidade</th></tr>
            <tr><td>Em Andamento</td><td>{data.get('projetos_andamento', 'N/A')}</td></tr>
            <tr><td>Concluídos</td><td>{data.get('projetos_concluidos', 'N/A')}</td></tr>
            <tr><td>Atrasados</td><td>{data.get('projetos_atrasados', 'N/A')}</td></tr>
        </table>
    </div>"""

    def _generate_performance_html_content(self, data):
        """Gerar conteúdo HTML específico para relatório de performance"""
        return f"""
    <div class="info-box">
        <h3>🚀 Indicadores de Performance</h3>
        <table>
            <tr><th>Indicador</th><th>Score</th></tr>
            <tr><td>Eficiência</td><td>{data.get('score_eficiencia', 'N/A')}</td></tr>
            <tr><td>Qualidade</td><td>{data.get('score_qualidade', 'N/A')}</td></tr>
            <tr><td>Produtividade</td><td>{data.get('score_produtividade', 'N/A')}</td></tr>
        </table>
    </div>"""

    def _generate_text_body(self, data, report_type):
        """Gerar corpo de texto simples do email"""
        report_info = REPORT_TYPES.get(report_type, REPORT_TYPES["custom"])
        timestamp = get_timestamp("br")

        summary = data.get('summary', 'Resumo não disponível')

        body = EMAIL_CONFIG["body_template"].format(
            report_type=report_info['name'],
            timestamp=timestamp,
            format="Email HTML",
            summary=summary
        )

        return body

    def _create_message(self, subject, body, format_type):
        """Criar mensagem de email"""
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = subject

        if format_type == "html":
            msg.attach(MIMEText(body, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

        return msg

    def _add_attachments(self, msg, attachments):
        """Adicionar anexos ao email"""
        for file_path in attachments:
            if os.path.isfile(file_path):
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)

                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file_path)}'
                )

                msg.attach(part)

    def _send_email(self, msg):
        """Enviar email via SMTP"""
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.from_email, self.password)
        text = msg.as_string()
        server.sendmail(self.from_email, self.to_email, text)
        server.quit()

    def send_test_email(self):
        """Enviar email de teste"""
        test_data = {
            'summary': 'Este é um teste do sistema de email do Ávila Report Framework.',
            'details': 'Teste realizado com sucesso. Sistema operacional.',
            'metrics': {
                'Status Sistema': '✅ Operacional',
                'Teste Email': '✅ Sucesso'
            }
        }

        return self.export(test_data, 'custom', None, 'html')

    def send_quick_notification(self, title, message, urgency="normal"):
        """Enviar notificação rápida"""
        urgency_colors = {
            "low": "#28a745",
            "normal": "#007bff",
            "high": "#fd7e14",
            "critical": "#dc3545"
        }

        color = urgency_colors.get(urgency, "#007bff")
        timestamp = get_timestamp("br")

        html_notification = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .notification {{
            border-left: 4px solid {color};
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
        }}
        .header {{ color: {color}; font-weight: bold; font-size: 18px; }}
    </style>
</head>
<body>
    <div class="notification">
        <div class="header">🏛️ Ávila Framework - {title}</div>
        <p>{message}</p>
        <small>📅 {timestamp} | 🤖 Sistema: Ávila Report Framework</small>
    </div>
</body>
</html>"""

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg['Subject'] = f"[Ávila] {title}"
        msg.attach(MIMEText(html_notification, 'html', 'utf-8'))

        self._send_email(msg)
        log_export_action("email_notification", f"{title} - {urgency}", "completed")

        return f"Notificação enviada: {title}"
