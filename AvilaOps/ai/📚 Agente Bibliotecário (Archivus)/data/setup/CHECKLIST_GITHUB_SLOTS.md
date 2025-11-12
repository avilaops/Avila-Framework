# CHECKLIST COMPLETO - SLOTS GITHUB PRO/ENTERPRISE

**Data:** 2025-11-10  
**Versao:** 1.0  
**Responsavel:** Nicolas Avila

---

## INSTRUCOES

Este documento lista **TODOS os slots** que precisam ser preenchidos para configuracao completa do GitHub Pro/Enterprise.

**Como usar:**
1. Va marcando `[x]` conforme preencher
2. Anote valores ao lado de `<!-- PREENCHER -->`
3. Execute comandos PowerShell quando indicado
4. Salve este arquivo apos cada atualizacao

---

## PARTE 1: CONFIGURACAO LOCAL GIT

### 1.1 Identidade Git

```powershell
# PREENCHER:
git config --global user.name "SEU_NOME_COMPLETO"
git config --global user.email "SEU_EMAIL@example.com"
```

- [ ] Nome configurado
- [ ] Email configurado
- [ ] Verificado: `git config user.name`
- [ ] Verificado: `git config user.email`

**Valores atuais:**
- Nome: <!-- PREENCHER -->
- Email: <!-- PREENCHER -->

---

### 1.2 Configuracao Editor

```powershell
# PREENCHER: Escolher editor padrao
git config --global core.editor "code --wait"  # VS Code
# OU
git config --global core.editor "notepad"  # Notepad
```

- [ ] Editor configurado

**Editor escolhido:** <!-- PREENCHER: code / notepad / vim -->

---

### 1.3 Branch Padrao

```powershell
git config --global init.defaultBranch main
```

- [ ] Branch padrao = main

---

## PARTE 2: REPOSITORIO GITHUB

### 2.1 Criar Repositorio

**URL:** https://github.com/new

- [ ] Repositorio criado no GitHub
- [ ] Nome: <!-- PREENCHER: nome-do-repo -->
- [ ] Descricao: <!-- PREENCHER: descricao -->
- [ ] Visibilidade: <!-- PREENCHER: Public / Private -->

**URL do repositorio:** <!-- PREENCHER: https://github.com/usuario/repo -->

---

### 2.2 Configurar Remote

```powershell
# PREENCHER: URL do seu repositorio
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git

# Verificar
git remote -v
```

- [ ] Remote configurado
- [ ] Verificado com `git remote -v`

**Remote URL:** <!-- PREENCHER -->

---

### 2.3 Push Inicial

```powershell
# Primeiro push
git push -u origin main
```

- [ ] Push inicial concluido
- [ ] Repositorio visivel no GitHub

---

## PARTE 3: GITHUB PRO/ENTERPRISE SETTINGS

### 3.1 Informacoes Basicas

**GitHub > Settings > General**

- [ ] Repository name: <!-- PREENCHER -->
- [ ] Description: <!-- PREENCHER: Avila Framework - Governanca e automacao -->
- [ ] Website: <!-- PREENCHER (opcional) -->
- [ ] Topics (tags):
  - [ ] governance
  - [ ] automation
  - [ ] ai-agents
  - [ ] python
  - [ ] powershell
  - [ ] enterprise

---

### 3.2 Features

**GitHub > Settings > General > Features**

- [ ] Issues: ✅ ON
- [ ] Projects: ✅ ON
- [ ] Wiki: ❌ OFF (usar Docs/)
- [ ] Discussions: <!-- PREENCHER: ON / OFF -->
- [ ] Sponsorships: ❌ OFF (a menos que aplicavel)

---

### 3.3 Pull Requests

**GitHub > Settings > General > Pull Requests**

- [ ] Allow squash merging: ✅ ON
- [ ] Allow merge commits: ❌ OFF
- [ ] Allow rebase merging: ✅ ON
- [ ] Automatically delete head branches: ✅ ON
- [ ] Allow auto-merge: <!-- PREENCHER: ON / OFF -->

---

### 3.4 Security & Analysis (CRITICO!)

**GitHub > Settings > Security & analysis**

#### Dependency Graph
- [ ] ✅ Enabled

#### Dependabot Alerts
- [ ] ✅ Enabled

#### Dependabot Security Updates
- [ ] ✅ Enabled

#### Secret Scanning (GitHub Pro/Enterprise)
- [ ] ✅ Enabled
- [ ] Push protection: ✅ ON

#### Code Scanning (GitHub Advanced Security)
- [ ] ✅ CodeQL analysis configured
- [ ] ✅ Third-party code scanning (se aplicavel)

**Status:** <!-- PREENCHER: Free / Pro / Enterprise -->

