"""
ÁVILA REPORT FRAMEWORK - INICIALIZADOR
======================================
Script de inicialização e instalação do framework
"""

import os
import sys
import subprocess

def check_python_version():
    """Verificar versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        return False

    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instalar dependências"""
    print("📦 Instalando dependências...")

    try:
        # Instalar dependências básicas
        basic_deps = [
            "pandas>=1.5.0",
            "openpyxl>=3.0.0",
            "sentry-sdk>=1.32.0"
        ]

        for dep in basic_deps:
            print(f"  Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

        print("✅ Dependências instaladas com sucesso")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_shortcuts():
    """Criar atalhos para execução"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Script PowerShell para Windows
    ps_script = f"""
# ÁVILA REPORT FRAMEWORK - LAUNCHER
# Atalho para executar o framework

$FrameworkPath = "{base_dir}"
$PythonPath = "{sys.executable}"

Write-Host "🏛️ Iniciando Ávila Report Framework..." -ForegroundColor Cyan

Set-Location $FrameworkPath

try {{
    & $PythonPath main.py
    Write-Host "✅ Framework executado com sucesso" -ForegroundColor Green
}}
catch {{
    Write-Host "❌ Erro ao executar framework: $_" -ForegroundColor Red
    Read-Host "Pressione Enter para continuar"
}}
"""

    launcher_path = os.path.join(base_dir, "launch_avila_reports.ps1")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(ps_script)

    print(f"✅ Atalho criado: {launcher_path}")

def setup_framework():
    """Setup completo do framework"""
    print("🏛️ ÁVILA REPORT FRAMEWORK - SETUP")
    print("=" * 50)

    # Verificar Python
    if not check_python_version():
        input("Pressione Enter para sair...")
        return False

    # Instalar dependências
    if not install_dependencies():
        input("Pressione Enter para sair...")
        return False

    # Criar atalhos
    create_shortcuts()

    # Verificar estrutura
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = ['logs', 'exports', 'assets']

    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"📁 Diretório criado: {dir_name}")

    print("\n🎉 SETUP CONCLUÍDO COM SUCESSO!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python main.py")
    print("2. Ou use: ./launch_avila_reports.ps1")
    print("3. Configure suas credenciais de email se necessário")
    print("4. Teste as funcionalidades")

    return True

if __name__ == "__main__":
    setup_framework()
    input("\nPressione Enter para continuar...")
