# ÁVILA REPORT FRAMEWORK - LAUNCHER
# =================================
# Script PowerShell para iniciar o framework

param(
    [switch]$Test,
    [switch]$Setup,
    [switch]$Help
)

# Configurações
$FrameworkPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonCmd = "python"

# Cores
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"

function Show-Header {
    Write-Host ""
    Write-Host "🏛️  ÁVILA REPORT FRAMEWORK" -ForegroundColor $ColorInfo
    Write-Host "=================================" -ForegroundColor $ColorInfo
    Write-Host "Versão: 1.0.0" -ForegroundColor White
    Write-Host "AvilaOps Team" -ForegroundColor White
    Write-Host ""
}

function Show-Help {
    Show-Header
    Write-Host "📋 OPÇÕES DISPONÍVEIS:" -ForegroundColor $ColorInfo
    Write-Host ""
    Write-Host "  .\launch_avila_reports.ps1          # Executar framework" -ForegroundColor White
    Write-Host "  .\launch_avila_reports.ps1 -Test    # Executar testes" -ForegroundColor White
    Write-Host "  .\launch_avila_reports.ps1 -Setup   # Executar setup" -ForegroundColor White
    Write-Host "  .\launch_avila_reports.ps1 -Help    # Mostrar ajuda" -ForegroundColor White
    Write-Host ""
    Write-Host "📁 ESTRUTURA:" -ForegroundColor $ColorInfo
    Write-Host "  main.py              # Interface principal"
    Write-Host "  test_framework.py    # Testes completos"
    Write-Host "  setup.py            # Instalação"
    Write-Host "  config.py           # Configurações"
    Write-Host ""
    Write-Host "🔗 SUPORTE:" -ForegroundColor $ColorInfo
    Write-Host "  Email: nicolas@avila.inc"
    Write-Host "  GitHub: https://github.com/avilaops/Avila-Framework"
    Write-Host ""
}

function Test-PythonInstalled {
    try {
        $pythonVersion = & $PythonCmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Python detectado: $pythonVersion" -ForegroundColor $ColorSuccess
            return $true
        }
    }
    catch {
        Write-Host "❌ Python não encontrado" -ForegroundColor $ColorError
        Write-Host "💡 Instale Python 3.8+ em https://python.org" -ForegroundColor $ColorWarning
        return $false
    }
    return $false
}

function Start-Framework {
    Show-Header

    Write-Host "🚀 Iniciando Ávila Report Framework..." -ForegroundColor $ColorInfo

    # Verificar Python
    if (-not (Test-PythonInstalled)) {
        Read-Host "Pressione Enter para sair"
        return
    }

    # Mudar para diretório do framework
    Push-Location $FrameworkPath

    try {
        Write-Host "📂 Diretório: $FrameworkPath" -ForegroundColor White
        Write-Host "⚡ Executando main.py..." -ForegroundColor $ColorInfo
        Write-Host ""

        # Executar framework
        & $PythonCmd main.py

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Framework executado com sucesso!" -ForegroundColor $ColorSuccess
        } else {
            Write-Host ""
            Write-Host "❌ Framework encerrado com erro (código: $LASTEXITCODE)" -ForegroundColor $ColorError
        }
    }
    catch {
        Write-Host ""
        Write-Host "💥 Erro ao executar framework: $_" -ForegroundColor $ColorError
        Write-Host ""
        Write-Host "🔧 SOLUÇÕES:" -ForegroundColor $ColorWarning
        Write-Host "  1. Execute: python setup.py"
        Write-Host "  2. Instale dependências: pip install pandas openpyxl sentry-sdk"
        Write-Host "  3. Verifique logs em: logs/"
    }
    finally {
        Pop-Location
    }
}

function Start-Tests {
    Show-Header

    Write-Host "🧪 Executando testes do framework..." -ForegroundColor $ColorInfo

    # Verificar Python
    if (-not (Test-PythonInstalled)) {
        Read-Host "Pressione Enter para sair"
        return
    }

    Push-Location $FrameworkPath

    try {
        Write-Host "⚡ Executando test_framework.py..." -ForegroundColor $ColorInfo
        Write-Host ""

        & $PythonCmd test_framework.py

        Write-Host ""
        Write-Host "✅ Testes concluídos!" -ForegroundColor $ColorSuccess
    }
    catch {
        Write-Host ""
        Write-Host "❌ Erro nos testes: $_" -ForegroundColor $ColorError
    }
    finally {
        Pop-Location
    }
}

function Start-Setup {
    Show-Header

    Write-Host "🔧 Executando setup do framework..." -ForegroundColor $ColorInfo

    # Verificar Python
    if (-not (Test-PythonInstalled)) {
        Read-Host "Pressione Enter para sair"
        return
    }

    Push-Location $FrameworkPath

    try {
        Write-Host "⚡ Executando setup.py..." -ForegroundColor $ColorInfo
        Write-Host ""

        & $PythonCmd setup.py

        Write-Host ""
        Write-Host "✅ Setup concluído!" -ForegroundColor $ColorSuccess
    }
    catch {
        Write-Host ""
        Write-Host "❌ Erro no setup: $_" -ForegroundColor $ColorError
    }
    finally {
        Pop-Location
    }
}

function Show-QuickInfo {
    Write-Host ""
    Write-Host "📋 INFORMAÇÕES RÁPIDAS:" -ForegroundColor $ColorInfo
    Write-Host "  📱 WhatsApp: +5517997811471" -ForegroundColor White
    Write-Host "  📧 Email: nicolas@avila.inc" -ForegroundColor White
    Write-Host "  📁 Logs: .\logs\" -ForegroundColor White
    Write-Host "  📊 Exports: .\exports\" -ForegroundColor White
    Write-Host ""
    Write-Host "⚡ Para ajuda: .\launch_avila_reports.ps1 -Help" -ForegroundColor $ColorWarning
}

# MAIN - Lógica principal
if ($Help) {
    Show-Help
}
elseif ($Test) {
    Start-Tests
    Show-QuickInfo
}
elseif ($Setup) {
    Start-Setup
    Show-QuickInfo
}
else {
    Start-Framework
    Show-QuickInfo
}

Write-Host ""
Read-Host "Pressione Enter para sair"
