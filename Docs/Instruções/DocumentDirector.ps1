# =============================================================================
# SCRIPT DE DIRECIONAMENTO E ORGANIZAÇÃO
# Organiza scripts gerados e direciona execução baseada no contexto
# =============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "menu",
    
    [Parameter(Mandatory=$false)]
    [string]$WorkspacePath = $PWD,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputDir = ".\output",
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Configurações globais
$ScriptName = "DocumentDirector"
$Version = "1.0.0"
$ConfigFile = ".\consolidation-config.ps1"

# Estrutura de diretórios padrão
$DirectoryStructure = @{
    "Scripts" = ".\scripts"
    "Output" = ".\output"
    "Backup" = ".\backup" 
    "Logs" = ".\logs"
    "Templates" = ".\templates"
    "Cache" = ".\cache"
}

# =============================================================================
# FUNÇÕES UTILITÁRIAS
# =============================================================================

function Write-Banner {
    param([string]$Title)
    
    Write-Host "`n" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host " $Title" -ForegroundColor Yellow
    Write-Host "=" * 80 -ForegroundColor Green
    Write-Host ""
}

function Initialize-DirectoryStructure {
    Write-Host "🔧 Inicializando estrutura de diretórios..." -ForegroundColor Cyan
    
    foreach ($key in $DirectoryStructure.Keys) {
        $path = $DirectoryStructure[$key]
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-Host "   ✅ Criado: $path" -ForegroundColor Green
        } else {
            Write-Host "   ℹ️  Existe: $path" -ForegroundColor Gray
        }
    }
}

function Get-AvailableScripts {
    $scriptsPath = $DirectoryStructure["Scripts"]
    if (Test-Path $scriptsPath) {
        return Get-ChildItem -Path $scriptsPath -Filter "*.ps1" | 
               Where-Object { $_.Name -ne "DocumentDirector.ps1" }
    }
    return @()
}

function Show-MainMenu {
    Write-Banner "$ScriptName v$Version - Menu Principal"
    
    Write-Host "📋 OPÇÕES DISPONÍVEIS:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. 🔄 Consolidar Documentos (Executar análise completa)" -ForegroundColor White
    Write-Host "2. 🗂️  Organizar Workspace (Limpar e organizar arquivos)" -ForegroundColor White
    Write-Host "3. 📊 Gerar Relatório Rápido (Análise superficial)" -ForegroundColor White
    Write-Host "4. ⚙️  Configurar Ambiente (Setup inicial)" -ForegroundColor White
    Write-Host "5. 🧹 Limpeza Avançada (Remover duplicados e temporários)" -ForegroundColor White
    Write-Host "6. 📈 Dashboard de Status (Visão geral do workspace)" -ForegroundColor White
    Write-Host "7. 🔧 Scripts Customizados (Executar scripts específicos)" -ForegroundColor White
    Write-Host "8. 📖 Documentação (Gerar README e docs)" -ForegroundColor White
    Write-Host "9. ❌ Sair" -ForegroundColor Red
    Write-Host ""
    
    $choice = Read-Host "👉 Escolha uma opção (1-9)"
    return $choice
}

function Execute-ConsolidationScript {
    param([string]$WorkspacePath)
    
    Write-Host "🚀 Executando consolidação de documentos..." -ForegroundColor Yellow
    
    $consolidationScript = ".\Consolidate-Documents.ps1"
    if (Test-Path $consolidationScript) {
        & $consolidationScript -WorkspacePath $WorkspacePath -Verbose
    } else {
        Write-Host "❌ Script de consolidação não encontrado: $consolidationScript" -ForegroundColor Red
        Write-Host "💡 Execute o comando: .\Generate-ConsolidationScript.ps1" -ForegroundColor Yellow
    }
}

