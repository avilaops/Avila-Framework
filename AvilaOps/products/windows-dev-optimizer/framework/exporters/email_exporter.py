# coding: utf-8
"""
Script: email_exporter.py
Função: Exportador via email
Autor: Nicolas Avila
Data: 2025-11-11
Projeto: Avila Ops - Windows Dev Optimizer Framework
Descrição: Envio de relatórios por email
"""

import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..core.config import settings

logger = logging.getLogger(__name__)

class EmailExporter:
    """Exportador via email"""
    
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.smtp_username
    
    async def send_analysis_report(
        self, 
        analysis_data: Dict[str, Any], 
        to_emails: List[str],
        subject: str = None,
        attach_files: List[str] = None
    ) -> bool:
        """Envia relatório de análise por email"""
        
        if subject is None:
            timestamp = datetime.now().strftime("%d/%m/%Y")
            subject = f"Windows Dev Optimizer - Relatório de Análise ({timestamp})"
        
        try:
            # Gerar corpo do email
            body = self._generate_analysis_email_body(analysis_data)
            
            # Enviar email
            success = await self._send_email(
                to_emails=to_emails,
                subject=subject,
                body=body,
                attach_files=attach_files or []
            )
            
            if success:
                logger.info(f"Relatório de análise enviado para: {', '.join(to_emails)}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao enviar relatório de análise: {e}")
            return False
    
    async def send_recommendations_report(
        self, 
        recommendations: Dict[str, Any], 
        to_emails: List[str],
        subject: str = None,
        attach_files: List[str] = None
    ) -> bool:
        """Envia relatório de recomendações por email"""
        
        if subject is None:
            timestamp = datetime.now().strftime("%d/%m/%Y")
            subject = f"Windows Dev Optimizer - Recomendações ({timestamp})"
        
        try:
            # Gerar corpo do email
            body = self._generate_recommendations_email_body(recommendations)
            
            # Enviar email
            success = await self._send_email(
                to_emails=to_emails,
                subject=subject,
                body=body,
                attach_files=attach_files or []
            )
            
            if success:
                logger.info(f"Relatório de recomendações enviado para: {', '.join(to_emails)}")
            
            return success
            
        except Exception as e:
            logger.error(f"Erro ao enviar relatório de recomendações: {e}")
            return False
    
    async def _send_email(
        self, 
        to_emails: List[str], 
        subject: str, 
        body: str, 
        attach_files: List[str] = None
    ) -> bool:
        """Envia email via SMTP"""
        
        if not self.smtp_server or not self.smtp_username or not self.smtp_password:
            logger.error("Configurações SMTP não encontradas")
            return False
        
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            
            # Adicionar corpo
            msg.attach(MIMEText(body, 'html'))
            
            # Adicionar anexos
            if attach_files:
                for file_path in attach_files:
                    if Path(file_path).exists():
                        self._attach_file(msg, file_path)
            
            # Configurar servidor SMTP
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.from_email, to_emails, msg.as_string())
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Anexa arquivo ao email"""
        
        try:
            file_path = Path(file_path)
            
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.name}',
            )
            
            msg.attach(part)
            
        except Exception as e:
            logger.warning(f"Erro ao anexar arquivo {file_path}: {e}")
    
    def _generate_analysis_email_body(self, analysis_data: Dict[str, Any]) -> str:
        """Gera corpo HTML do email de análise"""
        
        timestamp = analysis_data.get("timestamp", datetime.now().isoformat())
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #366092; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin: 20px 0; }}
        .stats {{ display: flex; flex-wrap: wrap; gap: 15px; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; min-width: 200px; }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #366092; }}
        .stat-label {{ color: #666; }}
        .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #366092; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🖥️ Windows Dev Optimizer</h1>
        <p>Relatório de Análise do Sistema</p>
        <p>{timestamp}</p>
    </div>
    
    <div class="content">
        <div class="section">
            <h2>📊 Resumo Executivo</h2>
            <div class="stats">
"""
        
        # Estatísticas do sistema
        if "system_info" in analysis_data and "error" not in analysis_data.get("system_info", {}):
            sys_info = analysis_data["system_info"]
            html += f"""
                <div class="stat-card">
                    <div class="stat-number">{sys_info.get('memory_total_gb', 'N/A')} GB</div>
                    <div class="stat-label">Memória Total</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{sys_info.get('memory_available_gb', 'N/A')} GB</div>
                    <div class="stat-label">Memória Disponível</div>
                </div>
"""
        
        # Estatísticas de programas
        if "programs_analysis" in analysis_data and "error" not in analysis_data.get("programs_analysis", {}):
            prog_analysis = analysis_data["programs_analysis"]
            html += f"""
                <div class="stat-card">
                    <div class="stat-number">{prog_analysis.get('total_programs', 'N/A')}</div>
                    <div class="stat-label">Programas Instalados</div>
                </div>
"""
            if "unused_programs" in prog_analysis:
                html += f"""
                <div class="stat-card">
                    <div class="stat-number">{len(prog_analysis['unused_programs'])}</div>
                    <div class="stat-label">Programas Não Utilizados</div>
                </div>
"""
        
        # Bloatware
        if "bloatware_detected" in analysis_data:
            html += f"""
                <div class="stat-card">
                    <div class="stat-number">{len(analysis_data['bloatware_detected'])}</div>
                    <div class="stat-label">Bloatware Detectado</div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
        
        # Top programas por tamanho
        if ("programs_analysis" in analysis_data and 
            "programs_by_size" in analysis_data["programs_analysis"] and
            len(analysis_data["programs_analysis"]["programs_by_size"]) > 0):
            
            html += """
        <div class="section">
            <h2>📦 Maiores Programas (Top 10)</h2>
            <table>
                <tr>
                    <th>Programa</th>
                    <th>Tamanho (MB)</th>
                    <th>Última Execução</th>
                </tr>
