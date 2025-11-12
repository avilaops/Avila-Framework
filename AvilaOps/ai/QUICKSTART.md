# ?? GUIA DE INÍCIO RÁPIDO - AGENTE ARCHIVUS

## ? Instalação em 3 Passos

### 1?? Instalar Dependências Python

```powershell
# Navegar até a pasta do Archivus
cd "C:\Users\nicol\OneDrive\Avila\AvilaOps\Agente Bibliotecario (Archivus)"

# Instalar dependências
pip install pyyaml
```

### 2?? Configurar Agendamento Automático

```powershell
# Executar script de instalação (como Administrador)
.\Run-Archivus.ps1 -Install
```

**Resultado esperado:**
```
? Agendamento instalado com sucesso!
Próxima execução: Diariamente às 02:00
```

### 3?? Executar Primeira Vez (Teste)

```powershell
# Executar manualmente para testar
.\Run-Archivus.ps1 -RunNow
```

---

## ?? Comandos Disponíveis

### Executar Agora (Manual)
```powershell
.\Run-Archivus.ps1 -RunNow
```

### Ver Status
```powershell
.\Run-Archivus.ps1 -Status
```

### Reinstalar Agendamento
```powershell
.\Run-Archivus.ps1 -Install
```

### Remover Agendamento
```powershell
.\Run-Archivus.ps1 -Uninstall
```

### Menu Interativo
```powershell
.\Run-Archivus.ps1
```

---

## ?? O Que o Archivus Faz?

### ? Validação de Estrutura
Remove automaticamente:
- Pastas não-oficiais em `Docs\Relatorios\`
- Arquivos fora do padrão
- Duplicatas e lixo digital

### ?? Rotação de Logs
- Move logs >30 dias para `Logs\Archive\`
- Comprime logs antigos
- Mantém apenas 90 dias de histórico

### ?? Backup de Scripts
- Cria ZIP completo de `Scripts\`
- Salvo em `Shared\backups\archivus\`
- Mantém últimos 30 backups

### ?? Verificação de Integridade
- Calcula SHA256 de todos os scripts
- Compara com manifesto anterior
- Alerta se houver modificações

### ?? Relatórios Diários
- Gerado em `Docs\Relatorios\Auditorias\`
- Formato: `AUDITORIA_ARCHIVUS_YYYY-MM-DD.md`
- Contém métricas e ações executadas

---

## ?? Verificar Resultados

### Ver Último Log
```powershell
Get-Content "C:\Users\nicol\OneDrive\Avila\Logs\Daily\archivus_$(Get-Date -Format 'yyyy-MM-dd').log"
```

### Ver Último Relatório
```powershell
$reportPath = "C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Auditorias"
Get-ChildItem $reportPath -Filter "AUDITORIA_ARCHIVUS_*.md" | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 1 | 
    Get-Content
```

### Ver Backups Criados
```powershell
Get-ChildItem "C:\Users\nicol\OneDrive\Avila\Shared\backups\archivus" | 
    Sort-Object LastWriteTime -Descending
```

---

## ?? Configuração Avançada

### Alterar Horário de Execução

Edite `config.yaml`:

```yaml
scheduled_tasks:
  daily_cleanup:
    time: "03:00"  # Alterar de 02:00 para 03:00
```

Depois reinstale:
```powershell
.\Run-Archivus.ps1 -Install
```

### Alterar Retenção de Logs

Edite `config.yaml`:

```yaml
monitored_paths:
  logs:
    retention_days: 180  # Alterar de 90 para 180 dias
    archive_after_days: 60  # Alterar de 30 para 60 dias
```

### Adicionar Pasta Monitorada

Edite `config.yaml`:

```yaml
monitored_paths:
  nova_pasta:
    path: "MinhaPasta"
    actions:
    - index
      - backup
    retention_days: 365
```

---

## ?? Troubleshooting

### ? Erro: "Python não encontrado"
**Solução:**
```powershell
# Verificar se Python está instalado
python --version

# Se não estiver, baixar de: https://www.python.org/
```

### ? Erro: "Permissão negada"
**Solução:**
```powershell
# Executar PowerShell como Administrador
# Botão direito ? "Executar como Administrador"
```

### ? Erro: "Módulo yaml não encontrado"
**Solução:**
```powershell
pip install pyyaml
```

### ?? Aviso: "Hash divergente"
**Causa:** Script foi modificado  
**Ação:**
1. Verificar se modificação foi legítima
2. Se sim, executar novamente para atualizar manifesto
3. Se não, investigar possível comprometimento

---

## ?? Suporte

- **Documentação completa:** `README.md`
- **Configuração:** `config.yaml`
- **Logs:** `C:\Users\nicol\OneDrive\Avila\Logs\Daily\`
- **Relatórios:** `C:\Users\nicol\OneDrive\Avila\Docs\Relatorios\Auditorias\`

---

## ? Checklist de Instalação

- [ ] Python instalado e funcionando
- [ ] Dependências instaladas (`pip install pyyaml`)
- [ ] Script executado manualmente com sucesso
- [ ] Agendamento configurado
- [ ] Primeiro relatório gerado
- [ ] Logs sendo criados em `Logs\Daily\`
- [ ] Backups sendo salvos em `Shared\backups\archivus\`

---

**Pronto!** ?? O Agente Archivus está configurado e rodando!

**Próxima execução automática:** Amanhã às 02:00
