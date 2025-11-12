# Script de Sincronização Ávila
# VS Code ↔ Obsidian ↔ GitHub
# Autor: Nícolas Ávila

param(
    [switch]$AutoMode,
    [switch]$GitSync,
    [switch]$ObsidianSync,
    [switch]$Setup
)

# Configurações
$AvilaPath = "C:\Users\nicol\OneDrive\Avila"
$DocsPath = "$AvilaPath\Docs"
$ObsidianVault = $DocsPath  # Usando a pasta Docs como vault
$LogPath = "$AvilaPath\Logs\sync-$(Get-Date -Format 'yyyy-MM-dd').log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage -ForegroundColor $(
        switch ($Level) {
            "ERROR" { "Red" }
            "WARN" { "Yellow" }
            "SUCCESS" { "Green" }
            default { "White" }
        }
    )
    $logMessage | Out-File $LogPath -Append
}

function Setup-Environment {
    Write-Log "🔧 Configurando ambiente de sincronização..." "INFO"

    # Verificar se é repositório Git
    if (-not (Test-Path "$AvilaPath\.git")) {
        Write-Log "Inicializando repositório Git..." "INFO"
        Set-Location $AvilaPath
        git init
        git add .
        git commit -m "🎯 Inicial: Setup Ávila Framework"
    }

    # Configurar Git hooks
    $hookPath = "$AvilaPath\.git\hooks\pre-commit"
    $hookContent = @"
#!/bin/sh
# Ávila Framework - Pre-commit hook
echo "🔍 Verificando arquivos antes do commit..."

# Atualizar timestamp em arquivos .md
find . -name "*.md" -type f -exec sed -i "s/modified: .*/modified: `$(date +%Y-%m-%d)/g" {} \;

# Verificar estrutura do projeto
if [ -f "Scripts/check_structure.py" ]; then
    python Scripts/check_structure.py
fi

echo "✅ Pre-commit verificações concluídas"
"@

    $hookContent | Out-File $hookPath -Encoding UTF8

    Write-Log "✅ Ambiente configurado com sucesso!" "SUCCESS"
}

function Sync-WithGit {
    Write-Log "🔄 Sincronizando com GitHub..." "INFO"

    Set-Location $AvilaPath

    # Pull primeiro
    try {
        git pull origin main
        Write-Log "📥 Pull concluído" "SUCCESS"
    } catch {
        Write-Log "⚠️ Erro no pull: $_" "WARN"
    }

    # Verificar mudanças
    $changes = git status --porcelain
    if ($changes) {
        Write-Log "📝 Detectadas $($changes.Count) mudanças" "INFO"

        # Add e commit
        git add .
        $commitMsg = "🔄 Auto sync: $(Get-Date -Format 'dd/MM/yyyy HH:mm')"
        git commit -m $commitMsg

        # Push
        try {
            git push origin main
            Write-Log "📤 Push concluído: $commitMsg" "SUCCESS"
        } catch {
            Write-Log "❌ Erro no push: $_" "ERROR"
        }
    } else {
        Write-Log "✅ Nenhuma mudança detectada" "INFO"
    }
}

function Sync-ObsidianConfig {
    Write-Log "📱 Sincronizando configuração do Obsidian..." "INFO"

    # Verificar se Obsidian está rodando
    $obsidianProcess = Get-Process "Obsidian" -ErrorAction SilentlyContinue

    if ($obsidianProcess) {
        Write-Log "⚠️ Obsidian em execução - algumas configurações podem não ser aplicadas" "WARN"
    }

    # Atualizar configurações
    $configFiles = @(
        "community-plugins.json",
        "core-plugins.json",
        "app.json"
    )

    foreach ($config in $configFiles) {
        $configPath = "$DocsPath\.obsidian\$config"
        if (Test-Path $configPath) {
            Write-Log "✅ Configuração atualizada: $config" "SUCCESS"
        }
    }
}

function Monitor-FileChanges {
    Write-Log "👀 Iniciando monitoramento de arquivos..." "INFO"

    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = $DocsPath
    $watcher.Filter = "*.md"
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true

    $action = {
        $path = $Event.SourceEventArgs.FullPath
        $name = $Event.SourceEventArgs.Name
        $changeType = $Event.SourceEventArgs.ChangeType

        Write-Log "📝 Arquivo modificado: $name ($changeType)" "INFO"

        # Auto-sync após 30 segundos de inatividade
        Start-Sleep 30
        Sync-WithGit
    }

    Register-ObjectEvent -InputObject $watcher -EventName "Changed" -Action $action

    Write-Log "🎯 Monitoramento ativo! Pressione Ctrl+C para parar..." "SUCCESS"

    try {
        while ($true) {
            Start-Sleep 5
        }
    } finally {
        $watcher.EnableRaisingEvents = $false
        $watcher.Dispose()
        Write-Log "⏹️ Monitoramento parado" "INFO"
    }
}

