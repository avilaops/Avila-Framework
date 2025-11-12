# Guia de Conversão de Arquivos para Markdown (.md)

## Contexto
Este guia ensina como converter qualquer tipo de arquivo para Markdown (.md) para organizar sua base de conhecimento no Obsidian, mantendo a mesma estrutura visual que você vê no VS Code.

---

## Métodos de Conversão

### 1. **Arquivos de Texto (.txt, .rtf)**

#### Via PowerShell (Método Rápido)
```powershell
# Renomear simples
Get-ChildItem -Path "C:\Users\nicol\OneDrive\Avila\Docs\" -Filter "*.txt" |
    ForEach-Object {
        Rename-Item $_.FullName -NewName ($_.BaseName + ".md")
    }
```

#### Via VS Code
1. Abra o arquivo `.txt`
2. `Ctrl+Shift+P` → "Save As"
3. Altere a extensão para `.md`
4. O VS Code automaticamente aplicará highlight de Markdown

---

### 2. **Documentos Word (.docx, .doc)**

#### Usando Pandoc (Recomendado)
```powershell
# Instalar Pandoc primeiro
choco install pandoc

# Converter arquivo único
pandoc "arquivo.docx" -o "arquivo.md"

# Converter pasta inteira
Get-ChildItem -Path ".\*.docx" | ForEach-Object {
    pandoc $_.FullName -o ($_.BaseName + ".md")
}
```

#### Usando PowerShell + Word COM
```powershell
# Script para converter Word → Markdown
$word = New-Object -ComObject Word.Application
$word.Visible = $false

Get-ChildItem "*.docx" | ForEach-Object {
    $doc = $word.Documents.Open($_.FullName)
    $markdownPath = $_.FullName -replace "\.docx$", ".md"

    # Salvar como texto e depois formatar
    $doc.SaveAs2($markdownPath, 2)
    $doc.Close()
}

$word.Quit()
```

---

### 3. **PDFs**

#### Via OCR + Pandoc
```powershell
# Primeiro extrair texto do PDF
pip install pdfplumber

# Script Python para extrair texto
python -c "
import pdfplumber
import sys

with pdfplumber.open(sys.argv[1]) as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text() + '\n\n'

    with open(sys.argv[1].replace('.pdf', '.md'), 'w', encoding='utf-8') as f:
        f.write('# ' + sys.argv[1].replace('.pdf', '') + '\n\n')
        f.write(text)
" "arquivo.pdf"
```

---

### 4. **Planilhas Excel (.xlsx, .csv)**

#### CSV → Markdown Table
```powershell
# Script para converter CSV em tabela Markdown
$csv = Import-Csv "dados.csv"
$markdown = "# Dados da Planilha`n`n"

# Cabeçalho da tabela
$headers = $csv[0].PSObject.Properties.Name
$markdown += "| " + ($headers -join " | ") + " |`n"
$markdown += "|" + (" ---" * $headers.Count) + " |`n"

# Dados
foreach ($row in $csv) {
    $values = $headers | ForEach-Object { $row.$_ }
    $markdown += "| " + ($values -join " | ") + " |`n"
}

$markdown | Out-File "dados.md" -Encoding UTF8
```

---

### 5. **Apresentações PowerPoint (.pptx)**

#### Via Pandoc + ImageMagick
```powershell
# Converter slides em imagens primeiro
magick convert "apresentacao.pptx" "slide_%02d.png"

# Criar Markdown com as imagens
$markdown = @"
# Apresentação

"@

Get-ChildItem "slide_*.png" | ForEach-Object {
    $slideNum = [regex]::Match($_.Name, '\d+').Value
    $markdown += "`n## Slide $slideNum`n`n"
    $markdown += "![$($_.Name)]($($_.Name))`n`n"
}

$markdown | Out-File "apresentacao.md" -Encoding UTF8
```

---

### 6. **Código Fonte (Qualquer Linguagem)**

#### Preservar Sintaxe
```powershell
# Script para converter código mantendo syntax highlighting
$extension = Read-Host "Digite a extensão do arquivo (ex: py, js, css)"
$language = @{
    'py' = 'python'
    'js' = 'javascript'
    'ts' = 'typescript'
    'css' = 'css'
    'html' = 'html'
    'sql' = 'sql'
    'ps1' = 'powershell'
}

Get-ChildItem "*.$extension" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $markdown = @"
# $($_.BaseName)

## Arquivo Original: $($_.Name)

``````$($language[$extension])
$content
``````

**Última modificação:** $(Get-Date $_.LastWriteTime -Format "dd/MM/yyyy HH:mm")
"@

    $markdown | Out-File "$($_.BaseName).md" -Encoding UTF8
}
```

---

### 7. **Estrutura de Pastas (Como no VS Code)**

#### Gerar Árvore de Arquivos
```powershell
# Função para gerar estrutura em Markdown
function Export-FolderStructure {
    param(
        [string]$Path = ".",
        [string]$OutputFile = "estrutura-projeto.md"
    )

    $structure = @"
# Estrutura do Projeto: $(Split-Path $Path -Leaf)

## Caminho Base
``````
$((Resolve-Path $Path).Path)
``````

## Árvore de Arquivos
``````
"@

    # Gerar árvore usando tree command
    $tree = tree $Path /F /A
    $structure += $tree -join "`n"
    $structure += "`n``````"

    # Adicionar estatísticas
    $files = Get-ChildItem -Path $Path -Recurse -File
    $folders = Get-ChildItem -Path $Path -Recurse -Directory

    $structure += @"

## Estatísticas
- **Total de Arquivos:** $($files.Count)
- **Total de Pastas:** $($folders.Count)
- **Tamanho Total:** $([math]::Round(($files | Measure-Object Length -Sum).Sum / 1MB, 2)) MB

## Arquivos por Extensão
"@

    $extensions = $files | Group-Object Extension | Sort-Object Count -Descending
    foreach ($ext in $extensions) {
        $structure += "`n- **$($ext.Name):** $($ext.Count) arquivos"
    }

    $structure += @"

---
**Gerado em:** $(Get-Date -Format "dd/MM/yyyy HH:mm")
**Ferramenta:** PowerShell + VS Code
**Autor:** Ávila Framework
"@

    $structure | Out-File $OutputFile -Encoding UTF8
    Write-Host "Estrutura salva em: $OutputFile"
}