---

### 3.5 Branch Protection (main)

**GitHub > Settings > Branches > Add rule**

**Branch name pattern:** `main`

- [ ] Require pull request before merging: ✅ ON
  - [ ] Require approvals: <!-- PREENCHER: 1 / 2 / 3 -->
  - [ ] Dismiss stale reviews: ✅ ON
  - [ ] Require review from Code Owners: <!-- PREENCHER: ON / OFF -->

- [ ] Require status checks: ✅ ON
  - [ ] Require branches to be up to date: ✅ ON
  - [ ] Status checks required:
    - [ ] Validacao Estrutura Avila
    - [ ] Lint Python
    - [ ] <!-- PREENCHER: outros checks -->

- [ ] Require conversation resolution: ✅ ON
- [ ] Require signed commits: <!-- PREENCHER: ON / OFF -->
- [ ] Require linear history: ✅ ON
- [ ] Require deployments to succeed: <!-- PREENCHER: ON / OFF -->
- [ ] Lock branch: ❌ OFF
- [ ] Do not allow bypassing (enforce for admins): <!-- PREENCHER: ON / OFF -->

**Approvals necessarios:** <!-- PREENCHER: numero -->

---

### 3.6 Collaborators & Teams

**GitHub > Settings > Collaborators**

#### Usuarios Individuais

- [ ] Usuario 1: <!-- PREENCHER: @username -->
  - Permissao: <!-- PREENCHER: Read / Write / Admin -->
  
- [ ] Usuario 2: <!-- PREENCHER: @username -->
  - Permissao: <!-- PREENCHER: Read / Write / Admin -->

#### Teams (se Organization/Enterprise)

- [ ] Team 1: <!-- PREENCHER: @org/team-name -->
  - Permissao: <!-- PREENCHER: Read / Write / Admin -->

---

### 3.7 GitHub Actions

**GitHub > Settings > Actions > General**

- [ ] Actions permissions:
  - [ ] Allow all actions ✅
  - [ ] Allow local actions only
  - [ ] Disable actions

- [ ] Workflow permissions:
  - [ ] Read and write permissions ✅
  - [ ] Read repository contents only

- [ ] Allow GitHub Actions to create PRs: <!-- PREENCHER: ON / OFF -->

**Secrets configurados:**

- [ ] Secret 1: <!-- PREENCHER: NOME_SECRET -->
  - Valor: <!-- NAO ANOTAR AQUI! -->
  
- [ ] Secret 2: <!-- PREENCHER: NOME_SECRET -->

---

### 3.8 Webhooks (Opcional)

**GitHub > Settings > Webhooks**

- [ ] Webhook 1: <!-- PREENCHER: URL -->
  - Events: <!-- PREENCHER: push, pull_request, etc. -->

---

### 3.9 GitHub Pages (Opcional)

**GitHub > Settings > Pages**

- [ ] Source: <!-- PREENCHER: None / gh-pages / docs -->
- [ ] Custom domain: <!-- PREENCHER (opcional) -->

---

## PARTE 4: GITHUB COPILOT

### 4.1 Verificar Acesso

- [ ] GitHub Copilot ativo na conta
- [ ] Copilot Chat disponivel
- [ ] Licenca: <!-- PREENCHER: Individual / Business / Enterprise -->

### 4.2 Configuracao Repositorio

**GitHub > Settings > Copilot**

- [ ] Enable Copilot: ✅ ON
- [ ] Copilot Chat: ✅ ON
- [ ] Policy: <!-- PREENCHER: Allow / Block / No policy -->

---

## PARTE 5: GITHUB PROJECTS

### 5.1 Criar Project Board (Opcional)

**GitHub > Projects > New project**

- [ ] Project criado
- [ ] Nome: <!-- PREENCHER -->
- [ ] Template: <!-- PREENCHER: Board / Table / Roadmap -->

**Views criadas:**
- [ ] Backlog
- [ ] In Progress
- [ ] Done

---

## PARTE 6: GITHUB ADVANCED SECURITY (Enterprise)

### 6.1 Code Scanning

- [ ] CodeQL configurado
- [ ] Scan on push: ✅ ON
- [ ] Scan on PR: ✅ ON

### 6.2 Secret Scanning

- [ ] Alerts configurados
- [ ] Push protection: ✅ ON
- [ ] Validity checks: ✅ ON

### 6.3 Dependency Review

- [ ] Enabled
- [ ] Block PRs with vulnerabilities: <!-- PREENCHER: ON / OFF -->

---

## PARTE 7: INTEGRACAO AZURE (Se Aplicavel)

### 7.1 Azure Boards

- [ ] Integrado com GitHub
- [ ] Work items linkados

### 7.2 Azure Pipelines

