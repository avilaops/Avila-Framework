---
title: <% tp.file.title %>
created: <% tp.date.now("YYYY-MM-DD") %>
modified: <% tp.date.now("YYYY-MM-DD") %>
tags: [avila, docs]
author: Nícolas Ávila
framework: Ávila Inc.
version: 1.0
---

# <% tp.file.title %>

## Contexto
<!-- Descreva o contexto e objetivo deste documento -->

## Conteúdo Principal
<!-- Seu conteúdo aqui -->

---

## Metadados
- **Criado em:** <% tp.date.now("DD/MM/YYYY HH:mm") %>
- **Responsável:** <% tp.system.prompt("Responsável pelo documento") %>
- **Setor:** <% tp.system.suggest("Escolha o setor", ["AvilaInc", "AvilaOps", "Shared", "Scripts"]) %>
- **Status:** <% tp.system.suggest("Status", ["Rascunho", "Em Revisão", "Aprovado", "Arquivado"]) %>

## Links Relacionados
<!-- Use [[]] para criar links para documentos relacionados -->

## Tarefas
<!-- Use - [ ] para criar tarefas -->

---
> 📋 **Template Padrão Ávila** | Gerado automaticamente via Templater