function Show-Status {
    Clear-Host
    Write-Host @"
🚀 ÁVILA SYNC CENTER
====================
$(Get-Date -Format "dd/MM/yyyy HH:mm:ss")

📊 STATUS ATUAL
"@ -ForegroundColor Magenta

    # Git Status
    Set-Location $AvilaPath
    $gitStatus = git status --porcelain
    $lastCommit = git log -1 --pretty=format:"%h - %s (%cr)"

    if ($gitStatus) {
        Write-Host "🔄 Git: $($gitStatus.Count) arquivos modificados" -ForegroundColor Yellow
    } else {
        Write-Host "✅ Git: Sincronizado" -ForegroundColor Green
    }

    Write-Host "📝 Último commit: $lastCommit" -ForegroundColor Cyan

    # Obsidian Status
    $obsidianRunning = Get-Process "Obsidian" -ErrorAction SilentlyContinue
    if ($obsidianRunning) {
        Write-Host "📱 Obsidian: ✅ Executando" -ForegroundColor Green
    } else {
        Write-Host "📱 Obsidian: ⏹️ Parado" -ForegroundColor Yellow
    }

    # VS Code Status
    $vscodeRunning = Get-Process "Code" -ErrorAction SilentlyContinue
    if ($vscodeRunning) {
        Write-Host "💻 VS Code: ✅ Executando" -ForegroundColor Green
    } else {
        Write-Host "💻 VS Code: ⏹️ Parado" -ForegroundColor Yellow
    }

    # Estatísticas
    $totalFiles = (Get-ChildItem $DocsPath -Recurse -File).Count
    $mdFiles = (Get-ChildItem $DocsPath -Recurse -Filter "*.md").Count

    Write-Host "`n📊 ESTATÍSTICAS" -ForegroundColor Cyan
    Write-Host "📄 Total de arquivos: $totalFiles"
    Write-Host "📝 Arquivos Markdown: $mdFiles"

    Write-Host "`n🎯 COMANDOS DISPONÍVEIS" -ForegroundColor Yellow
    Write-Host "1 - Sync Git          | 2 - Sync Obsidian"
    Write-Host "3 - Monitor Auto      | 4 - Abrir Obsidian"
    Write-Host "5 - Abrir VS Code     | 6 - Ver Logs"
    Write-Host "Q - Sair"
}

function Interactive-Menu {
    do {
        Show-Status
        $choice = Read-Host "`nEscolha uma opção"

        switch ($choice.ToUpper()) {
            '1' { Sync-WithGit }
            '2' { Sync-ObsidianConfig }
            '3' { Monitor-FileChanges }
            '4' {
                Write-Log "🚀 Abrindo Obsidian..." "INFO"
                Start-Process "obsidian://open?vault=Avila"
            }
            '5' {
                Write-Log "🚀 Abrindo VS Code..." "INFO"
                Set-Location $AvilaPath
                code .
            }
            '6' {
                if (Test-Path $LogPath) {
                    Get-Content $LogPath -Tail 20 | ForEach-Object {
                        Write-Host $_ -ForegroundColor Gray
                    }
                } else {
                    Write-Log "📋 Nenhum log encontrado hoje" "INFO"
                }
                Read-Host "`nPressione Enter para continuar"
            }
            'Q' {
                Write-Log "👋 Saindo do Sync Center..." "INFO"
                break
            }
            default {
                Write-Log "❌ Opção inválida!" "ERROR"
                Start-Sleep 2
            }
        }
    } while ($choice.ToUpper() -ne 'Q')
}

# EXECUÇÃO PRINCIPAL
Write-Host @"
🚀 ÁVILA SYNC CENTER
====================
Sincronização entre VS Code, Obsidian e GitHub
Autor: Nícolas Ávila | Framework: Ávila Inc.
"@ -ForegroundColor Magenta

if ($Setup) {
    Setup-Environment
    exit
}

if ($AutoMode) {
    Write-Log "🤖 Modo automático ativado" "INFO"
    Monitor-FileChanges
    exit
}

if ($GitSync) {
    Sync-WithGit
    exit
}

if ($ObsidianSync) {
    Sync-ObsidianConfig
    exit
}

# Menu interativo por padrão
Interactive-Menu
