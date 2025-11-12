# ?? Conversas GitHub Copilot - Projeto Ávila

**Última atualização:** 2025-11-10
**IDE:** Visual Studio 2022

---

## ?? Sobre Esta Pasta

Armazena exportações de conversas importantes do GitHub Copilot Chat no Visual Studio 2022, preservando:
- Análises técnicas
- Decisões arquiteturais
- Resoluções de problemas
- Sessões de brainstorming
- Orientações de desenvolvimento

---

## ?? Como Exportar Conversas no Visual Studio 2022

### Método 1: Copiar do Chat Window (Recomendado)

1. **Abrir GitHub Copilot Chat:**
   - `Ctrl + /` ou
   - Menu: **View** ? **GitHub Copilot Chat**

2. **Selecionar conversa completa:**
   ```
   - Clique no início da conversa
   - Scroll até o final
   - Shift + Click no final
   - Ctrl + C (copiar)
   ```

3. **Salvar usando script:**
   ```powershell
   # O conteúdo já está no clipboard
   python Shared/scripts/salvar_conversa_copilot.py --clipboard
   ```

### Método 2: Export Manual do Chat

**Visual Studio 2022 não tem botão "Export Chat" nativo**. Use:

```powershell
# 1. Copiar conversa completa (Ctrl+A, Ctrl+C no Chat Window)
# 2. Executar:
python Shared/scripts/salvar_conversa_copilot.py --clipboard

# OU criar arquivo manualmente:
Get-Clipboard | Out-File -FilePath "Docs/Relatorios/Conversas/CONVERSA_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').md" -Encoding UTF8
```

### Método 3: Screenshot do Chat Window

Para capturas visuais:
```powershell
# Windows Snipping Tool
Win + Shift + S

# Salvar em:
Docs/Relatorios/Conversas/Capturas/TEMA_$(Get-Date -Format 'yyyy-MM-dd').png
```

### Método 4: Output Window Logs

Se a conversa gerou outputs relevantes:
```powershell
# No Visual Studio 2022:
# View ? Output ? Selecionar "GitHub Copilot Chat" no dropdown
# Copiar conteúdo ? Salvar
```

---

## ?? Padrão de Nomenclatura

```
CONVERSA_COPILOT_vDATA_HORA.extensao
CONVERSA_MANUAL_TEMA_vDATA.md
CAPTURA_TEMA_DATA.png
```

**Exemplos Visual Studio 2022:**
```
? CONVERSA_VS2022_v2025-11-10_143022.md
? CONVERSA_MANUAL_REFACTORING_v2025-11-10.md
? CAPTURA_CHAT_ARQUITETURA_2025-11-10.png
? conversa.md (sem padrão)
```

---

## ?? Conversas Disponíveis

*(Será atualizado conforme conversas forem salvas)*

| Data | Arquivo | Tema | IDE | Tamanho |
|------|---------|------|-----|---------|
| 2025-11-10 | *Nenhuma ainda* | - | VS 2022 | - |

---

## ?? Quando Salvar uma Conversa?

Salve quando a conversa incluir:

- ? **Análises técnicas** importantes
- ? **Decisões arquiteturais** documentadas
- ? **Resoluções de bugs** complexos
- ? **Orientações de implementação**
- ? **Discussões de design patterns**
- ? **Planejamento de features**
- ? **Troubleshooting** de produção

Não precisa salvar:
- ? Perguntas triviais
- ? Testes rápidos
- ? Debugging simples
- ? Conversas duplicadas

---

## ?? Estrutura de Subpastas

```
Conversas/
??? Analises/          # Conversas sobre análises
??? Arquitetura/       # Decisões arquiteturais
??? Implementacao/     # Orientações de código
??? Troubleshooting/   # Resolução de problemas
??? Planejamento/      # Roadmaps e features
??? Capturas/          # Screenshots do VS 2022
??? OutputLogs/        # Logs do Output Window (novo)
```

---

## ?? Governança

### Retenção:
- **Conversas Técnicas:** 1 ano
- **Decisões Arquiteturais:** 2 anos
- **Capturas:** 6 meses

### Versionamento:
- Conversas não são versionadas (imutáveis)
- Data no nome do arquivo identifica versão temporal

### Privacidade:
- ?? **NÃO** salvar conversas com:
  - API Keys
  - Senhas
  - Dados pessoais sensíveis
  - Informações confidenciais

---

## ?? Scripts Disponíveis

| Script | Uso | IDE |
|--------|-----|-----|
| `salvar_conversa_copilot.py` | Salva do clipboard ou arquivo | VS 2022 |
| `salvar_conversa_copilot.py --clipboard` | Direto do clipboard do Windows | VS 2022 |
| `indexar_conversas.py` | Atualiza índice (futuro) | Qualquer |

---

## ?? Dicas Visual Studio 2022

### Atalhos Úteis:
```
Ctrl + /          ? Abrir/Fechar Copilot Chat
Ctrl + A          ? Selecionar tudo no Chat
Ctrl + C          ? Copiar conversa
Ctrl + Shift + V  ? Colar sem formatação
```

### Buscar em Conversas:
```powershell
# Buscar por palavra-chave
Get-ChildItem -Path "Docs/Relatorios/Conversas" -Filter "*.md" -Recurse | Select-String -Pattern "refactoring"
```

### Listar Conversas Recentes:
```powershell
Get-ChildItem -Path "Docs/Relatorios/Conversas" -Filter "*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 10
```

### Salvar Output Window:
```powershell
# 1. No VS 2022: View ? Output
# 2. Dropdown ? GitHub Copilot Chat
# 3. Copiar conteúdo
# 4. Executar:
python Shared/scripts/salvar_conversa_copilot.py --clipboard --tipo outputlog
```

### Estatísticas:
```powershell
# Total de conversas
(Get-ChildItem -Path "Docs/Relatorios/Conversas" -Filter "*.md").Count

# Tamanho total
(Get-ChildItem -Path "Docs/Relatorios/Conversas" -Filter "*.md" | Measure-Object -Property Length -Sum).Sum / 1MB
```

---

## ?? Configuração Visual Studio 2022

### Habilitar GitHub Copilot Chat:
1. **Extensions** ? **Manage Extensions**
2. Procurar: **"GitHub Copilot"**
3. Instalar/Atualizar para versão mais recente
4. Reiniciar Visual Studio

### Verificar se está ativo:
```
Menu: View ? GitHub Copilot Chat (deve estar disponível)
```

---

## ?? Suporte

Para dúvidas:
- **README Principal:** `Docs/Relatorios/README.md`
- **Script:** `Shared/scripts/salvar_conversa_copilot.py`
- **Governança:** `AvilaInc/governance_framework/procedimentos/`
- **Visual Studio Docs:** https://learn.microsoft.com/visualstudio/ide/github-copilot

---

**Gerado por:** Ávila Ops - Governança  
**Data:** 2025-11-10  
**Versão:** 2.0 (Visual Studio 2022)
**IDE:** Visual Studio 2022
