# =============================================================================
# PROCESSADOR AUTOMÁTICO POWERSHELL
# Versão PowerShell para integração com Windows Task Scheduler
# =============================================================================

param(
    [switch]$Scheduled,
    [switch]$Force,
    [switch]$SetupTask,
    [string]$ConfigFile = ".\automation-config.json"
)

# Configurações globais
$ScriptName = "AutomatedProcessor"
$Version = "2.0.0"
$LogDirectory = ".\logs"
$OutputDirectory = ".\output"
$BackupDirectory = ".\backup"
$LastRunFile = ".\.lastrun.json"

# =============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# =============================================================================

function Initialize-Configuration {
    param([string]$ConfigPath)
    
    $DefaultConfig = @{
        workspace_path = (Get-Location).Path
        output_path = ".\output"
        backup_path = ".\backup"
        email = @{
            enabled = $true
            smtp_server = "smtp-mail.outlook.com"
            smtp_port = 587
            sender_email = "sistema@empresa.com"
            sender_password = "APP_PASSWORD_HERE"
            recipients = @("gerente@empresa.com", "ti@empresa.com")
        }
        teams = @{
            enabled = $true
            webhook_url = "https://outlook.office.com/webhook/..."
        }
        processing = @{
            auto_cleanup = $true
            create_backup = $true
            deep_analysis = $true
            max_file_size_mb = 50
            file_extensions = @(".md", ".txt", ".json", ".yml", ".yaml", ".py", ".ps1")
        }
        exclusions = @{
            patterns = @("*.tmp", "*.log", "*.cache", "*backup*", "*temp*")
            directories = @("node_modules", "__pycache__", ".git", "backup", "cache", "logs")
        }
        schedule = @{
            enabled = $true
            frequency = "Daily"
            time = "02:00"
        }
    }
    
    if (Test-Path $ConfigPath) {
        try {
            $UserConfig = Get-Content $ConfigPath -Raw | ConvertFrom-Json -AsHashtable
            # Merge configurations
            foreach ($key in $UserConfig.Keys) {
                $DefaultConfig[$key] = $UserConfig[$key]
            }
        }
        catch {
            Write-Log "Erro ao carregar configuração: $_" -Level "ERROR"
        }
    }
    else {
        # Criar arquivo de configuração padrão
        $DefaultConfig | ConvertTo-Json -Depth 10 | Out-File $ConfigPath -Encoding UTF8
        Write-Log "Arquivo de configuração criado: $ConfigPath"
    }
    
    return $DefaultConfig
}

# =============================================================================
# SISTEMA DE LOGS
# =============================================================================

function Initialize-Logging {
    if (-not (Test-Path $LogDirectory)) {
        New-Item -ItemType Directory -Path $LogDirectory -Force | Out-Null
    }
    
    $global:LogFile = Join-Path $LogDirectory "processor_$(Get-Date -Format 'yyyyMMdd').log"
}

function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARNING", "ERROR", "SUCCESS")]
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "$timestamp - $Level - $Message"
    
    # Escrever no arquivo de log
    Add-Content -Path $global:LogFile -Value $logEntry -Encoding UTF8
    
    # Exibir no console com cores
    $color = switch ($Level) {
        "INFO" { "White" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        "SUCCESS" { "Green" }
    }
    
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
    Write-Host "$Message" -ForegroundColor $color
}

# =============================================================================
# FUNÇÕES DE PROCESSAMENTO
# =============================================================================

function Test-ShouldExcludeFile {
    param(
        [System.IO.FileInfo]$File,
        [hashtable]$Config
    )
    
    $fileName = $File.Name.ToLower()
    $filePath = $File.FullName.ToLower()
    
    # Verificar padrões de exclusão
    foreach ($pattern in $Config.exclusions.patterns) {
        if ($fileName -like $pattern) {
            return $true
        }
    }
    
    # Verificar diretórios excluídos
    foreach ($dir in $Config.exclusions.directories) {
        if ($filePath -like "*\$($dir.ToLower())\*") {
            return $true
        }
    }
    
    # Verificar tamanho do arquivo
    $maxSize = $Config.processing.max_file_size_mb * 1MB
    if ($File.Length -gt $maxSize) {
        return $true
    }
    
    return $false
}

