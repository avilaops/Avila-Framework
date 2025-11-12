# 🎯 Plano de Ação: Reorganização da Documentação Ávila

> **Documento Executável**
> **Data:** 2025-11-12
> **Status:** 📋 Pronto para execução
> **Prioridade:** 🔴 Alta

---

## 📊 Resumo Executivo

Este documento contém **ações concretas e scripts** para reorganizar a documentação Ávila, corrigir issues identificados e implementar a estrutura proposta.

**Tempo estimado total:** 15-20 dias
**Impacto:** 🔴 Alto - Melhoria significativa na navegabilidade e manutenção

---

## 🚀 Fase 1: Limpeza Crítica (1-2 dias)

### ✅ Ação 1.1: Mover Arquivos Binários

**Problema:** ~80 DLLs e executáveis na pasta de documentação
**Impacto:** Poluição do repositório, confusão de navegação

**Script PowerShell:**

```powershell
# Criar pasta bin se não existir
$binPath = "c:\Users\nicol\OneDrive\Avila\Docs\bin"
New-Item -ItemType Directory -Force -Path $binPath

# Listar todos os binários
$extensions = @("*.dll", "*.exe", "*.pri", "*.winmd", "*.pdb")
$files = Get-ChildItem -Path "c:\Users\nicol\OneDrive\Avila\Docs" -File |
         Where-Object { $extensions -contains "*$($_.Extension)" }

# Mover arquivos
foreach ($file in $files) {
    Move-Item -Path $file.FullName -Destination $binPath -Force
    Write-Host "Movido: $($file.Name)" -ForegroundColor Green
}

Write-Host "`nTotal de arquivos movidos: $($files.Count)" -ForegroundColor Cyan
```

**Resultado esperado:** ~80 arquivos movidos para `/bin`

---

### ✅ Ação 1.2: Remover Arquivos Duplicados

**Problema:** `ANALISE_PROJETO_AVILA_v2.0_2025-11-10 1.md` (duplicado)

**Script PowerShell:**

```powershell
$duplicate = "c:\Users\nicol\OneDrive\Avila\Docs\Analises\ANALISE_PROJETO_AVILA_v2.0_2025-11-10 1.md"

if (Test-Path $duplicate) {
    Remove-Item -Path $duplicate -Force
    Write-Host "Arquivo duplicado removido: $duplicate" -ForegroundColor Green
} else {
    Write-Host "Arquivo não encontrado (já removido?)" -ForegroundColor Yellow
}
```

---

### ✅ Ação 1.3: Corrigir Encoding do README em Analises

**Problema:** README.md com encoding UTF-8 corrompido (caracteres `??`)

**Script PowerShell:**

```powershell
$readmePath = "c:\Users\nicol\OneDrive\Avila\Docs\Analises\README.md"

# Backup
Copy-Item $readmePath "$readmePath.bak" -Force

# Ler com encoding correto e reescrever
$content = Get-Content -Path $readmePath -Encoding UTF8 -Raw
$content = $content -replace '\?\?', ''  # Remove caracteres corrompidos

# Salvar com UTF-8 BOM
$Utf8BomEncoding = New-Object System.Text.UTF8Encoding $true
[System.IO.File]::WriteAllText($readmePath, $content, $Utf8BomEncoding)

Write-Host "README.md corrigido. Backup salvo em: $readmePath.bak" -ForegroundColor Green
```

**Nota:** Pode ser necessário regenerar o README manualmente.

---

### ✅ Ação 1.4: Revisar Arquivos "Sem Título"

**Problema:** 3 arquivos sem contexto claro

**Script para análise:**

```powershell
$untitledFiles = @(
    "c:\Users\nicol\OneDrive\Avila\Docs\Sem título.md",
    "c:\Users\nicol\OneDrive\Avila\Docs\Sem título 1.md",
    "c:\Users\nicol\OneDrive\Avila\Docs\Sem título 2.md"
)