# Usar a função
Export-FolderStructure -Path "C:\Users\nicol\OneDrive\Avila" -OutputFile "C:\Users\nicol\OneDrive\Avila\Docs\avila-estrutura.md"
```

---

## Automatização Total

### Script Master de Conversão
```powershell
# Script principal para converter qualquer arquivo
function Convert-ToMarkdown {
    param(
        [Parameter(Mandatory=$true)]
        [string]$InputPath,

        [string]$OutputPath
    )

    $file = Get-Item $InputPath
    $baseName = $file.BaseName
    $extension = $file.Extension.ToLower()

    if (-not $OutputPath) {
        $OutputPath = Join-Path $file.Directory "$baseName.md"
    }

    switch ($extension) {
        '.txt' {
            $content = Get-Content $InputPath -Raw
            "# $baseName`n`n$content" | Out-File $OutputPath -Encoding UTF8
        }
        '.docx' {
            pandoc $InputPath -o $OutputPath
        }
        '.pdf' {
            python -c "import pdfplumber; import sys; pdf = pdfplumber.open('$InputPath'); text = ''.join([page.extract_text() for page in pdf.pages]); open('$OutputPath', 'w', encoding='utf-8').write(f'# $baseName\n\n{text}')"
        }
        '.csv' {
            $csv = Import-Csv $InputPath
            # [código da conversão CSV→MD table aqui]
        }
        default {
            $content = Get-Content $InputPath -Raw
            "# $baseName`n`n``````$($extension.Replace('.',''))`n$content`n``````" | Out-File $OutputPath -Encoding UTF8
        }
    }

    Write-Host "✅ Convertido: $OutputPath"
}

# Exemplos de uso:
# Convert-ToMarkdown -InputPath "documento.docx"
# Convert-ToMarkdown -InputPath "planilha.csv" -OutputPath "C:\Users\nicol\OneDrive\Avila\Docs\planilha.md"
```

---

## Integração com Obsidian

### Configurações Recomendadas

1. **Pasta de Vault do Obsidian:**
   ```
   C:\Users\nicol\ObsidianVault\Avila\
   ```

2. **Sincronização Automática:**
   ```powershell
   # Script de sincronização
   robocopy "C:\Users\nicol\OneDrive\Avila\Docs" "C:\Users\nicol\ObsidianVault\Avila" *.md /MIR /Z
   ```

3. **Plugins Úteis no Obsidian:**
   - **Dataview** - Para queries dinâmicas
   - **Templater** - Templates automáticos
   - **Advanced Tables** - Edição de tabelas
   - **Image Gallery** - Galeria de imagens

---

## Dicas Avançadas

### 1. Manter Links Internos
```powershell
# Converter links relativos para funcionar no Obsidian
(Get-Content "arquivo.md" -Raw) -replace '\[([^\]]+)\]\(([^)]+)\)', '[[\\$2|\\$1]]' | Set-Content "arquivo.md"
```

### 2. Adicionar Metadados YAML
```powershell
# Adicionar frontmatter em todos os .md
Get-ChildItem "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $frontmatter = @"
---
title: $($_.BaseName)
created: $(Get-Date -Format "yyyy-MM-dd")
modified: $(Get-Date $_.LastWriteTime -Format "yyyy-MM-dd")
tags: [avila, docs]
---

$content
"@
    $frontmatter | Set-Content $_.FullName
}
```

### 3. Criar Índice Automático
```powershell
# Gerar índice de todos os documentos
$docs = Get-ChildItem "C:\Users\nicol\OneDrive\Avila\Docs\*.md"
$index = "# Índice de Documentos Ávila`n`n"

foreach ($doc in $docs) {
    $title = (Get-Content $doc.FullName | Select-Object -First 1) -replace '^# ', ''
    $index += "- [[$($doc.BaseName)|$title]]`n"
}

$index | Out-File "C:\Users\nicol\ObsidianVault\Avila\INDEX.md" -Encoding UTF8
```

---

## Recursos Adicionais

### Ferramentas Recomendadas
- **Pandoc** - Conversão universal de documentos
- **ImageMagick** - Processamento de imagens
- **pdfplumber** - Extração de texto de PDFs
- **tree** - Geração de estruturas de pastas

### Extensões VS Code
- **Markdown All in One**
- **Markdown Preview Enhanced**
- **Table Formatter**

---

**Versão:** 1.0
**Data:** 11/11/2025
**Autor:** Nícolas Ávila
**Framework:** Ávila Inc.

> 💡 **Dica Final:** Use o VS Code como seu "centro de comando" para todas as conversões. Ele tem preview de Markdown em tempo real e integração perfeita com Obsidian!