- [ ] Pipeline configurado
- [ ] YAML em `.github/workflows/` ou `.azure-pipelines/`

**URL Pipeline:** <!-- PREENCHER (opcional) -->

---

## PARTE 8: LABELS

**GitHub > Issues > Labels**

- [ ] `bug` (vermelho)
- [ ] `enhancement` (azul claro)
- [ ] `documentation` (azul)
- [ ] `governance` (roxo)
- [ ] `archivus` (amarelo)
- [ ] `avila-ops` (verde)
- [ ] `avila-inc` (azul escuro)
- [ ] `priority-high` (laranja)
- [ ] `security` (vermelho escuro)

---

## PARTE 9: MILESTONES

**GitHub > Issues > Milestones**

- [ ] v1.0 - Setup Inicial
- [ ] v1.1 - Agentes Completos
- [ ] v2.0 - <!-- PREENCHER -->

---

## PARTE 10: DOCUMENTACAO GITHUB

### 10.1 README.md

- [ ] Titulo claro
- [ ] Badges (build status, license, etc.)
- [ ] Descricao do projeto
- [ ] Como instalar
- [ ] Como usar
- [ ] Como contribuir
- [ ] Licenca

### 10.2 Arquivos Essenciais

- [ ] `.github/copilot-instructions.md` ✅
- [ ] `CONTRIBUTING.md` ✅
- [ ] `CODE_OF_CONDUCT.md` ✅
- [ ] `SECURITY.md` ✅
- [ ] `LICENSE` <!-- PREENCHER: tipo de licenca -->
- [ ] `CHANGELOG.md` (criar quando houver releases)

---

## PARTE 11: GITHUB RELEASES

### 11.1 Primeira Release

- [ ] Tag criada: <!-- PREENCHER: v1.0.0 -->
- [ ] Release notes escritas
- [ ] Artifacts anexados (se aplicavel)

---

## VALIDACAO FINAL

Execute validacao completa:

```powershell
# 1. Validar estrutura
.\Setup\Validar-ConfiguracaoIDE.ps1

# 2. Validar Git
git status
git log --oneline -5

# 3. Validar remote
git remote -v

# 4. Testar pull
git pull origin main
```

### Checklist Validacao

- [ ] Todos arquivos .vscode/ criados
- [ ] Todos arquivos .github/ criados
- [ ] Git configurado localmente
- [ ] Remote configurado
- [ ] Push inicial concluido
- [ ] GitHub Pro/Enterprise configurado
- [ ] Branch protection ativa
- [ ] Security features habilitadas
- [ ] Workflows funcionando

---

## RESUMO DE SLOTS CRITICOS

### SLOTS QUE VOCE DEVE PREENCHER MANUALMENTE:

1. **Git Global:**
 - [ ] `user.name` = <!-- PREENCHER -->
   - [ ] `user.email` = <!-- PREENCHER -->

2. **GitHub Repository:**
   - [ ] URL = <!-- PREENCHER: https://github.com/usuario/repo -->
   - [ ] Visibilidade = <!-- PREENCHER: Public / Private -->

3. **Colaboradores:**
   - [ ] Usuario 1 = <!-- PREENCHER: @username -->
   - [ ] Permissao = <!-- PREENCHER: Write / Admin -->

4. **Branch Protection:**
   - [ ] Approvals = <!-- PREENCHER: 1 / 2 / 3 -->

5. **GitHub Copilot:**
 - [ ] Licenca = <!-- PREENCHER: Individual / Business / Enterprise -->

6. **Security Email:**
   - [ ] Email = <!-- PREENCHER para SECURITY.md -->

7. **Homepage:**
   - [ ] URL = <!-- PREENCHER (opcional) -->

---

## SCRIPT DE VALIDACAO

```powershell
# Executar para verificar tudo
.\Setup\Inicializar-Git.ps1
.\Setup\Validar-ConfiguracaoIDE.ps1

# Ver status
git status
```

---

## PROXIMOS PASSOS APOS PREENCHER

1. Criar repositorio no GitHub
2. Executar `.\Setup\Inicializar-Git.ps1`
3. Configurar Security & analysis
4. Proteger branch main
5. Adicionar colaboradores
6. Fazer primeiro push

---

## TEMPO ESTIMADO

- **Preencher slots:** 10-15 minutos
- **Configurar GitHub:** 15-20 minutos
- **Primeiro push:** 5 minutos
- **Total:** 30-40 minutos

---

**ESTE E O ARQUIVO MASTER DE CONFIGURACAO!**

Mantenha atualizado conforme preenche os slots.

---

**Criado por:** Nicolas Avila  
**Data:** 2025-11-10  
**Status:** AGUARDANDO PREENCHIMENTO
