# GUIA DEFINITIVO - GITHUB PRO/ENTERPRISE

**Projeto:** Avila Framework  
**Data:** 2025-11-10  
**Status:** CONFIGURACAO COMPLETA

---

## INICIO RAPIDO (5 MINUTOS)

### 1. Executar Script de Inicializacao

```powershell
cd C:\Users\nicol\OneDrive\Avila
.\Setup\Inicializar-Git.ps1
```

**O que faz:**
- Verifica Git instalado
- Configura user.name e user.email
- Inicializa repositorio
- Verifica secrets
- Cria commit inicial
- Configura remote (se fornecer URL)

### 2. Criar Repositorio no GitHub

**URL:** https://github.com/new

**Preencher:**
- **Repository name:** `avila` (ou nome desejado)
- **Description:** "Avila Framework - Governanca corporativa e automacao empresarial"
- **Visibility:** Private (recomendado inicialmente)
- **Initialize:** ❌ NAO (ja temos arquivos locais)

**Clicar:** Create repository

### 3. Conectar e Push

```powershell
# Copiar URL do repositorio criado
# Exemplo: https://github.com/seu-usuario/avila.git

git remote add origin https://github.com/SEU_USUARIO/avila.git
git push -u origin main
```

---

## CONFIGURACAO GITHUB PRO/ENTERPRISE (20 MINUTOS)

### PARTE A: SECURITY & ANALYSIS

**GitHub > Settings > Security & analysis**

#### 1. Dependency Graph
```
[✓] Enabled
```

#### 2. Dependabot Alerts
```
[✓] Enabled
```

#### 3. Dependabot Security Updates
```
[✓] Enabled
```

#### 4. Secret Scanning (Pro/Enterprise)
```
[✓] Enabled
[✓] Push protection: ON
```

**O que faz:** Bloqueia push se detectar credenciais!

#### 5. Code Scanning (Advanced Security)
```
[✓] Set up > CodeQL Analysis
```

**Arquivo criado:** `.github/workflows/codeql.yml`

---

### PARTE B: BRANCH PROTECTION

**GitHub > Settings > Branches > Add rule**

#### Branch Name Pattern
```
main
```

#### Configuracoes Essenciais

**1. Require Pull Request:**
```
[✓] Require a pull request before merging
    [✓] Required approvals: 1
    [✓] Dismiss stale reviews
    [ ] Require review from Code Owners (se tiver CODEOWNERS)
```

**2. Require Status Checks:**
```
[✓] Require status checks to pass
    [✓] Require branches to be up to date
 
    Status checks encontrados:
    [✓] Validacao Estrutura Avila
    [✓] Lint Python
```

**3. Outras Protecoes:**
```
[✓] Require conversation resolution before merging
[ ] Require signed commits (opcional)
[✓] Require linear history
[ ] Require deployments to succeed (se tiver)
```

**4. Regras para Admins:**
```
[ ] Do not allow bypassing the above settings
```

**Clicar:** Create / Save changes

---

### PARTE C: ACTIONS & WORKFLOWS

**GitHub > Settings > Actions > General**

#### 1. Actions Permissions
```
(•) Allow all actions and reusable workflows
```

#### 2. Workflow Permissions
```
(•) Read and write permissions
[✓] Allow GitHub Actions to create and approve pull requests
```

#### 3. Fork Pull Request Workflows
```
[✓] Require approval for first-time contributors
```

---

### PARTE D: SECRETS & VARIABLES

**GitHub > Settings > Secrets and variables > Actions**

#### Secrets (NAO anotar valores aqui!)

**Criar secrets:**

1. **OPENAI_API_KEY** (se usar OpenAI)
   ```
   New repository secret
   Name: OPENAI_API_KEY
   Value: sk-... (sua chave)
   ```
   - [ ] Criado

2. **AZURE_CREDENTIALS** (se usar Azure)
   ```
   Name: AZURE_CREDENTIALS
   Value: {...} (JSON do service principal)
   ```
   - [ ] Criado

3. **Outros secrets:**
   - [ ] <!-- PREENCHER: NOME_SECRET -->
   - [ ] <!-- PREENCHER: NOME_SECRET -->

#### Variables (valores nao-sensiveis)

1. **WORKSPACE_ROOT**
   ```
Name: WORKSPACE_ROOT
   Value: C:\Users\nicol\OneDrive\Avila
   ```
   - [ ] Criado

2. **PYTHON_VERSION**
   ```
   Name: PYTHON_VERSION
Value: 3.13
   ```
   - [ ] Criado

---

### PARTE E: ENVIRONMENTS (Pro/Enterprise)

**GitHub > Settings > Environments**

#### 1. Production
```
[New environment]
Name: production

Protection rules:
[✓] Required reviewers: 1
[✓] Wait timer: 0 minutes
[ ] Deployment branches: All branches / Selected branches
```

- [ ] Environment criado
- [ ] Reviewers: <!-- PREENCHER: @username -->

#### 2. Development (opcional)
```
Name: development
Protection rules: (menos restritivo)
```

- [ ] Environment criado

---

### PARTE F: CUSTOM PROPERTIES (Enterprise)

**Organization > Settings > Custom properties**

- [ ] `team`: <!-- PREENCHER: ops / inc / shared -->
- [ ] `criticality`: <!-- PREENCHER: low / medium / high -->
- [ ] `compliance`: <!-- PREENCHER: yes / no -->

---

## CONFIGURACAO AVANCADA (OPCIONAL)

### GitHub Apps

**GitHub > Settings > GitHub Apps**

