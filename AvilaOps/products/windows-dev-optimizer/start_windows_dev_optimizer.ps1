param(
    [switch]$NoBrowser
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "Python executable not found. Please install Python 3.10+ and ensure it is on PATH." -ForegroundColor Red
    exit 1
}

if ($NoBrowser) {
    Write-Host "Launching Windows Dev Optimizer in server mode..." -ForegroundColor Cyan
    & $pythonCmd.Path "app.py"
} else {
    Write-Host "Launching Windows Dev Optimizer desktop experience..." -ForegroundColor Cyan
    & $pythonCmd.Path "desktop_main.py"
}
