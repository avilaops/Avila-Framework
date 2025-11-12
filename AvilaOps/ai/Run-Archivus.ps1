# ???????????????????????????????????????????????????????????????????????????
# SCRIPT DE AUTOMAÇÃO - AGENTE ARCHIVUS
# Ávila Inc / Ávila Ops
# ???????????????????????????????????????????????????????????????????????????
# Função: Executar rotinas do Agente Archivus e agendar no Task Scheduler
# ???????????????????????????????????????????????????????????????????????????

param(
    [switch]$Install,  # Instala/atualiza o agendamento
  [switch]$Uninstall,      # Remove o agendamento
    [switch]$RunNow,         # Executa imediatamente
    [switch]$Status    # Mostra status do agendamento
)

# Configurações
$TaskName = "Avila_Archivus_Daily"
$PythonScript = "C:\Users\nicol\OneDrive\Avila\AvilaOps\Agente Bibliotecario (Archivus)\archivus_main.py"
$LogPath = "C:\Users\nicol\OneDrive\Avila\Logs\Daily"

# ???????????????????????????????????????????????????????????????????????????
# FUNÇÕES
# ???????????????????????????????????????????????????????????????????????????

function Write-ArchivusLog {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
  $logEntry = "[$timestamp] [$Level] $Message"
    
    Write-Host $logEntry -ForegroundColor $(
     switch ($Level) {
    "INFO" { "Cyan" }
            "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
      "ERROR" { "Red" }
            default { "White" }
}
    )
}

