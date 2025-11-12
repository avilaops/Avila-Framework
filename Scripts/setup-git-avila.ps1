# Script de Configuração Git para Projeto Ávila
# Autor: Nícolas Ávila | Framework: Ávila Inc.

param(
    [switch]$CreateNew,
    [switch]$Status,
    [switch]$Setup
)

$AvilaPath = "C:\Users\nicol\OneDrive\Avila"
$GitHubUser = "avilaops"  # Seu usuário do GitHub

function Write-ColorLog {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-CurrentStatus {
    Write-ColorLog "`n🔍 DIAGNÓSTICO ATUAL" "Cyan"
    Write-ColorLog "===================" "Cyan"

    Set-Location $AvilaPath

    # Verificar se existe .git local
    if (Test-Path ".git") {
        Write-ColorLog "✅ Repositório Git local encontrado" "Green"

        # Verificar remote
        try {
            $remote = git remote get-url origin 2>$null
            Write-ColorLog "🌐 Remote atual: $remote" "Yellow"

            # Verificar se é o geolocation
            if ($remote -like "*geolocation*") {
                Write-ColorLog "⚠️  PROBLEMA: Conectado ao repositório 'geolocation'" "Red"
                Write-ColorLog "   Precisamos desconectar e criar repositório próprio" "Red"
            }
        } catch {
            Write-ColorLog "⚠️  Sem remote configurado" "Yellow"
        }

        # Status local
        $status = git status --porcelain
        if ($status) {
            Write-ColorLog "📝 Arquivos modificados: $($status.Count)" "Yellow"
        } else {
            Write-ColorLog "✅ Área de trabalho limpa" "Green"
        }
    } else {
        Write-ColorLog "❌ Nenhum repositório Git encontrado" "Red"
    }

    # Verificar estrutura
    Write-ColorLog "`n📁 ESTRUTURA DO PROJETO" "Cyan"
    $folders = Get-ChildItem -Directory | Select-Object -ExpandProperty Name
    foreach ($folder in $folders) {
        if (Test-Path "$folder\.git") {
            Write-ColorLog "   📂 $folder (tem .git próprio) ⚠️" "Yellow"
        } else {
            Write-ColorLog "   📂 $folder" "White"
        }
    }

    # Verificar arquivos importantes
    $importantFiles = @(".gitignore", "README.md", ".gitattributes")
    foreach ($file in $importantFiles) {
        if (Test-Path $file) {
            Write-ColorLog "   ✅ $file" "Green"
        } else {
            Write-ColorLog "   ❌ $file (faltando)" "Red"
        }
    }
}

function Disconnect-FromGeolocation {
    Write-ColorLog "`n🔌 DESCONECTANDO DO GEOLOCATION" "Yellow"
    Write-ColorLog "===============================" "Yellow"

    Set-Location $AvilaPath

    # Backup das configurações atuais
    if (Test-Path ".git") {
        Write-ColorLog "📦 Fazendo backup das configurações Git..." "Cyan"
        Copy-Item ".git" ".git-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')" -Recurse -Force

        # Remover remote geolocation
        try {
            git remote remove origin
            Write-ColorLog "✅ Remote 'origin' removido" "Green"
        } catch {
            Write-ColorLog "ℹ️  Nenhum remote para remover" "Gray"
        }
    }
}

function Create-NewAvilaRepo {
    Write-ColorLog "`n🚀 CRIANDO REPOSITÓRIO ÁVILA" "Magenta"
    Write-ColorLog "=============================" "Magenta"

    Set-Location $AvilaPath

    # Inicializar Git se necessário
    if (-not (Test-Path ".git")) {
        Write-ColorLog "🔧 Inicializando repositório Git..." "Cyan"
        git init
        Write-ColorLog "✅ Repositório Git inicializado" "Green"
    }

    # Configurar usuário local
    Write-ColorLog "👤 Configurando usuário Git..." "Cyan"
    git config user.name "Nícolas Ávila"
    git config user.email "nicolas@avilaops.com"  # Ajuste conforme necessário

    # Adicionar todos os arquivos
    Write-ColorLog "📁 Adicionando arquivos ao Git..." "Cyan"
    git add .

    # Commit inicial
    Write-ColorLog "💾 Fazendo commit inicial..." "Cyan"
    git commit -m "🎯 Inicial: Setup Ávila Framework

✨ Features:
- Estrutura completa AvilaInc + AvilaOps
- Templates Obsidian configurados
- Scripts de automação
- Documentação completa
- Sync VS Code ↔ Obsidian ↔ GitHub

🔧 Configurações:
- Dataview, Templater, Tasks, Advanced Tables
- Auto-sync Git configurado
- Dashboard principal ativo
- Templates automáticos por pasta

📊 Projeto: Ávila Framework
👤 Autor: Nícolas Ávila
📅 Data: $(Get-Date -Format 'dd/MM/yyyy')
"

    Write-ColorLog "✅ Commit inicial criado" "Green"
}

function Setup-GitHubRepo {
    Write-ColorLog "`n🌐 CONFIGURANDO REPOSITÓRIO GITHUB" "Blue"
    Write-ColorLog "==================================" "Blue"

    # Instruções para criar repo no GitHub
    Write-ColorLog "`n📋 INSTRUÇÕES PARA GITHUB:" "Yellow"
    Write-ColorLog "1. Acesse https://github.com/$GitHubUser" "White"
    Write-ColorLog "2. Clique em 'New Repository'" "White"
    Write-ColorLog "3. Nome: 'avila-framework'" "White"
    Write-ColorLog "4. Descrição: 'Ávila Framework - Ecossistema corporativo integrado'" "White"
    Write-ColorLog "5. Deixe PÚBLICO ou PRIVADO (sua escolha)" "White"
    Write-ColorLog "6. NÃO inicialize com README (já temos)" "Red"
    Write-ColorLog "7. Clique 'Create repository'" "White"

    # URL que será criada
    $repoUrl = "https://github.com/$GitHubUser/avila-framework.git"
    Write-ColorLog "`n🔗 URL do repositório: $repoUrl" "Cyan"

    # Comando para adicionar remote
    Write-ColorLog "`n⚙️ COMANDO PARA EXECUTAR APÓS CRIAR O REPO:" "Green"
    Write-ColorLog "git remote add origin $repoUrl" "White"
    Write-ColorLog "git branch -M main" "White"
    Write-ColorLog "git push -u origin main" "White"

    # Oferecer execução automática
    $choice = Read-Host "`n❓ Já criou o repositório no GitHub? (s/n)"
    if ($choice -eq 's' -or $choice -eq 'S') {
        Set-Location $AvilaPath

        Write-ColorLog "`n🔗 Adicionando remote..." "Cyan"
        git remote add origin $repoUrl

        Write-ColorLog "🌿 Configurando branch main..." "Cyan"
        git branch -M main

        Write-ColorLog "📤 Fazendo push inicial..." "Cyan"
        try {
            git push -u origin main
            Write-ColorLog "✅ Push realizado com sucesso!" "Green"
            Write-ColorLog "🎉 Repositório Ávila configurado!" "Green"
        } catch {
            Write-ColorLog "❌ Erro no push: $_" "Red"
            Write-ColorLog "💡 Verifique se o repositório foi criado corretamente no GitHub" "Yellow"
        }
    }
}

function Protect-OtherRepos {
    Write-ColorLog "`n🛡️ PROTEGENDO OUTROS REPOSITÓRIOS" "Green"
    Write-ColorLog "==================================" "Green"

    # Criar .gitignore na pasta pai se necessário
    $parentPath = Split-Path $AvilaPath -Parent
    $gitignorePath = Join-Path $parentPath ".gitignore"

    # Lista de pastas para ignorar (outros repositórios)
    $otherRepos = @(
        "avilaops-saas",
        "avilaops-geolocation",
        "avilaops-caseinports",
        "avilaops-knowledge",
        "avilaInc-literate-rotary-phone-demo-repository",
        "avilaInc-demo-repository",
        "avilaops-avily",
        "avilaops-avimind-k4os",
        "avilaops-mrg",
        "avilaops-fiscal",
        "microsoft-ai-foundry-for-vscode",
        "microsoft-vscode-apimanagement",
        "avilaops-Controle-Roncatin",
        "avilaops-dots-hyperland",
        "avilaops-Oh",
        "avilaops-fa",
        "avilaops-roncav-budget",
        "avilaops-Garantia_Site",
        "avilaops-garantia",
        "avilaops-Avila_Transportes",
        "avilaops-avila-transportes",
        "avilaops-engenharia",
        "avilaops-Saas"
    )

    Write-ColorLog "📝 Criando proteção para outros repositórios..." "Cyan"

    $gitignoreContent = @"
# Ávila Framework - Proteção de outros repositórios
# Gerado automaticamente em $(Get-Date -Format 'dd/MM/yyyy HH:mm')

# Outros repositórios AvilaOps (não incluir no commit)
"@

    foreach ($repo in $otherRepos) {
        $gitignoreContent += "`n$repo/"
    }

    $gitignoreContent | Out-File $gitignorePath -Encoding UTF8
    Write-ColorLog "✅ Proteção criada em: $gitignorePath" "Green"

    Write-ColorLog "`n💡 RECOMENDAÇÃO:" "Yellow"
    Write-ColorLog "Cada repositório deve ficar em sua própria pasta" "White"
    Write-ColorLog "Evite fazer git add na pasta pai (OneDrive)" "White"
    Write-ColorLog "Sempre trabalhe dentro da pasta específica de cada projeto" "White"
}

function Interactive-Setup {
    Clear-Host
    Write-ColorLog @"
🚀 CONFIGURADOR GIT - PROJETO ÁVILA
=====================================
Autor: Nícolas Ávila | Framework: Ávila Inc.
Data: $(Get-Date -Format "dd/MM/yyyy HH:mm")

"@ "Magenta"

    Show-CurrentStatus

    Write-ColorLog "`n🎯 AÇÕES DISPONÍVEIS:" "Cyan"
    Write-ColorLog "1 - Desconectar do Geolocation" "White"
    Write-ColorLog "2 - Criar novo repositório Ávila" "White"
    Write-ColorLog "3 - Configurar GitHub" "White"
    Write-ColorLog "4 - Proteger outros repositórios" "White"
    Write-ColorLog "5 - Executar configuração completa" "Yellow"
    Write-ColorLog "6 - Apenas status" "Gray"
    Write-ColorLog "Q - Sair" "Red"

    do {
        $choice = Read-Host "`n❓ Escolha uma opção (1-6, Q)"

        switch ($choice.ToUpper()) {
            '1' { Disconnect-FromGeolocation }
            '2' { Create-NewAvilaRepo }
            '3' { Setup-GitHubRepo }
            '4' { Protect-OtherRepos }
            '5' {
                Write-ColorLog "`n🚀 EXECUTANDO CONFIGURAÇÃO COMPLETA..." "Magenta"
                Disconnect-FromGeolocation
                Create-NewAvilaRepo
                Setup-GitHubRepo
                Protect-OtherRepos
                Write-ColorLog "`n🎉 CONFIGURAÇÃO COMPLETA!" "Green"
            }
            '6' { Show-CurrentStatus }
            'Q' {
                Write-ColorLog "`n👋 Até logo!" "Cyan"
                break
            }
            default {
                Write-ColorLog "`n❌ Opção inválida!" "Red"
            }
        }

        if ($choice -ne 'Q' -and $choice -ne '6') {
            Read-Host "`n⏸️  Pressione Enter para continuar"
        }

    } while ($choice.ToUpper() -ne 'Q')
}

# EXECUÇÃO PRINCIPAL
if ($Status) {
    Show-CurrentStatus
    exit
}

if ($CreateNew) {
    Disconnect-FromGeolocation
    Create-NewAvilaRepo
    Setup-GitHubRepo
    exit
}

if ($Setup) {
    Protect-OtherRepos
    exit
}

# Menu interativo por padrão
Interactive-Setup
