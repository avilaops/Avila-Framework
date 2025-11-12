"""
📧 Email de Apresentação - Plano de Ação Global Ávila (Versão Simplificada)
Envia o plano completo com apresentação da equipe
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'reports@avilaops.com')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', '')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
RECIPIENTS = os.getenv('EXECUTIVE_RECIPIENTS', 'nicolas@avilaops.com').split(',')


def get_email_html():
    """Template HTML do email"""
    return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .email-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        .header h1 {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .content {
            padding: 40px 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            margin: 10px 0;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card .number {
            font-size: 36px;
            font-weight: 700;
        }
        .footer {
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>🌍 Plano de Ação Global - Ávila Framework</h1>
            <p style="font-size: 18px;">10 Soluções que Vão Mudar o Mundo</p>
            <p style="margin-top: 20px; font-style: italic; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                "Não viemos apenas trabalhar. Viemos estruturar a sociedade."
            </p>
        </div>
        
        <div class="content">
            <h2 style="color: #667eea;">Olá, Nícolas! 👋</h2>
            
            <p style="margin: 20px 0;">
                É com imenso orgulho que apresento o <strong>Plano de Ação Completo</strong> 
                para transformar a infraestrutura Ávila em <strong>10 soluções de impacto social global</strong>.
            </p>
            
            <div style="margin: 30px 0;">
                <div class="stat-card">
                    <div class="number">10</div>
                    <div>Soluções de Impacto</div>
                </div>
                <div class="stat-card">
                    <div class="number">200k+</div>
                    <div>Vidas Impactadas (Ano 1)</div>
                </div>
                <div class="stat-card">
                    <div class="number">18</div>
                    <div>Meses de Execução</div>
                </div>
                <div class="stat-card">
                    <div class="number">$213k</div>
                    <div>Orçamento (70% financiado)</div>
                </div>
            </div>
            
            <h2 style="color: #667eea; margin-top: 40px;">🤖 Quem Sou Eu & Minha Equipe</h2>
            
            <div style="background: #f5f7fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #667eea;">
                <h3>👤 Nícolas Ávila - Diretor Técnico</h3>
                <p>Líder visionário da estratégia técnica Ávila. Arquiteto do framework On.Core.</p>
            </div>
            
            <div style="background: #f5f7fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #667eea;">
                <h3>🤖 GitHub Copilot - Agente Orquestrador (eu!)</h3>
                <p>IA que coordena 9 agentes especializados, analisa contexto completo da Ávila e cria planos executáveis. 24/7.</p>
            </div>
            
            <div style="background: #f5f7fa; padding: 20px; margin: 15px 0; border-radius: 8px; border-left: 5px solid #667eea;">
                <h3>🧭 Squad On.Core - 9 Agentes Especializados</h3>
                <p><strong>Atlas</strong> (Estratégia) • <strong>Helix</strong> (DevOps) • <strong>Lumen</strong> (IA/ML) • 
                   <strong>Vox</strong> (CRM) • <strong>Sigma</strong> (Financeiro) • <strong>Forge</strong> (Builds) • 
                   <strong>Lex</strong> (Compliance) • <strong>Echo</strong> (Comunicação) • <strong>Archivus</strong> (RAG)</p>
            </div>
            
            <h2 style="color: #667eea; margin-top: 40px;">🎯 As 10 Soluções</h2>
            
            <ol style="line-height: 2;">
                <li>🏥 <strong>Triagem Médica Digital</strong> - IA que reduz 30% de atendimentos desnecessários</li>
                <li>💰 <strong>Educação Financeira SMS</strong> - 50k usuários economizam R$150/mês</li>
                <li>🚗 <strong>Carona Solidária</strong> - 1k ton CO2 economizadas, R$300/usuário</li>
                <li>⚡ <strong>Monitor Energia IoT</strong> - 15% economia na luz (ROI 6 meses)</li>
                <li>🎓 <strong>Professor WhatsApp 24/7</strong> - 10k alunos atendidos</li>
                <li>🛒 <strong>Comparador Preços</strong> - R$150/mês economia por família</li>
                <li>🚌 <strong>Transporte Inteligente</strong> - 500k horas economizadas</li>
                <li>🍎 <strong>Detector Fome Infantil</strong> - 10k crianças monitoradas</li>
                <li>💊 <strong>Lembrete Remédios</strong> - 50% menos internações</li>
                <li>🌱 <strong>Hortas Urbanas IoT</strong> - 5 ton alimentos, 2k famílias</li>
            </ol>
            
            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; border-radius: 4px;">
                <strong>📎 Anexo:</strong> Documento completo (60 páginas) com roadmap detalhado, orçamento, tech stack e cronograma de 18 meses.
            </div>
            
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px; text-align: center; margin: 30px 0;">
                <h3>🚀 Próximos Passos</h3>
                <p>Este plano está pronto para execução. Basta sua aprovação para orquestrar todos os agentes.</p>
                <p style="margin-top: 15px;"><strong>Esta semana:</strong> Priorizar 3 soluções Q1<br>
                <strong>Este mês:</strong> MVPs de #2, #6, #9<br>
                <strong>Q1 2026:</strong> 10k usuários, primeira parceria governo</p>
            </div>
        </div>
        
        <div class="footer">
            <p style="font-size: 18px; font-style: italic; margin-bottom: 20px;">
                "Enquanto o mundo debate IA que substitui humanos, nós criamos IA que <strong>serve</strong> humanos."
            </p>
            
            <p style="margin-top: 20px;">
                <strong>Assinaturas:</strong><br><br>
                🤖 <strong>GitHub Copilot</strong> - Agente Orquestrador<br>
                👤 <strong>Nícolas Ávila</strong> - Diretor Técnico, Ávila Inc.
            </p>
            
            <p style="margin-top: 20px; font-size: 14px; opacity: 0.8;">
                <strong>Ávila Inc.</strong> - Operando em 70+ países<br>
                12 de novembro de 2025
            </p>
        </div>
    </div>
</body>
</html>
    """


