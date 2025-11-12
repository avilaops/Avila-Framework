# Inicializacao Git - Avila Framework
# Script completo de configuracao Git e GitHub

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  CONFIGURACAO GIT - AVILA FRAMEWORK" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$root = "C:\Users\nicol\OneDrive\Avila"
Set-Location $root

# ========================================
# 1. VERIFICAR SE GIT ESTA INSTALADO
# ========================================
Write-Host "[1/10] Verificando Git..." -ForegroundColor Yellow

try {
    $gitVersion = git --version
    Write-Host "  OK: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERRO: Git nao instalado!" -ForegroundColor Red
    Write-Host "  Instalar: winget install Git.Git" -ForegroundColor Yellow
    exit 1
}

# ========================================
# 2. CONFIGURAR GIT GLOBAL
# ========================================
Write-Host "[2/10] Configurando Git global..." -ForegroundColor Yellow

# PREENCHER AQUI:
$gitUserName = Read-Host "  Nome completo para Git"
$gitUserEmail = Read-Host "  Email para Git"

git config --global user.name "$gitUserName"
git config --global user.email "$gitUserEmail"
git config --global init.defaultBranch main
git config --global core.autocrlf false
git config --global core.eol lf
git config --global pull.rebase false

Write-Host "  OK: Configuracao global aplicada" -ForegroundColor Green

# ========================================
# 3. INICIALIZAR REPOSITORIO
# ========================================
Write-Host "[3/10] Inicializando repositorio..." -ForegroundColor Yellow

if (Test-Path ".git") {
    Write-Host "  OK: Repositorio ja existe" -ForegroundColor Green
} else {
    git init
    Write-Host "  OK: Repositorio criado" -ForegroundColor Green
}

# ========================================
# 4. VERIFICAR ARQUIVOS ESSENCIAIS
# ========================================
Write-Host "[4/10] Verificando arquivos essenciais..." -ForegroundColor Yellow

$essentialFiles = @(
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    "README.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md"
)

$missing = @()
foreach ($file in $essentialFiles) {
    if (Test-Path $file) {
        Write-Host "  OK: $file" -ForegroundColor Green
    } else {
   Write-Host "  FALTA: $file" -ForegroundColor Red
     $missing += $file
    }
}

if ($missing.Count -gt 0) {
  Write-Host "  AVISO: $($missing.Count) arquivos faltando" -ForegroundColor Yellow
}

# ========================================
# 5. CRIAR .gitignore SE NAO EXISTIR
# ========================================
Write-Host "[5/10] Verificando .gitignore..." -ForegroundColor Yellow

if (!(Test-Path ".gitignore")) {
    @"
# Avila Framework - gitignore basico
.venv/
__pycache__/
*.pyc
*.log
.env
.env.*
node_modules/
.vs/
"@ | Out-File .gitignore -Encoding UTF8
    Write-Host "  OK: .gitignore criado" -ForegroundColor Green
} else {
    Write-Host "  OK: .gitignore existe" -ForegroundColor Green
}

# ========================================
# 6. VERIFICAR SECRETS ANTES DE ADD
# ========================================
Write-Host "[6/10] Verificando secrets..." -ForegroundColor Yellow

$foundSecrets = $false

# Procurar patterns perigosos
$patterns = @("password", "secret", "token", "api_key", "sk-")

Get-ChildItem -Recurse -File -Exclude @("*.log", "*.zip", ".git") | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        foreach ($pattern in $patterns) {
       if ($content -match $pattern) {
    Write-Host "  AVISO: Possivel secret em $($_.Name)" -ForegroundColor Yellow
        $foundSecrets = $true
 }
     }
    }
}

if (!$foundSecrets) {
    Write-Host "  OK: Nenhum secret detectado" -ForegroundColor Green
} else {
    Write-Host "  ATENCAO: Revise arquivos antes de commitar!" -ForegroundColor Red
    $continue = Read-Host "  Continuar mesmo assim? (s/n)"
    if ($continue -ne "s") {
 exit 1
    }
}

# ========================================
# 7. STAGE ARQUIVOS
# ========================================
Write-Host "[7/10] Staging arquivos..." -ForegroundColor Yellow

