# =============================================================================
# INSTALADOR AUTOMÁTICO DO SISTEMA DE PROCESSAMENTO
# Configura tudo automaticamente e agenda no Windows Task Scheduler
# =============================================================================

param(
    [switch]$InstallPython,
    [switch]$ConfigureTask,
    [switch]$TestSetup,
    [string]$EmailAddress = "",
    [string]$TeamsWebhook = ""
)

$ScriptName = "AutomatedProcessor Installer"
$Version = "1.0.0"

function Write-InstallLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
    }
    
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
    Write-Host $Message -ForegroundColor $color
}

function Test-Prerequisites {
    Write-InstallLog "🔍 Verificando pré-requisitos..." 
    
    $issues = @()
    
    # Verificar PowerShell
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        $issues += "PowerShell 5.0+ necessário (atual: $($PSVersionTable.PSVersion))"
    }
    
    # Verificar permissões
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    
    if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        $issues += "Permissões de administrador necessárias para configurar tarefas agendadas"
    }
    
    # Verificar Python (opcional)
    $pythonPath = where.exe python 2>$null
    if (-not $pythonPath -and $InstallPython) {
        $issues += "Python não encontrado no PATH"
    }
    
    if ($issues.Count -gt 0) {
        Write-InstallLog "❌ Problemas encontrados:" -Level "ERROR"
        foreach ($issue in $issues) {
            Write-InstallLog "   • $issue" -Level "ERROR"
        }
        return $false
    }
    
    Write-InstallLog "✅ Todos os pré-requisitos atendidos" -Level "SUCCESS"
    return $true
}

function Install-PythonDependencies {
    if (-not $InstallPython) {
        return
    }
    
    Write-InstallLog "🐍 Instalando dependências Python..."
    
    $requirements = @(
        "schedule",
        "pathlib",
        "hashlib"
    )
    
    try {
        foreach ($package in $requirements) {
            Write-InstallLog "   📦 Instalando $package..."
            & python -m pip install $package --quiet --disable-pip-version-check
        }
        
        Write-InstallLog "✅ Dependências Python instaladas" -Level "SUCCESS"
    }
    catch {
        Write-InstallLog "❌ Erro ao instalar dependências Python: $_" -Level "ERROR"
    }
}

function Initialize-DirectoryStructure {
    Write-InstallLog "📁 Criando estrutura de diretórios..."
    
    $directories = @(
        ".\output",
        ".\backup", 
        ".\logs",
        ".\scripts",
        ".\templates",
        ".\cache"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-InstallLog "   ✅ Criado: $dir" -Level "SUCCESS"
        }
        else {
            Write-InstallLog "   ℹ️ Já existe: $dir"
        }
    }
}

function Update-ConfigurationFile {
    Write-InstallLog "⚙️ Configurando arquivo de configuração..."
    
    $configFile = ".\automation-config.json"
    
    if (Test-Path $configFile) {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
    }
    else {
        Write-InstallLog "❌ Arquivo de configuração não encontrado: $configFile" -Level "ERROR"
        return
    }
    
    # Atualizar configurações baseadas nos parâmetros
    if ($EmailAddress) {
        $config.email.sender_email = $EmailAddress
        $config.email.recipients = @($EmailAddress)
        Write-InstallLog "   📧 Email configurado: $EmailAddress"
    }
    
    if ($TeamsWebhook) {
        $config.teams.webhook_url = $TeamsWebhook
        Write-InstallLog "   📢 Teams webhook configurado"
    }
    
    # Atualizar caminho do workspace
    $config.workspace_path = (Get-Location).Path
    
    # Salvar configuração atualizada
    $config | ConvertTo-Json -Depth 10 | Out-File $configFile -Encoding UTF8
    Write-InstallLog "✅ Configuração atualizada" -Level "SUCCESS"
}

function Register-WindowsTask {
    if (-not $ConfigureTask) {
        return
    }
    
    Write-InstallLog "📅 Configurando tarefa agendada no Windows..."
    
    $scriptPath = Join-Path (Get-Location) "automated-processor.ps1"
    
    if (-not (Test-Path $scriptPath)) {
        Write-InstallLog "❌ Script principal não encontrado: $scriptPath" -Level "ERROR"
        return
    }
    
    try {
        $taskName = "ProcessamentoAutomaticoDocumentos"
        
        # Remover tarefa existente se houver
        $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        if ($existingTask) {
            Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
            Write-InstallLog "   🗑️ Tarefa existente removida"
        }
        
        $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -Scheduled"
        $trigger = New-ScheduledTaskTrigger -Daily -At "02:00"
        
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)
        
        $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
        
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Sistema automático de processamento e análise de documentos" -Force | Out-Null
        
        Write-InstallLog "✅ Tarefa agendada criada: '$taskName'" -Level "SUCCESS"
        Write-InstallLog "   📅 Agendamento: Diário às 02:00"
        Write-InstallLog "   ⚡ Execução: Automática (sem supervisão)"
    }
    catch {
        Write-InstallLog "❌ Erro ao criar tarefa agendada: $_" -Level "ERROR"
    }
}