foreach ($file in $untitledFiles) {
    if (Test-Path $file) {
        Write-Host "`n=== $file ===" -ForegroundColor Cyan
        Get-Content -Path $file -TotalCount 20  # Primeiras 20 linhas
    }
}
```

**Ação manual:** Após revisar, renomear ou mover para `/Archive/Sem-Titulo/`

---

### ✅ Ação 1.5: Remover ou Mover Arquivos Fuzzer SPIRV

**Problema:** Arquivos C++ (fuzzer_pass_*.cpp/h) parecem deslocados em `/Instruções`

**Script PowerShell:**

```powershell
$instrPath = "c:\Users\nicol\OneDrive\Avila\Docs\Instruções"
$externosPath = "$instrPath\Externos-SPIRV"

# Criar pasta para arquivos externos
New-Item -ItemType Directory -Force -Path $externosPath

# Listar arquivos fuzzer
$fuzzerFiles = Get-ChildItem -Path $instrPath -Filter "fuzzer_*.cpp", "fuzzer_*.h", "*.hpp" -File

if ($fuzzerFiles.Count -gt 0) {
    foreach ($file in $fuzzerFiles) {
        Move-Item -Path $file.FullName -Destination $externosPath -Force
        Write-Host "Movido: $($file.Name)" -ForegroundColor Green
    }

    # Criar README explicativo
    $readmeContent = @"
# Arquivos Externos - SPIRV Fuzzer

Estes arquivos foram movidos automaticamente pois parecem ser de projeto externo.

**Origem:** Instruções/
**Data da movimentação:** $(Get-Date -Format "yyyy-MM-dd")

Se estes arquivos não fazem parte do projeto Ávila, podem ser removidos.
"@

    Set-Content -Path "$externosPath\README.md" -Value $readmeContent -Encoding UTF8
    Write-Host "`nTotal movido: $($fuzzerFiles.Count) arquivos" -ForegroundColor Cyan
} else {
    Write-Host "Nenhum arquivo fuzzer encontrado." -ForegroundColor Yellow
}
```

---

### ✅ Ação 1.6: Adicionar .gitignore para Logs

**Script PowerShell:**

```powershell
$gitignorePath = "c:\Users\nicol\OneDrive\Avila\Docs\Logs\.gitignore"

$gitignoreContent = @"
# Ignorar todos os logs
*.log
*.json
*.ndjson
*.tar.gz
*.chatreplay.json

# Manter apenas o README
!README.md

# Ignorar temporários
*.tmp
*.temp
"@

Set-Content -Path $gitignorePath -Value $gitignoreContent -Encoding UTF8
Write-Host ".gitignore criado em Logs/" -ForegroundColor Green
```

---

## 🏗️ Fase 2: Reestruturação (3-5 dias)

### ✅ Ação 2.1: Criar Estrutura de Pastas Proposta

**Script PowerShell (Estrutura Base):**

```powershell
$basePath = "c:\Users\nicol\OneDrive\Avila\Docs"

$newFolders = @(
    "00-Guias-Rapidos",
    "01-Arquitetura",
    "02-Agentes",
    "03-Produtos",
    "04-Projetos",
    "05-Modulos-Sistema",
    "05-Modulos-Sistema/Modulo-1-Coleta-Dados",
    "05-Modulos-Sistema/Modulo-2-Tratamento-Classificacao",
    "05-Modulos-Sistema/Modulo-3-Processamento",
    "05-Modulos-Sistema/Modulo-4-Orquestracao-Insights",
    "06-Scripts",
    "06-Scripts/tests",
    "06-Scripts/docs",
    "07-Instrucoes-Automacao",
    "07-Instrucoes-Automacao/PowerShell",
    "07-Instrucoes-Automacao/Python",
    "07-Instrucoes-Automacao/Configuracoes",
    "07-Instrucoes-Automacao/Guias",
    "08-Analises",
    "08-Analises/Historico",
    "09-Relatorios",
    "10-Templates",
    "11-Recursos",
    "11-Recursos/Referencias-Tecnicas",
    "11-Recursos/Tutoriais",
    "11-Recursos/Papers",
    "12-Consulting",
    "12-Consulting/Propostas",
    "12-Consulting/Projetos-Consultoria",
    "12-Consulting/Clientes",
    "13-Ferramentas",
    "13-Ferramentas/Ativas",
    "13-Ferramentas/Planejadas",
    "13-Ferramentas/Descontinuadas",
    "Archive",
    "config",
    "bin"
)

