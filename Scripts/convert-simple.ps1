# Ávila Markdown Converter - Versão Simplificada
# Autor: Nícolas Ávila | Framework: Ávila Inc.

param(
    [Parameter(Mandatory=$false)]
    [string]$InputPath,

    [Parameter(Mandatory=$false)]
    [switch]$GenerateStructure
)

$AvilaDocsPath = "C:\Users\nicol\OneDrive\Avila\Docs"

# Função para gerar estrutura do projeto
function Export-ProjectStructure {
    Write-Host "📁 Gerando estrutura do projeto..." -ForegroundColor Cyan

    $ProjectPath = "C:\Users\nicol\OneDrive\Avila"
    $OutputFile = "$AvilaDocsPath\avila-estrutura.md"

    # Coletar estatísticas
    $files = Get-ChildItem -Path $ProjectPath -Recurse -File -ErrorAction SilentlyContinue
    $folders = Get-ChildItem -Path $ProjectPath -Recurse -Directory -ErrorAction SilentlyContinue

    $structure = @"
# Estrutura do Projeto Ávila

**Caminho Base:** ``$ProjectPath``
**Gerado em:** $(Get-Date -Format "dd/MM/yyyy HH:mm")

---

## Árvore de Diretórios Principal

````
AVILA/
├── AvilaInc/           # Governança, finanças, marketing, jurídico
├── AvilaOps/           # Engenharia, DevOps, AI, infraestrutura
├── Docs/               # Documentação e relatórios oficiais
├── Logs/               # Logs de sistema e auditoria
├── Scripts/            # Scripts de automação e utilitários
├── Setup/              # Configuração e instalação
└── Shared/             # Templates e backups globais
````

## Estatísticas Gerais

- **Total de Arquivos:** $($files.Count)
- **Total de Pastas:** $($folders.Count)
- **Tamanho Total:** $([math]::Round(($files | Measure-Object Length -Sum).Sum / 1MB, 2)) MB

## Distribuição por Extensão

"@

    # Top 15 extensões mais comuns
    $extensions = $files | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 15
    foreach ($ext in $extensions) {
        $extName = if ($ext.Name) { $ext.Name.ToUpper() } else { "[SEM EXTENSÃO]" }
        $structure += "- **$extName:** $($ext.Count) arquivos`n"
    }

    $structure += @"

## Estrutura Detalhada por Setor

### 🏢 AvilaInc (Corporativo)
````
AvilaInc/
├── docs/                   # Documentação corporativa
├── finance/                # Financeiro e controladoria
├── governance_framework/   # Estrutura de governança
├── legal/                  # Jurídico e compliance
└── marketing/              # Marketing e comunicação
````

### ⚙️ AvilaOps (Operacional)
````
AvilaOps/
├── ai/                     # Inteligência artificial e ML
├── data/                   # Dados e analytics
├── devops/                 # DevOps e CI/CD
├── docs/                   # Documentação técnica
├── governance/             # Governança técnica
├── infra/                  # Infraestrutura
├── products/               # Produtos e soluções
└── research/               # Pesquisa e desenvolvimento
````

### 📚 Documentação
````
Docs/
├── Instruções/             # Guias e manuais
├── Relatórios/             # Relatórios executivos
└── [Diversos arquivos MD] # Documentos diversos
````

---

**Framework:** Ávila Inc.
**Responsável:** Nícolas Ávila
**Última Atualização:** $(Get-Date -Format "dd/MM/yyyy HH:mm")

> 💡 **Dica:** Use este mapa para navegar rapidamente pelo ecossistema Ávila no Obsidian!
"@

    # Salvar o arquivo
    $structure | Out-File $OutputFile -Encoding UTF8
    Write-Host "✅ Estrutura salva em: $OutputFile" -ForegroundColor Green

    return $OutputFile
}

# Função simples para converter qualquer arquivo
function Convert-AnyFileToMarkdown {
    param([string]$FilePath)

    $file = Get-Item $FilePath
    $baseName = $file.BaseName
    $extension = $file.Extension.ToLower()
    $outputPath = Join-Path $file.Directory "$baseName.md"

    Write-Host "🔄 Convertendo: $($file.Name)" -ForegroundColor Yellow

    try {
        switch ($extension) {
            '.txt' {
                $content = Get-Content $FilePath -Raw -Encoding UTF8
                $markdown = "# $baseName`n`n$content"
            }
            '.csv' {
                $csv = Import-Csv $FilePath
                $markdown = "# $baseName`n`n"

                # Criar tabela Markdown
                $headers = $csv[0].PSObject.Properties.Name
                $markdown += "| " + ($headers -join " | ") + " |`n"
                $markdown += "|" + (" ---" * $headers.Count) + " |`n"

                foreach ($row in $csv) {
                    $values = $headers | ForEach-Object { $row.$_ }
                    $markdown += "| " + ($values -join " | ") + " |`n"
                }
            }
            {$_ -in '.py','.js','.ps1','.sql'} {
                $content = Get-Content $FilePath -Raw -Encoding UTF8
                $language = switch ($extension) {
                    '.py' { 'python' }
                    '.js' { 'javascript' }
                    '.ps1' { 'powershell' }
                    '.sql' { 'sql' }
                }
                $markdown = "# $baseName`n`n````$language`n$content`n````"
            }
            default {
                $content = Get-Content $FilePath -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
                if ($content) {
                    $markdown = "# $baseName`n`n`````n$content`n````"
                } else {
                    $markdown = "# $baseName`n`n*[Arquivo binário ou não legível]*"
                }
            }
        }

        # Adicionar metadados
        $frontmatter = @"
---
title: "$baseName"
created: $(Get-Date -Format "yyyy-MM-dd")
original_file: "$($file.Name)"
tags: [avila, converted]
---

$markdown
"@

        $frontmatter | Out-File $outputPath -Encoding UTF8
        Write-Host "✅ Convertido para: $outputPath" -ForegroundColor Green

    } catch {
        Write-Host "❌ Erro ao converter: $_" -ForegroundColor Red
    }
}

# EXECUÇÃO PRINCIPAL
Write-Host @"
🚀 ÁVILA MARKDOWN CONVERTER (Simplificado)
==========================================
Framework: Ávila Inc.
Data: $(Get-Date -Format "dd/MM/yyyy")
"@ -ForegroundColor Magenta

if ($GenerateStructure) {
    Export-ProjectStructure
    exit
}

if ($InputPath) {
    if (Test-Path $InputPath) {
        Convert-AnyFileToMarkdown -FilePath $InputPath
    } else {
        Write-Host "❌ Arquivo não encontrado: $InputPath" -ForegroundColor Red
    }
} else {
    Write-Host "`nUso:" -ForegroundColor Yellow
    Write-Host "  .\convert-simple.ps1 -GenerateStructure"
    Write-Host "  .\convert-simple.ps1 -InputPath 'caminho\arquivo.txt'"
    Write-Host ""
    Write-Host "Ou execute sem parâmetros para modo interativo..."

    $choice = Read-Host "`nGerar estrutura do projeto? (s/n)"
    if ($choice -eq 's' -or $choice -eq 'S') {
        Export-ProjectStructure
    }
}

Write-Host "`n✅ Concluído!" -ForegroundColor Green