Apps recomendadas:
- [ ] **Codecov** (coverage reports)
- [ ] **Sentry** (error tracking)
- [ ] **Dependabot** (ja incluido)

### Integracoes

**GitHub > Settings > Integrations**

- [ ] Slack (notificacoes)
- [ ] Microsoft Teams
- [ ] Azure Boards
- [ ] <!-- PREENCHER: outras -->

---

## VERIFICACAO POS-CONFIGURACAO

### Checklist Visual

Visite seu repositorio no GitHub e verifique:

#### Aba Code
- [ ] Arquivos visiveis
- [ ] README renderizado
- [ ] Badges aparecendo (se tiver)

#### Aba Issues
- [ ] Templates disponiveis (Bug, Feature)
- [ ] Labels configuradas

#### Aba Pull Requests
- [ ] Template disponivel

#### Aba Actions
- [ ] Workflows listados
- [ ] Ultimo run bem-sucedido (ou esperando push)

#### Aba Security
- [ ] Dependency graph ativo
- [ ] Alerts configurados
- [ ] Code scanning ativo (se Pro/Enterprise)

#### Settings
- [ ] Branch protection em `main`
- [ ] Actions habilitadas
- [ ] Secrets configurados

---

## TESTE COMPLETO

### 1. Criar Branch de Teste

```powershell
git checkout -b test/verificacao-github
```

### 2. Fazer Mudanca Minima

```powershell
echo "# Teste" > TESTE.md
git add TESTE.md
git commit -m "test: verificar configuracao GitHub"
git push -u origin test/verificacao-github
```

### 3. Abrir Pull Request

**GitHub > Pull requests > New pull request**

```
Base: main
Compare: test/verificacao-github

[Create pull request]
```

**Verificar:**
- [ ] Template de PR apareceu
- [ ] Status checks estao rodando
- [ ] Branch protection esta ativa
- [ ] Nao consegue fazer merge sem approval (se configurado)

### 4. Testar Merge

- [ ] Aprovar PR (se necessario)
- [ ] Merge
- [ ] Branch deletada automaticamente

### 5. Limpar

```powershell
git checkout main
git pull
git branch -d test/verificacao-github
```

---

## MANUTENCAO CONTINUA

### Mensal
- [ ] Revisar Dependabot alerts
- [ ] Atualizar dependencias
- [ ] Verificar security advisories

### Trimestral
- [ ] Revisar branch protection rules
- [ ] Auditar colaboradores
- [ ] Revisar secrets (rotacionar se necessario)

### Anual
- [ ] Revisar toda configuracao
- [ ] Atualizar SECURITY.md
- [ ] Renovar licencas (se aplicavel)

---

## TROUBLESHOOTING

### Erro: "Push protection blocked"

**Causa:** Secret detectado no codigo

**Solucao:**
1. Remover secret do codigo
2. Adicionar ao .gitignore
3. Usar environment variable
4. Retry push

### Erro: "Branch protection failed"

**Causa:** Status check nao passou

**Solucao:**
1. Ver detalhes do check
2. Corrigir erro
3. Push novamente

### Workflow nao executa

**Verificar:**
1. Actions habilitadas?
2. Workflow file valido (.yml)?
3. Trigger correto (on: push)?

---

## RECURSOS GITHUB PRO/ENTERPRISE

### GitHub Pro ($4/mes)
- ✅ 3.000 Actions minutes/mes
- ✅ 2GB Packages storage
- ✅ Advanced code review tools
- ✅ Required reviewers
- ✅ Multiple PR reviewers
- ✅ Auto-linked references

### GitHub Enterprise ($21/user/mes)
- ✅ Tudo do Pro +
- ✅ GitHub Advanced Security
- ✅ Secret scanning
- ✅ Code scanning
- ✅ Dependency review
- ✅ SAML SSO
- ✅ 50.000 Actions minutes/mes

---

## LINKS UTEIS

- **GitHub Docs:** https://docs.github.com
- **Actions:** https://github.com/features/actions
- **Advanced Security:** https://github.com/features/security
- **Copilot:** https://github.com/features/copilot
- **Status:** https://www.githubstatus.com

---

## SUPORTE

### Problemas com configuracao?

1. Ver logs: `Logs/Daily/git_setup_*.log`
2. Verificar checklist: `Setup/CHECKLIST_GITHUB_SLOTS.md`
3. Executar validador: `.\Setup\Validar-ConfiguracaoIDE.ps1`

### Duvidas sobre GitHub?

- **Docs:** https://docs.github.com
- **Community:** https://github.community
- **Support:** (se Pro/Enterprise)

---

## CONCLUSAO

**TUDO CRIADO E DOCUMENTADO!**

Arquivos do GitHub:
- [x] .gitignore (profissional)
- [x] .gitattributes (line endings)
- [x] Issue templates (bug, feature)
- [x] PR template
- [x] Workflows (validacao, lint, security)
- [x] CONTRIBUTING.md
- [x] CODE_OF_CONDUCT.md
- [x] SECURITY.md
- [x] settings.yml

Scripts e guias:
- [x] Inicializar-Git.ps1
- [x] Validar-ConfiguracaoIDE.ps1
- [x] CHECKLIST_GITHUB_SLOTS.md
- [x] Este guia

**Proxima acao:**

```powershell
.\Setup\Inicializar-Git.ps1
```

Depois preencha os slots em:
```
Setup\CHECKLIST_GITHUB_SLOTS.md
```

---

**Criado por:** Nicolas Avila  
**Data:** 2025-11-10  
**Versao:** 1.0  
**Framework:** Avila Inc / Avila Ops