foreach ($folder in $newFolders) {
    $fullPath = Join-Path $basePath $folder
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Force -Path $fullPath | Out-Null
        Write-Host "Criado: $folder" -ForegroundColor Green
    } else {
        Write-Host "Já existe: $folder" -ForegroundColor Yellow
    }
}

Write-Host "`nEstrutura de pastas criada!" -ForegroundColor Cyan
```

---

### ✅ Ação 2.2: Criar READMEs em Pastas Principais

**Script PowerShell (Template de README):**

```powershell
function Create-FolderReadme {
    param(
        [string]$FolderPath,
        [string]$FolderName,
        [string]$Description
    )

    $readmePath = Join-Path $FolderPath "README.md"

    $content = @"
# 📁 $FolderName

> $Description

## 📋 Conteúdo

(Lista de arquivos será atualizada automaticamente)

## 🔗 Links Relacionados

- [🏠 Voltar ao Índice Principal](../README.md)
- [🗂️ Índice de Organização](../INDICE_ORGANIZACAO.md)

---

**Última atualização:** $(Get-Date -Format "yyyy-MM-dd")
**Responsável:** Ávila Ops
"@

    Set-Content -Path $readmePath -Value $content -Encoding UTF8
    Write-Host "README criado: $readmePath" -ForegroundColor Green
}

# Exemplos de uso
Create-FolderReadme -FolderPath "c:\Users\nicol\OneDrive\Avila\Docs\00-Guias-Rapidos" `
                    -FolderName "Guias Rápidos" `
                    -Description "Documentação de início rápido, tutoriais básicos e FAQs"

Create-FolderReadme -FolderPath "c:\Users\nicol\OneDrive\Avila\Docs\01-Arquitetura" `
                    -FolderName "Arquitetura" `
                    -Description "Documentação de arquitetura do sistema, diagramas e decisões técnicas"

# ... (repetir para outras pastas)
```

---

### ✅ Ação 2.3: Mover Arquivos para Nova Estrutura

**Script PowerShell (Movimentações Principais):**

```powershell
$basePath = "c:\Users\nicol\OneDrive\Avila\Docs"

# Função auxiliar
function Move-File-Safe {
    param([string]$Source, [string]$Destination)

    if (Test-Path $Source) {
        $destDir = Split-Path $Destination -Parent
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Force -Path $destDir | Out-Null
        }
        Move-Item -Path $Source -Destination $Destination -Force
        Write-Host "✓ $Source → $Destination" -ForegroundColor Green
    } else {
        Write-Host "✗ Não encontrado: $Source" -ForegroundColor Red
    }
}

# Arquitetura
Move-File-Safe "$basePath\SISTEMA DE ANÁLISE DE PRODUTIVIDADE EMPRESARIAL.md" `
               "$basePath\01-Arquitetura\SISTEMA-ANALISE-PRODUTIVIDADE.md"

Move-File-Safe "$basePath\Principais orquestradores.md" `
               "$basePath\01-Arquitetura\Principais-Orquestradores.md"

Move-File-Safe "$basePath\Parâmetros.md" `
               "$basePath\01-Arquitetura\Parametros.md"

# Guias
Move-File-Safe "$basePath\Modo de usar.md" `
               "$basePath\00-Guias-Rapidos\Modo-de-Usar.md"

# Agentes (já está em pasta, apenas renomear)
# (Manter em "Agentes/" por enquanto, pode ser movido depois)

