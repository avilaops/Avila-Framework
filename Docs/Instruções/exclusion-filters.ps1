# =============================================================================
# EXCLUSÕES E FILTROS PARA CONSOLIDAÇÃO
# Lista de arquivos e padrões a serem excluídos durante o processamento
# =============================================================================

# Configuração de exclusões
$ExclusionConfig = @{
    
    # =========================================================================
    # ARQUIVOS JÁ PROCESSADOS
    # =========================================================================
    ProcessedFiles = @(
        "azure.instructions.md",
        "tools.instructions.md", 
        "DEPLOY_INSTRUCTIONS.md",
        "Pipeline de Inteligência contínua.md",
        "OpenAI.md",
        "RELATÓRIO_CORPORATIVO_*.md"
    )
    
    # =========================================================================
    # PADRÕES DE EXCLUSÃO POR TIPO
    # =========================================================================
    TemporaryFiles = @(
        "*.tmp",
        "*.temp",
        "*.log",
        "*.cache",
        "*~",
        "*.swp",
        "*.swo",
        "*.bak",
        "*-backup.*",
        "*-temp.*",
        "*-copy.*"
    )
    
    SystemFiles = @(
        "Thumbs.db",
        "Desktop.ini",
        ".DS_Store",
        "$RECYCLE.BIN/*",
        "*.lnk"
    )
    
    DevelopmentFiles = @(
        "node_modules/*",
        "__pycache__/*",
        ".pytest_cache/*",
        ".coverage",
        "*.pyc",
        ".vscode/*",
        "*.vsix",
        ".git/*",
        ".gitignore"
    )
    
    BinaryFiles = @(
        "*.exe",
        "*.dll",
        "*.so",
        "*.dylib",
        "*.bin",
        "*.obj",
        "*.lib",
        "*.a"
    )
    
    MediaFiles = @(
        "*.jpg",
        "*.jpeg", 
        "*.png",
        "*.gif",
        "*.bmp",
        "*.svg",
        "*.mp4",
        "*.avi",
        "*.mov",
        "*.mp3",
        "*.wav"
    )
    
    # =========================================================================
    # DIRETÓRIOS A EXCLUIR
    # =========================================================================
    ExcludedDirectories = @(
        "backup",
        "cache",
        ".cache",
        "temp",
        "tmp",
        "logs",
        "output",
        "build",
        "dist",
        "target",
        "bin",
        "obj"
    )
    
    # =========================================================================
    # ARQUIVOS SENSÍVEIS (SEGURANÇA)
    # =========================================================================
    SensitiveFiles = @(
        "*.key",
        "*.pem",
        "*.p12",
        "*.pfx",
        "*.secret",
        "*.token",
        "api-keys.*",
        "credentials.*",
        "password*",
        "secret*",
        ".env",
        ".env.local",
        ".env.production"
    )
    
    # =========================================================================
    # ARQUIVOS DE CONFIGURAÇÃO ESPECÍFICOS
    # =========================================================================
    ConfigFiles = @(
        "consolidation-config.ps1",
        "DocumentDirector.ps1",
        "exclusion-filters.ps1"
    )
}

# =============================================================================
# FUNÇÕES DE FILTRO
# =============================================================================