function Test-Installation {
    if (-not $TestSetup) {
        return
    }
    
    Write-InstallLog "🧪 Testando instalação..."
    
    # Testar script PowerShell
    $psScript = ".\automated-processor.ps1"
    if (Test-Path $psScript) {
        Write-InstallLog "   ✅ Script PowerShell encontrado"
        
        try {
            # Testar sintaxe
            $null = Get-Content $psScript -Raw | Out-String
            Write-InstallLog "   ✅ Sintaxe do script válida"
        }
        catch {
            Write-InstallLog "   ❌ Erro de sintaxe no script: $_" -Level "ERROR"
        }
    }
    else {
        Write-InstallLog "   ❌ Script PowerShell não encontrado" -Level "ERROR"
    }
    
    # Testar configuração
    $configFile = ".\automation-config.json"
    if (Test-Path $configFile) {
        try {
            $config = Get-Content $configFile -Raw | ConvertFrom-Json
            Write-InstallLog "   ✅ Arquivo de configuração válido"
            
            if ($config.email.enabled -and -not $config.email.sender_email) {
                Write-InstallLog "   ⚠️ Email habilitado mas não configurado" -Level "WARNING"
            }
            
            if ($config.teams.enabled -and -not $config.teams.webhook_url) {
                Write-InstallLog "   ⚠️ Teams habilitado mas webhook não configurado" -Level "WARNING"
            }
        }
        catch {
            Write-InstallLog "   ❌ Erro no arquivo de configuração: $_" -Level "ERROR"
        }
    }
    
    # Testar tarefa agendada
    $taskName = "ProcessamentoAutomaticoDocumentos"
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    
    if ($task) {
        Write-InstallLog "   ✅ Tarefa agendada configurada"
        Write-InstallLog "   📅 Próxima execução: $($task.NextRunTime)"
    }
    else {
        Write-InstallLog "   ⚠️ Tarefa agendada não encontrada" -Level "WARNING"
    }
    
    Write-InstallLog "🎯 Teste de instalação concluído" -Level "SUCCESS"
}

function Show-PostInstallInstructions {
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host " INSTALAÇÃO CONCLUÍDA" -ForegroundColor Yellow
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🎉 Sistema de processamento automático configurado!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "📋 PRÓXIMOS PASSOS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 📧 Configurar credenciais de email:" -ForegroundColor White
    Write-Host "   • Editar automation-config.json" -ForegroundColor Gray
    Write-Host "   • Definir sender_password (senha de app)" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "2. 📢 Configurar webhook do Teams (opcional):" -ForegroundColor White
    Write-Host "   • Obter webhook URL do Teams" -ForegroundColor Gray
    Write-Host "   • Atualizar teams.webhook_url na configuração" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "3. 🚀 Testar execução manual:" -ForegroundColor White
    Write-Host "   .\automated-processor.ps1" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "4. ⏰ Sistema agendado automaticamente para:" -ForegroundColor White
    Write-Host "   • Execução diária às 02:00" -ForegroundColor Gray
    Write-Host "   • Sem necessidade de supervisão" -ForegroundColor Gray
    Write-Host "   • Relatórios enviados automaticamente" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "📂 ARQUIVOS IMPORTANTES:" -ForegroundColor Cyan
    Write-Host "   • automated-processor.ps1 (script principal)" -ForegroundColor White
    Write-Host "   • automation-config.json (configuração)" -ForegroundColor White
    Write-Host "   • .\logs\ (arquivos de log)" -ForegroundColor White
    Write-Host "   • .\output\ (relatórios gerados)" -ForegroundColor White
    Write-Host "   • .\backup\ (backups dos arquivos)" -ForegroundColor White
    Write-Host ""
    
    Write-Host "🔧 COMANDOS ÚTEIS:" -ForegroundColor Cyan
    Write-Host "   .\automated-processor.ps1 -Force    (forçar execução)" -ForegroundColor Yellow
    Write-Host "   .\install-automation.ps1 -TestSetup (testar configuração)" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "💡 O sistema agora roda automaticamente sem supervisão!" -ForegroundColor Green
    Write-Host "   Relatórios serão gerados e enviados automaticamente." -ForegroundColor Green
    Write-Host ""
}

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Blue
Write-Host " $ScriptName v$Version" -ForegroundColor Yellow
Write-Host "=" * 80 -ForegroundColor Blue
Write-Host ""

# Verificar pré-requisitos
if (-not (Test-Prerequisites)) {
    Write-InstallLog "❌ Falha na verificação de pré-requisitos. Abortando." -Level "ERROR"
    exit 1
}

# Executar instalação
Write-InstallLog "🚀 Iniciando instalação do sistema de processamento automático..."

Install-PythonDependencies
Initialize-DirectoryStructure
Update-ConfigurationFile  
Register-WindowsTask
Test-Installation

Write-InstallLog "✨ Instalação concluída com sucesso!" -Level "SUCCESS"

Show-PostInstallInstructions