# Produtos
# (Já está organizado em "Produtos/")

# Consulting
Move-File-Safe "$basePath\Avila Consulting\BrainStorm - Avila Consulting.md" `
               "$basePath\12-Consulting\BrainStorm.md"

# Ferramentas
Move-File-Safe "$basePath\Ferramentas - Futuras\Team Viewer.md" `
               "$basePath\13-Ferramentas\Planejadas\Team-Viewer.md"

# Recursos
Move-File-Safe "$basePath\Recursos\Kernel Semântico.md" `
               "$basePath\11-Recursos\Kernel-Semantico.md"

# Configs
Move-File-Safe "$basePath\workloads.json" "$basePath\config\workloads.json"
Move-File-Safe "$basePath\workloads.365.json" "$basePath\config\workloads.365.json"
Move-File-Safe "$basePath\workloads.lnl.json" "$basePath\config\workloads.lnl.json"
Move-File-Safe "$basePath\workloads.qnn.json" "$basePath\config\workloads.qnn.json"
Move-File-Safe "$basePath\workloads.stx.json" "$basePath\config\workloads.stx.json"

Write-Host "`nMovimentação concluída!" -ForegroundColor Cyan
```

---

### ✅ Ação 2.4: Reorganizar Instruções

**Script PowerShell:**

```powershell
$instrPath = "c:\Users\nicol\OneDrive\Avila\Docs\Instruções"
$newInstrPath = "c:\Users\nicol\OneDrive\Avila\Docs\07-Instrucoes-Automacao"

# PowerShell scripts
Get-ChildItem "$instrPath\*.ps1" | ForEach-Object {
    Move-Item $_.FullName "$newInstrPath\PowerShell\$($_.Name)" -Force
}

# Python scripts
Get-ChildItem "$instrPath\*.py" | ForEach-Object {
    Move-Item $_.FullName "$newInstrPath\Python\$($_.Name)" -Force
}

# JSON configs
Get-ChildItem "$instrPath\*.json" | ForEach-Object {
    Move-Item $_.FullName "$newInstrPath\Configuracoes\$($_.Name)" -Force
}

# Markdown guides
Get-ChildItem "$instrPath\*.md" | ForEach-Object {
    Move-Item $_.FullName "$newInstrPath\Guias\$($_.Name)" -Force
}

Write-Host "Instruções reorganizadas!" -ForegroundColor Green
```

---

## 📝 Fase 3: Documentação (5-7 dias)

### ✅ Ação 3.1: Criar Template para Agentes

**Arquivo:** `Templates/template-agente.md`

```markdown
---
title: "Agente <NOME>"
created: <DATA>
updated: <DATA>
version: 1.0
tags: [avila, agente, batuta]
type: agente
status: draft
---

# 🤖 Agente <NOME>

> **Tagline:** <Descrição curta>

## 📋 Resumo

**Função Principal:** <Função>
**Domínio:** <Domínio>
**Skills:** <Lista de skills>
**Status:** <Status>

## 🎯 Propósito

<Descrição detalhada do propósito do agente>

## 🔧 Capabilities (Skills)

### Skill 1: <Nome>
**Descrição:** <Desc>
**Input:** <Input schema>
**Output:** <Output schema>
**Exemplo:**
```json
{...}
```

### Skill 2: <Nome>
...

## 🔌 Integrações

- **Sistemas:** <Lista>
- **APIs:** <Lista>
- **Agentes Relacionados:** <Lista>

## 📊 Métricas

- **Latência média:** <Valor>
- **Taxa de sucesso:** <Valor>
- **Custo por execução:** <Valor>

## 🚀 Roadmap

- [ ] Feature 1
- [ ] Feature 2

## 🔗 Links

- [[Batuta]] - Orquestrador
- [[Dashboard-Principal]]

---

