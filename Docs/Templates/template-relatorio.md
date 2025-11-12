---
title: "Relatório <% tp.system.prompt('Tipo de relatório (ex: Diário, Semanal, Mensal)') %> - <% tp.date.now('DD/MM/YYYY') %>"
created: <% tp.date.now("YYYY-MM-DD") %>
report_date: <% tp.date.now("YYYY-MM-DD") %>
report_type: <% tp.system.suggest("Tipo", ["Diário", "Semanal", "Mensal", "Trimestral", "Anual"]) %>
tags: [avila, relatorio, <% tp.date.now("YYYY-MM") %>]
author: <% tp.system.prompt("Responsável pelo relatório") %>
---

# 📊 Relatório <% tp.system.suggest("Tipo", ["Diário", "Semanal", "Mensal", "Trimestral", "Anual"]) %> - <% tp.date.now("DD/MM/YYYY") %>

## 📋 Resumo Executivo
<!-- Resumo de 2-3 parágrafos dos principais pontos -->

---

## 📈 Métricas Principais

### 🏢 ÁvilaInc (Corporativo)
- **Receita:**
- **Custos:**
- **Lucro:**
- **Clientes Ativos:**

### ⚙️ ÁvilaOps (Operacional)
- **Uptime:**
- **Performance:**
- **Deploys:**
- **Incidentes:**

---

## 🎯 Objetivos vs Realizações

### ✅ Concluído
```dataview
TASK
FROM "AvilaInc" OR "AvilaOps"
WHERE completed = true AND file.ctime >= date(<% tp.date.now("YYYY-MM-DD", -7) %>)
```

### 🔄 Em Progresso
```dataview
TASK
FROM "AvilaInc" OR "AvilaOps"
WHERE !completed
```

### ❌ Pendências Críticas
- [ ]

---

## 📊 Dashboards

### Dataview - Arquivos Recentes
```dataview
TABLE file.ctime as "Criado", file.mtime as "Modificado"
FROM ""
WHERE file.ctime >= date(<% tp.date.now("YYYY-MM-DD", -7) %>)
SORT file.ctime DESC
LIMIT 10
```

### Dataview - Status por Setor
```dataview
TABLE tags, author, modified
FROM ""
WHERE contains(tags, "avila")
GROUP BY tags[0]
```

---

## 🔍 Análise Detalhada

### 🏢 ÁvilaInc
<!-- Análise do setor corporativo -->

### ⚙️ ÁvilaOps
<!-- Análise do setor operacional -->

### 📁 Gestão Documental
- **Novos Documentos:**
- **Atualizações:**
- **Arquivamentos:**

---

## ⚠️ Alertas e Riscos

### 🚨 Crítico
-

### ⚡ Alto
-

### 🔶 Médio
-

---

## 🎯 Próximos Passos

### Esta Semana
- [ ]

### Próximo Período
- [ ]

### Longo Prazo
- [ ]

---

## 📎 Anexos e Links
- [[Relatório Anterior]]
- [[Métricas Dashboard]]
- [[Action Items]]

---

## 👥 Participantes
| Nome | Setor | Contribuição |
| ---- | ----- | ------------ |
|      |       |              |

---

**Relatório gerado em:** <% tp.date.now("DD/MM/YYYY HH:mm") %>
**Próximo relatório:** <% tp.date.now("DD/MM/YYYY", +7) %>
**Status:** 🔄 Em Progresso

> 📊 **Template de Relatório Ávila** | Automação via Templater + Dataview
