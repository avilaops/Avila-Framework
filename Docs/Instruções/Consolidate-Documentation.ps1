# ============================================================================
# SCRIPT DE CONSOLIDAÇÃO AUTOMÁTICA DE DOCUMENTAÇÃO
# Data de Criação: Novembro 2025
# Versão: 1.0
# Descrição: Automatiza a análise e consolidação de documentos técnicos
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$InputPath = (Get-Location).Path,
    
    [Parameter(Mandatory=$false)]
    [string]$OutputFileName = "RELATÓRIO_CORPORATIVO_CONSOLIDADO.md",
    
    [Parameter(Mandatory=$false)]
    [switch]$DeleteAnalyzedFiles = $true,
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateBackup = $true,
    
    [Parameter(Mandatory=$false)]
    [string]$BackupPath = ".\backup"
)

# Configuração inicial
$ErrorActionPreference = "Stop"
$ProgressPreference = "Continue"

# Arrays para controle de arquivos
$AnalyzedFiles = @()
$SkipFiles = @(
    "RELATÓRIO_CORPORATIVO_CONSOLIDADO.md",
    "Consolidate-Documentation.ps1",
    "*.log",
    "*.tmp"
)

# Tipos de arquivo suportados
$SupportedExtensions = @(".md", ".txt", ".json", ".hpp", ".cpp", ".h", ".js", ".ts")

Write-Host "🚀 INICIANDO CONSOLIDAÇÃO AUTOMÁTICA DE DOCUMENTAÇÃO" -ForegroundColor Green
Write-Host "📁 Diretório de trabalho: $InputPath" -ForegroundColor Cyan
Write-Host "📄 Arquivo de saída: $OutputFileName" -ForegroundColor Cyan

# Função para criar backup
function New-DocumentationBackup {
    param($Path)
    
    if ($CreateBackup) {
        Write-Host "💾 Criando backup..." -ForegroundColor Yellow
        
        if (-not (Test-Path $BackupPath)) {
            New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
        }
        
        $BackupName = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        $FullBackupPath = Join-Path $BackupPath $BackupName
        
        Copy-Item -Path $Path -Destination $FullBackupPath -Recurse -Force
        Write-Host "✅ Backup criado em: $FullBackupPath" -ForegroundColor Green
        
        return $FullBackupPath
    }
}

# Função para analisar conteúdo de arquivo
function Get-FileAnalysis {
    param(
        [string]$FilePath,
        [string]$Content
    )
    
    $Analysis = @{
        FilePath = $FilePath
        FileName = (Get-Item $FilePath).Name
        Extension = (Get-Item $FilePath).Extension
        Size = (Get-Item $FilePath).Length
        LineCount = ($Content -split "`n").Count
        WordCount = ($Content -split '\s+').Count
        Keywords = @()
        Category = ""
        Priority = 1
        Summary = ""
    }
    
    # Categorização automática baseada em conteúdo
    if ($Content -match "(?i)(deploy|deployment|migration|database)" -or $FilePath -match "(?i)deploy") {
        $Analysis.Category = "Deployment & Infrastructure"
        $Analysis.Priority = 1
    }
    elseif ($Content -match "(?i)(ai|artificial intelligence|machine learning|llm|gpt|pipeline)" -or $FilePath -match "(?i)(ai|ml|pipeline)") {
        $Analysis.Category = "Artificial Intelligence & ML"
        $Analysis.Priority = 1
    }
    elseif ($Content -match "(?i)(azure|aws|cloud|kubernetes|docker)" -or $FilePath -match "(?i)(azure|cloud)") {
        $Analysis.Category = "Cloud & DevOps"
        $Analysis.Priority = 1
    }
    elseif ($Content -match "(?i)(codecov|test|quality|ci/cd)" -or $FilePath -match "(?i)(test|quality)") {
        $Analysis.Category = "Quality Assurance & Testing"
        $Analysis.Priority = 2
    }
    elseif ($Content -match "(?i)(instruction|guide|how-to)" -or $FilePath -match "(?i)instruction") {
        $Analysis.Category = "Documentation & Guidelines"
        $Analysis.Priority = 2
    }
    elseif ($Analysis.Extension -in @(".cpp", ".hpp", ".h")) {
        $Analysis.Category = "C++ Development"
        $Analysis.Priority = 3
    }
    elseif ($Analysis.Extension -in @(".js", ".ts", ".json")) {
        $Analysis.Category = "JavaScript/TypeScript"
        $Analysis.Priority = 3
    }
    else {
        $Analysis.Category = "General Documentation"
        $Analysis.Priority = 4
    }
    
    # Extração de palavras-chave
    $CommonKeywords = @("PostgreSQL", "Azure", "Kubernetes", "Docker", "AI", "ML", "Pipeline", "Deploy", "Test", "API", "Database", "Cloud", "DevOps", "Automation", "Security")
    foreach ($keyword in $CommonKeywords) {
        if ($Content -match "(?i)$keyword") {
            $Analysis.Keywords += $keyword
        }
    }
    
    # Geração de resumo automático (primeiras linhas significativas)
    $ContentLines = $Content -split "`n" | Where-Object { $_.Trim() -ne "" }
    $Summary = ($ContentLines | Select-Object -First 3) -join " "
    if ($Summary.Length -gt 200) {
        $Summary = $Summary.Substring(0, 197) + "..."
    }
    $Analysis.Summary = $Summary
    
    return $Analysis
}