**Última atualização:** <DATA>
**Autor:** <Nome>
```

---

### ✅ Ação 3.2: Gerar Esqueletos para Agentes Pendentes

**Script PowerShell:**

```powershell
$templatePath = "c:\Users\nicol\OneDrive\Avila\Docs\Templates\template-agente.md"
$agentesPath = "c:\Users\nicol\OneDrive\Avila\Docs\Agentes"

$agentes = @(
    @{Nome="Atlas"; Desc="Cartografia e Navegação"; Dominio="Mapeamento"},
    @{Nome="Helix"; Desc="DevOps e Deploy"; Dominio="Infraestrutura"},
    @{Nome="Sigma"; Desc="Análise Financeira"; Dominio="Finance"},
    @{Nome="Vox"; Desc="CRM e Comunicação"; Dominio="Customer"},
    @{Nome="Lumen"; Desc="Knowledge Management"; Dominio="Search"},
    @{Nome="Forge"; Desc="Build e Produção"; Dominio="Engineering"},
    @{Nome="Lex"; Desc="Compliance e Legal"; Dominio="Governance"},
    @{Nome="Echo"; Desc="Feedback e Analytics"; Dominio="Analytics"}
)

foreach ($agente in $agentes) {
    $filepath = Join-Path $agentesPath "$($agente.Nome).md"

    if (-not (Test-Path $filepath)) {
        $content = @"
---
title: "Agente $($agente.Nome)"
created: $(Get-Date -Format "yyyy-MM-dd")
updated: $(Get-Date -Format "yyyy-MM-dd")
version: 1.0
tags: [avila, agente, batuta, $($agente.Nome.ToLower())]
type: agente
status: draft
---

# 🤖 Agente $($agente.Nome)

> **Tagline:** $($agente.Desc)

## 📋 Resumo

**Função Principal:** $($agente.Desc)
**Domínio:** $($agente.Dominio)
**Skills:** A definir
**Status:** 🟡 Em desenvolvimento

## 🎯 Propósito

<A ser documentado>

## 🔧 Capabilities (Skills)

<A ser documentado>

## 🔌 Integrações

<A ser documentado>

## 📊 Métricas

<A ser documentado>

## 🚀 Roadmap

- [ ] Definir skills principais
- [ ] Implementar protótipo
- [ ] Integrar com BATUTA
- [ ] Testes e validação
- [ ] Documentação completa

## 🔗 Links

- [[Batuta]] - Orquestrador
- [[Dashboard-Principal]]

---

**Última atualização:** $(Get-Date -Format "yyyy-MM-dd")
**Autor:** Ávila Ops
"@

        Set-Content -Path $filepath -Value $content -Encoding UTF8
        Write-Host "Criado: $($agente.Nome).md" -ForegroundColor Green
    } else {
        Write-Host "Já existe: $($agente.Nome).md" -ForegroundColor Yellow
    }
}
```

---

### ✅ Ação 3.3: Expandir "Modo de Usar"

**Ação manual:** Expandir com seções:
- Instalação e setup
- Primeiros passos
- Workflows comuns
- Troubleshooting
- FAQ

---

### ✅ Ação 3.4: Criar CHANGELOG.md

**Script PowerShell:**

```powershell
$changelogPath = "c:\Users\nicol\OneDrive\Avila\Docs\CHANGELOG.md"

$content = @"
# 📜 Changelog - Documentação Ávila

Todas as mudanças notáveis nesta documentação serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [2.0.0] - 2025-11-12

### Adicionado
- ✅ README.md principal com navegação completa
- ✅ INDICE_ORGANIZACAO.md com análise detalhada e mapeamento
- ✅ Este CHANGELOG.md
- ✅ Estrutura de pastas reorganizada (00-13)
- ✅ Templates para agentes
- ✅ Documentação esqueleto para 8 agentes pendentes
- ✅ READMEs em todas as pastas principais
- ✅ .gitignore em /Logs
- ✅ Pasta /bin para binários
- ✅ Pasta /config para configurações
- ✅ Pasta /Archive para arquivos obsoletos

