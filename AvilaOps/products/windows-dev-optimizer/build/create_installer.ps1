param(
    [string]$Version = (Get-Date -Format 'yyyyMMdd'),
    [string]$OutputDirectory
)

$scriptRoot = $PSScriptRoot
$projectRoot = Split-Path $scriptRoot -Parent
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $projectRoot "exports\installers"
}

if (-not (Test-Path $OutputDirectory)) {
    New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
}

$packageName = "WindowsDevOptimizer_$Version"
$buildRoot = Join-Path $OutputDirectory "build"
$packageRoot = Join-Path $buildRoot $packageName

if (Test-Path $buildRoot) {
    Remove-Item $buildRoot -Recurse -Force -ErrorAction SilentlyContinue
}

New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null

$itemsToCopy = @(
    "app.py",
    "main.py",
    "desktop_main.py",
    "start_windows_dev_optimizer.ps1",
    "framework",
    "modules",
    "templates",
    "config",
    "requirements_framework.txt",
    "requirements.txt",
    "README.md",
    "setup.ps1",
    ".env.example"
)

foreach ($item in $itemsToCopy) {
    $sourcePath = Join-Path $projectRoot $item
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath -Destination $packageRoot -Recurse -Force
    }
}

# Create installer script inside package
$installScriptPath = Join-Path $packageRoot "install.ps1"
$installScript = @'
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\Avila\WindowsDevOptimizer",
    [switch]$SkipVenv
)

Write-Host "🔧 Windows Dev Optimizer Installer" -ForegroundColor Cyan

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

Write-Host "Copying application files to $InstallDir"
Copy-Item (Join-Path $sourceDir '*') $InstallDir -Recurse -Force

if (-not $SkipVenv) {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "Python 3.10+ is required. Please install Python and ensure it is on PATH."
    }

    $venvPath = Join-Path $InstallDir ".venv"
    if (-not (Test-Path $venvPath)) {
        Write-Host "Creating isolated Python environment..."
        & $python.Path -m venv $venvPath
    }

    $venvPython = Join-Path $venvPath "Scripts\python.exe"
    Write-Host "Installing dependencies..."
    & $venvPython -m pip install --upgrade pip > $null
    & $venvPython -m pip install -r (Join-Path $InstallDir "requirements_framework.txt")
}
else {
    Write-Host "Skipping virtual environment setup as requested."
}

$launcherScript = Join-Path $InstallDir "launch_windows_dev_optimizer.ps1"
@"
param(
    [switch]`$NoBrowser
)

`$root = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$venvPython = Join-Path `$root '.venv\Scripts\python.exe'

if (Test-Path `$venvPython) {
    `$pythonExe = `$venvPython
} else {
    `$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not `$pythonCmd) {
        Write-Error 'Python executable not found. Please install Python 3.10+.'
        exit 1
    }
    `$pythonExe = `$pythonCmd.Path
}

if (-not `$NoBrowser) {
    Start-Process 'http://127.0.0.1:8000' | Out-Null
}

Set-Location `$root
Write-Host 'Starting Windows Dev Optimizer...' -ForegroundColor Cyan
`$pythonExe 'app.py'
"@ | Set-Content -Path $launcherScript -Encoding UTF8

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Windows Dev Optimizer.lnk"

Write-Host "Creating desktop shortcut at $shortcutPath"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "pwsh.exe"
$shortcut.Arguments = "-NoLogo -ExecutionPolicy Bypass -File `"$launcherScript`""
$shortcut.WorkingDirectory = $InstallDir
$shortcut.IconLocation = "$env:SystemRoot\system32\shell32.dll,109"
$shortcut.Description = "Launch Windows Dev Optimizer"
$shortcut.Save()

Write-Host "✅ Installation complete." -ForegroundColor Green
Write-Host "Launch the app from the desktop icon or by running $launcherScript"
'@
Set-Content -Path $installScriptPath -Value $installScript -Encoding UTF8

$summary = @"
Windows Dev Optimizer Installer
===============================

Created: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Package: $packageName

Included Components:
- Application source (FastAPI + HTMX interface)
- Framework modules and services
- Privacy-first telemetry service
- Configuration templates and sample environment
- Automated installer (install.ps1)
- Launcher script (launch_windows_dev_optimizer.ps1)
- Desktop shortcut creation

Installation:
1. Extract the ZIP file to a temporary directory.
2. Run install.ps1 (right-click -> Run with PowerShell).
3. Follow on-screen prompts. A desktop shortcut is created automatically.

Uninstall:
Delete the installation directory (default %LOCALAPPDATA%\Avila\WindowsDevOptimizer) and remove the desktop shortcut.
"@
Set-Content (Join-Path $packageRoot "INSTALLATION_SUMMARY.txt") $summary -Encoding UTF8

$zipPath = Join-Path $OutputDirectory "$packageName.zip"
if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path (Join-Path $packageRoot '*') -DestinationPath $zipPath -Force

Set-Content (Join-Path $OutputDirectory "$packageName-summary.txt") $summary -Encoding UTF8

Remove-Item $buildRoot -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Installer package created at $zipPath" -ForegroundColor Green