git add .
$stagedFiles = git diff --cached --name-only
$count = ($stagedFiles | Measure-Object).Count

Write-Host "  OK: $count arquivos staged" -ForegroundColor Green

# ========================================
# 8. CRIAR COMMIT INICIAL
# ========================================
Write-Host "[8/10] Criando commit inicial..." -ForegroundColor Yellow

$hasCommits = git log -1 2>&1
if ($hasCommits -match "fatal: your current branch") {
    git commit -m "chore: setup inicial Avila Framework

- Estrutura de pastas oficial
- Configuracoes VS Code e Visual Studio 2022
- GitHub templates e workflows
- Agente Archivus implementado
- Documentacao completa

Setor: Setup
Agente: Sistema
Data: $(Get-Date -Format 'yyyy-MM-dd')"
    
    Write-Host "  OK: Commit inicial criado" -ForegroundColor Green
} else {
    Write-Host "  OK: Repositorio ja tem commits" -ForegroundColor Green
}

# ========================================
# 9. CONFIGURAR REMOTE (PREENCHER!)
# ========================================
Write-Host "[9/10] Configurando remote..." -ForegroundColor Yellow

$remoteUrl = git remote get-url origin 2>&1

if ($remoteUrl -match "fatal:") {
    Write-Host "  Nenhum remote configurado ainda" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  PREENCHER: URL do repositorio GitHub" -ForegroundColor Cyan
    Write-Host "  Exemplo: https://github.com/seu-usuario/avila.git" -ForegroundColor DarkGray
    Write-Host ""
    
    $githubUrl = Read-Host "  URL do repositorio (ou Enter para pular)"
    
    if ($githubUrl) {
        git remote add origin $githubUrl
     Write-Host "  OK: Remote configurado" -ForegroundColor Green
    } else {
        Write-Host "  PULADO: Configure manualmente depois" -ForegroundColor Yellow
 }
} else {
    Write-Host "  OK: Remote ja configurado: $remoteUrl" -ForegroundColor Green
}

# ========================================
# 10. RESUMO E PROXIMOS PASSOS
# ========================================
Write-Host "[10/10] Finalizando..." -ForegroundColor Yellow
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  CONFIGURACAO GIT CONCLUIDA!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "RESUMO:" -ForegroundColor Cyan
Write-Host "  Git version: " -NoNewline; git --version
Write-Host "  User name: " -NoNewline; git config user.name
Write-Host "  User email: " -NoNewline; git config user.email
Write-Host "  Branch: " -NoNewline; git branch --show-current
Write-Host "  Commits: " -NoNewline; git rev-list --count HEAD 2>$null
Write-Host ""

Write-Host "PROXIMOS PASSOS:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Criar repositorio no GitHub:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor DarkGray
Write-Host ""
Write-Host "2. Configurar remote (se nao fez):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/SEU_USUARIO/avila.git" -ForegroundColor DarkGray
Write-Host ""
Write-Host "3. Push inicial:" -ForegroundColor White
Write-Host " git push -u origin main" -ForegroundColor DarkGray
Write-Host ""
Write-Host "4. Configurar GitHub Pro/Enterprise:" -ForegroundColor White
Write-Host "   - Settings > Security & analysis > Habilitar tudo" -ForegroundColor DarkGray
Write-Host "   - Settings > Branches > Proteger main" -ForegroundColor DarkGray
Write-Host "   - Settings > Actions > Allow all actions" -ForegroundColor DarkGray
Write-Host ""
Write-Host "5. Ver checklist completo:" -ForegroundColor White
Write-Host "   code Setup\CHECKLIST_GITHUB_SLOTS.md" -ForegroundColor DarkGray
Write-Host ""

# Salvar log
$logFile = "Logs\Daily\git_setup_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').log"
@"
Git Setup Log
=============
Data: $(Get-Date)
User: $(git config user.name)
Email: $(git config user.email)
Branch: $(git branch --show-current)
Remote: $(git remote get-url origin 2>&1)
Status: Concluido
"@ | Out-File $logFile -Encoding UTF8

Write-Host "Log salvo: $logFile" -ForegroundColor DarkGray
Write-Host ""
