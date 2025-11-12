# ⚡ Início Rápido: Automação de Relatórios

## 🎯 Objetivo
Configurar envio automático de relatórios em **5 minutos**.

## 📋 Opções de Automação

### Opção A: Windows (Local) ⭐ Mais Fácil

**1. Execute o configurador:**
```pwsh
.\setup_scheduler.ps1
```

**2. Escolha o tipo:**
- `1` = Diário (SEG-SEX 8h)
- `2` = Semanal (SEG 9h)  
- `3` = Ambos

**3. Pronto!** 🎉

Os relatórios serão enviados automaticamente se o PC estiver ligado.

---

### Opção B: GitHub Actions (Nuvem) ☁️ Recomendado

**1. Configure Secrets:**
```
Settings → Secrets → New repository secret

Nome: SMTP_HOST     | Valor: smtp.porkbun.com
Nome: SMTP_PORT     | Valor: 587
Nome: SMTP_USER     | Valor: dev@avila.inc
Nome: SMTP_PASSWORD | Valor: sua-senha
Nome: TO_EMAIL      | Valor: nicolas@avila.inc
```

**2. Ative o workflow:**
- Vá em `Actions`
- Clique em "Send Reports"
- Botão "Enable workflow"

**3. Teste:**
- Clique "Run workflow"
- Escolha tipo: `semanal`
- "Run workflow"

**4. Pronto!** 🚀

Agora roda automaticamente toda semana.

---

## 🧪 Testar Antes de Agendar

### Teste rápido (sem enviar):
```pwsh
python send_scheduled_report.py weekly --dry-run
```

### Teste completo (envia email):
```pwsh
python send_scheduled_report.py weekly
```

---

## 📊 Atualizar Dados

### Dados atuais (exemplo):
```
data/dashboard_metrics.json  → Semanal
data/daily_metrics.json      → Diário
data/monthly_metrics.json    → Mensal (criar)
```

### Para usar dados reais:

**Opção 1: Manual**
Edite os JSONs antes do envio agendado.

**Opção 2: Script ETL**
```pwsh
# Rode antes do relatório
python scripts/fetch_from_db.py > data/dashboard_metrics.json
```

**Opção 3: API**
Configure webhook para atualizar automaticamente.

---

## ⏰ Horários Padrão

| Tipo | Quando | Destinatário |
|------|--------|--------------|
| **Diário** | SEG-SEX 8h | `DAILY_TO` ou `TO_EMAIL` |
| **Semanal** | SEG 9h | `nicolas@avila.inc` |
| **Mensal** | Dia 1, 10h | `MONTHLY_TO` |

Para mudar: edite `.env.reports` ou `.github/workflows/send-reports.yml`

---

## 🔧 Personalizar Destinatários

Edite `.env.reports`:
```env
DAILY_TO=operacoes@avila.inc
WEEKLY_TO=nicolas@avila.inc,board@avila.inc
MONTHLY_TO=investidores@avila.inc
```

---

## 📞 Suporte

**Não funciona?**
1. Teste manual: `.\send_report.ps1`
2. Veja logs: `docs/analytics/automation_guide.md`
3. Troubleshooting completo: `SETUP_COMPLETO.md`

**Dúvidas sobre configuração?**
- GitHub Actions: `docs/analytics/automation_guide.md`
- Windows Scheduler: `.github/workflows/send-reports.yml` (comentários)