function Execute-WorkspaceOrganization {
    Write-Host "🗂️ Organizando workspace..." -ForegroundColor Yellow
    
    # Criar backup antes de organizar
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backupPath = Join-Path $DirectoryStructure["Backup"] "workspace-backup-$timestamp"
    
    Write-Host "📦 Criando backup em: $backupPath" -ForegroundColor Cyan
    
    # Mover arquivos processados para backup
    $processedFiles = @(
        "azure.instructions.md",
        "tools.instructions.md", 
        "DEPLOY_INSTRUCTIONS.md",
        "Pipeline*.md",
        "OpenAI.md"
    )
    
    foreach ($pattern in $processedFiles) {
        $files = Get-ChildItem -Path $WorkspacePath -Filter $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            if (-not (Test-Path $backupPath)) {
                New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
            }
            Move-Item -Path $file.FullName -Destination $backupPath -Force
            Write-Host "   📁 Movido: $($file.Name)" -ForegroundColor Green
        }
    }
    
    Write-Host "✅ Organização concluída!" -ForegroundColor Green
}

function Generate-QuickReport {
    Write-Host "📊 Gerando relatório rápido..." -ForegroundColor Yellow
    
    $reportPath = Join-Path $DirectoryStructure["Output"] "quick-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').md"
    
    $report = @"
# RELATÓRIO RÁPIDO DO WORKSPACE
**Data:** $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
**Caminho:** $WorkspacePath

## ESTATÍSTICAS

### Arquivos por Tipo
"@

    # Contar arquivos por extensão
    $fileStats = Get-ChildItem -Path $WorkspacePath -File | 
                 Group-Object Extension | 
                 Sort-Object Count -Descending |
                 ForEach-Object { "- $($_.Name): $($_.Count) arquivo(s)" }
    
    $report += "`n" + ($fileStats -join "`n")
    
    $report += @"

### Tamanho Total
**$('{0:N2}' -f ((Get-ChildItem -Path $WorkspacePath -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)) MB**

### Últimas Modificações
"@

    # Arquivos modificados recentemente
    $recentFiles = Get-ChildItem -Path $WorkspacePath -File | 
                   Sort-Object LastWriteTime -Descending | 
                   Select-Object -First 5 |
                   ForEach-Object { "- $($_.Name) ($(Get-Date $_.LastWriteTime -Format 'dd/MM HH:mm'))" }
    
    $report += "`n" + ($recentFiles -join "`n")
    
    $report | Out-File -FilePath $reportPath -Encoding UTF8
    Write-Host "✅ Relatório salvo: $reportPath" -ForegroundColor Green
}

function Initialize-Environment {
    Write-Host "⚙️ Configurando ambiente..." -ForegroundColor Yellow
    
    Initialize-DirectoryStructure
    
    # Criar arquivo de configuração se não existir
    if (-not (Test-Path $ConfigFile)) {
        Write-Host "📝 Criando arquivo de configuração..." -ForegroundColor Cyan
        
        $configContent = @'
# Configurações para consolidação de documentos
$ConsolidationConfig = @{
    # Diretórios
    WorkspacePath = $PWD
    OutputDirectory = ".\output"
    BackupDirectory = ".\backup"
    
    # Arquivo de saída
    OutputFileName = "RELATÓRIO_CORPORATIVO_CONSOLIDADO.md"
    
    # Exclusões
    ExcludePatterns = @(
        "*.tmp", "*.log", "*.cache",
        "*-backup.*", "*-temp.*",
        "node_modules\*", "__pycache__\*"
    )
    
    # Análise
    EnableDeepAnalysis = $true
    CreateBackup = $true
    GenerateIndex = $true
    
    # Limpeza automática
    AutoCleanup = $true
    RemoveProcessedFiles = $true
}
'@
        $configContent | Out-File -FilePath $ConfigFile -Encoding UTF8
    }
    
    # Criar .gitignore se não existir
    if (-not (Test-Path ".\.gitignore")) {
        Write-Host "📝 Criando arquivo .gitignore..." -ForegroundColor Cyan
        # Conteúdo do .gitignore já foi criado anteriormente
    }
    
    Write-Host "✅ Ambiente configurado!" -ForegroundColor Green
}

function Execute-AdvancedCleanup {
    Write-Host "🧹 Executando limpeza avançada..." -ForegroundColor Yellow
    
    $cleaned = 0
    
    # Remover arquivos temporários
    $tempPatterns = @("*.tmp", "*.log", "*~", "*.swp", "*.swo")
    foreach ($pattern in $tempPatterns) {
        $files = Get-ChildItem -Path $WorkspacePath -Filter $pattern -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            Remove-Item $file.FullName -Force
            $cleaned++
            Write-Host "   🗑️ Removido: $($file.Name)" -ForegroundColor Gray
        }
    }
    
    # Remover diretórios vazios
    Get-ChildItem -Path $WorkspacePath -Directory -Recurse | 
        Where-Object { (Get-ChildItem $_.FullName -ErrorAction SilentlyContinue).Count -eq 0 } |
        ForEach-Object {
            Remove-Item $_.FullName -Force
            $cleaned++
            Write-Host "   📁 Diretório vazio removido: $($_.Name)" -ForegroundColor Gray
        }
    
    Write-Host "✅ Limpeza concluída! $cleaned item(s) removido(s)." -ForegroundColor Green
}

