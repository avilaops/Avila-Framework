# Script PowerShell para Agendar Envio Automático de Relatórios
# Uso: .\setup_scheduler.ps1

$ErrorActionPreference = "Stop"

Write-Host "🗓️  Configurando Agendamento de Relatórios Ávila" -ForegroundColor Cyan
Write-Host ""

# Caminhos
$repoRoot = $PSScriptRoot
$pythonExe = "C:/Program Files/Python313/python.exe"
$scriptPath = Join-Path $repoRoot "analytics\reporting\generate_dashboard_email.py"
$envFile = Join-Path $repoRoot ".env"

# Verifica dependências
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python não encontrado em: $pythonExe" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ Script não encontrado em: $scriptPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $envFile)) {
    Write-Host "❌ Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "   Configure .env antes de agendar" -ForegroundColor Yellow
    exit 1
}

# Menu de opções
Write-Host "Escolha o tipo de agendamento:" -ForegroundColor Yellow
Write-Host "1. Relatório Diário (Segunda a Sexta, 8h)"
Write-Host "2. Relatório Semanal (Segundas, 9h)"
Write-Host "3. Ambos"
Write-Host "4. Personalizado"
Write-Host ""
$choice = Read-Host "Opção"

function Create-ScheduledTask {
    param(
        [string]$TaskName,
        [string]$Description,
        [string]$TriggerSchedule,
        [string]$Subject
    )
    
    # Remove tarefa existente se houver
    $existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "⚠️  Removendo tarefa existente: $TaskName" -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }
    
    # Ação: executar script Python
    $action = New-ScheduledTaskAction `
        -Execute $pythonExe `
        -Argument "$scriptPath --send-email --subject `"$Subject`"" `
        -WorkingDirectory $repoRoot
    
    # Trigger baseado no tipo
    switch ($TriggerSchedule) {
        "Daily" {
            $trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
            # Configura apenas dias úteis
            $trigger.DaysOfWeek = "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        }
        "Weekly" {
            $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "09:00"
        }
    }
    
    # Configurações
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable
    
    # Registra tarefa
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $Description `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -User $env:USERNAME `
        -RunLevel Highest
    
    Write-Host "✅ Tarefa criada: $TaskName" -ForegroundColor Green
}

# Cria tarefas baseado na escolha
switch ($choice) {
    "1" {
        Create-ScheduledTask `
            -TaskName "Avila-Relatorio-Diario" `
            -Description "Envio automático de relatório diário Ávila Inc" `
            -TriggerSchedule "Daily" `
            -Subject "Relatório Diário — $(Get-Date -Format 'dd/MM/yyyy')"
    }
    "2" {
        Create-ScheduledTask `
            -TaskName "Avila-Relatorio-Semanal" `
            -Description "Envio automático de relatório semanal Ávila Inc" `
            -TriggerSchedule "Weekly" `
            -Subject "Relatório Executivo Semanal"
    }
    "3" {
        Create-ScheduledTask `
            -TaskName "Avila-Relatorio-Diario" `
            -Description "Envio automático de relatório diário Ávila Inc" `
            -TriggerSchedule "Daily" `
            -Subject "Relatório Diário — $(Get-Date -Format 'dd/MM/yyyy')"
        
        Create-ScheduledTask `
            -TaskName "Avila-Relatorio-Semanal" `
            -Description "Envio automático de relatório semanal Ávila Inc" `
            -TriggerSchedule "Weekly" `
            -Subject "Relatório Executivo Semanal"
    }
    "4" {
        Write-Host "Use o Agendador de Tarefas do Windows para personalizar" -ForegroundColor Yellow
        Start-Process taskschd.msc
    }
    default {
        Write-Host "❌ Opção inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Agendamento concluído!" -ForegroundColor Green
Write-Host ""
Write-Host "Para gerenciar tarefas:" -ForegroundColor Cyan
Write-Host "  - Abra 'Agendador de Tarefas' (taskschd.msc)"
Write-Host "  - Procure por 'Avila-Relatorio-*'"
Write-Host ""
Write-Host "Para testar agora:" -ForegroundColor Cyan
Write-Host "  .\send_report.ps1" -ForegroundColor Yellow