### Modificado
- 🔄 Arquivos binários movidos de raiz para /bin
- 🔄 Configurações JSON movidas para /config
- 🔄 Instruções reorganizadas por tipo (PS, Python, etc.)
- 🔄 Encoding corrigido em Analises/README.md

### Removido
- ❌ Arquivos duplicados (ANALISE_PROJETO_AVILA_v2.0_2025-11-10 1.md)
- ❌ Arquivos fuzzer SPIRV movidos para /Externos

### Corrigido
- 🐛 Encoding UTF-8 em README de Analises
- 🐛 Issues de navegabilidade e descoberta de documentos

### Pendente
- 🔜 Documentar 8 agentes (Atlas, Helix, Sigma, Vox, Lumen, Forge, Lex, Echo)
- 🔜 Documentar 3 produtos (ArcSat, Arkana, LojaBlock)
- 🔜 Resolver ausência do Módulo 3
- 🔜 Expandir guias e tutoriais
- 🔜 Revisar e processar arquivos "Sem título"

## [1.0.0] - 2025-11-10

### Inicial
- Estrutura básica da documentação
- Dashboard Principal
- Documentação dos primeiros 3 agentes (Batuta, GA4, Pulse)
- Análise v2.0 do projeto
- Templates básicos

---

**Formato de versão:** [MAJOR.MINOR.PATCH]
- **MAJOR:** Mudanças incompatíveis na estrutura
- **MINOR:** Adição de funcionalidades compatíveis
- **PATCH:** Correções e pequenas melhorias
"@

Set-Content -Path $changelogPath -Value $content -Encoding UTF8
Write-Host "CHANGELOG.md criado!" -ForegroundColor Green
```

---

## 🤖 Fase 4: Automação (2-3 dias)

### ✅ Ação 4.1: Script de Validação de Estrutura

**Arquivo:** `scripts/validate-docs-structure.ps1`

```powershell
# Valida estrutura da documentação
param(
    [string]$BasePath = "c:\Users\nicol\OneDrive\Avila\Docs"
)

$errors = @()
$warnings = @()

# Verificar pastas obrigatórias
$requiredFolders = @(
    "Agentes",
    "Templates",
    "scripts",
    "Relatorios",
    "Analises"
)

foreach ($folder in $requiredFolders) {
    $path = Join-Path $BasePath $folder
    if (-not (Test-Path $path)) {
        $errors += "❌ Pasta obrigatória ausente: $folder"
    }
}

# Verificar READMEs
$foldersNeedingReadme = Get-ChildItem -Path $BasePath -Directory |
    Where-Object { $_.Name -notlike ".*" -and $_.Name -ne "bin" }

foreach ($folder in $foldersNeedingReadme) {
    $readmePath = Join-Path $folder.FullName "README.md"
    if (-not (Test-Path $readmePath)) {
        $warnings += "⚠️ README ausente em: $($folder.Name)"
    }
}

# Verificar arquivos binários na raiz
$binaries = Get-ChildItem -Path $BasePath -File |
    Where-Object { $_.Extension -in @(".dll", ".exe", ".pri", ".winmd") }

if ($binaries.Count -gt 0) {
    $errors += "❌ $($binaries.Count) arquivos binários encontrados na raiz (devem estar em /bin)"
}

# Verificar frontmatter em MDs principais
$mainMDs = @("README.md", "Dashboard-Principal.md", "INDICE_ORGANIZACAO.md")

foreach ($md in $mainMDs) {
    $path = Join-Path $BasePath $md
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        if ($content -notmatch "^---[\r\n]") {
            $warnings += "⚠️ Frontmatter ausente ou incorreto em: $md"
        }
    }
}

# Relatório
Write-Host "`n=== VALIDAÇÃO DA ESTRUTURA ===" -ForegroundColor Cyan
Write-Host "`nErros: $($errors.Count)" -ForegroundColor $(if($errors.Count -eq 0){"Green"}else{"Red"})
foreach ($err in $errors) { Write-Host $err -ForegroundColor Red }