function Show-WorkspaceDashboard {
    Write-Banner "DASHBOARD DO WORKSPACE"
    
    $totalFiles = (Get-ChildItem -Path $WorkspacePath -File).Count
    $totalDirs = (Get-ChildItem -Path $WorkspacePath -Directory).Count
    $totalSize = [math]::Round(((Get-ChildItem -Path $WorkspacePath -Recurse -File | Measure-Object Length -Sum).Sum / 1MB), 2)
    
    Write-Host "📊 ESTATÍSTICAS GERAIS" -ForegroundColor Cyan
    Write-Host "   📄 Arquivos: $totalFiles" -ForegroundColor White
    Write-Host "   📁 Diretórios: $totalDirs" -ForegroundColor White
    Write-Host "   💾 Tamanho total: $totalSize MB" -ForegroundColor White
    Write-Host ""
    
    # Tipos de arquivo mais comuns
    Write-Host "📋 TIPOS DE ARQUIVO" -ForegroundColor Cyan
    Get-ChildItem -Path $WorkspacePath -File | 
        Group-Object Extension | 
        Sort-Object Count -Descending | 
        Select-Object -First 10 |
        ForEach-Object {
            $ext = if ($_.Name) { $_.Name } else { "(sem extensão)" }
            Write-Host "   $ext : $($_.Count)" -ForegroundColor White
        }
    
    Write-Host ""
    
    # Verificar se há relatórios existentes
    $reports = Get-ChildItem -Path $WorkspacePath -Filter "*RELATÓRIO*" -ErrorAction SilentlyContinue
    if ($reports) {
        Write-Host "📈 RELATÓRIOS ENCONTRADOS" -ForegroundColor Cyan
        foreach ($report in $reports) {
            Write-Host "   📊 $($report.Name) ($(Get-Date $report.LastWriteTime -Format 'dd/MM HH:mm'))" -ForegroundColor White
        }
    }
}

function Execute-CustomScripts {
    Write-Host "🔧 Scripts customizados disponíveis:" -ForegroundColor Yellow
    
    $scripts = Get-AvailableScripts
    
    if ($scripts.Count -eq 0) {
        Write-Host "❌ Nenhum script customizado encontrado em $($DirectoryStructure['Scripts'])" -ForegroundColor Red
        return
    }
    
    Write-Host ""
    for ($i = 0; $i -lt $scripts.Count; $i++) {
        Write-Host "$($i + 1). $($scripts[$i].Name)" -ForegroundColor White
    }
    Write-Host ""
    
    $choice = Read-Host "Escolha um script (1-$($scripts.Count)) ou Enter para voltar"
    
    if ($choice -and $choice -match '^\d+$' -and [int]$choice -le $scripts.Count) {
        $selectedScript = $scripts[[int]$choice - 1]
        Write-Host "🚀 Executando: $($selectedScript.Name)" -ForegroundColor Yellow
        & $selectedScript.FullName
    }
}

