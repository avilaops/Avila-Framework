# Script PowerShell para enviar relatório executivo
# Uso: .\send_report.ps1 [tipo_relatorio] -To "destinatario@exemplo.com"

param(
    [Parameter(Position=0)]
    [string]$ReportType = "dashboard",
    
    [Parameter(Mandatory=$false)]
    [string]$To,
    
    [Parameter(Mandatory=$false)]
    [string]$Subject,
    
    [switch]$SkipGeneration
)

$pythonExe = "C:/Program Files/Python313/python.exe"
$scriptPath = "analytics/reporting/generate_dashboard_email.py"

# Verifica se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "Arquivo .env nao encontrado!" -ForegroundColor Red
    Write-Host "Copie .env.example para .env e configure suas credenciais:" -ForegroundColor Yellow
    Write-Host "   cp .env.example .env" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Veja docs/analytics/email_setup_guide.md para instrucoes detalhadas" -ForegroundColor Yellow
    exit 1
}

# Carrega .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.+?)\s*$') {
        $name = $matches[1]
        $value = $matches[2]
        # Remove aspas
        $value = $value -replace '^["'']|["'']$', ''
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

# Monta comando
$cmd = @(
    $pythonExe,
    $scriptPath,
    "--send-email",
    "--report-type",
    $ReportType
)

if ($To) {
    $cmd += "--to"
    $cmd += $To
} elseif ($env:TO_EMAIL) {
    $cmd += "--to"
    $cmd += $env:TO_EMAIL
} else {
    Write-Host "Destinatario nao especificado!" -ForegroundColor Red
    Write-Host "Use: .\send_report.ps1 marketing_plan -To 'email@exemplo.com'" -ForegroundColor Yellow
    Write-Host "Ou configure TO_EMAIL no arquivo .env" -ForegroundColor Yellow
    exit 1
}

if ($Subject) {
    $cmd += "--subject"
    $cmd += $Subject
}

# Executa
Write-Host "Gerando e enviando relatorio..." -ForegroundColor Cyan
& $cmd[0] $cmd[1..($cmd.Length-1)]

if ($LASTEXITCODE -eq 0) {
    Write-Host "Relatorio enviado com sucesso!" -ForegroundColor Green
} else {
    Write-Host "Erro ao enviar relatorio" -ForegroundColor Red
    exit $LASTEXITCODE
}