# Função para gerar seção do relatório
function New-ReportSection {
    param(
        [string]$Category,
        [array]$Files
    )
    
    $Section = @"

## 📁 $Category

"@

    foreach ($File in $Files) {
        $Section += @"

### 📄 $($File.FileName)
**Caminho**: ``$($File.FilePath)``  
**Tamanho**: $([math]::Round($File.Size/1KB, 2)) KB | **Linhas**: $($File.LineCount) | **Palavras**: $($File.WordCount)  
**Palavras-chave**: $($File.Keywords -join ", ")  

**Resumo**: $($File.Summary)

---

"@
    }
    
    return $Section
}

# Função principal de consolidação
function Start-DocumentationConsolidation {
    Write-Host "🔍 Escaneando arquivos..." -ForegroundColor Yellow
    
    # Busca todos os arquivos suportados
    $AllFiles = Get-ChildItem -Path $InputPath -Recurse | Where-Object {
        $_.Extension -in $SupportedExtensions -and 
        -not ($SkipFiles | Where-Object { $_.Name -like $_ })
    }
    
    Write-Host "📊 Encontrados $($AllFiles.Count) arquivos para análise" -ForegroundColor Cyan
    
    if ($AllFiles.Count -eq 0) {
        Write-Warning "Nenhum arquivo encontrado para análise."
        return
    }
    
    # Análise de cada arquivo
    $FileAnalyses = @()
    $Counter = 0
    
    foreach ($File in $AllFiles) {
        $Counter++
        Write-Progress -Activity "Analisando arquivos" -Status "Processando: $($File.Name)" -PercentComplete (($Counter / $AllFiles.Count) * 100)
        
        try {
            $Content = Get-Content -Path $File.FullName -Raw -Encoding UTF8
            $Analysis = Get-FileAnalysis -FilePath $File.FullName -Content $Content
            $FileAnalyses += $Analysis
            $AnalyzedFiles += $File.FullName
            
            Write-Host "✅ Analisado: $($File.Name) [$($Analysis.Category)]" -ForegroundColor Green
        }
        catch {
            Write-Warning "Erro ao processar $($File.Name): $($_.Exception.Message)"
        }
    }
    
    Write-Progress -Activity "Analisando arquivos" -Completed
    
    # Agrupamento por categoria
    $CategorizedFiles = $FileAnalyses | Group-Object Category | Sort-Object Name
    
    # Geração do relatório consolidado
    Write-Host "📝 Gerando relatório consolidado..." -ForegroundColor Yellow
    
    $ReportHeader = @"
# RELATÓRIO CORPORATIVO CONSOLIDADO
## Análise Técnica e Estratégica dos Sistemas de Desenvolvimento
**Data de Geração**: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")  
**Ferramenta**: Script de Consolidação Automática v1.0  
**Diretório Analisado**: $InputPath  
**Total de Arquivos**: $($FileAnalyses.Count)  

---

## 📋 SUMÁRIO EXECUTIVO

Este relatório foi gerado automaticamente através da análise de $($FileAnalyses.Count) arquivos de documentação técnica. A análise identificou $($CategorizedFiles.Count) categorias principais de conteúdo, priorizadas por relevância estratégica e técnica.

### 📊 Distribuição por Categoria:
"@

    foreach ($Category in $CategorizedFiles) {
        $ReportHeader += "`n- **$($Category.Name)**: $($Category.Count) arquivo(s)"
    }
    
    $ReportHeader += @"

### 🔍 Palavras-chave Mais Frequentes:
"@

    # Análise de frequência de palavras-chave
    $AllKeywords = $FileAnalyses | ForEach-Object { $_.Keywords } | Group-Object | Sort-Object Count -Descending | Select-Object -First 10
    foreach ($Keyword in $AllKeywords) {
        $ReportHeader += "`n- **$($Keyword.Name)**: $($Keyword.Count) ocorrência(s)"
    }
    
    $ReportHeader += "`n`n---"
    
    # Geração das seções por categoria (ordenadas por prioridade)
    $ReportBody = ""
    $SectionCounter = 1
    
    foreach ($Category in ($CategorizedFiles | Sort-Object @{Expression={($_.Group | Measure-Object Priority -Average).Average}})) {
        $ReportBody += "`n`n## $SectionCounter. $($Category.Name.ToUpper())"
        $ReportBody += "`n**Prioridade**: $(($Category.Group | Measure-Object Priority -Average).Average.ToString("F1"))"
        $ReportBody += "`n**Arquivos nesta categoria**: $($Category.Count)"
        
        foreach ($File in ($Category.Group | Sort-Object Priority, FileName)) {
            $ReportBody += @"

### 📄 $($File.FileName)
**📍 Localização**: ``$($File.FilePath -replace [regex]::Escape($InputPath), ".")``  
**📏 Métricas**: $([math]::Round($File.Size/1KB, 2)) KB • $($File.LineCount) linhas • $($File.WordCount) palavras  
**🏷️ Tags**: $(if($File.Keywords.Count -gt 0) { $File.Keywords -join " • " } else { "Nenhuma tag identificada" })  
**⭐ Prioridade**: $($File.Priority)/4

**📖 Resumo Automático**:  
$($File.Summary)

---

"@
        }
        $SectionCounter++
    }
    
    # Geração de recomendações automáticas
    $Recommendations = @"

## 🎯 RECOMENDAÇÕES AUTOMÁTICAS

### ✅ Implementação Imediata
"@

    $HighPriorityFiles = $FileAnalyses | Where-Object { $_.Priority -eq 1 }
    if ($HighPriorityFiles.Count -gt 0) {
        $Recommendations += "`n- Revisar e implementar guidelines dos $($HighPriorityFiles.Count) arquivo(s) de alta prioridade"
        foreach ($File in $HighPriorityFiles | Select-Object -First 3) {
            $Recommendations += "`n  - $($File.FileName): $($File.Category)"
        }
    }
    
    $Recommendations += @"

### 📈 Desenvolvimento Contínuo
- Estabelecer processo de atualização automática desta documentação
- Implementar métricas de qualidade baseadas nas diretrizes identificadas
- Criar pipeline de validação para novos documentos

### 🔄 Manutenção
- Executar esta análise semanalmente para detectar mudanças
- Manter backup histórico das versões de documentação
- Monitorar palavras-chave emergentes para identificar novas tendências

---

## 📊 ESTATÍSTICAS DETALHADAS

### 📁 Distribuição por Tipo de Arquivo:
"@

    $ExtensionStats = $FileAnalyses | Group-Object Extension | Sort-Object Count -Descending
    foreach ($Ext in $ExtensionStats) {
        $Recommendations += "`n- **$($Ext.Name)**: $($Ext.Count) arquivo(s)"
    }
    
    $Recommendations += @"

### 📈 Métricas Gerais:
- **Total de linhas analisadas**: $(($FileAnalyses | Measure-Object LineCount -Sum).Sum)
- **Total de palavras processadas**: $(($FileAnalyses | Measure-Object WordCount -Sum).Sum)
- **Tamanho total processado**: $([math]::Round(($FileAnalyses | Measure-Object Size -Sum).Sum/1MB, 2)) MB

---

**🤖 Relatório gerado automaticamente em**: $(Get-Date -Format "dd/MM/yyyy HH:mm:ss")  
**🔧 Ferramenta**: Consolidate-Documentation.ps1 v1.0  
**📂 Diretório**: $InputPath  
**✅ Status**: Consolidação concluída com sucesso
"@

    # Montagem final do relatório
    $FinalReport = $ReportHeader + $ReportBody + $Recommendations
    
    # Salvamento do arquivo
    $OutputPath = Join-Path $InputPath $OutputFileName
    $FinalReport | Out-File -FilePath $OutputPath -Encoding UTF8 -Force
    
    Write-Host "✅ Relatório consolidado salvo em: $OutputPath" -ForegroundColor Green
    
    return @{
        ReportPath = $OutputPath
        AnalyzedFiles = $AnalyzedFiles
        Categories = $CategorizedFiles.Count
        TotalFiles = $FileAnalyses.Count
    }
}

