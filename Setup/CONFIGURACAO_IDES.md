# CONFIGURACAO COMPLETA - VS CODE E VISUAL STUDIO 2022
## Padrao Avila Framework

**Data:** 2025-11-10  
**Versao:** 1.0  
**Responsavel:** Nicolas Avila

---

## ARQUIVOS CRIADOS

### VS Code
```
.vscode/
??? avila.code-workspace        # Workspace multi-pastas
??? settings.json   # Configuracoes globais
??? extensions.json             # Extensoes recomendadas
??? tasks.json             # Tarefas automatizadas
??? launch.json       # Configuracoes debug
??? avila-snippets.code-snippets # Snippets personalizados
```

### Visual Studio 2022
```
.visualstudio/
??? Avila-VS2022-Settings.vssettings      # Configuracoes IDE
??? Avila-VS2022-Components.vsconfig      # Componentes necessarios
```

---

## INSTALACAO VS CODE

### 1. Abrir Workspace

```powershell
cd C:\Users\nicol\OneDrive\Avila
code .vscode\avila.code-workspace
```

**OU** no VS Code:
```
File > Open Workspace from File > .vscode\avila.code-workspace
```

### 2. Instalar Extensoes Recomendadas

Ao abrir o workspace, VS Code mostrara notificacao:
```
"Este workspace recomenda extensoes. Deseja instala-las?"
> Instalar Todas
```

**OU manualmente:**
```
Ctrl+Shift+X > Aba "RECOMENDADAS" > Instalar Todas
```

### 3. Extensoes Essenciais (verificar)

- [x] GitHub Copilot
- [x] GitHub Copilot Chat
- [x] Python
- [x] Pylance
- [x] PowerShell
- [x] Prettier
- [x] YAML
- [x] Markdown All in One

### 4. Verificar Configuracoes

```
Ctrl+, (Settings) > Workspace
```

Deve mostrar:
- Editor: Tab Size = 4
- Files: Encoding = UTF-8
- Files: Auto Save = afterDelay
- Python: Formatter = black

---

## INSTALACAO VISUAL STUDIO 2022

### 1. Importar Configuracoes

```
Visual Studio 2022
> Tools
> Import and Export Settings
> Import selected environment settings
> Browse: .visualstudio\Avila-VS2022-Settings.vssettings
> Finish
```

### 2. Verificar Componentes

```
Visual Studio Installer
> Modify
> Import configuration: .visualstudio\Avila-VS2022-Components.vsconfig
```

Componentes necessarios:
- [x] .NET desktop development
- [x] ASP.NET and web development
- [x] Python development
- [x] Node.js development
- [x] Azure development
- [x] GitHub Copilot

### 3. Configurar GitHub Copilot

```
Extensions > Manage Extensions
> Pesquisar: "GitHub Copilot"
> Instalar
> Restart Visual Studio
> View > GitHub Copilot Chat (Ctrl+/)
```

---

## USO DAS CONFIGURACOES

### VS Code: Tasks Disponiveis

Pressione `Ctrl+Shift+P` > `Tasks: Run Task`:

1. **Avila: Executar Archivus (Manual)**
2. **Avila: Setup Ambiente**
3. **Avila: Verificar Estrutura**
4. **Avila: Gerar Relatorio Diario**
5. **Avila: Backup Scripts**
6. **Python: Criar venv**
7. **Python: Instalar Dependencias**
8. **Git: Status**
9. **Git: Log (ultimos 10)**

### VS Code: Debugging

Pressione `F5` ou `Ctrl+Shift+D`:

**Configuracoes disponiveis:**
- Python: Arquivo Atual
- Python: Archivus Main
- Python: Script em Scripts/
- PowerShell: Script Atual
- PowerShell: Setup Ambiente
- PowerShell: Run Archivus

### VS Code: Snippets

Digite o prefixo e pressione `Tab`:

