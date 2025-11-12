---
title: "🚀 Dashboard Principal - Ávila Framework"
created: 2025-11-11
tags: [avila, dashboard, main]
cssclasses: [dashboard]
---

# 🚀 Dashboard Principal - Ávila Framework

> **Bem-vindo ao Centro de Comando do Ecossistema Ávila**
> Sincronizado entre **GitHub** ↔ **VS Code** ↔ **Obsidian**

---

## 📊 Visão Geral em Tempo Real

```dataview
TABLE
  choice(contains(tags, "corporativo"), "🏢", choice(contains(tags, "operacional"), "⚙️", "📄")) as "Tipo",
  file.name as "Documento",
  author as "Responsável",
  choice(file.mtime > date(today) - dur(1 day), "🔥 Hoje",
    choice(file.mtime > date(today) - dur(7 days), "📅 Esta Semana",
      "📋 Anterior")) as "Status"
FROM ""
WHERE tags
SORT file.mtime DESC
LIMIT 15
```

---

## 🎯 Action Center

### ⚡ Tasks Urgentes
```tasks
not done
priority is high
limit 10
```

### 📅 Agenda Hoje
```tasks
not done
scheduled today
```

### 🔄 Em Progresso
```tasks
not done
tags include #in-progress
```

---

## 📈 Métricas do Ecossistema

### 📊 Distribuição por Setor
```dataview
TABLE rows.length as "Quantidade"
FROM ""
WHERE tags
FLATTEN tags as tag
GROUP BY tag
WHERE contains(tag, "avila")
SORT rows.length DESC
LIMIT 8
```

### 📅 Atividade Recente (7 dias)
```dataview
TABLE
  dateformat(file.ctime, "dd/MM") as "Criado",
  dateformat(file.mtime, "dd/MM") as "Editado",
  file.name as "Arquivo"
FROM ""
WHERE file.ctime >= date(today) - dur(7 days) OR file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 12
```

---

## 🗂️ Navegação Rápida

### 🏢 ÁvilaInc (Corporativo)
- [[Governance Framework]] | [[Legal]] | [[Finance]] | [[Marketing]]

### ⚙️ ÁvilaOps (Operacional)
- [[AI & ML]] | [[DevOps]] | [[Infrastructure]] | [[Products]] | [[Research]]

### 📚 Documentação
- [[Templates]] | [[Relatórios]] | [[Instruções]] | [[Scripts]]

### 🔗 Links Essenciais
- [[GitHub Repository]] | [[VS Code Workspace]] | [[Setup Guide]]

---

## 📋 Centro de Templates

| Template                           | Uso             | Atalho         |
| ---------------------------------- | --------------- | -------------- |
| [[Templates/template-documento]]   | Documento geral | `Ctrl+T`       |
| [[Templates/template-corporativo]] | ÁvilaInc        | `Ctrl+Shift+C` |
| [[Templates/template-operacional]] | ÁvilaOps        | `Ctrl+Shift+O` |
| [[Templates/template-relatorio]]   | Relatórios      | `Ctrl+Shift+R` |

---

## 🔄 Status de Sincronização

### Git Status
```dataview
TABLE
  choice(contains(file.path, "AvilaInc"), "🏢 Corporativo",
    choice(contains(file.path, "AvilaOps"), "⚙️ Operacional",
      "📄 Documentação")) as "Setor",
  file.name as "Arquivo",
  dateformat(file.mtime, "HH:mm") as "Última Modificação"
FROM ""
WHERE file.mtime >= date(today)
SORT file.mtime DESC
LIMIT 10
```

### 🔄 Auto-Sync Status
> **Git Auto-Commit:** ✅ A cada 10 min
> **Auto-Push:** ✅ A cada 30 min
> **Auto-Pull:** ✅ A cada 10 min

---

## 📊 Analytics Rápido

### Top 5 Documentos Mais Editados
```dataview
TABLE file.name as "Documento", file.mtime as "Última Edição"
FROM ""
SORT file.mtime DESC
LIMIT 5
```

### Documentos por Tag
```dataview
TABLE rows.length as "Quantidade"
FROM ""
FLATTEN tags as tag
GROUP BY tag
SORT rows.length DESC
LIMIT 10
```

---

## 🚀 Quick Actions

### Criar Novo
- **Documento:** `Ctrl+N` → Selecionar template
- **Relatório:** `Ctrl+Shift+R`
- **Task:** `Ctrl+T`

### Sincronização
- **Commit & Push:** `Ctrl+Shift+G`
- **Pull Latest:** `Ctrl+Shift+P`
- **Force Sync:** `Ctrl+Alt+S`

### Navegação
- **Command Palette:** `Ctrl+Shift+P`
- **Quick Switcher:** `Ctrl+O`
- **Search:** `Ctrl+F`

---

## 🎨 Personalization

### Tema Atual
> **Ávila Dark Theme** - Otimizado para produtividade

### Plugins Ativos
✅ **Dataview** - Queries dinâmicas
✅ **Templater** - Templates automáticos
✅ **Tasks** - Gerenciamento de tarefas
✅ **Advanced Tables** - Edição de tabelas
✅ **Git** - Sincronização automática
✅ **Image Gallery** - Galeria de imagens

---

## 📱 Mobile & Desktop Sync

### Status de Dispositivos
- 💻 **Desktop (VS Code):** ✅ Conectado
- 📱 **Mobile (Obsidian):** ✅ Sincronizado
- ☁️ **Cloud (GitHub):** ✅ Atualizado

---

**🕐 Última atualização:** `= date(now)`
**📊 Total de documentos:** `= length(dv.pages())`
**🔄 Status do sistema:** 🟢 **Online & Sincronizado**

> 🎯 **Bem-vindo ao futuro da produtividade!** Este dashboard é atualizado automaticamente via Dataview e sincronizado entre todos os seus dispositivos.