# Função para limpeza de arquivos analisados
function Remove-AnalyzedFiles {
    param([array]$FilesToDelete)
    
    if ($DeleteAnalyzedFiles -and $FilesToDelete.Count -gt 0) {
        Write-Host "🧹 Removendo arquivos analisados..." -ForegroundColor Yellow
        
        foreach ($File in $FilesToDelete) {
            try {
                Remove-Item -Path $File -Force
                Write-Host "🗑️  Removido: $(Split-Path $File -Leaf)" -ForegroundColor Gray
            }
            catch {
                Write-Warning "Não foi possível remover: $File"
            }
        }
        
        Write-Host "✅ Limpeza concluída" -ForegroundColor Green
    }
}

# EXECUÇÃO PRINCIPAL
try {
    Write-Host "`n" + ("="*80) -ForegroundColor Magenta
    Write-Host "    CONSOLIDAÇÃO AUTOMÁTICA DE DOCUMENTAÇÃO - INICIANDO" -ForegroundColor Magenta
    Write-Host ("="*80) -ForegroundColor Magenta
    
    # Criação de backup
    $BackupResult = New-DocumentationBackup -Path $InputPath
    
    # Consolidação principal
    $ConsolidationResult = Start-DocumentationConsolidation
    
    # Limpeza (se solicitada)
    if ($ConsolidationResult.AnalyzedFiles.Count -gt 0) {
        Remove-AnalyzedFiles -FilesToDelete $ConsolidationResult.AnalyzedFiles
    }
    
    # Relatório final
    Write-Host "`n" + ("="*80) -ForegroundColor Green
    Write-Host "    CONSOLIDAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
    Write-Host ("="*80) -ForegroundColor Green
    Write-Host "📊 Estatísticas finais:" -ForegroundColor Cyan
    Write-Host "   📁 Arquivos analisados: $($ConsolidationResult.TotalFiles)" -ForegroundColor White
    Write-Host "   📂 Categorias identificadas: $($ConsolidationResult.Categories)" -ForegroundColor White
    Write-Host "   📄 Relatório gerado: $($ConsolidationResult.ReportPath)" -ForegroundColor White
    if ($BackupResult) {
        Write-Host "   💾 Backup criado: $BackupResult" -ForegroundColor White
    }
    Write-Host "`n🎉 Processo finalizado! O relatório está pronto para análise." -ForegroundColor Green
    
}
catch {
    Write-Error "❌ Erro durante a consolidação: $($_.Exception.Message)"
    Write-Host "Stack trace completo salvo em error.log" -ForegroundColor Red
    $_.Exception | Out-File -FilePath "error.log" -Append
}
finally {
    Write-Host "`n📝 Para executar novamente, use:" -ForegroundColor Yellow
    Write-Host "   .\Consolidate-Documentation.ps1" -ForegroundColor Cyan
    Write-Host "   .\Consolidate-Documentation.ps1 -InputPath 'C:\Docs' -DeleteAnalyzedFiles:`$false" -ForegroundColor Cyan
}