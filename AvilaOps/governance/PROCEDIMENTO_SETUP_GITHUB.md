# PROCEDIMENTO OPERACIONAL: SETUP GITHUB REPOSITORY

**Documento:** PROCEDIMENTO_SETUP_GITHUB.md
**Versão:** 1.0
**Data:** 11/11/2025
**Responsável:** AvilaOps - DevOps Team
**Categoria:** Infraestrutura e Versionamento

## OBJETIVO
Estabelecer conexão entre repositório Git local e GitHub, completando a configuração do ecossistema de sincronização Ávila Framework.

## PRÉ-REQUISITOS
✅ **Repositório Git local inicializado**
✅ **Arquivos commitados (1000+ arquivos)**
✅ **Configuração Git definida (user.name, user.email)**
✅ **Conta GitHub ativa (avilaops)**

## PROCEDIMENTO STEP-BY-STEP

### ETAPA 1: CRIAÇÃO DO REPOSITÓRIO GITHUB

**1.1 Acesso ao GitHub**
```
URL: https://github.com/avilaops
```

**1.2 Criar Repositório**
- Clicar em **"New Repository"** (botão verde)
- **Nome:** `avila-framework`
- **Descrição:** "🏛️ Ávila Framework - Ecosistema integrado para gestão empresarial"
- **Visibilidade:** Private (recomendado para dados corporativos)
- **Configurações:**
  - ❌ NÃO marcar: Initialize with README
  - ❌ NÃO marcar: Add .gitignore
  - ❌ NÃO marcar: Choose a license
- Clicar em **"Create Repository"**

**Justificativa:** Não inicializar com arquivos pois já possuímos estrutura local completa.

### ETAPA 2: CONEXÃO REPOSITÓRIO LOCAL → GITHUB

**2.1 Comandos de Configuração**
Executar **EM SEQUÊNCIA** no PowerShell (diretório raiz do projeto):

```powershell
# Comando 1: Adicionar origem remota
git remote add origin https://github.com/avilaops/Avila-Framework.git

# Comando 2: Renomear branch principal
git branch -M main

# Comando 3: Push inicial
git push -u origin main
```

**2.2 Validação**
```powershell
# Verificar conexão remota
git remote -v

# Verificar status do repositório
git status
```

**Resultado esperado:** Todos os arquivos sincronizados no GitHub.

## PROCEDIMENTOS DE SINCRONIZAÇÃO

### SYNC AUTOMÁTICO (RECOMENDADO)
```powershell
# Script centralizado de sincronização
.\Scripts\sync-center.ps1
```

### SYNC MANUAL
```powershell
# 1. Verificar status
git status

# 2. Adicionar alterações
git add .

# 3. Commit com mensagem descritiva
git commit -m "📝 [CATEGORIA] Descrição da mudança"

# 4. Push para GitHub
git push
```

**Padrão de mensagens de commit:**
- `� [DOC]` - Documentação
- `🔧 [FIX]` - Correções
- `✨ [FEAT]` - Nova funcionalidade
- `🏗️ [INFRA]` - Infraestrutura
- `🔒 [SEC]` - Segurança

## INTEGRAÇÃO OBSIDIAN

### CONFIGURAÇÃO PÓS-SETUP
1. **Abrir Obsidian:** `C:\Users\nicol\OneDrive\Avila\Docs`
2. **Dashboard:** Acessar `Dashboard-Principal.md`
3. **Plugin Git:**
   - Settings → Community Plugins → Obsidian Git
   - Ativar "Auto pull/push" (intervalo: 30 minutos)
   - Configurar "Auto backup" (intervalo: 10 minutos)

## VALIDAÇÃO FINAL

### CHECKLIST DE VERIFICAÇÃO
- [ ] Repositório GitHub criado (`avila-framework`)
- [ ] Conexão remota estabelecida
- [ ] Push inicial realizado com sucesso
- [ ] Sincronização GitHub ↔ VS Code operacional
- [ ] Plugin Obsidian Git configurado
- [ ] Dashboard Obsidian funcional
- [ ] Scripts de automação testados

### RESULTADO ESPERADO
Ecossistema integrado de sincronização:
```
GitHub ↔ Git Local ↔ VS Code ↔ Obsidian
```

## TROUBLESHOOTING

### ERRO: "Permission denied" ou "Authentication failed"
**Causa:** Token de autenticação não configurado
**Solução:**
```powershell
git config credential.helper store
```
Utilizar **Personal Access Token** como senha no primeiro push.

### ERRO: "Repository not found"
**Causa:** URL do repositório incorreta ou repositório não criado
**Solução:** Verificar se repositório foi criado no GitHub com nome exato: `avila-framework`

### ERRO: "fatal: refusing to merge unrelated histories"
**Causa:** Conflito entre históricos Git
**Solução:**
```powershell
git pull origin main --allow-unrelated-histories
```

## RESPONSABILIDADES

**AvilaOps DevOps Team:**
- Manutenção dos scripts de sincronização
- Monitoramento da integridade do repositório
- Backup e disaster recovery

**Usuários Finais:**
- Execução dos procedimentos conforme documentado
- Reporte de problemas via issue tracking
- Aderência aos padrões de commit

---

**DOCUMENTO APROVADO:** AvilaOps Governance Framework
**PRÓXIMA REVISÃO:** 11/12/2025

## 🎯 VERIFICAÇÃO FINAL

Após executar os comandos acima, você deve ter:
- ✅ Repositório no GitHub criado
- ✅ Código sincronizado GitHub ↔ VS Code ↔ Obsidian
- ✅ Sync automático funcionando
- ✅ Dashboard operacional

## 🆘 SE DER ERRO

**Problema comum:** "Permission denied" ou "Authentication failed"
**Solução:** Configure o token do GitHub:
```powershell
git config credential.helper store
```
Depois use seu **Personal Access Token** como senha.

---

**🎉 QUASE LÁ! Só falta criar o repositório no GitHub e executar 3 comandos!**