Write-Host "`nAvisos: $($warnings.Count)" -ForegroundColor Yellow
foreach ($warn in $warnings) { Write-Host $warn -ForegroundColor Yellow }

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "`n✅ Estrutura validada com sucesso!" -ForegroundColor Green
    exit 0
} elseif ($errors.Count -eq 0) {
    Write-Host "`n⚠️ Validação concluída com avisos." -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "`n❌ Validação falhou. Corrija os erros acima." -ForegroundColor Red
    exit 1
}
```

---

### ✅ Ação 4.2: Script de Limpeza de Logs

**Arquivo:** `scripts/cleanup-logs.ps1`

```powershell
# Limpa logs antigos (mantém últimos 30 dias)
param(
    [int]$DaysToKeep = 30,
    [string]$LogsPath = "c:\Users\nicol\OneDrive\Avila\Docs\Logs"
)

$cutoffDate = (Get-Date).AddDays(-$DaysToKeep)
$files = Get-ChildItem -Path $LogsPath -File -Recurse |
    Where-Object { $_.LastWriteTime -lt $cutoffDate -and $_.Name -ne "README.md" }

Write-Host "Arquivos a remover (>$DaysToKeep dias): $($files.Count)" -ForegroundColor Yellow

foreach ($file in $files) {
    Remove-Item $file.FullName -Force
    Write-Host "Removido: $($file.Name) ($(Get-Date $file.LastWriteTime -Format 'yyyy-MM-dd'))" -ForegroundColor Gray
}

Write-Host "`n✅ Limpeza concluída. $($files.Count) arquivos removidos." -ForegroundColor Green
```

---

### ✅ Ação 4.3: Script de Geração de Índices

**Arquivo:** `scripts/generate-indexes.ps1`

```powershell
# Gera índices automáticos para pastas
param(
    [string]$BasePath = "c:\Users\nicol\OneDrive\Avila\Docs"
)

function Generate-Index {
    param([string]$FolderPath)

    $folderName = Split-Path $FolderPath -Leaf
    $files = Get-ChildItem -Path $FolderPath -File | Where-Object { $_.Name -ne "README.md" }
    $subfolders = Get-ChildItem -Path $FolderPath -Directory

    $index = @"
# 📁 Índice: $folderName

> Gerado automaticamente em $(Get-Date -Format "yyyy-MM-dd HH:mm")

## 📄 Arquivos ($($files.Count))

"@

    foreach ($file in $files | Sort-Object Name) {
        $size = if ($file.Length -lt 1KB) { "$($file.Length) B" }
                elseif ($file.Length -lt 1MB) { "$([math]::Round($file.Length/1KB, 2)) KB" }
                else { "$([math]::Round($file.Length/1MB, 2)) MB" }

        $index += "- [$($file.BaseName)]($($file.Name)) - $size`n"
    }

    if ($subfolders.Count -gt 0) {
        $index += "`n## 📁 Subpastas ($($subfolders.Count))`n`n"
        foreach ($sub in $subfolders | Sort-Object Name) {
            $index += "- [$($sub.Name)]($($sub.Name)/)`n"
        }
    }

    $indexPath = Join-Path $FolderPath "INDEX.md"
    Set-Content -Path $indexPath -Value $index -Encoding UTF8
    Write-Host "Índice criado: $folderName" -ForegroundColor Green
}

# Gerar índices para pastas principais
$folders = Get-ChildItem -Path $BasePath -Directory |
    Where-Object { $_.Name -notlike ".*" -and $_.Name -ne "bin" }

foreach ($folder in $folders) {
    Generate-Index -FolderPath $folder.FullName
}

Write-Host "`n✅ $($folders.Count) índices gerados!" -ForegroundColor Cyan
```

---

## 📅 Fase 5: Governança (Contínuo)

### ✅ Ação 5.1: Implementar Rotina de Revisão Semanal

**Criar:** `scripts/weekly-review.ps1`

```powershell
# Review semanal da documentação
$basePath = "c:\Users\nicol\OneDrive\Avila\Docs"
$logsPath = Join-Path $basePath "Logs"

