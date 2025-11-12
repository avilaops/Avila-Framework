# Geração de relatório executivo (dashboard email)

## Requisitos
- Python 3.13+ (`C:/Program Files/Python313/python.exe` já configurado)
- Dados agregados em `data/dashboard_metrics.json`, `data/dashboard_alerts.json`, `data/dashboard_actions.json`
- **Para envio de email**: credenciais SMTP (Gmail, Outlook, Office365)

## Como executar

### Gerar relatórios (sem enviar)
```pwsh
# do diretório raiz do repositório
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py
```

### Gerar E ENVIAR email
```pwsh
# Configurar variáveis de ambiente primeiro (copie .env.example para .env e preencha)
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --send-email `
    --to destinatario@exemplo.com

# Ou passar credenciais diretamente
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --send-email `
    --to destinatario@exemplo.com `
    --from-email seu-email@gmail.com `
    --smtp-host smtp.gmail.com `
    --smtp-port 587 `
    --smtp-user seu-email@gmail.com `
    --smtp-password "sua-senha-app"
```

## Configuração SMTP

### Gmail
1. Ative autenticação de 2 fatores na sua conta Google
2. Gere uma "App Password" em https://myaccount.google.com/apppasswords
3. Use `smtp.gmail.com` porta `587`

### Outlook/Hotmail
- Host: `smtp-mail.outlook.com`
- Porta: `587`
- Use seu email e senha normal

### Office 365
- Host: `smtp.office365.com`
- Porta: `587`

## Variáveis de ambiente (.env)
Crie um arquivo `.env` na raiz do projeto (veja `.env.example`):
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-app-password
TO_EMAIL=destinatario@exemplo.com
```

Parâmetros opcionais:
```pwsh
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --metrics .\data\dashboard_metrics.json `
    --alerts .\data\dashboard_alerts.json `
    --actions .\data\dashboard_actions.json `
    --template .\marketing\templates\email\dashboard_report.md `
    --html-template .\marketing\templates\email\dashboard_report.html `
    --output .\out\executive_email.md `
    --html-output .\out\executive_email.html `
    --skip-html  # usar se quiser pular renderização HTML
```

## Saídas
- `out/executive_email.md`: arquivo Markdown com front-matter preservado e corpo preenchido
- `out/executive_email.html`: versão HTML com cabeçalho/branding padrão Ávila
- Caminhos finais são exibidos no console para facilitar revisão

## Integração sugerida
1. Job semanal (GitHub Actions ou tarefa agendada) para gerar datasets JSON.
2. Executar script após ingestão (produz Markdown + HTML automaticamente).
3. Enviar e-mail via API (Mailgun, SES, Microsoft Graph) usando o conteúdo gerado.
4. Registrar envio e anexar link dos dashboards (`https://intranet.avila/dashboard`).

## Privacidade & auditoria
- Apenas métricas agregadas; sem PII.
- Validar se coortes ≥ 20 antes de publicar.
- Manter logs de execução e artefatos em storage seguro.
