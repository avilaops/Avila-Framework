# ============================================
# Script: validate_governance.ps1
# Função: Validar conformidade com governança Avila
# Autor: Nicolas Avila
# Data: 2025-11-11
# Projeto: Avila Ops - Windows Dev Optimizer
# ============================================

$WorkspaceRoot = "C:\Users\nicol\OneDrive\Avila"
$ProjectPath = "$WorkspaceRoot\AvilaOps\products\windows-dev-optimizer"

Write-Host "🔍 VALIDAÇÃO DE GOVERNANÇA - AVILA FRAMEWORK" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Yellow

$errors = @()
$warnings = @()
$passed = @()

# 1. Verificar localização do projeto
Write-Host "`n📍 Verificando localização..." -ForegroundColor Yellow
if (Test-Path $ProjectPath) {
    $passed += "✅ Projeto localizado corretamente em AvilaOps/products/"
} else {
    $errors += "❌ Projeto não está na localização correta"
}

# 2. Verificar estrutura de arquivos obrigatórios
Write-Host "📁 Verificando estrutura..." -ForegroundColor Yellow
$requiredFiles = @(
    "README.md",
    "requirements.txt", 
    ".gitignore",
    ".env.example",
    "main.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path "$ProjectPath\$file") {
        $passed += "✅ Arquivo obrigatório presente: $file"
    } else {
        $errors += "❌ Arquivo obrigatório ausente: $file"
    }
}

# 3. Verificar headers Avila nos arquivos Python
Write-Host "🐍 Verificando headers Python..." -ForegroundColor Yellow
$pythonFiles = Get-ChildItem "$ProjectPath" -Recurse -Filter "*.py"

foreach ($file in $pythonFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    if ($content -match "# coding: utf-8" -and 
        $content -match "Autor: Nicolas Avila" -and 
        $content -match "Projeto: Avila Ops") {
        $passed += "✅ Header Avila correto: $($file.Name)"
    } else {
        $warnings += "⚠️ Header Avila ausente/incorreto: $($file.Name)"
    }
}

# 4. Verificar .gitignore
Write-Host "🔒 Verificando segurança..." -ForegroundColor Yellow
if (Test-Path "$ProjectPath\.gitignore") {
    $gitignore = Get-Content "$ProjectPath\.gitignore" -Raw
    
    $securityPatterns = @(".env", "*.key", "*.pem", "*.log")
    $securityOk = $true
    
    foreach ($pattern in $securityPatterns) {
        if ($gitignore -match [regex]::Escape($pattern)) {
            $passed += "✅ Padrão de segurança no .gitignore: $pattern"
        } else {
            $warnings += "⚠️ Padrão de segurança ausente: $pattern"
            $securityOk = $false
        }
    }
} else {
    $errors += "❌ Arquivo .gitignore ausente"
}

# 5. Verificar se .env não está versionado
if (Test-Path "$ProjectPath\.env") {
    $warnings += "⚠️ Arquivo .env presente - certifique-se que está no .gitignore"
}

# 6. Verificar .env.example
if (Test-Path "$ProjectPath\.env.example") {
    $passed += "✅ Template .env.example presente"
} else {
    $errors += "❌ Template .env.example ausente"
}

# 7. Verificar pastas proibidas
Write-Host "🚫 Verificando locais proibidos..." -ForegroundColor Yellow
$forbiddenPaths = @(
    "C:\Temp\WindowsDevOptimizer",
    "C:\Users\nicol\Desktop\WindowsDevOptimizer",
    "C:\Users\nicol\Documents\WindowsDevOptimizer"
)

foreach ($path in $forbiddenPaths) {
    if (Test-Path $path) {
        $errors += "❌ Projeto encontrado em local proibido: $path"
    } else {
        $passed += "✅ Local proibido limpo: $path"
    }
}

# 8. Relatório final
Write-Host "`n📊 RESULTADO DA VALIDAÇÃO" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Yellow

if ($passed.Count -gt 0) {
    Write-Host "`n✅ APROVADO ($($passed.Count) itens):" -ForegroundColor Green
    foreach ($item in $passed) {
        Write-Host "  $item" -ForegroundColor Green
    }
}

if ($warnings.Count -gt 0) {
    Write-Host "`n⚠️ AVISOS ($($warnings.Count) itens):" -ForegroundColor Yellow
    foreach ($item in $warnings) {
        Write-Host "  $item" -ForegroundColor Yellow
    }
}

if ($errors.Count -gt 0) {
    Write-Host "`n❌ ERROS ($($errors.Count) itens):" -ForegroundColor Red
    foreach ($item in $errors) {
        Write-Host "  $item" -ForegroundColor Red
    }
}

# Status final
Write-Host "`n🏆 STATUS FINAL:" -ForegroundColor Cyan
if ($errors.Count -eq 0) {
    if ($warnings.Count -eq 0) {
        Write-Host "✅ TOTALMENTE CONFORME COM GOVERNANÇA AVILA" -ForegroundColor Green
        $exitCode = 0
    } else {
        Write-Host "⚠️ CONFORME COM AVISOS - Revisar itens destacados" -ForegroundColor Yellow
        $exitCode = 0
    }
} else {
    Write-Host "❌ NÃO CONFORME - Corrigir erros obrigatórios" -ForegroundColor Red
    $exitCode = 1
}

Write-Host "`nDocumentação: $WorkspaceRoot\CONTRIBUTING.md" -ForegroundColor Gray
Write-Host "Segurança: $WorkspaceRoot\SECURITY.md" -ForegroundColor Gray

exit $exitCode