function Get-FileHash {
    param([string]$FilePath)
    
    try {
        $hash = Get-FileHash -Path $FilePath -Algorithm MD5
        return $hash.Hash
    }
    catch {
        return "ERROR"
    }
}

function Get-ValidFiles {
    param(
        [string]$WorkspacePath,
        [hashtable]$Config
    )
    
    Write-Log "🔍 Escaneando workspace: $WorkspacePath"
    
    $validFiles = @()
    
    foreach ($extension in $Config.processing.file_extensions) {
        $files = Get-ChildItem -Path $WorkspacePath -Filter "*$extension" -Recurse -File -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            if (-not (Test-ShouldExcludeFile -File $file -Config $Config)) {
                $validFiles += $file
            }
        }
    }
    
    Write-Log "✅ Encontrados $($validFiles.Count) arquivos válidos" -Level "SUCCESS"
    return $validFiles
}

function Test-HasChanges {
    param(
        [array]$Files,
        [string]$LastRunFile
    )
    
    if (-not (Test-Path $LastRunFile)) {
        return $true
    }
    
    try {
        $lastRun = Get-Content $LastRunFile -Raw | ConvertFrom-Json
        
        $currentHashes = @{}
        foreach ($file in $Files) {
            $currentHashes[$file.FullName] = Get-FileHash -FilePath $file.FullName
        }
        
        $lastHashes = @{}
        if ($lastRun.file_hashes) {
            $lastRun.file_hashes.PSObject.Properties | ForEach-Object {
                $lastHashes[$_.Name] = $_.Value
            }
        }
        
        # Comparar hashes
        $changesDetected = $false
        
        foreach ($filePath in $currentHashes.Keys) {
            if ($lastHashes[$filePath] -ne $currentHashes[$filePath]) {
                $changesDetected = $true
                break
            }
        }
        
        if ($currentHashes.Count -ne $lastHashes.Count) {
            $changesDetected = $true
        }
        
        if ($changesDetected) {
            Write-Log "🔄 Mudanças detectadas no workspace" -Level "INFO"
        }
        else {
            Write-Log "ℹ️ Nenhuma mudança detectada desde a última execução" -Level "INFO"
        }
        
        return $changesDetected
    }
    catch {
        Write-Log "Erro ao verificar mudanças: $_" -Level "WARNING"
        return $true
    }
}

