#!/usr/bin/env python3
"""
Script de Envio Automático - Auto-Análise ON Platform
Envia email HTML profissional via SMTP
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import sys

# Configurações SMTP
SMTP_SERVER = "mail.porkbun.com"
SMTP_PORT = 465  # Porta SSL (tentativa alternativa)
EMAIL_FROM = "dev@avila.inc"
EMAIL_PASSWORD = "7Aciqgr7@3278579"
EMAIL_TO = "nicolas@avila.inc"

def send_email():
    """Envia o email HTML com a auto-análise"""
    
    print("=" * 60)
    print("📧 ENVIANDO AUTO-ANÁLISE POR EMAIL")
    print("=" * 60)
    print()
    
    # Carregar conteúdo HTML
    html_file = Path(__file__).parent / "AUTO_ANALISE_EMAIL.html"
    
    if not html_file.exists():
        print("❌ Erro: Arquivo AUTO_ANALISE_EMAIL.html não encontrado!")
        print(f"   Procurado em: {html_file}")
        return False
    
    print(f"📄 Carregando: {html_file.name}")
    html_content = html_file.read_text(encoding='utf-8')
    print(f"   ✓ {len(html_content)} caracteres carregados")
    
    # Criar mensagem
    print("\n📝 Montando email...")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "🔍 Auto-Análise ON Platform - Status e Recomendações"
    msg['From'] = f"ON Platform Diagnostics <{EMAIL_FROM}>"
    msg['To'] = EMAIL_TO
    msg['Reply-To'] = EMAIL_FROM
    
    # Adicionar conteúdo HTML
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    print(f"   ✓ Assunto: {msg['Subject']}")
    print(f"   ✓ De: {msg['From']}")
    print(f"   ✓ Para: {msg['To']}")
    
    # Enviar email
    try:
        print(f"\n🌐 Conectando ao servidor SMTP...")
        print(f"   Servidor: {SMTP_SERVER}")
        print(f"   Porta: {SMTP_PORT} (TLS/STARTTLS)")
        
        # Usar SMTP com SSL (porta 465)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            print("   ✓ Conexão SSL estabelecida")
            
            print("\n� Autenticando...")
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            print("   ✓ Autenticação bem-sucedida")
            
            print("\n📤 Enviando email...")
            server.send_message(msg)
            print("   ✓ Email enviado com sucesso!")
        
        print("\n" + "=" * 60)
        print("✅ EMAIL ENVIADO COM SUCESSO!")
        print("=" * 60)
        print()
        print(f"📧 Destinatário: {EMAIL_TO}")
        print(f"📋 Assunto: {msg['Subject']}")
        print()
        print("💡 Verifique sua caixa de entrada em alguns segundos.")
        print()
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print("\n❌ ERRO DE AUTENTICAÇÃO!")
        print(f"   {e}")
        print("\n💡 Verifique:")
        print("   • Email correto: dev@avila.inc")
        print("   • Senha correta")
        print("   • Servidor permite autenticação SMTP")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ ERRO SMTP: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    
    print()
    print("🚀 Iniciando envio de email...")
    print()
    
    success = send_email()
    
    if success:
        print("✨ Processo concluído com sucesso!")
        print()
        return 0
    else:
        print("⚠️ Falha no envio do email.")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
