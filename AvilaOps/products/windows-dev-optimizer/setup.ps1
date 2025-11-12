# ============================================
# Script: setup.ps1
# Função: Configuração inicial do Windows Dev Optimizer
# Autor: Nicolas Avila
# Data: 2025-11-11
# Projeto: Avila Ops - Windows Dev Optimizer
# ============================================

param(
    [switch]$SkipVenv,
    [switch]$Force
)

$WorkspaceRoot = "C:\Users\nicol\OneDrive\Avila"
$ProjectPath = "$WorkspaceRoot\AvilaOps\products\windows-dev-optimizer"

Write-Host "🚀 Windows Dev Optimizer - Setup" -ForegroundColor Cyan
Write-Host "Projeto: Avila Ops" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow

# Verificar se está no local correto
if (-not (Test-Path $ProjectPath)) {
    Write-Error "❌ Projeto não encontrado em: $ProjectPath"
    Write-Host "Execute o setup a partir do diretório correto do projeto."
    exit 1
}

Set-Location $ProjectPath

# 1. Verificar Python
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Error "❌ Python não encontrado. Instale Python 3.8+ primeiro."
    exit 1
}

# 2. Criar ambiente virtual
if (-not $SkipVenv) {
    Write-Host "📦 Configurando ambiente virtual..." -ForegroundColor Yellow
    
    if (Test-Path ".venv" -and -not $Force) {
        Write-Host "⚠️ Ambiente virtual já existe. Use -Force para recriar." -ForegroundColor Yellow
    } else {
        if (Test-Path ".venv") {
            Remove-Item ".venv" -Recurse -Force
        }
        
        python -m venv .venv
        Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
    }
    
    # Ativar ambiente
    & ".\.venv\Scripts\Activate.ps1"
    Write-Host "✅ Ambiente virtual ativado" -ForegroundColor Green
}

# 3. Instalar dependências
Write-Host "📚 Instalando dependências..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✅ Dependências instaladas" -ForegroundColor Green

# 4. Criar diretórios necessários
Write-Host "📁 Criando estrutura de diretórios..." -ForegroundColor Yellow
$directories = @("logs", "reports", "exports")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Criado: $dir" -ForegroundColor Green
    }
}

# 5. Verificar .env
Write-Host "🔧 Verificando configurações..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Arquivo .env criado a partir do template" -ForegroundColor Green
        Write-Host "⚠️ Configure suas variáveis de ambiente em .env" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️ Arquivo .env.example não encontrado" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Arquivo .env já existe" -ForegroundColor Green
}

# 6. Verificar permissões
Write-Host "🔐 Verificando permissões..." -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if ($isAdmin) {
    Write-Host "✅ Executando como administrador" -ForegroundColor Green
} else {
    Write-Host "⚠️ Recomendado executar como administrador para funcionalidade completa" -ForegroundColor Yellow
}

# 7. Teste rápido
Write-Host "🧪 Executando teste básico..." -ForegroundColor Yellow
try {
    python -c "
import sys
sys.path.append('.')
from config.settings import APP_NAME, APP_VERSION
print(f'✅ {APP_NAME} v{APP_VERSION} configurado com sucesso!')
"
} catch {
    Write-Host "❌ Erro no teste básico. Verifique as dependências." -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 SETUP CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Para executar a aplicação:" -ForegroundColor Cyan
Write-Host "  1. cd '$ProjectPath'" -ForegroundColor White
Write-Host "  2. .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  3. python main.py" -ForegroundColor White
Write-Host "`nDocumentação: README.md" -ForegroundColor Gray
Write-Host "Logs: logs/" -ForegroundColor Gray
Write-Host "Relatórios: reports/" -ForegroundColor Gray