function Generate-Documentation {
    Write-Host "📖 Gerando documentação..." -ForegroundColor Yellow
    
    $readmePath = Join-Path $DirectoryStructure["Output"] "README-Workspace.md"
    
    $readme = @"
# WORKSPACE DOCUMENTATION

## Visão Geral
Este workspace contém documentação técnica e scripts de automação para consolidação de documentos.

## Estrutura de Diretórios
$(foreach ($key in $DirectoryStructure.Keys) { "- **$key**: $($DirectoryStructure[$key])" }) -join "`n")

## Scripts Principais
- **DocumentDirector.ps1**: Script principal de direcionamento
- **Consolidate-Documents.ps1**: Consolidação automática de documentos
- **consolidation-config.ps1**: Arquivo de configuração

## Uso Rápido
```powershell
# Executar menu principal
.\DocumentDirector.ps1

# Consolidação direta
.\DocumentDirector.ps1 -Action "consolidate"

# Limpeza do workspace
.\DocumentDirector.ps1 -Action "cleanup"
```

## Configuração
Edite o arquivo \`consolidation-config.ps1\` para personalizar o comportamento dos scripts.

## Suporte
Para dúvidas ou problemas, verifique os logs em \`.\logs\` ou execute o dashboard para diagnóstico.

---
**Última atualização**: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')
"@

    $readme | Out-File -FilePath $readmePath -Encoding UTF8
    Write-Host "✅ Documentação gerada: $readmePath" -ForegroundColor Green
}

# =============================================================================
# LÓGICA PRINCIPAL
# =============================================================================

Write-Banner "$ScriptName v$Version - Sistema de Direcionamento"

# Verificar se está na execução com parâmetro específico
switch ($Action.ToLower()) {
    "consolidate" {
        Initialize-DirectoryStructure
        Execute-ConsolidationScript -WorkspacePath $WorkspacePath
        return
    }
    "organize" {
        Initialize-DirectoryStructure
        Execute-WorkspaceOrganization
        return
    }
    "cleanup" {
        Execute-AdvancedCleanup
        return
    }
    "report" {
        Initialize-DirectoryStructure
        Generate-QuickReport
        return
    }
    "setup" {
        Initialize-Environment
        return
    }
    "dashboard" {
        Show-WorkspaceDashboard
        return
    }
}

# Menu interativo
do {
    $choice = Show-MainMenu
    
    switch ($choice) {
        "1" {
            Initialize-DirectoryStructure
            Execute-ConsolidationScript -WorkspacePath $WorkspacePath
        }
        "2" {
            Initialize-DirectoryStructure
            Execute-WorkspaceOrganization
        }
        "3" {
            Initialize-DirectoryStructure
            Generate-QuickReport
        }
        "4" {
            Initialize-Environment
        }
        "5" {
            Execute-AdvancedCleanup
        }
        "6" {
            Show-WorkspaceDashboard
        }
        "7" {
            Execute-CustomScripts
        }
        "8" {
            Initialize-DirectoryStructure
            Generate-Documentation
        }
        "9" {
            Write-Host "👋 Saindo... Até logo!" -ForegroundColor Green
            break
        }
        default {
            Write-Host "❌ Opção inválida. Tente novamente." -ForegroundColor Red
            Start-Sleep 1
        }
    }
    
    if ($choice -ne "9") {
        Write-Host "`n⏸️ Pressione qualquer tecla para continuar..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    
} while ($choice -ne "9")

Write-Host "🎯 Script finalizado com sucesso!" -ForegroundColor Green