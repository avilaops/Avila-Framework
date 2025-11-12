# 🎯 Guia Rápido: Configurar Gmail em 5 Minutos

## Passo 1: Ativar Autenticação de 2 Fatores

1. Acesse: https://myaccount.google.com/security
2. Procure por "Verificação em duas etapas"
3. Clique em "Começar" e siga as instruções
4. Configure usando seu telefone

## Passo 2: Gerar App Password

1. Acesse: https://myaccount.google.com/apppasswords
2. No campo "Nome do app", digite: **Avila Dashboard**
3. Clique em "Criar"
4. **COPIE** a senha de 16 caracteres que aparece (formato: `xxxx xxxx xxxx xxxx`)

## Passo 3: Configurar .env

1. Copie o arquivo template:
   ```pwsh
   cp .env.template .env
   ```

2. Abra `.env` no editor e preencha:
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=seu-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Cole a App Password aqui
   TO_EMAIL=destinatario@exemplo.com  # Para quem enviar
   ```

3. Salve o arquivo

## Passo 4: Testar

Execute no terminal (PowerShell):

```pwsh
.\send_report.ps1 -To "seu-proprio-email@gmail.com"
```

Se tudo der certo, você verá:
```
✅ Relatório enviado com sucesso!
```

E receberá o email em alguns segundos!

## 🆘 Problemas Comuns

### ❌ "Username and Password not accepted"
- Certifique-se de usar a **App Password**, não sua senha normal do Gmail
- A App Password tem 16 caracteres sem espaços
- Copie e cole diretamente do Google

### ❌ "Application-specific password required"
- Você precisa ativar autenticação de 2 fatores primeiro (Passo 1)
- Só depois consegue gerar App Passwords

### ❌ "Email não chegou"
- Verifique a pasta de SPAM
- Confirme que TO_EMAIL está correto
- Teste enviando para seu próprio email primeiro

## 🔄 Próximos Passos

Depois de configurar, você pode:

1. **Automatizar envios semanais** (veja `docs/analytics/dashboard_email_automation.md`)
2. **Personalizar o template HTML** (`marketing/templates/email/dashboard_report.html`)
3. **Adicionar mais destinatários** (envie para vários emails separados por vírgula)

## 🔐 Segurança

**IMPORTANTE**: 
- ✅ O arquivo `.env` está no `.gitignore` (não será commitado)
- ✅ Nunca compartilhe sua App Password
- ✅ Se comprometer, revogue em https://myaccount.google.com/apppasswords
