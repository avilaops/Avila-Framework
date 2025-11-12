# Script de Configuração Git para Projeto Ávila
# Autor: Nícolas Ávila | Framework: Ávila Inc.

param(
    [switch]$Status,
    [switch]$CreateNew,
    [switch]$Setup
)

$AvilaPath = "C:\Users\nicol\OneDrive\Avila"
$GitHubUser = "avilaops"

function Write-ColorLog {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-CurrentStatus {
    Write-ColorLog "" "White"
    Write-ColorLog "🔍 DIAGNÓSTICO ATUAL" "Cyan"
    Write-ColorLog "===================" "Cyan"

    Set-Location $AvilaPath

    # Verificar se existe .git local
    if (Test-Path ".git") {
        Write-ColorLog "✅ Repositório Git local encontrado" "Green"

        # Verificar remote
        try {
            $remote = git remote get-url origin 2>$null
            if ($remote) {
                Write-ColorLog "🌐 Remote atual: $remote" "Yellow"

                # Verificar se é o geolocation
                if ($remote -like "*geolocation*") {
                    Write-ColorLog "⚠️  PROBLEMA: Conectado ao repositório 'geolocation'" "Red"
                    Write-ColorLog "   Precisamos desconectar e criar repositório próprio" "Red"
                } else {
                    Write-ColorLog "✅ Remote configurado corretamente" "Green"
                }
            } else {
                Write-ColorLog "⚠️  Sem remote configurado" "Yellow"
            }
        } catch {
            Write-ColorLog "⚠️  Sem remote configurado" "Yellow"
        }

        # Status local
        $status = git status --porcelain 2>$null
        if ($status) {
            Write-ColorLog "📝 Arquivos modificados: $($status.Count)" "Yellow"
        } else {
            Write-ColorLog "✅ Área de trabalho limpa" "Green"
        }
    } else {
        Write-ColorLog "❌ Nenhum repositório Git encontrado" "Red"
        Write-ColorLog "   Precisamos inicializar um repositório Git" "Yellow"
    }

    Write-ColorLog "" "White"
    Write-ColorLog "📁 ESTRUTURA DO PROJETO" "Cyan"
    $folders = @("AvilaInc", "AvilaOps", "Docs", "Scripts", "Setup", "Shared", "Logs")
    foreach ($folder in $folders) {
        if (Test-Path $folder) {
            Write-ColorLog "   ✅ $folder" "Green"
        } else {
            Write-ColorLog "   ❌ $folder (faltando)" "Red"
        }
    }
}

function Create-AvilaRepository {
    Write-ColorLog "" "White"
    Write-ColorLog "🚀 CRIANDO REPOSITÓRIO ÁVILA" "Magenta"
    Write-ColorLog "=============================" "Magenta"

    Set-Location $AvilaPath

    # Verificar se já existe .git e é do geolocation
    if (Test-Path ".git") {
        try {
            $remote = git remote get-url origin 2>$null
            if ($remote -and $remote -like "*geolocation*") {
                Write-ColorLog "🔌 Desconectando do repositório geolocation..." "Yellow"
                git remote remove origin
                Write-ColorLog "✅ Desconectado do geolocation" "Green"
            }
        } catch {
            Write-ColorLog "ℹ️  Nenhum remote para remover" "Gray"
        }
    } else {
        Write-ColorLog "🔧 Inicializando repositório Git..." "Cyan"
        git init
        Write-ColorLog "✅ Repositório Git inicializado" "Green"
    }

    # Configurar usuário
    Write-ColorLog "👤 Configurando usuário Git..." "Cyan"
    git config user.name "Nicolas Avila"
    git config user.email "nicolas@avilaops.com"

    # Adicionar arquivos
    Write-ColorLog "📁 Adicionando arquivos..." "Cyan"
    git add .

    # Commit inicial
    Write-ColorLog "💾 Fazendo commit inicial..." "Cyan"
    $commitMessage = @"
🎯 Inicial: Setup Ávila Framework

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
"@

    git commit -m $commitMessage
    Write-ColorLog "✅ Commit inicial criado" "Green"

    # Instruções para GitHub
    Write-ColorLog "" "White"
    Write-ColorLog "🌐 PRÓXIMO PASSO: CRIAR REPOSITÓRIO NO GITHUB" "Blue"
    Write-ColorLog "=============================================" "Blue"
    Write-ColorLog "1. Acesse: https://github.com/$GitHubUser" "White"
    Write-ColorLog "2. Clique 'New Repository'" "White"
    Write-ColorLog "3. Nome: 'avila-framework'" "White"
    Write-ColorLog "4. Descrição: 'Ávila Framework - Ecossistema corporativo'" "White"
    Write-ColorLog "5. PÚBLICO ou PRIVADO (sua escolha)" "White"
    Write-ColorLog "6. NÃO inicialize com README" "Red"
    Write-ColorLog "7. Clique 'Create repository'" "White"

    $repoUrl = "https://github.com/$GitHubUser/avila-framework.git"
    Write-ColorLog "" "White"
    Write-ColorLog "🔗 Depois execute estes comandos:" "Green"
    Write-ColorLog "git remote add origin $repoUrl" "White"
    Write-ColorLog "git branch -M main" "White"
    Write-ColorLog "git push -u origin main" "White"

    # Pergunta se quer executar agora
    Write-ColorLog "" "White"
    $choice = Read-Host "❓ Já criou o repositório no GitHub? (s/n)"
    if ($choice -eq 's' -or $choice -eq 'S') {
        Write-ColorLog "🔗 Configurando remote..." "Cyan"
        git remote add origin $repoUrl
        git branch -M main

        Write-ColorLog "📤 Fazendo push..." "Cyan"
        try {
            git push -u origin main
            Write-ColorLog "🎉 SUCESSO! Repositório Ávila criado e sincronizado!" "Green"
        } catch {
            Write-ColorLog "❌ Erro no push. Verifique se o repositório foi criado no GitHub" "Red"
        }
    }
}

function Show-MultiRepoAdvice {
    Write-ColorLog "" "White"
    Write-ColorLog "🛡️ GERENCIANDO MÚLTIPLOS REPOSITÓRIOS" "Green"
    Write-ColorLog "=====================================" "Green"
    Write-ColorLog "" "White"
    Write-ColorLog "📋 REGRAS IMPORTANTES:" "Yellow"
    Write-ColorLog "1. NUNCA faça 'git add .' na pasta OneDrive" "Red"
    Write-ColorLog "2. Sempre navegue para a pasta específica do projeto" "White"
    Write-ColorLog "3. Cada repositório deve ter seu próprio .git" "White"
    Write-ColorLog "4. Use 'cd' para entrar na pasta antes de git commands" "White"
    Write-ColorLog "" "White"
    Write-ColorLog "📁 ESTRUTURA RECOMENDADA:" "Cyan"
    Write-ColorLog "C:\Users\nicol\OneDrive\" "Gray"
    Write-ColorLog "├── Avila\ (este projeto)" "Green"
    Write-ColorLog "│   ├── .git\" "Green"
    Write-ColorLog "│   ├── AvilaInc\" "Green"
    Write-ColorLog "│   └── AvilaOps\" "Green"
    Write-ColorLog "├── outros-projetos\" "Gray"
    Write-ColorLog "│   └── .git\" "Gray"
    Write-ColorLog "└── mais-projetos\" "Gray"
    Write-ColorLog "    └── .git\" "Gray"
    Write-ColorLog "" "White"
    Write-ColorLog "✅ COMANDOS SEGUROS:" "Green"
    Write-ColorLog "cd C:\Users\nicol\OneDrive\Avila" "White"
    Write-ColorLog "git status" "White"
    Write-ColorLog "git add ." "White"
    Write-ColorLog "git commit -m 'mensagem'" "White"
    Write-ColorLog "git push" "White"
}

# MENU PRINCIPAL
Clear-Host
Write-Host @"
🚀 CONFIGURADOR GIT - PROJETO ÁVILA
=====================================
Autor: Nícolas Ávila
Data: $(Get-Date -Format "dd/MM/yyyy HH:mm")
"@ -ForegroundColor Magenta

if ($Status) {
    Show-CurrentStatus
    exit
}

if ($CreateNew) {
    Create-AvilaRepository
    exit
}

if ($Setup) {
    Show-MultiRepoAdvice
    exit
}

# Menu interativo
do {
    Show-CurrentStatus
    Write-ColorLog "" "White"
    Write-ColorLog "🎯 AÇÕES DISPONÍVEIS:" "Cyan"
    Write-ColorLog "1 - Criar repositório Ávila" "White"
    Write-ColorLog "2 - Ver dicas multi-repositórios" "White"
    Write-ColorLog "3 - Apenas mostrar status" "Gray"
    Write-ColorLog "Q - Sair" "Red"

    $choice = Read-Host "`n❓ Escolha uma opção (1-3, Q)"

    switch ($choice.ToUpper()) {
        '1' {
            Create-AvilaRepository
            Read-Host "`n⏸️  Pressione Enter para continuar"
        }
        '2' {
            Show-MultiRepoAdvice
            Read-Host "`n⏸️  Pressione Enter para continuar"
        }
        '3' {
            # Status já foi mostrado no início do loop
        }
        'Q' {
            Write-ColorLog "`n👋 Até logo!" "Cyan"
            break
        }
        default {
            Write-ColorLog "`n❌ Opção inválida!" "Red"
        }
    }

} while ($choice.ToUpper() -ne 'Q')

Write-ColorLog "`n✅ Script finalizado!" "Green"
