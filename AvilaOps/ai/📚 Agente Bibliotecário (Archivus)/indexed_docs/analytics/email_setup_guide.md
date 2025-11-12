# 📧 Guia de Configuração de Email - Ávila Inc

## Passo 1: Escolha seu provedor de email

### ✅ Gmail (Recomendado)
1. Acesse https://myaccount.google.com/security
2. Ative "Verificação em duas etapas"
3. Acesse https://myaccount.google.com/apppasswords
4. Crie uma "App Password" chamada "Avila Dashboard"
5. Copie a senha de 16 caracteres gerada

### ✅ Outlook/Hotmail
- Use seu email e senha normal
- Não precisa de configuração adicional

### ✅ Office 365
- Use seu email corporativo e senha
- Pode precisar autorizar "aplicativos menos seguros"

## Passo 2: Configurar arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto com:

```env
# Para Gmail
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # App Password gerada
TO_EMAIL=destinatario@exemplo.com

# Para Outlook/Hotmail
# SMTP_HOST=smtp-mail.outlook.com
# SMTP_PORT=587
# SMTP_USER=seu-email@outlook.com
# SMTP_PASSWORD=sua-senha-normal
# TO_EMAIL=destinatario@exemplo.com

# Para Office 365
# SMTP_HOST=smtp.office365.com
# SMTP_PORT=587
# SMTP_USER=seu-email@empresa.com
# SMTP_PASSWORD=sua-senha-corporativa
# TO_EMAIL=destinatario@empresa.com
```

## Passo 3: Testar envio

```pwsh
# Teste básico (usa .env)
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py --send-email

# Ou especifique o destinatário
& "C:/Program Files/Python313/python.exe" analytics/reporting/generate_dashboard_email.py `
    --send-email `
    --to seu-email@exemplo.com
```

## Passo 4: Automatizar (Opcional)

### GitHub Actions
Adicione secrets no repositório:
- `SMTP_HOST`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `TO_EMAIL`

### Windows Task Scheduler
1. Abra "Agendador de Tarefas"
2. Crie nova tarefa básica
3. Configure para executar semanalmente
4. Ação: executar o script Python com `--send-email`

## Troubleshooting

### ❌ "Authentication failed"
- **Gmail**: Certifique-se de usar App Password, não sua senha normal
- **Outlook**: Verifique se 2FA não está bloqueando
- **Office365**: Pode precisar autorizar em admin.microsoft.com

### ❌ "Connection refused"
- Verifique se SMTP_HOST e SMTP_PORT estão corretos
- Confirme que sua rede não bloqueia porta 587

### ❌ "Email não chegou"
- Verifique pasta de spam
- Confirme que TO_EMAIL está correto
- Teste enviando para seu próprio email primeiro

## 🔒 Segurança

**NUNCA** commite o arquivo `.env` no git!

O arquivo `.gitignore` deve conter:
```
.env
*.env
```

Para compartilhar configuração com equipe, use `.env.example` (sem senhas reais).