function New-Backup {
    param(
        [array]$Files,
        [string]$BackupPath
    )
    
    if (-not (Test-Path $BackupPath)) {
        New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = Join-Path $BackupPath "backup_$timestamp"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    Write-Log "📦 Criando backup em: $backupDir"
    
    foreach ($file in $Files) {
        try {
            $relativePath = $file.FullName.Substring($PWD.Path.Length + 1)
            $backupFilePath = Join-Path $backupDir $relativePath
            $backupFileDir = Split-Path $backupFilePath -Parent
            
            if (-not (Test-Path $backupFileDir)) {
                New-Item -ItemType Directory -Path $backupFileDir -Force | Out-Null
            }
            
            Copy-Item -Path $file.FullName -Destination $backupFilePath -Force
        }
        catch {
            Write-Log "Erro ao fazer backup de $($file.Name): $_" -Level "WARNING"
        }
    }
    
    Write-Log "✅ Backup concluído" -Level "SUCCESS"
}

function Get-FileAnalysis {
    param([System.IO.FileInfo]$File)
    
    try {
        $content = Get-Content -Path $File.FullName -Raw -Encoding UTF8 -ErrorAction Stop
        
        # Análise básica
        $lines = ($content -split "`n").Count
        $words = ($content -split '\s+').Count
        $characters = $content.Length
        
        # Detectar tópicos-chave
        $keywords = @(
            'azure', 'aws', 'kubernetes', 'docker', 'api', 'database',
            'python', 'javascript', 'powershell', 'sql', 'git',
            'deployment', 'configuration', 'security', 'automation',
            'testing', 'ci/cd', 'devops', 'infrastructure', 'monitoring'
        )
        
        $foundTopics = @()
        $contentLower = $content.ToLower()
        
        foreach ($keyword in $keywords) {
            if ($contentLower -contains $keyword) {
                $foundTopics += $keyword
            }
        }
        
        # Detectar se contém código
        $codeIndicators = @('function', 'class', 'import', 'def ', 'var ', 'let ', 'const ')
        $hasCode = $false
        
        foreach ($indicator in $codeIndicators) {
            if ($contentLower -contains $indicator) {
                $hasCode = $true
                break
            }
        }
        
        return @{
            file = $File.FullName
            name = $File.Name
            size = $File.Length
            lines = $lines
            words = $words
            characters = $characters
            modified = $File.LastWriteTime
            extension = $File.Extension
            key_topics = $foundTopics
            has_code = $hasCode
            language = Get-LanguageFromExtension -Extension $File.Extension
        }
    }
    catch {
        Write-Log "Erro ao analisar $($File.Name): $_" -Level "WARNING"
        return @{
            file = $File.FullName
            name = $File.Name
            error = $_.Exception.Message
        }
    }
}

function Get-LanguageFromExtension {
    param([string]$Extension)
    
    $langMap = @{
        '.py' = 'Python'
        '.js' = 'JavaScript'
        '.ps1' = 'PowerShell'
        '.md' = 'Markdown'
        '.json' = 'JSON'
        '.yml' = 'YAML'
        '.yaml' = 'YAML'
        '.sql' = 'SQL'
        '.txt' = 'Text'
    }
    
    return $langMap[$Extension.ToLower()] ?? 'Unknown'
}

function New-ConsolidatedReport {
    param(
        [array]$Analyses,
        [hashtable]$Config
    )
    
    $timestamp = Get-Date
    
    # Estatísticas gerais
    $totalFiles = $Analyses.Count
    $totalSize = ($Analyses | Where-Object { $_.size } | Measure-Object -Property size -Sum).Sum
    $totalLines = ($Analyses | Where-Object { $_.lines } | Measure-Object -Property lines -Sum).Sum
    
    # Análises por categoria
    $extensions = @{}
    $languages = @{}
    $topics = @{}
    
    foreach ($analysis in $Analyses) {
        if ($analysis.extension) {
            $extensions[$analysis.extension] = ($extensions[$analysis.extension] ?? 0) + 1
        }
        
        if ($analysis.language) {
            $languages[$analysis.language] = ($languages[$analysis.language] ?? 0) + 1
        }
        
        foreach ($topic in $analysis.key_topics) {
            $topics[$topic] = ($topics[$topic] ?? 0) + 1
        }
    }
    
    $codeFiles = $Analyses | Where-Object { $_.has_code -eq $true }
    $largeFiles = $Analyses | Where-Object { $_.size } | Sort-Object size -Descending | Select-Object -First 10
    
    # Gerar relatório
    $report = @"
# RELATÓRIO AUTOMÁTICO DE ANÁLISE DE DOCUMENTOS

**Data de Geração:** $($timestamp.ToString('dd/MM/yyyy HH:mm:ss'))  
**Workspace:** $($Config.workspace_path)  
**Processamento:** Automático (sem intervenção humana)

---

## 📊 ESTATÍSTICAS GERAIS

- **Total de arquivos processados:** $totalFiles
- **Tamanho total:** $([math]::Round($totalSize / 1MB, 2)) MB
- **Total de linhas:** $($totalLines.ToString('N0'))
- **Arquivos com código:** $($codeFiles.Count)

## 📁 DISTRIBUIÇÃO POR TIPO

### Extensões de Arquivo
"@

    foreach ($ext in ($extensions.GetEnumerator() | Sort-Object Value -Descending)) {
        $report += "- **$($ext.Key)**: $($ext.Value) arquivo(s)`n"
    }
    
    $report += "`n### Linguagens Identificadas`n"
    foreach ($lang in ($languages.GetEnumerator() | Sort-Object Value -Descending)) {
        $report += "- **$($lang.Key)**: $($lang.Value) arquivo(s)`n"
    }
    
    $report += "`n## 🏷️ TÓPICOS PRINCIPAIS`n"
    foreach ($topic in ($topics.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 15)) {
        $report += "- **$($topic.Key)**: $($topic.Value) ocorrência(s)`n"
    }
    
    $report += "`n## 📈 ARQUIVOS MAIS RELEVANTES`n"
    for ($i = 0; $i -lt [Math]::Min(10, $largeFiles.Count); $i++) {
        $file = $largeFiles[$i]
        $sizeMB = [math]::Round($file.size / 1MB, 2)
        $report += "$($i + 1). **$($file.name)** ($sizeMB MB, $($file.lines) linhas)`n"
    }
    
    $nextRun = Get-NextRunTime -Config $Config
    
    $report += @"

## 🤖 PROCESSAMENTO AUTOMÁTICO

- **Última execução:** $($timestamp.ToString('dd/MM/yyyy HH:mm:ss'))
- **Próxima execução:** $nextRun
- **Status:** ✅ Concluído com sucesso
- **Arquivos processados automaticamente:** $totalFiles
- **Backup criado:** $(if ($Config.processing.create_backup) { '✅ Sim' } else { '❌ Não' })

## 📋 AÇÕES AUTOMÁTICAS REALIZADAS

1. ✅ Escaneamento automático do workspace
2. ✅ Filtro automático de arquivos relevantes
3. ✅ Análise de conteúdo e extração de tópicos
4. ✅ Geração automática de relatório
"@

    if ($Config.processing.create_backup) {
        $report += "5. ✅ Backup automático dos arquivos processados`n"
    }
    
    if ($Config.processing.auto_cleanup) {
        $report += "6. ✅ Limpeza automática de arquivos temporários`n"
    }
    
    $report += @"

---

*Este relatório foi gerado automaticamente pelo sistema de análise de documentos.*  
*Configurado para execução: $($Config.schedule.frequency) às $($Config.schedule.time)*

**Sistema:** $ScriptName v$Version  
**Plataforma:** PowerShell $($PSVersionTable.PSVersion)
"@

    return $report
}

function Get-NextRunTime {
    param([hashtable]$Config)
    
    $now = Get-Date
    $scheduleTime = [DateTime]::ParseExact($Config.schedule.time, "HH:mm", $null)
    $nextRun = $now.Date.Add($scheduleTime.TimeOfDay)
    
    switch ($Config.schedule.frequency) {
        "Daily" {
            if ($nextRun -le $now) {
                $nextRun = $nextRun.AddDays(1)
            }
        }
        "Weekly" {
            $daysUntilMonday = (8 - [int]$now.DayOfWeek) % 7
            if ($daysUntilMonday -eq 0 -and $nextRun -le $now) {
                $daysUntilMonday = 7
            }
            $nextRun = $nextRun.AddDays($daysUntilMonday)
        }
    }
    
    return $nextRun.ToString('dd/MM/yyyy HH:mm')
}

function Invoke-Cleanup {
    param([hashtable]$Config)
    
    if (-not $Config.processing.auto_cleanup) {
        return
    }
    
    Write-Log "🧹 Executando limpeza automática..."
    
    $cleanupPatterns = @('*.tmp', '*.log', '*.cache', '*~', '*.bak')
    $cleanedCount = 0
    
    foreach ($pattern in $cleanupPatterns) {
        $files = Get-ChildItem -Path $Config.workspace_path -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            try {
                Remove-Item $file.FullName -Force
                $cleanedCount++
                Write-Log "   🗑️ Removido: $($file.Name)"
            }
            catch {
                Write-Log "Erro ao remover $($file.Name): $_" -Level "WARNING"
            }
        }
    }
    
    Write-Log "✅ Limpeza concluída: $cleanedCount arquivo(s) removidos" -Level "SUCCESS"
}