"""
            for program in analysis_data["programs_analysis"]["programs_by_size"][:10]:
                name = program.get("display_name", "N/A")
                size = program.get("size_mb", "N/A")
                last_used = program.get("last_used", "N/A")
                html += f"""
                <tr>
                    <td>{name}</td>
                    <td>{size}</td>
                    <td>{last_used}</td>
                </tr>
"""
            html += """
            </table>
        </div>
"""
        
        # Bloatware detectado
        if "bloatware_detected" in analysis_data and len(analysis_data["bloatware_detected"]) > 0:
            html += """
        <div class="section">
            <h2>🗑️ Bloatware Detectado</h2>
            <table>
                <tr>
                    <th>Aplicativo</th>
                    <th>Categoria</th>
                    <th>Seguro Remover</th>
                </tr>
"""
            for app in analysis_data["bloatware_detected"][:15]:  # Top 15
                name = app.get("name", "N/A")
                category = app.get("category", "N/A")
                safe = "✅ Sim" if app.get("safe_to_remove", False) else "⚠️ Verificar"
                html += f"""
                <tr>
                    <td>{name}</td>
                    <td>{category}</td>
                    <td>{safe}</td>
                </tr>
"""
            html += """
            </table>
        </div>
"""
        
        html += f"""
    </div>
    
    <div class="footer">
        <p><strong>Windows Dev Optimizer Framework</strong></p>
        <p>Desenvolvido por Nicolas Avila - Avila Ops</p>
        <p>Email: nicolas@avila.inc | WhatsApp: +55 17 99781-1471</p>
        <p>Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</p>
    </div>
</body>
</html>
"""
        
        return html
    
    def _generate_recommendations_email_body(self, recommendations: Dict[str, Any]) -> str:
        """Gera corpo HTML do email de recomendações"""
        
        timestamp = recommendations.get("timestamp", datetime.now().isoformat())
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #366092; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .section {{ margin: 20px 0; }}
        .recommendation {{ background: #f8f9fa; margin: 10px 0; padding: 15px; border-radius: 5px; border-left: 4px solid #366092; }}
        .priority-high {{ border-left-color: #dc3545; }}
        .priority-medium {{ border-left-color: #ffc107; }}
        .priority-low {{ border-left-color: #28a745; }}
        .priority-badge {{ display: inline-block; padding: 2px 8px; border-radius: 3px; color: white; font-size: 12px; }}
        .badge-high {{ background: #dc3545; }}
        .badge-medium {{ background: #ffc107; }}
        .badge-low {{ background: #28a745; }}
        .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Windows Dev Optimizer</h1>
        <p>Recomendações de Otimização</p>
        <p>{timestamp}</p>
    </div>
    
    <div class="content">
        <div class="section">
            <h2>📋 Recomendações Personalizadas</h2>
            <p>Baseado na análise do seu sistema, seguem as recomendações para otimização:</p>
        </div>
"""
        
        # Performance
        if "performance" in recommendations and len(recommendations["performance"]) > 0:
            html += """
        <div class="section">
            <h2>⚡ Performance</h2>
"""
            for rec in recommendations["performance"]:
                priority = rec.get("priority", "low")
                priority_class = f"priority-{priority}"
                badge_class = f"badge-{priority}"
                
                html += f"""
            <div class="recommendation {priority_class}">
                <span class="priority-badge {badge_class}">{priority.upper()}</span>
                <h3>{rec.get('category', 'N/A').title()}</h3>
                <p><strong>Descrição:</strong> {rec.get('description', 'N/A')}</p>
                <p><strong>Ação:</strong> <code>{rec.get('action', 'N/A')}</code></p>
            </div>
"""
            html += """
        </div>
"""
        
        # Cleanup
        if "cleanup" in recommendations and len(recommendations["cleanup"]) > 0:
            html += """
        <div class="section">
            <h2>🧹 Limpeza</h2>
"""
            for rec in recommendations["cleanup"]:
                priority = rec.get("priority", "low")
                priority_class = f"priority-{priority}"
                badge_class = f"badge-{priority}"
                
                html += f"""
            <div class="recommendation {priority_class}">
                <span class="priority-badge {badge_class}">{priority.upper()}</span>
                <h3>{rec.get('category', 'N/A').title()}</h3>
                <p><strong>Descrição:</strong> {rec.get('description', 'N/A')}</p>
                <p><strong>Ação:</strong> <code>{rec.get('action', 'N/A')}</code></p>
            </div>
"""
            html += """
        </div>
"""
        
        # Development
        if "development" in recommendations and len(recommendations["development"]) > 0:
            html += """
        <div class="section">
            <h2>👨‍💻 Desenvolvimento</h2>
"""
            for rec in recommendations["development"]:
                priority = rec.get("priority", "low")
                priority_class = f"priority-{priority}"
                badge_class = f"badge-{priority}"
                
                html += f"""
            <div class="recommendation {priority_class}">
                <span class="priority-badge {badge_class}">{priority.upper()}</span>
                <h3>{rec.get('category', 'N/A').title()}</h3>
                <p><strong>Descrição:</strong> {rec.get('description', 'N/A')}</p>
                <p><strong>Ação:</strong> <code>{rec.get('action', 'N/A')}</code></p>
            </div>
"""
            html += """
        </div>
"""
        
        html += f"""
    </div>
    
    <div class="footer">
        <p><strong>Windows Dev Optimizer Framework</strong></p>
        <p>Desenvolvido por Nicolas Avila - Avila Ops</p>
        <p>Email: nicolas@avila.inc | WhatsApp: +55 17 99781-1471</p>
        <p>Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M:%S")}</p>
    </div>
</body>
</html>
"""
        
        return html