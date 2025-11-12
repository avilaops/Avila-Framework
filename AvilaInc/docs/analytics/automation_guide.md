# 🤖 Guia de Automação de Relatórios

## Visão Geral

Sistema completo de automação para envio de relatórios em três níveis:
- **Diário**: Operacional (SEG-SEX, 8h)
- **Semanal**: Executivo (SEG, 9h)
- **Mensal**: Estratégico (1º dia do mês, 10h)

## 🚀 Setup Rápido

### 1. Configuração Local (Windows Task Scheduler)

```pwsh
# Execute o script de configuração
.\setup_scheduler.ps1

# Escolha:
# 1 = Apenas diário
# 2 = Apenas semanal
# 3 = Ambos
# 4 = Personalizado
```

### 2. Configuração GitHub Actions (Nuvem)

1. **Configure Secrets no GitHub**:
   - Vá em: `Settings → Secrets and variables → Actions`
   - Adicione os secrets:
     ```
     SMTP_HOST = smtp.porkbun.com
     SMTP_PORT = 587
     SMTP_USER = dev@avila.inc
     SMTP_PASSWORD = sua-senha
     TO_EMAIL = nicolas@avila.inc
     ```

2. **Ative o Workflow**:
   - Vá em: `Actions → Send Reports`
   - Clique em "Enable workflow"

3. **Teste manual**:
   - Em Actions, clique em "Run workflow"
   - Escolha tipo de relatório
   - Confirme

## 📋 Tipos de Relatório

### Diário (Operacional)
- **Quando**: Segunda a Sexta, 8h
- **Para quem**: Time de operações
- **Conteúdo**: Métricas do dia anterior
- **Dados**: `data/daily_metrics.json`

### Semanal (Executivo)
- **Quando**: Segundas, 9h
- **Para quem**: Liderança executiva
- **Conteúdo**: KPIs consolidados da semana
- **Dados**: `data/dashboard_metrics.json`

### Mensal (Estratégico)
- **Quando**: Dia 1 de cada mês, 10h
- **Para quem**: Board/Investidores
- **Conteúdo**: Análise estratégica do mês
- **Dados**: `data/monthly_metrics.json`

## 🔧 Personalização

### Adicionar Novo Tipo de Relatório

1. **Crie template HTML**:
   ```
   marketing/templates/email/custom_report.html
   ```

2. **Configure em `.env.reports`**:
   ```env
   CUSTOM_METRICS=data/custom_metrics.json
   CUSTOM_TEMPLATE=marketing/templates/email/custom_report.html
   CUSTOM_SUBJECT=Meu Relatório Custom
   CUSTOM_TO=destinatario@exemplo.com
   ```

3. **Adicione ao `send_scheduled_report.py`**:
   ```python
   "custom": {
       "metrics": os.getenv("CUSTOM_METRICS"),
       # ... etc
   }
   ```

### Ajustar Horários

**GitHub Actions** (`.github/workflows/send-reports.yml`):
```yaml
schedule:
  - cron: '0 11 * * *'  # Todo dia 11h UTC (8h Brasília)
```

**Windows Task Scheduler**:
```pwsh
# Edite setup_scheduler.ps1 e ajuste linha:
$trigger = New-ScheduledTaskTrigger -Daily -At "11:00"
```

## 🧪 Testes

### Teste Local (sem enviar)
```pwsh
python send_scheduled_report.py weekly --dry-run
```

### Teste Completo (envia email)
```pwsh
python send_scheduled_report.py weekly
```

### Teste GitHub Actions
1. Vá em `Actions → Send Reports`
2. Clique `Run workflow`
3. Escolha `report_type: semanal`
4. Confirme

## 📊 Integração com Dados Reais

### Opção 1: ETL Manual
Crie script que atualiza JSONs:
```pwsh
# Exemplo: atualiza_dados.ps1
python scripts/fetch_from_database.py > data/dashboard_metrics.json
```

### Opção 2: API/Webhook
Configure webhook que atualiza dados quando houver mudança:
```python
# api/webhook_receiver.py
@app.post("/update-metrics")
def update_metrics(data: dict):
    with open("data/dashboard_metrics.json", "w") as f:
        json.dump(data, f)
```

### Opção 3: BI Integration
Conecte com Power BI / Tableau:
```python
# scripts/fetch_from_powerbi.py
from powerbi import PowerBIClient
client = PowerBIClient(token)
data = client.get_report_data("dashboard-id")
# Salva em data/
```

## 🔍 Monitoramento

### Logs GitHub Actions
- Vá em `Actions → Workflow runs`
- Clique no run para ver logs
- Download artefatos (MD/HTML gerados)

### Logs Windows
```pwsh
# Ver histórico de tarefas
Get-ScheduledTask -TaskName "Avila-*" | Get-ScheduledTaskInfo

# Ver log de eventos
Get-EventLog -LogName Application -Source "Task Scheduler" -Newest 10
```

### Alertas de Falha
Configure notificação quando workflow falhar:
```yaml
# .github/workflows/send-reports.yml
- name: Notificar falha
  if: failure()
  uses: actions/setup-node@v3
  # Envie email/Slack/etc
```

## 🛠️ Troubleshooting

### ❌ "Tarefa não executa no horário"
- Verifique se computador está ligado
- Windows: Marque "Executar quando disponível"
- GitHub: Verifique timezone (UTC vs local)

### ❌ "Dados desatualizados"
- Configure script de ETL antes do envio
- Valide timestamp dos JSONs

### ❌ "Email não chega"
- Verifique secrets no GitHub
- Confirme `.env` local está correto
- Teste com `send_report.ps1` primeiro

## 📅 Roadmap

- [ ] Integração com banco de dados
- [ ] Dashboard web para visualizar histórico
- [ ] Multi-destinatário (CC/BCC)
- [ ] Anexos (PDFs, CSVs)
- [ ] Notificações Slack/Teams
- [ ] A/B testing de templates