function Send-EmailReport {
    param(
        [string]$ReportContent,
        [string]$ReportFile,
        [hashtable]$Config
    )
    
    if (-not $Config.email.enabled) {
        return
    }
    
    try {
        Write-Log "📧 Enviando relatório por email..."
        
        $smtpClient = New-Object System.Net.Mail.SmtpClient($Config.email.smtp_server, $Config.email.smtp_port)
        $smtpClient.EnableSsl = $true
        $smtpClient.Credentials = New-Object System.Net.NetworkCredential($Config.email.sender_email, $Config.email.sender_password)
        
        $mailMessage = New-Object System.Net.Mail.MailMessage
        $mailMessage.From = New-Object System.Net.Mail.MailAddress($Config.email.sender_email)
        
        foreach ($recipient in $Config.email.recipients) {
            $mailMessage.To.Add($recipient)
        }
        
        $mailMessage.Subject = "Relatório Automático de Documentos - $(Get-Date -Format 'dd/MM/yyyy')"
        
        $body = @"
Relatório automático de análise de documentos gerado em $(Get-Date -Format 'dd/MM/yyyy às HH:mm').

Este relatório foi processado automaticamente pelo sistema de análise de documentos.

Principais informações:
- Status: Processamento concluído com sucesso
- Próxima execução: $(Get-NextRunTime -Config $Config)
- Sistema: $ScriptName v$Version

Relatório completo em anexo.

---
Sistema Automatizado de Análise de Documentos
"@

        $mailMessage.Body = $body
        
        # Anexar relatório
        if (Test-Path $ReportFile) {
            $attachment = New-Object System.Net.Mail.Attachment($ReportFile)
            $mailMessage.Attachments.Add($attachment)
        }
        
        $smtpClient.Send($mailMessage)
        $mailMessage.Dispose()
        $smtpClient.Dispose()
        
        Write-Log "✅ Relatório enviado por email com sucesso" -Level "SUCCESS"
    }
    catch {
        Write-Log "Erro ao enviar email: $_" -Level "ERROR"
    }
}