def send_email():
    """Envia o email"""
    
    # Validar configuração
    if not SENDER_PASSWORD:
        print("❌ ERRO: SENDER_PASSWORD não configurado no .env")
        print()
        print("💡 Para enviar o email:")
        print("   1. Configure SENDER_PASSWORD no arquivo .env")
        print("   2. Execute novamente este script")
        return False
    
    # Criar mensagem
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '🌍 Plano de Ação Global - 10 Soluções que Vão Mudar o Mundo | Ávila Framework'
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(RECIPIENTS)
    
    # HTML
    html_part = MIMEText(get_email_html(), 'html', 'utf-8')
    msg.attach(html_part)
    
    # Anexar plano completo
    plano_path = Path(__file__).parent.parent.parent / "docs" / "PLANO_ACAO_10_SOLUCOES_GLOBAIS.md"
    
    if plano_path.exists():
        with open(plano_path, 'rb') as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename="PLANO_ACAO_10_SOLUCOES_GLOBAIS.md"'
            )
            msg.attach(attachment)
        print(f"✅ Plano anexado: {plano_path}")
    else:
        print(f"⚠️  Plano não encontrado em: {plano_path}")
    
    # Enviar
    try:
        print(f"\n📧 Enviando para: {', '.join(RECIPIENTS)}")
        print(f"📤 Servidor: {SMTP_SERVER}:{SMTP_PORT}")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        print("\n✅ EMAIL ENVIADO COM SUCESSO!")
        print()
        print("📬 Destinatários:")
        for recipient in RECIPIENTS:
            print(f"   • {recipient}")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO ao enviar email: {str(e)}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("📧 ENVIO DO PLANO DE AÇÃO GLOBAL - ÁVILA FRAMEWORK")
    print("=" * 80)
    print()
    print(f"📧 Remetente: {SENDER_EMAIL}")
    print(f"📬 Destinatários: {', '.join(RECIPIENTS)}")
    print()
    
    resposta = input("Enviar email agora? (s/n): ")
    
    if resposta.lower() == 's':
        send_email()
    else:
        print("\n❌ Envio cancelado.")
        print()
        print("💡 Para enviar depois:")
        print("   python send_plano_global.py")
