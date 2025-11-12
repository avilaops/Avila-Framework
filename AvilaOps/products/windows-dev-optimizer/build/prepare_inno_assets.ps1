param(
    [string]$Version = (Get-Date -Format 'yyyyMMdd')
)

$projectRoot = Split-Path -Parent $PSScriptRoot
$distRoot = Join-Path $projectRoot "build\inno_dist"
$packageRoot = Join-Path $distRoot "WindowsDevOptimizer"

if (Test-Path $distRoot) {
    Remove-Item $distRoot -Recurse -Force -ErrorAction SilentlyContinue
}

New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null

$itemsToCopy = @(
    "app.py",
    "main.py",
    "desktop_main.py",
    "framework",
    "modules",
    "templates",
    "config",
    "requirements.txt",
    "requirements_framework.txt",
    "README.md",
    "setup.ps1",
    "validate_governance.ps1",
    ".env.example"
)

foreach ($item in $itemsToCopy) {
    $source = Join-Path $projectRoot $item
    if (Test-Path $source) {
        Copy-Item $source -Destination $packageRoot -Recurse -Force
    }
}

# Copy launcher script if present
$launcherSource = Join-Path $projectRoot "start_windows_dev_optimizer.ps1"
if (Test-Path $launcherSource) {
    Copy-Item $launcherSource (Join-Path $packageRoot "start_windows_dev_optimizer.ps1") -Force
}

# Create dependency installer script
$installDependencies = @'
param(
    [switch]$Force
)

Write-Host "🔧 Instalando dependências do Windows Dev Optimizer" -ForegroundColor Cyan

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command python -ErrorAction SilentlyContinue

if (-not $python) {
    Write-Error "Python 3.10+ não encontrado no PATH. Instale Python e tente novamente."
    exit 1
}

$venvPath = Join-Path $root ".venv"

if (Test-Path $venvPath) {
    if ($Force) {
        Remove-Item $venvPath -Recurse -Force
    } else {
        Write-Host "Ambiente virtual existente detectado. Usando .venv atual." -ForegroundColor Yellow
    }
}

if (-not (Test-Path $venvPath)) {
    Write-Host "Criando ambiente virtual isolado..."
    & $python.Path -m venv $venvPath
}

$venvPython = Join-Path $venvPath "Scripts\python.exe"
Write-Host "Atualizando pip..."
& $venvPython -m pip install --upgrade pip
Write-Host "Instalando dependências do framework..."
& $venvPython -m pip install -r (Join-Path $root "requirements_framework.txt")

Write-Host "✅ Dependências instaladas com sucesso." -ForegroundColor Green
'@

Set-Content -Path (Join-Path $packageRoot "install_dependencies.ps1") -Value $installDependencies -Encoding UTF8

# Create launcher script for installed app
$launchScript = @'
param(
    [switch]$NoBrowser
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        Write-Error "Python 3.10+ não encontrado. Instale Python ou execute install_dependencies.ps1."
        exit 1
    }
    $pythonExe = $pythonCmd.Path
}

if (-not $NoBrowser) {
    Start-Process "http://127.0.0.1:8000" | Out-Null
}

Set-Location $root
Write-Host "Iniciando Windows Dev Optimizer..." -ForegroundColor Cyan
& $pythonExe "app.py"
'@
Set-Content -Path (Join-Path $packageRoot "launch_windows_dev_optimizer.ps1") -Value $launchScript -Encoding UTF8

# Create batch launcher for convenience
$batchLauncher = @"
@echo off
setlocal
set SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -NoLogo -File "%SCRIPT_DIR%launch_windows_dev_optimizer.ps1" %*
"@
Set-Content -Path (Join-Path $packageRoot "launch_windows_dev_optimizer.cmd") -Value $batchLauncher -Encoding ASCII

Write-Host "Inno Setup distribution prepared at $packageRoot" -ForegroundColor Green