function Send-TeamsNotification {
    param(
        [string]$ReportSummary,
        [hashtable]$Config
    )
    
    if (-not $Config.teams.enabled -or -not $Config.teams.webhook_url) {
        return
    }
    
    try {
        Write-Log "📢 Enviando notificação para Teams..."
        
        $teamsMessage = @{
            "@type" = "MessageCard"
            "@context" = "http://schema.org/extensions"
            "themeColor" = "0078D4"
            "summary" = "Relatório Automático de Documentos"
            "sections" = @(
                @{
                    "activityTitle" = "🤖 Relatório Automático de Documentos"
                    "activitySubtitle" = "$(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')"
                    "facts" = @(
                        @{
                            "name" = "Status"
                            "value" = "✅ Concluído com sucesso"
                        },
                        @{
                            "name" = "Próxima execução"
                            "value" = "$(Get-NextRunTime -Config $Config)"
                        },
                        @{
                            "name" = "Sistema"
                            "value" = "$ScriptName v$Version"
                        }
                    )
                    "text" = $ReportSummary
                }
            )
        }
        
        $jsonPayload = $teamsMessage | ConvertTo-Json -Depth 10
        
        Invoke-RestMethod -Uri $Config.teams.webhook_url -Method Post -Body $jsonPayload -ContentType "application/json"
        
        Write-Log "✅ Notificação enviada para Teams" -Level "SUCCESS"
    }
    catch {
        Write-Log "Erro ao enviar notificação Teams: $_" -Level "WARNING"
    }
}

function Update-LastRunFile {
    param(
        [array]$Files,
        [string]$LastRunFile
    )
    
    $fileHashes = @{}
    foreach ($file in $Files) {
        $fileHashes[$file.FullName] = Get-FileHash -FilePath $file.FullName
    }
    
    $runData = @{
        timestamp = (Get-Date).ToString('o')
        files_processed = $Files.Count
        file_hashes = $fileHashes
    }
    
    $runData | ConvertTo-Json -Depth 10 | Out-File $LastRunFile -Encoding UTF8
}