Write-Host "=== REVIEW SEMANAL - $(Get-Date -Format 'yyyy-MM-dd') ===" -ForegroundColor Cyan

# 1. Limpar logs antigos
Write-Host "`n1. Limpando logs..." -ForegroundColor Yellow
& "$basePath\scripts\cleanup-logs.ps1"

# 2. Validar estrutura
Write-Host "`n2. Validando estrutura..." -ForegroundColor Yellow
& "$basePath\scripts\validate-docs-structure.ps1"

# 3. Verificar arquivos não versionados
Write-Host "`n3. Verificando Git..." -ForegroundColor Yellow
Set-Location $basePath
$untracked = git ls-files --others --exclude-standard
if ($untracked) {
    Write-Host "⚠️ Arquivos não versionados: $($untracked.Count)" -ForegroundColor Yellow
    $untracked | ForEach-Object { Write-Host "  - $_" -ForegroundColor Gray }
}

# 4. Estatísticas
Write-Host "`n4. Estatísticas:" -ForegroundColor Yellow
$mdFiles = (Get-ChildItem -Path $basePath -Filter "*.md" -Recurse).Count
$totalSize = (Get-ChildItem -Path $basePath -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "  - Arquivos MD: $mdFiles" -ForegroundColor Cyan
Write-Host "  - Tamanho total: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Cyan

Write-Host "`n✅ Review semanal concluído!" -ForegroundColor Green
```

**Agendar no Windows Task Scheduler:**

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File c:\Users\nicol\OneDrive\Avila\Docs\scripts\weekly-review.ps1"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9am

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "Avila Docs - Weekly Review" `
    -Description "Revisão semanal da documentação Ávila"
```

---

## 📊 Checklist de Execução

### Fase 1: Limpeza (Prioridade Alta)
- [ ] 1.1 - Mover arquivos binários para /bin
- [ ] 1.2 - Remover arquivo duplicado
- [ ] 1.3 - Corrigir encoding do README
- [ ] 1.4 - Revisar arquivos "Sem título"
- [ ] 1.5 - Mover arquivos fuzzer SPIRV
- [ ] 1.6 - Adicionar .gitignore em Logs

### Fase 2: Reestruturação
- [ ] 2.1 - Criar estrutura de pastas
- [ ] 2.2 - Criar READMEs em pastas principais
- [ ] 2.3 - Mover arquivos para nova estrutura
- [ ] 2.4 - Reorganizar /Instruções

### Fase 3: Documentação
- [ ] 3.1 - Criar template de agentes
- [ ] 3.2 - Gerar esqueletos para 8 agentes
- [ ] 3.3 - Expandir "Modo de Usar"
- [ ] 3.4 - Criar CHANGELOG.md

### Fase 4: Automação
- [ ] 4.1 - Script de validação de estrutura
- [ ] 4.2 - Script de limpeza de logs
- [ ] 4.3 - Script de geração de índices

### Fase 5: Governança
- [ ] 5.1 - Implementar review semanal
- [ ] 5.2 - Agendar tarefas automáticas
- [ ] 5.3 - Documentar processo de contribuição

---

## 🎯 Próximos Passos Imediatos

1. **Executar Fase 1 completa** (todas as ações de limpeza)
2. **Validar resultados** manualmente
3. **Commit e push** das mudanças
4. **Executar Fase 2** (reestruturação)
5. **Atualizar links** em documentos existentes

---

## 📞 Suporte

**Dúvidas sobre este plano?**
- Revisar [INDICE_ORGANIZACAO.md](INDICE_ORGANIZACAO.md)
- Consultar [Dashboard-Principal.md](Dashboard-Principal.md)

---

**Última atualização:** 2025-11-12
**Status:** 📋 Pronto para execução
**Responsável:** Ávila Ops
