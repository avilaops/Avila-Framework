#!/usr/bin/env python3
"""
ÁVILA FRAMEWORK - SETUP E DEMONSTRAÇÃO DO DASHBOARD
==================================================
Script de setup e teste do sistema de dashboards executivos
Autor: Nicolas Avila - Ávila Framework
Data: 2025-11-11
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any

def print_banner():
    """Imprime banner do sistema"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                   🏛️  ÁVILA FRAMEWORK                         ║
    ║                DASHBOARD EXECUTIVO - SETUP                    ║
    ║                                                               ║
    ║  Sistema completo de relatórios gerenciais com HTML premium  ║
    ║  📧 Email automático | 📊 Gráficos | 🎯 Métricas em tempo real ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} detectado")

def install_requirements():
    """Instala dependências"""
    print("\n📦 Instalando dependências...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
        else:
            print(f"⚠️ Aviso na instalação: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")

def setup_environment():
    """Configura ambiente"""
    print("\n🔧 Configurando ambiente...")
    
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado!")
        print("📝 Criando arquivo .env de exemplo...")
        
        # Criar .env de exemplo
        env_content = """# ÁVILA FRAMEWORK - CONFIGURAÇÕES DO DASHBOARD EXECUTIVO
# ==================================================
# Configurações de Email SMTP
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Destinatários de Email
EMAIL_RECIPIENTS=nicolas@avila.inc
WEEKLY_RECIPIENTS=nicolas@avila.inc,board@avila.inc
BOARD_RECIPIENTS=nicolas@avila.inc,board@avila.inc,investors@avila.inc

# Configurações da Empresa
COMPANY_NAME=Ávila Framework
COMPANY_LOGO=https://avatars.githubusercontent.com/avilaops

# IMPORTANTE: Configure seu email e senha antes de executar!
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"📝 Arquivo .env criado: {env_file}")
        print("⚠️  CONFIGURE SEU EMAIL E SENHA antes de continuar!")
        return False
    else:
        print("✅ Arquivo .env encontrado")
        return True

def test_configuration():
    """Testa configuração"""
    print("\n🧪 Testando configuração...")
    
    try:
        from config_manager import test_configuration
        test_configuration()
        return True
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

async def run_demo():
    """Executa demonstração do dashboard"""
    print("\n🚀 Executando demonstração do dashboard...")
    
    try:
        from dashboard_generator import main as dashboard_main
        await dashboard_main()
        return True
    except Exception as e:
        print(f"❌ Erro na demonstração: {e}")
        return False

def create_shortcuts():
    """Cria scripts de atalho"""
    print("\n📜 Criando scripts de atalho...")
    
    # Script para Windows
    run_script = Path(__file__).parent / "run_dashboard.bat"
    with open(run_script, 'w', encoding='utf-8') as f:
        f.write(f"""@echo off
cd /d "{Path(__file__).parent}"
python dashboard_generator.py
pause
""")
    
    # Script para Python direto
    py_script = Path(__file__).parent / "quick_run.py"
    with open(py_script, 'w', encoding='utf-8') as f:
        f.write("""#!/usr/bin/env python3
import asyncio
from dashboard_generator import main

if __name__ == "__main__":
    asyncio.run(main())
""")
    
    print(f"✅ Scripts criados:")
    print(f"   - {run_script}")
    print(f"   - {py_script}")

def print_usage_instructions():
    """Imprime instruções de uso"""
    print("""
    📋 INSTRUÇÕES DE USO
    ==================
    
    1. 🔧 CONFIGURAÇÃO INICIAL:
       • Configure seu email no arquivo .env
       • Defina SENDER_PASSWORD com sua senha de app do Gmail
       • Ajuste destinatários conforme necessário
    
    2. 🚀 EXECUTAR DASHBOARD:
       • python dashboard_generator.py
       • python quick_run.py
       • Executar run_dashboard.bat (Windows)
    
    3. 📧 CONFIGURAÇÃO DE EMAIL:
       • Use senha de aplicativo do Gmail (não sua senha normal)
       • Configure SMTP_SERVER se usar outro provedor
       • Teste com EMAIL_RECIPIENTS simples primeiro
    
    4. 📊 RECURSOS DISPONÍVEIS:
       • Dashboard HTML premium responsivo
       • Envio automático por email
       • Gráficos interativos com Plotly
       • Métricas em tempo real dos produtos
       • Templates mobile-friendly
       • Backup automático de relatórios
    
    5. 🔧 PERSONALIZAÇÃO:
       • Modifique cores em COMPANY_COLORS
       • Adicione novos destinatários por tipo
       • Configure horários de agendamento
       • Ative/desative features específicas
    
    6. 📂 ARQUIVOS IMPORTANTES:
       • .env - Configurações principais
       • dashboard_generator.py - Gerador principal
       • config_manager.py - Gerenciador de configuração
       • email_templates.py - Templates HTML premium
    
    💡 DICAS:
    • Execute o teste de configuração primeiro: python config_manager.py
    • Verifique o log 'dashboard.log' para debug
    • Relatórios salvos em ./output/
    """)

def main():
    """Função principal do setup"""
    print_banner()
    
    # Verificações básicas
    check_python_version()
    
    # Instalar dependências
    install_requirements()
    
    # Configurar ambiente
    env_ready = setup_environment()
    
    if not env_ready:
        print("\n⚠️  Configure o arquivo .env antes de continuar!")
        print("   1. Edite o arquivo .env criado")
        print("   2. Configure seu email e senha")
        print("   3. Execute novamente este script")
        input("\nPressione Enter para continuar...")
        return
    
    # Testar configuração
    config_ok = test_configuration()
    
    if not config_ok:
        print("\n❌ Problemas na configuração detectados")
        print("   Verifique o arquivo .env e tente novamente")
        return
    
    # Criar scripts de atalho
    create_shortcuts()
    
    # Perguntir se deseja executar demo
    print("\n🤔 Deseja executar uma demonstração do dashboard agora?")
    response = input("   Digite 'sim' ou 's' para continuar: ").lower().strip()
    
    if response in ['sim', 's', 'yes', 'y']:
        print("\n🚀 Iniciando demonstração...")
        try:
            asyncio.run(run_demo())
            print("\n🎉 Demonstração concluída!")
        except Exception as e:
            print(f"\n❌ Erro na demonstração: {e}")
    
    # Instruções finais
    print_usage_instructions()
    
    print("\n✅ Setup concluído com sucesso!")
    print("🎯 Sistema pronto para uso!")

if __name__ == "__main__":
    main()