function Install-ArchivusSchedule {
    Write-ArchivusLog "Instalando agendamento do Archivus..." "INFO"
    
    try {
# Verificar se Python está instalado
        $pythonPath = (Get-Command python -ErrorAction Stop).Source
        Write-ArchivusLog "Python encontrado: $pythonPath" "INFO"
        
        # Remover tarefa existente se houver
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
        
    # Criar ação
        $action = New-ScheduledTaskAction `
            -Execute $pythonPath `
            -Argument "`"$PythonScript`"" `
    -WorkingDirectory (Split-Path $PythonScript)
        
        # Criar trigger diário às 02:00
        $trigger = New-ScheduledTaskTrigger -Daily -At "02:00"
        
        # Configurações adicionais
      $settings = New-ScheduledTaskSettingsSet `
            -AllowStartIfOnBatteries `
            -DontStopIfGoingOnBatteries `
     -StartWhenAvailable `
          -RunOnlyIfNetworkAvailable:$false
        
 # Registrar tarefa
        Register-ScheduledTask `
            -TaskName $TaskName `
   -Action $action `
      -Trigger $trigger `
 -Settings $settings `
     -Description "Rotina diária do Agente Bibliotecário (Archivus) - Ávila Inc/Ops" `
       -User $env:USERNAME `
            -RunLevel Highest | Out-Null
        
        Write-ArchivusLog "? Agendamento instalado com sucesso!" "SUCCESS"
        Write-ArchivusLog "Próxima execução: Diariamente às 02:00" "INFO"
        
    } catch {
        Write-ArchivusLog "? Erro ao instalar agendamento: $_" "ERROR"
    }
}

function Uninstall-ArchivusSchedule {
    Write-ArchivusLog "Removendo agendamento do Archivus..." "INFO"
    
  try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction Stop
        Write-ArchivusLog "? Agendamento removido com sucesso!" "SUCCESS"
    } catch {
 Write-ArchivusLog "??  Agendamento não encontrado ou já removido." "WARNING"
    }
}

function Get-ArchivusStatus {
    Write-ArchivusLog "Verificando status do Archivus..." "INFO"
    Write-Host ""
    
    # Status do agendamento
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    
    if ($task) {
        Write-Host "?? Agendamento" -ForegroundColor Cyan
        Write-Host "Status: " -NoNewline
  Write-Host $task.State -ForegroundColor $(if ($task.State -eq "Ready") { "Green" } else { "Yellow" })
        Write-Host "  Próxima execução: " -NoNewline
        
        $nextRun = (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime
        if ($nextRun) {
  Write-Host $nextRun.ToString("yyyy-MM-dd HH:mm:ss") -ForegroundColor Green
        } else {
         Write-Host "Não agendado" -ForegroundColor Yellow
 }
 
        $lastRun = (Get-ScheduledTaskInfo -TaskName $TaskName).LastRunTime
        if ($lastRun -and $lastRun -ne (Get-Date "1/1/1")) {
            Write-Host "  Última execução: " -NoNewline
     Write-Host $lastRun.ToString("yyyy-MM-dd HH:mm:ss") -ForegroundColor Cyan
        }
    } else {
Write-Host "? Agendamento não instalado" -ForegroundColor Red
     Write-Host "   Execute: .\Run-Archivus.ps1 -Install" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
    # Último log
    $todayLog = "$LogPath\archivus_$(Get-Date -Format 'yyyy-MM-dd').log"
    if (Test-Path $todayLog) {
        Write-Host "?? Último Log (hoje)" -ForegroundColor Cyan
        Get-Content $todayLog -Tail 10 | ForEach-Object {
            Write-Host "  $_" -ForegroundColor DarkGray
        }
    } else {
  Write-Host "?? Nenhum log hoje" -ForegroundColor Yellow
    }
    
    Write-Host ""
    
    # Último relatório
    $reportPath = "C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Auditorias"
    $lastReport = Get-ChildItem $reportPath -Filter "AUDITORIA_ARCHIVUS_*.md" -ErrorAction SilentlyContinue | 
        Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1
    
    if ($lastReport) {
        Write-Host "?? Último Relatório" -ForegroundColor Cyan
      Write-Host "  Arquivo: " -NoNewline
        Write-Host $lastReport.Name -ForegroundColor Green
        Write-Host "  Data: " -NoNewline
        Write-Host $lastReport.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss") -ForegroundColor Cyan
    } else {
    Write-Host "?? Nenhum relatório encontrado" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

function Invoke-ArchivusNow {
    Write-ArchivusLog "Executando Archivus agora..." "INFO"
    Write-Host ""
    
    try {
        # Executar script Python
        python $PythonScript
        
        Write-Host ""
        Write-ArchivusLog "? Execução concluída!" "SUCCESS"
        
  # Mostrar último relatório gerado
        $reportPath = "C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Auditorias"
  $lastReport = Get-ChildItem $reportPath -Filter "AUDITORIA_ARCHIVUS_*.md" -ErrorAction SilentlyContinue | 
            Sort-Object LastWriteTime -Descending | 
         Select-Object -First 1
        
    if ($lastReport) {
            Write-ArchivusLog "Relatório gerado: $($lastReport.Name)" "INFO"
        }
        
    } catch {
        Write-ArchivusLog "? Erro durante execução: $_" "ERROR"
    }
}

# ???????????????????????????????????????????????????????????????????????????
# EXECUÇÃO PRINCIPAL
# ???????????????????????????????????????????????????????????????????????????

Write-Host ""
Write-Host "???????????????????????????????????????????????????????????" -ForegroundColor Cyan
Write-Host "  AGENTE BIBLIOTECÁRIO - ARCHIVUS" -ForegroundColor Cyan
Write-Host "  Ávila Inc / Ávila Ops" -ForegroundColor Cyan
Write-Host "???????????????????????????????????????????????????????????" -ForegroundColor Cyan
Write-Host ""

if ($Install) {
    Install-ArchivusSchedule
    Write-Host ""
    Get-ArchivusStatus
}
elseif ($Uninstall) {
    Uninstall-ArchivusSchedule
}
elseif ($RunNow) {
    Invoke-ArchivusNow
}
elseif ($Status) {
    Get-ArchivusStatus
}
else {
    # Menu interativo
    Write-Host "Escolha uma opção:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Instalar/Atualizar agendamento" -ForegroundColor Cyan
    Write-Host "  2. Executar agora (manual)" -ForegroundColor Cyan
    Write-Host "  3. Ver status" -ForegroundColor Cyan
    Write-Host "  4. Remover agendamento" -ForegroundColor Cyan
    Write-Host "  5. Sair" -ForegroundColor Cyan
  Write-Host ""
    
    $choice = Read-Host "Digite o número da opção"
    
    switch ($choice) {
        "1" { 
          Write-Host ""
       Install-ArchivusSchedule 
     Write-Host ""
  Get-ArchivusStatus
        }
        "2" { 
            Write-Host ""
            Invoke-ArchivusNow 
        }
        "3" { 
        Write-Host ""
            Get-ArchivusStatus 
    }
     "4" { 
            Write-Host ""
            Uninstall-ArchivusSchedule 
        }
        "5" { 
            Write-Host ""
  Write-ArchivusLog "Saindo..." "INFO"
   }
        default { 
            Write-Host ""
 Write-ArchivusLog "Opção inválida!" "ERROR" 
     }
    }
}

Write-Host ""
