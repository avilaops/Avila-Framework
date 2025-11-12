# SLOTS OBRIGATORIOS - MASTER LIST

**ESTE E O ARQUIVO PRINCIPAL!**

Use para preencher TODOS os slots necessarios para configuracao completa.

---

## CATEGORIA 1: GIT LOCAL

### user.name
**Comando:** `git config --global user.name "PREENCHER"`  
**Valor:** <!-- PREENCHER: Seu nome completo -->  
**Status:** [ ] Configurado

### user.email
**Comando:** `git config --global user.email "PREENCHER"`  
**Valor:** <!-- PREENCHER: seu.email@example.com -->  
**Status:** [ ] Configurado

### core.editor
**Comando:** `git config --global core.editor "code --wait"`  
**Valor:** <!-- PREENCHER: code / notepad / vim -->  
**Status:** [ ] Configurado

---

## CATEGORIA 2: GITHUB REPOSITORY

### Repository URL
**GitHub:** https://github.com/new  
**Valor:** <!-- PREENCHER: https://github.com/usuario/repo.git -->  
**Status:** [ ] Criado

### Repository Name
**Valor:** <!-- PREENCHER: avila -->  
**Status:** [ ] Definido

### Description
**Valor:** <!-- PREENCHER: Avila Framework - Governanca e automacao -->  
**Status:** [ ] Definido

### Visibility
**Valor:** <!-- PREENCHER: Public / Private -->  
**Status:** [ ] Definido

### Homepage URL
**Valor:** <!-- PREENCHER (opcional): https://... -->  
**Status:** [ ] Definido

---

## CATEGORIA 3: GITHUB TOPICS

**GitHub > Settings > Topics**

- [ ] governance
- [ ] automation
- [ ] ai-agents
- [ ] python
- [ ] powershell
- [ ] azure
- [ ] enterprise
- [ ] <!-- PREENCHER: outros topics -->

---

## CATEGORIA 4: SECURITY EMAIL

### Security Contact
**Arquivo:** `SECURITY.md` linha 24
**Valor:** <!-- PREENCHER: security@avilaframework.com -->  
**Status:** [ ] Atualizado

---

## CATEGORIA 5: BRANCH PROTECTION

### Approvals Required
**GitHub > Settings > Branches > main**  
**Valor:** <!-- PREENCHER: 1 / 2 / 3 -->  
**Status:** [ ] Configurado

### Status Checks Required
**Valor:** <!-- PREENCHER: lista de checks obrigatorios -->
- [ ] Validacao Estrutura Avila
- [ ] Lint Python
- [ ] <!-- PREENCHER: outros -->

---

## CATEGORIA 6: COLLABORATORS

### Colaborador 1
**Username:** <!-- PREENCHER: @username -->  
**Permission:** <!-- PREENCHER: Read / Write / Admin -->  
**Status:** [ ] Adicionado

### Colaborador 2
**Username:** <!-- PREENCHER: @username -->  
**Permission:** <!-- PREENCHER: Read / Write / Admin -->  
**Status:** [ ] Adicionado

---

## CATEGORIA 7: GITHUB COPILOT

### License Type
**Valor:** <!-- PREENCHER: Individual / Business / Enterprise -->  
**Status:** [ ] Verificado

### Repository Access
**GitHub > Settings > Copilot**  
**Valor:** <!-- PREENCHER: Enabled / Disabled -->  
**Status:** [ ] Configurado

---

## CATEGORIA 8: SECRETS (Actions)

### OPENAI_API_KEY (se aplicavel)
**GitHub > Settings > Secrets > Actions > New secret**  
**Name:** `OPENAI_API_KEY`  
**Value:** `sk-...` (NAO anotar aqui!)  
**Status:** [ ] Configurado

### AZURE_CREDENTIALS (se aplicavel)
**Name:** `AZURE_CREDENTIALS`  
**Value:** `{...}` (JSON service principal)  
**Status:** [ ] Configurado

### Outros Secrets
**Name:** <!-- PREENCHER -->  
**Status:** [ ] Configurado

---

## CATEGORIA 9: ENVIRONMENTS

### Production
**GitHub > Settings > Environments > New**  
**Name:** `production`  
**Reviewers:** <!-- PREENCHER: @username -->  
**Status:** [ ] Criado

### Development
**Name:** `development`  
**Status:** [ ] Criado (opcional)

---

## CATEGORIA 10: PROJECTS

### Project Board
**GitHub > Projects > New project**  
**Name:** <!-- PREENCHER: Avila Roadmap -->  
**Template:** <!-- PREENCHER: Board / Table / Roadmap -->  
**Status:** [ ] Criado

---

## CATEGORIA 11: INTEGRACOES

### Slack (opcional)
**Webhook URL:** <!-- PREENCHER (se usar) -->  
**Channel:** <!-- PREENCHER: #avila-notificacoes -->  
**Status:** [ ] Configurado

