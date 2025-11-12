# 🤖 Archivus - Sistema de Automação de Documentação
# Versão: 1.0
# Autor: Ávila Ops
# Data: 2025-11-12

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("index", "validate", "audit", "organize", "standardize", "archive", "sync", "report")]
    [string]$Command = "audit",

    [Parameter(Mandatory=$false)]
    [string]$Path = "c:\Users\nicol\OneDrive\Avila\Docs",

    [Parameter(Mandatory=$false)]
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ArchivusVersion = "1.0.0"

# ═══════════════════════════════════════════════════════════
# ARCHIVUS ASCII ART
# ═══════════════════════════════════════════════════════════

function Show-ArchivusBanner {
    Write-Host @"

    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     █████╗ ██████╗  ██████╗██╗  ██╗██╗██╗   ██╗███████╗ ║
    ║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██║██║   ██║██╔════╝ ║
    ║    ███████║██████╔╝██║     ███████║██║██║   ██║███████╗ ║
    ║    ██╔══██║██╔══██╗██║     ██╔══██║██║╚██╗ ██╔╝╚════██║ ║
    ║    ██║  ██║██║  ██║╚██████╗██║  ██║██║ ╚████╔╝ ███████║ ║
    ║    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝ ║
    ║                                                           ║
    ║              O Guardião da Documentação                  ║
    ║                   Versão $ArchivusVersion                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan
}

# ═══════════════════════════════════════════════════════════
# UTILITÁRIOS
# ═══════════════════════════════════════════════════════════

function Write-ArchivusLog {
    param([string]$Message, [string]$Level = "INFO")

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "White" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        default { "White" }
    }

    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

function Get-DocumentMetadata {
    param([string]$FilePath)

    $content = Get-Content -Path $FilePath -Raw -ErrorAction SilentlyContinue
    if (-not $content) { return $null }

    # Extrair frontmatter YAML
    if ($content -match "^---\r?\n(.*?)\r?\n---") {
        $frontmatter = $matches[1]
        $metadata = @{}

        foreach ($line in $frontmatter -split "\r?\n") {
            if ($line -match "^(\w+):\s*(.+)$") {
                $metadata[$matches[1]] = $matches[2].Trim('"')
            }
        }

        return $metadata
    }

    return $null
}

# ═══════════════════════════════════════════════════════════
# COMANDO: INDEX
# ═══════════════════════════════════════════════════════════