| Prefixo | Resultado |
|---------|-----------|
| `avila-py-header` | Header Python completo |
| `avila-ps-header` | Header PowerShell completo |
| `avila-readme` | Template README Avila |
| `avila-relatorio` | Template relatorio auditoria |
| `avila-config` | Template config.yaml |
| `avila-commit` | Mensagem commit padrao |
| `avila-log` | Funcao log padrao |
| `avila-try` | Try-except com log |

---

## ATALHOS PERSONALIZADOS

### VS Code (adicionar em Keyboard Shortcuts)

```json
[
  {
    "key": "ctrl+alt+a",
 "command": "workbench.action.tasks.runTask",
    "args": "Avila: Executar Archivus (Manual)"
  },
  {
    "key": "ctrl+alt+s",
    "command": "workbench.action.tasks.runTask",
    "args": "Avila: Setup Ambiente"
  }
]
```

### Visual Studio 2022

```
Tools > Options > Keyboard
> Pesquisar: "GitHub.Copilot.Chat"
> Shortcut: Ctrl+/ (padrao)
```

---

## VALIDACAO

### Checklist VS Code

```powershell
# Verificar se workspace esta correto
Get-Content .vscode\avila.code-workspace | Select-String "Avila"

# Verificar settings
Get-Content .vscode\settings.json | Select-String "avila"

# Verificar extensions
Get-Content .vscode\extensions.json | Select-String "copilot"
```

### Checklist Visual Studio 2022

- [ ] Configuracoes importadas
- [ ] GitHub Copilot instalado
- [ ] Copilot Chat acessivel (Ctrl+/)
- [ ] Projeto default em C:\Users\nicol\OneDrive\Avila
- [ ] Tab size = 4 espacos

---

## TROUBLESHOOTING

### VS Code: Extensoes nao instalam

```powershell
# Reinstalar VS Code
winget upgrade --id Microsoft.VisualStudioCode
```

### VS Code: Settings nao aplicam

```
1. Fechar VS Code
2. Deletar: %APPDATA%\Code\User\settings.json (backup antes)
3. Reabrir workspace
```

### Visual Studio: Copilot nao aparece

```
1. Extensions > Manage Extensions
2. Uninstall GitHub Copilot
3. Restart VS
4. Reinstalar GitHub Copilot
5. Sign in com conta GitHub
```

### Python venv nao funciona

```powershell
# Criar manualmente
cd C:\Users\nicol\OneDrive\Avila
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pyyaml
```

---

## PROXIMOS PASSOS

### Apos Instalacao

1. **Abrir workspace no VS Code:**
   ```powershell
   code .vscode\avila.code-workspace
   ```

2. **Instalar extensoes recomendadas**

3. **Testar task:**
   ```
   Ctrl+Shift+P > Tasks: Run Task > Avila: Setup Ambiente
 ```

4. **Testar snippet:**
   - Criar arquivo: `teste.py`
   - Digitar: `avila-py-header` + Tab
   - Deve gerar header completo

5. **Importar settings no VS 2022:**
   ```
   Tools > Import/Export Settings > .visualstudio\Avila-VS2022-Settings.vssettings
   ```

---

## MANUTENCAO

### Atualizar Configuracoes

Sempre que alterar `.vscode/settings.json` ou `.visualstudio/*.vssettings`:

1. Commitar no Git:
   ```powershell
   git add .vscode/ .visualstudio/
   git commit -m "chore: atualizar configuracoes IDE"
   git push
   ```

2. Notificar equipe para reimportar settings

### Adicionar Nova Extensao

Editar `.vscode/extensions.json`:
```json
{
  "recommendations": [
    "publisher.extension-name"
  ]
}
```

---

## LINKS UTEIS

- **VS Code Settings:** https://code.visualstudio.com/docs/getstarted/settings
- **VS Code Tasks:** https://code.visualstudio.com/docs/editor/tasks
- **VS Code Snippets:** https://code.visualstudio.com/docs/editor/userdefinedsnippets
- **VS 2022 Settings:** https://learn.microsoft.com/visualstudio/ide/environment-settings

---

**Criado por:** Nicolas Avila  
**Data:** 2025-11-10  
**Versao:** 1.0  
**Framework:** Avila Inc / Avila Ops
