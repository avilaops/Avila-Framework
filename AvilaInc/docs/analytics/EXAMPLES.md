# 📚 Exemplos Práticos de Uso

## Casos de Uso Comuns

### 1️⃣ Enviar Relatório Agora (Ad-hoc)

```pwsh
# Método mais simples
.\send_report.ps1

# Com destinatário específico
.\send_report.ps1 -To "cliente@empresa.com"

# Com assunto customizado
.\send_report.ps1 -To "board@avila.inc" -Subject "Reunião de Board - Métricas Q4"
```

### 2️⃣ Agendar Relatórios Recorrentes

#### Windows (computador ligado)
```pwsh
# Configurar agendamento interativo
.\setup_scheduler.ps1

# Resultado: emails enviados automaticamente mesmo se você não estiver no PC
```

#### GitHub Actions (sempre funciona)
```yaml
# Já configurado em .github/workflows/send-reports.yml
# Basta ativar em: Settings → Actions → General → Enable
```

### 3️⃣ Múltiplos Destinatários

```pwsh
# Edite .env e adicione múltiplos emails separados por vírgula
# Nota: implementação atual suporta 1 destinatário
# Para múltiplos, rode script várias vezes ou customize o código
```

Solução temporária:
```pwsh
$destinatarios = @("joao@avila.inc", "maria@avila.inc", "pedro@avila.inc")
foreach ($email in $destinatarios) {
    .\send_report.ps1 -To $email
    Start-Sleep -Seconds 2  # Evita rate limiting
}
```

### 4️⃣ Diferentes Relatórios para Diferentes Pessoas

```pwsh
# Diário para operações
& "C:/Program Files/Python313/python.exe" send_scheduled_report.py daily

# Semanal para executivos
& "C:/Program Files/Python313/python.exe" send_scheduled_report.py weekly

# Configure destinatários em .env.reports:
# DAILY_TO=operacoes@avila.inc
# WEEKLY_TO=nicolas@avila.inc
```

### 5️⃣ Integrar com Pipeline de Dados

```pwsh
# 1. Atualizar dados
python scripts/etl_dashboard.py

# 2. Validar qualidade
python scripts/validate_metrics.py

# 3. Enviar relatório
.\send_report.ps1

# Automatize tudo:
# .\pipeline_completo.ps1
```

### 6️⃣ Teste Antes de Enviar

```pwsh
# Gera arquivos mas NÃO envia
& "C:/Program Files/Python313/python.exe" send_scheduled_report.py weekly --dry-run

# Verifique os arquivos:
# out/weekly_email.html  (abra no navegador)
# out/weekly_email.md    (revise conteúdo)

# Se OK, envie:
.\send_report.ps1
```

### 7️⃣ Envio Condicional (baseado em métricas)

```pwsh
# Envie apenas se métricas estiverem ruins
$metrics = Get-Content data/dashboard_metrics.json | ConvertFrom-Json
if ($metrics.csat -lt 85) {
    .\send_report.ps1 -To "urgente@avila.inc" -Subject "ALERTA: CSAT abaixo de 85%"
}
```

### 8️⃣ Relatório de Fim de Mês

```pwsh
# Rode no último dia do mês
$hoje = Get-Date
$ultimoDia = (Get-Date -Day 1).AddMonths(1).AddDays(-1)

if ($hoje.Day -eq $ultimoDia.Day) {
    # Gere métricas mensais
    python scripts/consolidate_monthly.py
    
    # Envie relatório
    & "C:/Program Files/Python313/python.exe" send_scheduled_report.py monthly
}
```

### 9️⃣ Relatórios A/B (testar templates)

```pwsh
# Template A (atual)
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --send-email `
    --to "teste-a@avila.inc" `
    --html-template marketing/templates/email/dashboard_report.html

# Template B (novo)
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --send-email `
    --to "teste-b@avila.inc" `
    --html-template marketing/templates/email/dashboard_report_v2.html
```

### 🔟 Debug de Problemas

```pwsh
# Ativar modo verbose
$env:DEBUG = "true"

# Ver configuração SMTP
Get-Content .env

# Testar conectividade SMTP
Test-NetConnection smtp.porkbun.com -Port 587

# Verificar logs do agendador
Get-ScheduledTask -TaskName "Avila-*" | Get-ScheduledTaskInfo
```

## 🎯 Workflows Completos

### Workflow 1: Setup Inicial

```pwsh
# 1. Clone repositório
git clone https://github.com/avilaops/Avila-Framework
cd AvilaInc

# 2. Configure email
cp .env.template .env
notepad .env  # Preencha credenciais

# 3. Teste envio
.\send_report.ps1 -To "seu-email@exemplo.com"

# 4. Configure automação
.\setup_scheduler.ps1  # Windows
# OU configure GitHub Actions secrets

# 5. Pronto! ✅
```

### Workflow 2: Atualização Diária

```pwsh
# Executado automaticamente pelo agendador:

# 7h55: ETL atualiza dados
python scripts/fetch_metrics.py > data/daily_metrics.json

# 8h00: Envia relatório
python send_scheduled_report.py daily
```

### Workflow 3: Reunião de Board

```pwsh
# Semana antes da reunião:
# 1. Consolide dados do mês
python scripts/monthly_report.py

# 2. Gere preview
python send_scheduled_report.py monthly --dry-run

# 3. Revise HTML
start out/monthly_email.html

# 4. Ajuste conforme necessário
notepad data/monthly_metrics.json

# 5. Re-gere
python send_scheduled_report.py monthly --dry-run

# 6. Envie para board
python send_scheduled_report.py monthly
```

## 💡 Dicas Pro

### Tip 1: Use Aliases
```pwsh
# Adicione ao seu $PROFILE
Set-Alias -Name relatorio -Value "C:\path\to\send_report.ps1"

# Agora pode usar:
relatorio -To "cliente@empresa.com"
```

### Tip 2: Notificações
```pwsh
# Adicione ao final do send_report.ps1:
if ($LASTEXITCODE -eq 0) {
    # Windows Toast
    New-BurntToastNotification -Text "Relatório enviado com sucesso!"
}
```

### Tip 3: Logs Persistentes
```pwsh
# Salve histórico de envios
.\send_report.ps1 | Tee-Object -FilePath "logs/envios.log" -Append
```

### Tip 4: Validação de Dados
```python
# Antes de enviar, valide qualidade dos dados
# scripts/validate_metrics.py
import json
metrics = json.load(open("data/dashboard_metrics.json"))
assert metrics["csat"] >= 0 and metrics["csat"] <= 100
assert metrics["periodo"] != "semana não informada"
# ... etc
```