function Test-ShouldExcludeFile {
    param(
        [string]$FilePath,
        [string]$FileName
    )
    
    # Normalizar o caminho para comparação
    $normalizedPath = $FilePath.Replace('\', '/').ToLower()
    $normalizedName = $FileName.ToLower()
    
    # Verificar arquivos já processados
    foreach ($pattern in $ExclusionConfig.ProcessedFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (processado): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos temporários
    foreach ($pattern in $ExclusionConfig.TemporaryFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (temporário): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos de sistema
    foreach ($pattern in $ExclusionConfig.SystemFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (sistema): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos de desenvolvimento
    foreach ($pattern in $ExclusionConfig.DevelopmentFiles) {
        if ($normalizedPath -like "*/$($pattern.ToLower())" -or $normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (desenvolvimento): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos binários
    foreach ($pattern in $ExclusionConfig.BinaryFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (binário): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos de mídia
    foreach ($pattern in $ExclusionConfig.MediaFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (mídia): $FileName"
            return $true
        }
    }
    
    # Verificar arquivos sensíveis
    foreach ($pattern in $ExclusionConfig.SensitiveFiles) {
        if ($normalizedName -like $pattern.ToLower()) {
            Write-Verbose "Excluído (sensível): $FileName"
            return $true
        }
    }
    
    # Verificar se está em diretório excluído
    foreach ($dir in $ExclusionConfig.ExcludedDirectories) {
        if ($normalizedPath -like "*/$($dir.ToLower())/*") {
            Write-Verbose "Excluído (diretório): $FileName"
            return $true
        }
    }
    
    return $false
}

function Test-ShouldExcludeDirectory {
    param([string]$DirectoryName)
    
    $normalizedName = $DirectoryName.ToLower()
    
    foreach ($excludedDir in $ExclusionConfig.ExcludedDirectories) {
        if ($normalizedName -eq $excludedDir.ToLower()) {
            return $true
        }
    }
    
    return $false
}

function Get-FilteredFileList {
    param(
        [string]$WorkspacePath,
        [string[]]$FileExtensions = @("*.md", "*.txt", "*.json", "*.yml", "*.yaml")
    )
    
    $filteredFiles = @()
    
    Write-Host "🔍 Analisando arquivos em: $WorkspacePath" -ForegroundColor Cyan
    
    foreach ($extension in $FileExtensions) {
        $files = Get-ChildItem -Path $WorkspacePath -Filter $extension -Recurse -File -ErrorAction SilentlyContinue
        
        foreach ($file in $files) {
            # Verificar se deve excluir o arquivo
            if (-not (Test-ShouldExcludeFile -FilePath $file.FullName -FileName $file.Name)) {
                # Verificar se está em diretório excluído
                $parentDir = Split-Path $file.DirectoryName -Leaf
                if (-not (Test-ShouldExcludeDirectory -DirectoryName $parentDir)) {
                    $filteredFiles += $file
                    Write-Verbose "Incluído: $($file.Name)"
                }
            }
        }
    }
    
    Write-Host "✅ Encontrados $($filteredFiles.Count) arquivo(s) válidos para processamento" -ForegroundColor Green
    
    return $filteredFiles
}

function Show-ExclusionSummary {
    param([string]$WorkspacePath)
    
    Write-Host "`n📋 RESUMO DE FILTROS DE EXCLUSÃO" -ForegroundColor Yellow
    Write-Host "=" * 50 -ForegroundColor Yellow
    
    Write-Host "📁 Workspace: $WorkspacePath" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "🚫 Tipos de exclusão ativados:" -ForegroundColor Red
    Write-Host "   • Arquivos já processados: $($ExclusionConfig.ProcessedFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos temporários: $($ExclusionConfig.TemporaryFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos de sistema: $($ExclusionConfig.SystemFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos de desenvolvimento: $($ExclusionConfig.DevelopmentFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos binários: $($ExclusionConfig.BinaryFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos de mídia: $($ExclusionConfig.MediaFiles.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Diretórios excluídos: $($ExclusionConfig.ExcludedDirectories.Count) padrões" -ForegroundColor Gray
    Write-Host "   • Arquivos sensíveis: $($ExclusionConfig.SensitiveFiles.Count) padrões" -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "ℹ️ Para ver detalhes, execute com -Verbose" -ForegroundColor Blue
    Write-Host ""
}

function Add-CustomExclusion {
    param(
        [string]$Pattern,
        [ValidateSet("ProcessedFiles", "TemporaryFiles", "SystemFiles", "DevelopmentFiles", "BinaryFiles", "MediaFiles", "ExcludedDirectories", "SensitiveFiles")]
        [string]$Category = "TemporaryFiles"
    )
    
    if ($ExclusionConfig[$Category] -notcontains $Pattern) {
        $ExclusionConfig[$Category] += $Pattern
        Write-Host "✅ Padrão '$Pattern' adicionado à categoria '$Category'" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️ Padrão '$Pattern' já existe na categoria '$Category'" -ForegroundColor Yellow
        return $false
    }
}

function Remove-CustomExclusion {
    param(
        [string]$Pattern,
        [string]$Category
    )
    
    if ($ExclusionConfig[$Category] -contains $Pattern) {
        $ExclusionConfig[$Category] = $ExclusionConfig[$Category] | Where-Object { $_ -ne $Pattern }
        Write-Host "✅ Padrão '$Pattern' removido da categoria '$Category'" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️ Padrão '$Pattern' não encontrado na categoria '$Category'" -ForegroundColor Yellow
        return $false
    }
}

# =============================================================================
# EXPORTAR CONFIGURAÇÃO
# =============================================================================

# Tornar as configurações disponíveis para outros scripts
$global:DocumentExclusionConfig = $ExclusionConfig

# Exportar funções principais
Export-ModuleMember -Function @(
    'Test-ShouldExcludeFile',
    'Test-ShouldExcludeDirectory', 
    'Get-FilteredFileList',
    'Show-ExclusionSummary',
    'Add-CustomExclusion',
    'Remove-CustomExclusion'
)