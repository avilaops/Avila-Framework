# Script Master: Conversão para Markdown
# Autor: Nícolas Ávila | Framework: Ávila Inc.
# Data: 11/11/2025

param(
    [Parameter(Mandatory=$false)]
    [string]$InputPath,

    [Parameter(Mandatory=$false)]
    [string]$OutputPath,

    [Parameter(Mandatory=$false)]
    [switch]$GenerateStructure,

    [Parameter(Mandatory=$false)]
    [switch]$SyncToObsidian
)

# Configurações globais
$AvilaDocsPath = "C:\Users\nicol\OneDrive\Avila\Docs"
$ObsidianVaultPath = "C:\Users\nicol\ObsidianVault\Avila"

# Função principal de conversão
function Convert-ToMarkdown {
    param(
        [Parameter(Mandatory=$true)]
        [string]$InputFile,

        [string]$OutputFile
    )

    $file = Get-Item $InputFile -ErrorAction SilentlyContinue
    if (-not $file) {
        Write-Error "Arquivo não encontrado: $InputFile"
        return
    }

    $baseName = $file.BaseName
    $extension = $file.Extension.ToLower()

    if (-not $OutputFile) {
        $OutputFile = Join-Path $file.Directory "$baseName.md"
    }

    Write-Host "🔄 Convertendo: $($file.Name) → $([System.IO.Path]::GetFileName($OutputFile))" -ForegroundColor Yellow

    switch ($extension) {
        '.txt' {
            Convert-TextToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
        '.docx' {
            Convert-DocxToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
        '.pdf' {
            Convert-PdfToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
        '.csv' {
            Convert-CsvToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
        '.xlsx' {
            Convert-ExcelToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
        {$_ -in '.py','.js','.ts','.css','.html','.sql','.ps1','.json','.xml'} {
            Convert-CodeToMarkdown -InputFile $InputFile -OutputFile $OutputFile -Language $extension
        }
        default {
            Convert-GenericToMarkdown -InputFile $InputFile -OutputFile $OutputFile
        }
    }

    Add-MarkdownFrontmatter -FilePath $OutputFile -OriginalFile $file
    Write-Host "✅ Sucesso: $OutputFile" -ForegroundColor Green
}

# Conversão de texto simples
function Convert-TextToMarkdown {
    param($InputFile, $OutputFile)

    $content = Get-Content $InputFile -Raw -Encoding UTF8
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)

    $markdown = @"
# $baseName

$content
"@

    $markdown | Out-File $OutputFile -Encoding UTF8
}

# Conversão de Word (requer Pandoc)
function Convert-DocxToMarkdown {
    param($InputFile, $OutputFile)

    if (Get-Command pandoc -ErrorAction SilentlyContinue) {
        pandoc "$InputFile" -o "$OutputFile" --extract-media="$($AvilaDocsPath)\media"
    } else {
        Write-Warning "Pandoc não encontrado. Instalando..."
        Write-Host "Execute: choco install pandoc" -ForegroundColor Cyan
        return
    }
}

# Conversão de PDF (requer Python + pdfplumber)
function Convert-PdfToMarkdown {
    param($InputFile, $OutputFile)

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
    $pythonScript = @"
import pdfplumber
import sys
import os

try:
    with pdfplumber.open(r'$InputFile') as pdf:
        text = ''
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text += f'## Página {i}\n\n{page_text}\n\n'

    markdown_content = f'''# $baseName

**Arquivo Original:** {os.path.basename(r'$InputFile')}
**Páginas:** {len(pdf.pages)}
**Extraído em:** {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}

---

{text}'''

    with open(r'$OutputFile', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f'✅ PDF convertido: $OutputFile')
except Exception as e:
    print(f'❌ Erro: {e}')
"@

    $pythonScript | Out-File "temp_pdf_converter.py" -Encoding UTF8
    python "temp_pdf_converter.py"
    Remove-Item "temp_pdf_converter.py" -ErrorAction SilentlyContinue
}

# Conversão de CSV para tabela Markdown
function Convert-CsvToMarkdown {
    param($InputFile, $OutputFile)

    try {
        $csv = Import-Csv $InputFile
        $baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)

        $markdown = "# $baseName`n`n"

        # Cabeçalho da tabela
        $headers = $csv[0].PSObject.Properties.Name
        $markdown += "| " + ($headers -join " | ") + " |`n"
        $markdown += "|" + (" ---" * $headers.Count) + " |`n"

        # Dados
        foreach ($row in $csv) {
            $values = $headers | ForEach-Object {
                $cellValue = $row.$_
                if ($cellValue -match '[|]') { $cellValue = $cellValue -replace '\|', '\|' }
                $cellValue
            }
            $markdown += "| " + ($values -join " | ") + " |`n"
        }

        $markdown += "`n**Total de registros:** $($csv.Count)"
        $markdown | Out-File $OutputFile -Encoding UTF8

    } catch {
        Write-Error "Erro ao converter CSV: $_"
    }
}

# Conversão de código mantendo sintaxe
function Convert-CodeToMarkdown {
    param($InputFile, $OutputFile, $Language)

    $content = Get-Content $InputFile -Raw -Encoding UTF8
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
    $fileName = [System.IO.Path]::GetFileName($InputFile)

    # Mapear extensões para linguagens
    $languageMap = @{
        '.py' = 'python'
        '.js' = 'javascript'
        '.ts' = 'typescript'
        '.ps1' = 'powershell'
        '.css' = 'css'
        '.html' = 'html'
        '.sql' = 'sql'
        '.json' = 'json'
        '.xml' = 'xml'
    }

    $syntaxLang = if ($languageMap[$Language]) { $languageMap[$Language] } else { $Language.TrimStart('.') }

    $markdown = @"
# $baseName

**Arquivo:** ``$fileName``
**Linguagem:** $syntaxLang
**Tamanho:** $([math]::Round((Get-Item $InputFile).Length / 1KB, 2)) KB

---

````$syntaxLang
$content
````

---
**Última modificação:** $(Get-Date (Get-Item $InputFile).LastWriteTime -Format "dd/MM/yyyy HH:mm")
"@    $markdown | Out-File $OutputFile -Encoding UTF8
}

# Conversão genérica
function Convert-GenericToMarkdown {
    param($InputFile, $OutputFile)

    $content = Get-Content $InputFile -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $content) {
        $content = "[Conteúdo binário ou não legível]"
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputFile)
    $fileName = [System.IO.Path]::GetFileName($InputFile)

    $markdown = @"
# $baseName

**Arquivo Original:** ``$fileName``
**Tipo:** $(([System.IO.Path]::GetExtension($InputFile)).ToUpper())

---

````
$content
````
"@    $markdown | Out-File $OutputFile -Encoding UTF8
}

# Adicionar metadados YAML
function Add-MarkdownFrontmatter {
    param($FilePath, $OriginalFile)

    $content = Get-Content $FilePath -Raw
    $title = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)

    $frontmatter = @"
---
title: "$title"
created: $(Get-Date -Format "yyyy-MM-dd")
modified: $(Get-Date $OriginalFile.LastWriteTime -Format "yyyy-MM-dd")
original_file: "$($OriginalFile.Name)"
tags: [avila, converted, $($OriginalFile.Extension.TrimStart('.').ToLower())]
---

$content
"@

    $frontmatter | Set-Content $FilePath -Encoding UTF8
}

# Gerar estrutura do projeto
function Export-ProjectStructure {
    param(
        [string]$ProjectPath = "C:\Users\nicol\OneDrive\Avila",
        [string]$OutputFile = "$AvilaDocsPath\avila-estrutura.md"
    )

    Write-Host "📁 Gerando estrutura do projeto..." -ForegroundColor Cyan

    $structure = @"
# Estrutura do Projeto Ávila

**Caminho Base:** ``$ProjectPath``
**Gerado em:** $(Get-Date -Format "dd/MM/yyyy HH:mm")

---

## Árvore de Diretórios

````
"@

    # Usar tree se disponível, senão gerar manualmente
    try {
        $tree = tree $ProjectPath /F /A | Select-Object -Skip 1
        $structure += ($tree -join "`n")
    } catch {
        # Fallback manual se tree não funcionar
        $structure += "Estrutura do projeto Avila`n"
    }

    $structure += @"

````

## Estatísticas

"@    $files = Get-ChildItem -Path $ProjectPath -Recurse -File -ErrorAction SilentlyContinue
    $folders = Get-ChildItem -Path $ProjectPath -Recurse -Directory -ErrorAction SilentlyContinue

    $structure += "- **Total de Arquivos:** $($files.Count)`n"
    $structure += "- **Total de Pastas:** $($folders.Count)`n"
    $structure += "- **Tamanho Total:** $([math]::Round(($files | Measure-Object Length -Sum).Sum / 1MB, 2)) MB`n`n"

    $structure += "## Arquivos por Extensão`n`n"
    $extensions = $files | Group-Object Extension | Sort-Object Count -Descending | Select-Object -First 10
    foreach ($ext in $extensions) {
        $extName = if ($ext.Name) { $ext.Name } else { "[sem extensão]" }
        $structure += "- **$extName:** $($ext.Count) arquivos`n"
    }

    $structure | Out-File $OutputFile -Encoding UTF8
    Write-Host "✅ Estrutura salva em: $OutputFile" -ForegroundColor Green
}

# Sincronizar com Obsidian
function Sync-ToObsidian {
    Write-Host "🔄 Sincronizando com Obsidian..." -ForegroundColor Cyan

    if (-not (Test-Path $ObsidianVaultPath)) {
        New-Item -ItemType Directory -Path $ObsidianVaultPath -Force | Out-Null
    }

    robocopy $AvilaDocsPath $ObsidianVaultPath *.md /MIR /Z /NDL /NJH /NJS
    Write-Host "✅ Sincronização concluída!" -ForegroundColor Green
}

# EXECUÇÃO PRINCIPAL
Write-Host @"
🚀 ÁVILA MARKDOWN CONVERTER
================================
Framework: Ávila Inc.
Autor: Nícolas Ávila
Data: $(Get-Date -Format "dd/MM/yyyy")
"@ -ForegroundColor Magenta

# Gerar estrutura se solicitado
if ($GenerateStructure) {
    Export-ProjectStructure
}

# Converter arquivo específico
if ($InputPath) {
    if (Test-Path $InputPath) {
        Convert-ToMarkdown -InputFile $InputPath -OutputFile $OutputPath
    } else {
        Write-Error "Arquivo não encontrado: $InputPath"
    }
} else {
    # Menu interativo
    Write-Host "`nOpções disponíveis:" -ForegroundColor Yellow
    Write-Host "1. Converter arquivo específico"
    Write-Host "2. Converter todos os arquivos de uma pasta"
    Write-Host "3. Gerar estrutura do projeto"
    Write-Host "4. Sincronizar com Obsidian"
    Write-Host "5. Sair"

    do {
        $choice = Read-Host "`nEscolha uma opção (1-5)"

        switch ($choice) {
            '1' {
                $file = Read-Host "Caminho do arquivo"
                if (Test-Path $file) {
                    Convert-ToMarkdown -InputFile $file
                } else {
                    Write-Host "❌ Arquivo não encontrado!" -ForegroundColor Red
                }
            }
            '2' {
                $folder = Read-Host "Caminho da pasta"
                if (Test-Path $folder) {
                    $files = Get-ChildItem $folder -File | Where-Object { $_.Extension -ne '.md' }
                    foreach ($file in $files) {
                        Convert-ToMarkdown -InputFile $file.FullName
                    }
                } else {
                    Write-Host "❌ Pasta não encontrada!" -ForegroundColor Red
                }
            }
            '3' {
                Export-ProjectStructure
            }
            '4' {
                Sync-ToObsidian
            }
            '5' {
                Write-Host "👋 Até logo!" -ForegroundColor Cyan
                break
            }
            default {
                Write-Host "❌ Opção inválida!" -ForegroundColor Red
            }
        }
    } while ($choice -ne '5')
}

# Sincronizar com Obsidian se solicitado
if ($SyncToObsidian) {
    Sync-ToObsidian
}

Write-Host "`n🎯 Processo concluído!" -ForegroundColor Green