function Invoke-Index {
    Write-ArchivusLog "Indexando documentação em: $Path" "INFO"

    $files = Get-ChildItem -Path $Path -Recurse -File -Include "*.md" -Exclude "INDEX.md"
    $index = @{
        generated = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        total_files = $files.Count
        by_type = @{}
        by_category = @{}
        by_folder = @{}
    }

    foreach ($file in $files) {
        $relativePath = $file.FullName.Replace($Path, "").TrimStart('\')
        $folder = Split-Path $relativePath -Parent

        # Contar por pasta
        if (-not $index.by_folder.ContainsKey($folder)) {
            $index.by_folder[$folder] = 0
        }
        $index.by_folder[$folder]++

        # Extrair metadata
        $metadata = Get-DocumentMetadata -FilePath $file.FullName
        if ($metadata) {
            if ($metadata.type) {
                if (-not $index.by_type.ContainsKey($metadata.type)) {
                    $index.by_type[$metadata.type] = 0
                }
                $index.by_type[$metadata.type]++
            }
        }
    }

    Write-ArchivusLog "Total de arquivos indexados: $($index.total_files)" "SUCCESS"
    Write-ArchivusLog "Por tipo: $($index.by_type | ConvertTo-Json -Compress)" "INFO"

    return $index
}

# ═══════════════════════════════════════════════════════════
# COMANDO: VALIDATE
# ═══════════════════════════════════════════════════════════

function Invoke-Validate {
    Write-ArchivusLog "Validando estrutura de documentos..." "INFO"

    $files = Get-ChildItem -Path $Path -Recurse -File -Include "*.md"
    $issues = @{
        missing_frontmatter = @()
        invalid_naming = @()
        missing_required_fields = @()
    }

    foreach ($file in $files) {
        # Validar frontmatter
        $metadata = Get-DocumentMetadata -FilePath $file.FullName
        if (-not $metadata) {
            $issues.missing_frontmatter += $file.FullName
            continue
        }

        # Validar campos obrigatórios
        $required = @("title", "created", "tags")
        foreach ($field in $required) {
            if (-not $metadata.ContainsKey($field)) {
                $issues.missing_required_fields += "$($file.FullName) (falta: $field)"
            }
        }

        # Validar nomenclatura
        if ($file.Name -match '\s' -or $file.Name -match '[àáâãäèéêëìíîïòóôõöùúûü]') {
            $issues.invalid_naming += $file.FullName
        }
    }

    $totalIssues = $issues.missing_frontmatter.Count +
                   $issues.invalid_naming.Count +
                   $issues.missing_required_fields.Count

    if ($totalIssues -eq 0) {
        Write-ArchivusLog "✅ Validação completa! Nenhum issue encontrado." "SUCCESS"
    } else {
        Write-ArchivusLog "⚠️ Validação encontrou $totalIssues issues" "WARNING"

        if ($issues.missing_frontmatter.Count -gt 0) {
            Write-ArchivusLog "Sem frontmatter: $($issues.missing_frontmatter.Count)" "WARNING"
        }
        if ($issues.invalid_naming.Count -gt 0) {
            Write-ArchivusLog "Nomenclatura inválida: $($issues.invalid_naming.Count)" "WARNING"
        }
        if ($issues.missing_required_fields.Count -gt 0) {
            Write-ArchivusLog "Campos obrigatórios ausentes: $($issues.missing_required_fields.Count)" "WARNING"
        }
    }

    return $issues
}

# ═══════════════════════════════════════════════════════════
# COMANDO: AUDIT
# ═══════════════════════════════════════════════════════════

function Invoke-Audit {
    Write-ArchivusLog "Auditando saúde da documentação..." "INFO"

    $audit = @{
        timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        health_score = 100
        issues = @{
            broken_links = @()
            missing_frontmatter = @()
            duplicates = @()
            orphans = @()
            binaries_in_root = @()
        }
        metrics = @{
            total_docs = 0
            total_size = 0
            avg_size = 0
        }
    }

    # Contar documentos
    $docs = Get-ChildItem -Path $Path -Recurse -File -Include "*.md"
    $audit.metrics.total_docs = $docs.Count
    $audit.metrics.total_size = ($docs | Measure-Object -Property Length -Sum).Sum
    $audit.metrics.avg_size = [math]::Round($audit.metrics.total_size / $docs.Count, 2)

    # Verificar binários na raiz
    $binariesInRoot = Get-ChildItem -Path $Path -File | Where-Object {
        $_.Extension -in @(".dll", ".exe", ".pri", ".winmd", ".pdb")
    }
    $audit.issues.binaries_in_root = $binariesInRoot | ForEach-Object { $_.Name }

    # Verificar frontmatter
    foreach ($doc in $docs) {
        $metadata = Get-DocumentMetadata -FilePath $doc.FullName
        if (-not $metadata) {
            $audit.issues.missing_frontmatter += $doc.FullName.Replace($Path, "")
        }
    }

    # Calcular health score
    $deductions = 0
    $deductions += $audit.issues.binaries_in_root.Count * 0.5
    $deductions += $audit.issues.missing_frontmatter.Count * 2

    $audit.health_score = [math]::Max(0, 100 - $deductions)

    # Relatório
    Write-ArchivusLog "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"
    Write-ArchivusLog "RELATÓRIO DE AUDITORIA" "INFO"
    Write-ArchivusLog "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"
    Write-ArchivusLog "Health Score: $($audit.health_score)/100" $(if($audit.health_score -gt 80){"SUCCESS"}elseif($audit.health_score -gt 50){"WARNING"}else{"ERROR"})
    Write-ArchivusLog "Total de Documentos: $($audit.metrics.total_docs)" "INFO"
    Write-ArchivusLog "Tamanho Total: $([math]::Round($audit.metrics.total_size / 1MB, 2)) MB" "INFO"
    Write-ArchivusLog "" "INFO"
    Write-ArchivusLog "ISSUES:" "WARNING"
    Write-ArchivusLog "  • Binários na raiz: $($audit.issues.binaries_in_root.Count)" "WARNING"
    Write-ArchivusLog "  • Sem frontmatter: $($audit.issues.missing_frontmatter.Count)" "WARNING"
    Write-ArchivusLog "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "INFO"

    return $audit
}

# ═══════════════════════════════════════════════════════════
# COMANDO: REPORT
# ═══════════════════════════════════════════════════════════

function Invoke-Report {
    Write-ArchivusLog "Gerando relatório semanal..." "INFO"

    $reportPath = Join-Path $Path "Relatorios\Archivus-Weekly-Report-$(Get-Date -Format 'yyyy-MM-dd').md"
    $reportDir = Split-Path $reportPath -Parent

    if (-not (Test-Path $reportDir)) {
        New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
    }

    # Executar audit
    $audit = Invoke-Audit

    # Executar index
    $index = Invoke-Index

    # Gerar relatório markdown
    $report = @"
# 📊 Relatório Semanal do Archivus

> **Gerado em:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
> **Health Score:** $($audit.health_score)/100
> **Status:** $(if($audit.health_score -gt 80){"🟢 Saudável"}elseif($audit.health_score -gt 50){"🟡 Atenção"}else{"🔴 Crítico"})

---

## 📈 Métricas Gerais

| Métrica | Valor |
|---------|-------|
| Total de Documentos | $($audit.metrics.total_docs) |
| Tamanho Total | $([math]::Round($audit.metrics.total_size / 1MB, 2)) MB |
| Tamanho Médio | $([math]::Round($audit.metrics.avg_size / 1KB, 2)) KB |

---

## 🚨 Issues Identificados

### Binários na Raiz: $($audit.issues.binaries_in_root.Count)
$(if($audit.issues.binaries_in_root.Count -gt 0){"- " + ($audit.issues.binaries_in_root -join "`n- ")}else{"✅ Nenhum binário na raiz"})

### Sem Frontmatter: $($audit.issues.missing_frontmatter.Count)
$(if($audit.issues.missing_frontmatter.Count -gt 0){"⚠️ $($audit.issues.missing_frontmatter.Count) arquivos sem frontmatter"}else{"✅ Todos os documentos têm frontmatter"})

---

## 📁 Distribuição por Pasta

$(($index.by_folder.GetEnumerator() | Sort-Object Value -Descending | ForEach-Object { "- **$($_.Key)**: $($_.Value) arquivos" }) -join "`n")

---

## 🎯 Recomendações

$(if($audit.issues.binaries_in_root.Count -gt 0){"- 🔴 Mover binários para /bin"}else{""})
$(if($audit.issues.missing_frontmatter.Count -gt 5){"- 🟡 Adicionar frontmatter em documentos"}else{""})
$(if($audit.health_score -lt 80){"- 🔴 Executar limpeza e reorganização"}else{"- ✅ Manter padrão atual"})

---

**Próxima auditoria:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss" -Date (Get-Date).AddDays(7))
**Responsável:** Archivus v$ArchivusVersion
"@

    Set-Content -Path $reportPath -Value $report -Encoding UTF8
    Write-ArchivusLog "✅ Relatório salvo em: $reportPath" "SUCCESS"

    return $reportPath
}

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

Show-ArchivusBanner

switch ($Command) {
    "index" {
        Invoke-Index
    }
    "validate" {
        Invoke-Validate
    }
    "audit" {
        Invoke-Audit
    }
    "report" {
        Invoke-Report
    }
    default {
        Write-ArchivusLog "Comando não implementado: $Command" "ERROR"
    }
}

Write-Host "`n✨ Archivus nunca dorme. Ele observa, organiza, protege. ✨`n" -ForegroundColor Cyan
