# Ávila Inc
Matriz institucional e estratégica. 
Abriga a governança, finanças, jurídico, marketing e documentação corporativa.

## 📧 Sistema de Relatórios Automatizados

### 🚀 Envio Único (Manual)

```pwsh
# Enviar relatório agora
.\send_report.ps1 -To "destinatario@exemplo.com"

# Ou com Python
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py --send-email
```

### 🤖 Envio Automático (Agendado)

#### Opção 1: Windows Task Scheduler
```pwsh
# Configurar agendamento local
.\setup_scheduler.ps1

# Escolha: 1=Diário | 2=Semanal | 3=Ambos
```

#### Opção 2: GitHub Actions (Recomendado)
1. Configure secrets no GitHub (SMTP_HOST, SMTP_USER, etc.)
2. Ative workflow em `Actions → Send Reports`
3. Pronto! Roda automaticamente

### 📊 Tipos de Relatório

| Tipo | Comando | Dados | Quando |
|------|---------|-------|--------|
| **Diário** | `python send_scheduled_report.py daily` | `data/daily_metrics.json` | SEG-SEX 8h |
| **Semanal** | `python send_scheduled_report.py weekly` | `data/dashboard_metrics.json` | SEG 9h |
| **Mensal** | `python send_scheduled_report.py monthly` | `data/monthly_metrics.json` | Dia 1, 10h |

### 🔧 Configuração Inicial

1. **Copie o template**:
   ```pwsh
   cp .env.template .env
   ```

2. **Edite `.env`** com suas credenciais SMTP

3. **Teste**:
   ```pwsh
   .\send_report.ps1
   ```

### 📖 Documentação Completa

- **Início Rápido**: `docs/analytics/QUICKSTART_AUTOMATION.md` ⚡
- **Setup Gmail**: `docs/analytics/GMAIL_SETUP.md`
- **Automação Completa**: `docs/analytics/automation_guide.md`
- **Configuração Email**: `docs/analytics/email_setup_guide.md`
- **Scripts**: `analytics/reporting/README.md`

### 🎯 Próximos Passos

1. ✅ Configure `.env` com credenciais
2. ✅ Teste envio manual
3. ⚙️ Configure agendamento (Windows ou GitHub)
4. 📊 Integre com dados reais (opcional)

**Dúvidas?** Consulte `SETUP_COMPLETO.md` ou `docs/analytics/`
