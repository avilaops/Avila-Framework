---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
modified: <% tp.date.now("YYYY-MM-DD") %>
tags: [avila, corporativo, avilaInc]
type: corporativo
department: <% tp.system.suggest("Departamento", ["Finance", "Legal", "Marketing", "Governance"]) %>
confidentiality: <% tp.system.suggest("Confidencialidade", ["Público", "Interno", "Confidencial", "Restrito"]) %>
---

# <% tp.file.title %>

## 🏢 Informações Corporativas

**Departamento:** <% tp.system.suggest("Departamento", ["Finance", "Legal", "Marketing", "Governance"]) %>
**Responsável:** <% tp.system.prompt("Nome do responsável") %>
**Aprovação:** <% tp.system.suggest("Nível de aprovação", ["Gerencial", "Diretoria", "C-Level"]) %>

---

## 📋 Resumo Executivo
<!-- Resumo de 2-3 parágrafos para executivos -->

## 🎯 Objetivos
<!-- Liste os objetivos principais -->

## 📊 Análise e Dados
<!-- Dados, métricas, análises -->

## 💼 Recomendações
<!-- Recomendações estratégicas -->

## 📈 Próximos Passos
<!-- Ações e cronograma -->

---

## 🔗 Links Relacionados
- [[Governance Framework]]
- [[Políticas Corporativas]]

## ✅ Action Items
<!-- Use - [ ] para tarefas -->
- [ ]

---

## 📋 Histórico de Versões
| Versão | Data                            | Autor                              | Alterações     |
| ------ | ------------------------------- | ---------------------------------- | -------------- |
| 1.0    | <% tp.date.now("DD/MM/YYYY") %> | <% tp.system.prompt("Seu nome") %> | Versão inicial |

---
> 🏢 **Template Corporativo ÁvilaInc** | Confidencialidade: <% tp.system.suggest("Confidencialidade", ["Público", "Interno", "Confidencial", "Restrito"]) %>