### Azure Boards (opcional)
**Organization:** <!-- PREENCHER -->  
**Project:** <!-- PREENCHER -->  
**Status:** [ ] Configurado

### Outras Integracoes
**Nome:** <!-- PREENCHER -->  
**URL:** <!-- PREENCHER -->  
**Status:** [ ] Configurado

---

## CATEGORIA 12: LICENCA

### License Type
**Arquivo:** `LICENSE`  
**Tipo:** <!-- PREENCHER: MIT / Apache-2.0 / Proprietary -->  
**Status:** [ ] Criado

**Se open source, criar:**
```powershell
# Exemplo MIT License
code LICENSE
# Copiar de: https://opensource.org/licenses/MIT
```

---

## CATEGORIA 13: BADGES README

### Badges a Adicionar em README.md

**Build Status:**
```markdown
![Build](https://github.com/USUARIO/REPO/actions/workflows/validate-structure.yml/badge.svg)
```
**Valor:** <!-- PREENCHER: usuario/repo -->

**License:**
```markdown
![License](https://img.shields.io/github/license/USUARIO/REPO)
```

**Language:**
```markdown
![Python](https://img.shields.io/badge/python-3.13-blue)
```

---

## CATEGORIA 14: CODEOWNERS (Pro/Enterprise)

### Criar .github/CODEOWNERS

```
# Donos de codigo por diretorio
* @nicolas-avila

# Archivus
/AvilaOps/Agente\ Bibliotecario\ \(Archivus\)/ @nicolas-avila

# Scripts criticos
/Scripts/ @nicolas-avila
/Setup/ @nicolas-avila

# Documentacao
/Docs/ @nicolas-avila
```

**Status:** [ ] Criado

---

## CATEGORIA 15: GITHUB INSIGHTS

### Configurar Metricas

**GitHub > Insights > Community Standards**

Verificar se 100%:
- [ ] Description
- [ ] README
- [ ] Code of conduct
- [ ] Contributing
- [ ] License
- [ ] Security policy
- [ ] Issue templates
- [ ] Pull request template

---

## VALIDACAO FINAL

### Executar Todos Scripts

```powershell
# 1. Inicializar Git
.\Setup\Inicializar-Git.ps1

# 2. Validar IDE
.\Setup\Validar-ConfiguracaoIDE.ps1

# 3. Verificar status
git status

# 4. Ver remote
git remote -v
```

### Checklist Visual GitHub

Visitar cada aba do repositorio:

- [ ] Code - Arquivos visiveis
- [ ] Issues - Templates OK
- [ ] Pull requests - Template OK
- [ ] Actions - Workflows rodando
- [ ] Security - Alerts habilitadas
- [ ] Insights - Community 100%
- [ ] Settings - Tudo configurado

---

## RESUMO DE SLOTS CRITICOS

### MINIMO NECESSARIO (5 slots):

1. **Git user.name** = <!-- PREENCHER -->
2. **Git user.email** = <!-- PREENCHER -->
3. **GitHub repo URL** = <!-- PREENCHER -->
4. **Visibility (Public/Private)** = <!-- PREENCHER -->
5. **Branch protection (approvals)** = <!-- PREENCHER: 0/1/2 -->

### RECOMENDADO (10 slots adicionais):

6. **Security email** = <!-- PREENCHER -->
7. **GitHub Copilot license** = <!-- PREENCHER -->
8. **Topics (tags)** = <!-- PREENCHER: governance, automation... -->
9. **Colaboradores** = <!-- PREENCHER: @username -->
10. **Secrets** = <!-- PREENCHER: nomes dos secrets -->
11. **Environment (production)** = <!-- PREENCHER: reviewers -->
12. **License type** = <!-- PREENCHER: MIT / Apache / Proprietary -->
13. **Homepage URL** = <!-- PREENCHER (opcional) -->
14. **Integracoes** = <!-- PREENCHER: Slack / Azure / etc -->
15. **Project board** = <!-- PREENCHER: nome do project -->

---

## ORDEM DE PREENCHIMENTO RECOMENDADA

```
1. Git local (user.name, user.email)        ← PRIMEIRO
2. Criar repositorio GitHub     ← SEGUNDO
3. Push inicial            ← TERCEIRO
4. Security & analysis        ← QUARTO
5. Branch protection      ← QUINTO
6. Secrets & environments       ← SEXTO
7. Colaboradores   ← SETIMO
8. Resto (opcional)               ← DEPOIS
```

---

## COMANDO UNICO PARA INICIAR TUDO

```powershell
# Executar script master
.\Setup\Inicializar-Git.ps1

# Seguir prompts e preencher:
# - Nome
# - Email
# - URL do repo (se ja criou no GitHub)
```

---

**ESTE E O ARQUIVO MASTER DE SLOTS!**

Preencha um por um, marcando [x] conforme completa.

---

**Criado por:** Nicolas Avila  
**Data:** 2025-11-10  
**Status:** AGUARDANDO PREENCHIMENTO  
**Uso:** REFERENCIA PRINCIPAL
