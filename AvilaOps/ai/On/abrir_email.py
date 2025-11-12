#!/usr/bin/env python3
"""
Gerador de Email Pronto para Envio
Abre o HTML no navegador padrão para envio manual
"""

import webbrowser
from pathlib import Path
import sys

def open_email_in_browser():
    """Abre o email HTML no navegador para envio manual"""
    
    print("=" * 70)
    print("📧 PREPARANDO EMAIL PARA ENVIO MANUAL")
    print("=" * 70)
    print()
    
    html_file = Path(__file__).parent / "AUTO_ANALISE_EMAIL.html"
    
    if not html_file.exists():
        print("❌ Erro: Arquivo AUTO_ANALISE_EMAIL.html não encontrado!")
        return False
    
    print(f"📄 Arquivo: {html_file.name}")
    print(f"📊 Tamanho: {html_file.stat().st_size:,} bytes")
    print()
    
    print("🌐 Abrindo no navegador...")
    webbrowser.open(html_file.as_uri())
    
    print()
    print("=" * 70)
    print("✅ EMAIL ABERTO NO NAVEGADOR!")
    print("=" * 70)
    print()
    print("📋 INSTRUÇÕES PARA ENVIO:")
    print()
    print("  1️⃣  Selecione TODO o conteúdo da página")
    print("      • Ctrl+A (Windows/Linux)")
    print("      • Cmd+A (Mac)")
    print()
    print("  2️⃣  Copie o conteúdo")
    print("      • Ctrl+C (Windows/Linux)")
    print("      • Cmd+C (Mac)")
    print()
    print("  3️⃣  Abra seu cliente de email:")
    print("      • Gmail: https://mail.google.com")
    print("      • Outlook: https://outlook.com")
    print("      • Ou use seu cliente desktop")
    print()
    print("  4️⃣  Cole o conteúdo no corpo do email")
    print("      • Ctrl+V (Windows/Linux)")
    print("      • Cmd+V (Mac)")
    print()
    print("  5️⃣  Preencha:")
    print(f"      • Para: nicolas@avila.inc")
    print(f"      • Assunto: 🔍 Auto-Análise ON Platform - Status e Recomendações")
    print()
    print("  6️⃣  Envie! 🚀")
    print()
    print("=" * 70)
    print()
    print("💡 ALTERNATIVA: Enviar como anexo")
    print("   • Anexe o arquivo AUTO_ANALISE_EMAIL.html")
    print("   • Nicolas pode abrir direto no navegador")
    print()
    
    return True

def create_mailto_link():
    """Cria um link mailto (pode não funcionar com HTML grande)"""
    
    print("📧 OPÇÃO ALTERNATIVA: Link Mailto")
    print()
    print("⚠️  Nota: Links mailto têm limite de tamanho e podem não funcionar")
    print("    para HTML grande. Use o método de copiar/colar acima.")
    print()
    
    mailto_link = (
        "mailto:nicolas@avila.inc"
        "?subject=🔍%20Auto-Análise%20ON%20Platform%20-%20Status%20e%20Recomendações"
        "&body=Olá%20Nicolas,%0A%0A"
        "Segue%20anexo%20a%20análise%20completa%20do%20sistema.%0A%0A"
        "Por%20favor,%20abra%20o%20arquivo%20AUTO_ANALISE_EMAIL.html%20no%20navegador."
    )
    
    print(f"Link gerado (copie e cole no navegador):")
    print(f"{mailto_link}")
    print()

def main():
    """Função principal"""
    
    print()
    success = open_email_in_browser()
    
    if success:
        print()
        create_mailto_link()
        print("✨ Processo concluído!")
        print()
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
