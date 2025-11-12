# Git Setup para Projeto Avila - Versao Simples
# Autor: Nicolas Avila

Write-Host "🚀 CONFIGURADOR GIT - PROJETO AVILA" -ForegroundColor Magenta
Write-Host "====================================" -ForegroundColor Magenta

$AvilaPath = "C:\Users\nicol\OneDrive\Avila"
Set-Location $AvilaPath

Write-Host "`n🔍 VERIFICANDO SITUACAO ATUAL..." -ForegroundColor Cyan

# Verificar se existe .git
if (Test-Path ".git") {
    Write-Host "✅ Repositorio Git encontrado" -ForegroundColor Green

    # Verificar remote
    try {
        $remote = git remote get-url origin 2>$null
        if ($remote) {
            Write-Host "🌐 Remote atual: $remote" -ForegroundColor Yellow
            if ($remote -like "*geolocation*") {
                Write-Host "⚠️  PROBLEMA: Conectado ao 'geolocation'" -ForegroundColor Red

                $disconnect = Read-Host "`n❓ Desconectar do geolocation? (s/n)"
                if ($disconnect -eq 's' -or $disconnect -eq 'S') {
                    Write-Host "🔌 Desconectando..." -ForegroundColor Yellow
                    git remote remove origin
                    Write-Host "✅ Desconectado!" -ForegroundColor Green
                }
            }
        } else {
            Write-Host "⚠️  Sem remote configurado" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Sem remote configurado" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Nenhum repositorio Git encontrado" -ForegroundColor Red

    $init = Read-Host "`n❓ Inicializar repositorio Git? (s/n)"
    if ($init -eq 's' -or $init -eq 'S') {
        Write-Host "🔧 Inicializando Git..." -ForegroundColor Cyan
        git init
        Write-Host "✅ Git inicializado!" -ForegroundColor Green
    }
}

Write-Host "`n📋 OPCOES:" -ForegroundColor Cyan
Write-Host "1 - Criar repositorio Avila completo"
Write-Host "2 - Apenas configurar remote"
Write-Host "3 - Ver dicas de multiplos repos"
Write-Host "4 - Sair"

$choice = Read-Host "`n❓ Escolha (1-4)"

switch ($choice) {
    '1' {
        Write-Host "`n🚀 CRIANDO REPOSITORIO AVILA..." -ForegroundColor Magenta

        # Configurar usuario
        git config user.name "Nicolas Avila"
        git config user.email "nicolas@avilaops.com"

        # Add e commit
        Write-Host "📁 Adicionando arquivos..." -ForegroundColor Cyan
        git add .

        Write-Host "💾 Fazendo commit..." -ForegroundColor Cyan
        git commit -m "🎯 Inicial: Setup Avila Framework

✨ Estrutura completa AvilaInc + AvilaOps
🔧 Templates Obsidian configurados
📊 Scripts de automacao
📚 Documentacao completa
🔄 Sync VS Code - Obsidian - GitHub

👤 Autor: Nicolas Avila
📅 Data: $(Get-Date -Format 'dd/MM/yyyy')"

        Write-Host "✅ Commit criado!" -ForegroundColor Green

        # Instrucoes GitHub
        Write-Host "`n🌐 AGORA NO GITHUB:" -ForegroundColor Blue
        Write-Host "1. Acesse: https://github.com/avilaops"
        Write-Host "2. Clique 'New Repository'"
        Write-Host "3. Nome: 'avila-framework'"
        Write-Host "4. Publico ou Privado"
        Write-Host "5. NAO inicialize com README"
        Write-Host "6. Clique 'Create repository'"

        $github = Read-Host "`n❓ Ja criou no GitHub? (s/n)"
        if ($github -eq 's' -or $github -eq 'S') {
            $repoUrl = "https://github.com/avilaops/avila-framework.git"
            Write-Host "🔗 Conectando ao GitHub..." -ForegroundColor Cyan

            git remote add origin $repoUrl
            git branch -M main
            git push -u origin main

            Write-Host "🎉 SUCESSO! Repositorio criado!" -ForegroundColor Green
        } else {
            Write-Host "`n📋 EXECUTE DEPOIS:" -ForegroundColor Yellow
            Write-Host "git remote add origin https://github.com/avilaops/avila-framework.git"
            Write-Host "git branch -M main"
            Write-Host "git push -u origin main"
        }
    }

    '2' {
        $url = Read-Host "`n🔗 URL do repositorio GitHub"
        git remote add origin $url
        git branch -M main
        Write-Host "✅ Remote configurado!" -ForegroundColor Green
    }

    '3' {
        Write-Host "`n🛡️ DICAS MULTIPLOS REPOSITORIOS:" -ForegroundColor Green
        Write-Host "=================================="
        Write-Host "1. NUNCA faca 'git add .' na pasta OneDrive" -ForegroundColor Red
        Write-Host "2. Sempre entre na pasta especifica do projeto"
        Write-Host "3. Use: cd C:\Users\nicol\OneDrive\Avila"
        Write-Host "4. Depois: git add . / git commit / git push"
        Write-Host "5. Cada projeto = uma pasta = um .git"
    }

    '4' {
        Write-Host "`n👋 Ate logo!" -ForegroundColor Cyan
    }
}

Write-Host "`n✅ Concluido!" -ForegroundColor Green