function New-WindowsTask {
    $scriptPath = $PSCommandPath
    $taskName = "ProcessamentoAutomaticoDocumentos"
    
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`" -Scheduled"
    $trigger = New-ScheduledTaskTrigger -Daily -At "02:00"
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
    
    try {
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Processamento automático de documentos" -Force
        
        Write-Log "✅ Tarefa '$taskName' criada no Task Scheduler" -Level "SUCCESS"
        Write-Log "📅 Agendamento: Diário às 02:00" -Level "INFO"
    }
    catch {
        Write-Log "Erro ao criar tarefa agendada: $_" -Level "ERROR"
    }
}

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

function Invoke-AutomatedProcessing {
    param(
        [bool]$ForceRun = $false,
        [string]$ConfigFile = ".\automation-config.json"
    )
    
    try {
        Write-Log "🚀 Iniciando processamento automático de documentos..."
        
        # Carregar configuração
        $config = Initialize-Configuration -ConfigPath $ConfigFile
        
        # Obter arquivos válidos
        $files = Get-ValidFiles -WorkspacePath $config.workspace_path -Config $config
        
        if ($files.Count -eq 0) {
            Write-Log "⚠️ Nenhum arquivo válido encontrado para processamento" -Level "WARNING"
            return $false
        }
        
        # Verificar se há mudanças
        if (-not $ForceRun -and -not (Test-HasChanges -Files $files -LastRunFile $LastRunFile)) {
            Write-Log "⏭️ Nenhuma mudança detectada. Processo ignorado."
            return $false
        }
        
        # Criar backup se configurado
        if ($config.processing.create_backup) {
            New-Backup -Files $files -BackupPath $config.backup_path
        }
        
        # Analisar arquivos
        Write-Log "🔍 Analisando conteúdo dos arquivos..."
        $analyses = @()
        
        foreach ($file in $files) {
            $analysis = Get-FileAnalysis -File $file
            $analyses += $analysis
        }
        
        # Gerar relatório
        Write-Log "📊 Gerando relatório consolidado..."
        $reportContent = New-ConsolidatedReport -Analyses $analyses -Config $config
        
        # Salvar relatório
        if (-not (Test-Path $OutputDirectory)) {
            New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
        }
        
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $reportFile = Join-Path $OutputDirectory "relatorio_automatico_$timestamp.md"
        
        $reportContent | Out-File $reportFile -Encoding UTF8
        Write-Log "✅ Relatório salvo: $reportFile" -Level "SUCCESS"
        
        # Enviar notificações
        Send-EmailReport -ReportContent $reportContent -ReportFile $reportFile -Config $config
        
        $reportSummary = "Processamento concluído com $($files.Count) arquivos analisados."
        Send-TeamsNotification -ReportSummary $reportSummary -Config $config
        
        # Limpeza automática
        Invoke-Cleanup -Config $config
        
        # Atualizar arquivo de controle
        Update-LastRunFile -Files $files -LastRunFile $LastRunFile
        
        Write-Log "🎯 Processamento automático concluído com sucesso!" -Level "SUCCESS"
        return $true
    }
    catch {
        Write-Log "Erro durante processamento: $_" -Level "ERROR"
        return $false
    }
}

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

# Inicializar sistema de logs
Initialize-Logging

Write-Log "🤖 $ScriptName v$Version iniciado"

if ($SetupTask) {
    Write-Log "⚙️ Configurando tarefa agendada no Windows..."
    New-WindowsTask
    exit 0
}

if ($Scheduled) {
    # Execução via agendamento
    $success = Invoke-AutomatedProcessing -ForceRun $Force -ConfigFile $ConfigFile
    exit $(if ($success) { 0 } else { 1 })
}
else {
    # Execução manual
    Write-Log "📋 Modo de execução manual"
    Write-Log "💡 Para configurar execução automática, use: -SetupTask"
    
    $success = Invoke-AutomatedProcessing -ForceRun $true -ConfigFile $ConfigFile
    
    if ($success) {
        Write-Log "✨ Processamento concluído. Configure execução automática com -SetupTask" -Level "SUCCESS"
    }
}