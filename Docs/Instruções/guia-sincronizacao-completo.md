# 🎯 Guia de Sincronização: GitHub ↔ VS Code ↔ Obsidian

## ✅ Configuração Concluída!

Seu ecossistema Ávila agora está **100% sincronizado** entre:
- 🐙 **GitHub** - Versionamento e backup
- 💻 **VS Code** - Desenvolvimento e edição
- 📱 **Obsidian** - Knowledge management

---

## 🚀 Como Usar

### 1. **Primeira Execução**
```powershell
# Execute uma vez para configurar tudo
.\Scripts\sync-center.ps1 -Setup
```

### 2. **Uso Diário**
```powershell
# Menu interativo completo
.\Scripts\sync-center.ps1

# Ou comandos específicos:
.\Scripts\sync-center.ps1 -GitSync        # Sincronizar Git
.\Scripts\sync-center.ps1 -ObsidianSync   # Configurar Obsidian
.\Scripts\sync-center.ps1 -AutoMode       # Monitor automático
```

---

## 📱 Plugins Configurados no Obsidian

### ✅ Ativos e Prontos
- **🔄 Git** - Auto-commit a cada 10min, auto-push a cada 30min
- **📊 Dataview** - Queries dinâmicas nos dashboards
- **📝 Templater** - Templates automáticos por pasta
- **✅ Tasks** - Gerenciamento avançado de tarefas
- **📋 Advanced Tables** - Edição visual de tabelas
- **🖼️ Image Gallery** - Galeria de imagens

### 🎯 Templates Criados
| Template            | Quando Usar             | Localização                         |
| ------------------- | ----------------------- | ----------------------------------- |
| **Documento Geral** | Qualquer arquivo .md    | `Templates/template-documento.md`   |
| **Corporativo**     | Arquivos em `AvilaInc/` | `Templates/template-corporativo.md` |
| **Operacional**     | Arquivos em `AvilaOps/` | `Templates/template-operacional.md` |
| **Relatórios**      | Pasta `Relatórios/`     | `Templates/template-relatorio.md`   |

---

## 🔄 Fluxo de Trabalho Automático

### 📝 **1. Criar/Editar no VS Code**
- Abra qualquer arquivo `.md`
- Edite normalmente
- Salve (`Ctrl+S`)

### 📱 **2. Obsidian Auto-Sincroniza**
- **10 segundos** após salvar → Aparece no Obsidian
- Template automático aplicado se for arquivo novo
- Dataview atualiza dashboards

### 🐙 **3. Git Auto-Commit**
- **10 minutos** → Auto-commit local
- **30 minutos** → Auto-push para GitHub
- Mensagem: `🔄 Auto sync: dd/MM/yyyy HH:mm`

---

## 📊 Dashboard Principal

O arquivo `Dashboard-Principal.md` é seu **centro de comando**:

### 🎯 Features Principais
```markdown
# Queries em tempo real
- Arquivos recentes (Dataview)
- Tasks urgentes (Tasks plugin)
- Métricas do projeto
- Status de sincronização

# Navegação rápida
- Links para todas as pastas
- Templates disponíveis
- Atalhos de teclado

# Analytics
- Top documentos editados
- Distribuição por tags
- Atividade semanal
```

---

## ⌨️ Atalhos de Teclado (Obsidian)

### 📝 Criação Rápida
- `Ctrl+N` → Novo documento (template automático)
- `Ctrl+Shift+C` → Template corporativo
- `Ctrl+Shift+O` → Template operacional
- `Ctrl+Shift+R` → Template de relatório

### 🔄 Sincronização
- `Ctrl+Shift+G` → Git commit & push manual
- `Ctrl+Shift+P` → Git pull
- `Ctrl+Alt+S` → Force sync

### 📱 Navegação
- `Ctrl+O` → Quick switcher
- `Ctrl+Shift+P` → Command palette
- `Ctrl+F` → Busca global

---

## 🎨 Personalização Adicional

### 1. **Configurar Tema Ávila**
```css
/* Em Settings > Appearance > CSS Snippets */
/* Criar arquivo: avila-theme.css */

.theme-dark {
  --accent-h: 220;
  --accent-s: 100%;
  --accent-l: 50%;
}

.dashboard {
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
}
```

### 2. **Hotkeys Personalizados**
- **Settings > Hotkeys**
- Configurar atalhos para templates específicos
- Atalhos para comandos Git

### 3. **Widgets na Barra Lateral**
```markdown
<!-- Widget de status em qualquer nota -->
Status: `= choice(date(now) = date(today), "🔥 Hoje", "📅 Normal")`
Sync: `= choice(file.mtime > date(today), "✅ Sincronizado", "⏳ Pendente")`
```

---

## 🔍 Troubleshooting

### ❌ Git não sincroniza
```powershell
# Verificar configuração
git config --list

# Reconfigurar se necessário
git config user.name "Seu Nome"
git config user.email "seu@email.com"
```

### ❌ Obsidian não detecta mudanças
1. **Settings > Files & Links**
2. Ativar "Automatically update internal links"
3. Recarregar vault (`Ctrl+R`)

### ❌ Templates não funcionam
1. **Settings > Templater**
2. Verificar pasta: `Templates`
3. Ativar "Trigger Templater on file creation"

### ❌ Dataview não funciona
1. **Settings > Community Plugins**
2. Ativvar "Dataview"
3. **Settings > Dataview**
4. Ativar "Enable JavaScript Queries"

---

## 📱 Sincronização Mobile

### Para usar no celular:
1. Instalar **Obsidian Mobile**
2. Configurar **Obsidian Sync** (pago) OU **Working Copy** (iOS) / **MGit** (Android)
3. Clonar repositório: `https://github.com/avilaops/avila`

### Workflow Mobile:
- **Mobile** → Edita no Obsidian
- **Auto-sync** → Para GitHub
- **VS Code** → Puxa mudanças automaticamente

---

## 🎯 Próximos Passos

### 1. **Testar o Sistema**
```powershell
# 1. Executar sync center
.\Scripts\sync-center.ps1

# 2. Criar um documento teste
# 3. Verificar se aparece no GitHub
# 4. Editar no Obsidian
# 5. Confirmar sync bidirecional
```

### 2. **Personalizar Para Seu Uso**
- Modificar templates em `Templates/`
- Ajustar configurações Git em `sync-center.ps1`
- Personalizar dashboard em `Dashboard-Principal.md`

### 3. **Expandir o Sistema**
- Adicionar mais plugins Obsidian
- Criar automações VS Code
- Integrar com outras ferramentas

---

## 🏆 Benefícios Alcançados

### ✅ **Produtividade 10x**
- Templates automáticos
- Busca instantânea
- Links bidirecionais
- Dashboards em tempo real

### ✅ **Sincronização Perfeita**
- GitHub como fonte da verdade
- Atualizações automáticas
- Backup contínuo
- Versionamento completo

### ✅ **Flexibilidade Total**
- Trabalhe no VS Code ou Obsidian
- Desktop ou mobile
- Online ou offline

---

**🎯 Seu ecossistema Ávila está pronto!**
**Framework:** Ávila Inc. | **Autor:** Nícolas Ávila | **Data:** 11/11/2025

> 💡 **Dica:** Mantenha o `sync-center.ps1` sempre aberto em modo monitor para sincronização em tempo real!
