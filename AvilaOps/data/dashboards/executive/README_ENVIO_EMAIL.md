# 🚀 **ENVIO AUTOMÁTICO - PLANO GLOBAL ÁVILA**

## 📧 **Como Funciona**

### **100% Automatizado - Zero Interação**
✅ Lê configurações do `.env`  
✅ Usa templates HTML premium prontos  
✅ Anexa documentos automaticamente  
✅ Envia sem perguntar nada no console  

---

## 🎯 **Scripts Disponíveis**

### **1. `enviar_plano.py` - ENVIO AUTOMÁTICO** ⭐
```bash
python enviar_plano.py
```

**O que faz:**
- ✅ Envia email automaticamente (SEM perguntas)
- ✅ Template HTML premium com gradientes
- ✅ Anexa PLANO_ACAO_10_SOLUCOES_GLOBAIS.md (60 páginas)
- ✅ Anexa RESUMO_EXECUTIVO_PLANO_GLOBAL.md (1 página)
- ✅ Múltiplos destinatários do .env
- ✅ Log completo do envio

**Resultado:**
```
🚀 ENVIO AUTOMÁTICO - PLANO DE AÇÃO GLOBAL ÁVILA
⏰ Timestamp: 2025-11-12 00:30:45
📧 Remetente: reports@avilaops.com
📬 Destinatários: nicolas@avilaops.com

✅ Plano anexado: PLANO_ACAO_10_SOLUCOES_GLOBAIS.md
✅ Resumo anexado: RESUMO_EXECUTIVO_PLANO_GLOBAL.md

📤 Enviando email...

✅ EMAIL ENVIADO COM SUCESSO!

📬 Destinatários que receberam:
   ✓ nicolas@avilaops.com

📎 Anexos enviados:
   • PLANO_ACAO_10_SOLUCOES_GLOBAIS.md (60 páginas)
   • RESUMO_EXECUTIVO_PLANO_GLOBAL.md (1 página)

🌍 Agora é só orquestrar a equipe e mudar o mundo!
```

---

### **2. `preview_email.py` - VER SEM ENVIAR** 👀
```bash
python preview_email.py
```

**O que faz:**
- ✅ Gera HTML local (não envia email)
- ✅ Abre automaticamente no navegador
- ✅ Salva em `output/email_plano_global_preview_[timestamp].html`
- ✅ Perfeito para testar o design

---

## ⚙️ **Configuração (.env)**

### **Arquivo: `.env` (na raiz do projeto)**

```env
# Email Configuration
SENDER_EMAIL=reports@avilaops.com
SENDER_PASSWORD=sua_senha_app_gmail_aqui
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Recipients
EXECUTIVE_RECIPIENTS=nicolas@avilaops.com,outro@email.com
TEAM_RECIPIENTS=equipe@avilaops.com
CLIENT_RECIPIENTS=cliente@empresa.com

# Company Info
COMPANY_NAME=Ávila Inc.
WORKSPACE_PATH=C:\Users\nicol\OneDrive\Avila\AvilaOps

# Features
ENABLE_CHARTS=true
ENABLE_AI_INSIGHTS=true
TIMEZONE=America/Sao_Paulo
```

### **⚠️ IMPORTANTE: Senha de App do Gmail**

Para Gmail, use **senha de app** (não a senha normal):

1. Acesse: https://myaccount.google.com/apppasswords
2. Crie senha para "Mail" (escolha "Other")
3. Cole a senha gerada no `.env`

---

## 📁 **Estrutura de Arquivos**

```
data/dashboards/executive/
├── enviar_plano.py              ⭐ PRINCIPAL - Envio automático
├── preview_email.py              👀 Preview sem enviar
├── config_manager.py             ⚙️ Gerenciador de configuração
├── email_templates.py            📧 Templates HTML (backup)
├── .env                          🔐 Configurações (criar na raiz)
└── output/
    └── email_plano_global_preview_*.html

docs/
├── PLANO_ACAO_10_SOLUCOES_GLOBAIS.md      📄 60 páginas
├── RESUMO_EXECUTIVO_PLANO_GLOBAL.md       📄 1 página
└── ENTREGA_COMPLETA_PLANO_GLOBAL.md       📄 Sumário da entrega
```

---

## 🎨 **Design do Email**

### **Características:**
- ✅ **Gradientes modernos** (roxo/azul)
- ✅ **Responsivo** (mobile + desktop)
- ✅ **Cards com hover** effects
- ✅ **Estatísticas visuais** (10 soluções, 200k vidas, etc.)
- ✅ **Apresentação da equipe** (humanos + 9 agentes IA)
- ✅ **Preview das 10 soluções**
- ✅ **Call-to-action** destacado
- ✅ **Footer com assinaturas**

### **Preview:**
```
┌─────────────────────────────────────┐
│ 🌍 Plano de Ação Global             │ ← Hero com gradiente
│ 10 Soluções que Vão Mudar o Mundo  │
└─────────────────────────────────────┘

┌──────┬──────┬──────┬──────┐
│  10  │200k+ │  18  │$213k │          ← Stats cards
│Soluç.│Vidas │Meses │Budget│
└──────┴──────┴──────┴──────┘

🤖 Quem Sou Eu & Minha Equipe          ← Team cards
┌─────────────────────────────────┐
│ 👤 Nícolas Ávila - Diretor      │
│ 🤖 GitHub Copilot - Orquestrador│
│ 🧭 9 Agentes Especializados     │
└─────────────────────────────────┘

🎯 As 10 Soluções                      ← Solutions list
1. 🏥 Triagem Médica IA
2. 💰 SMS Financeiro
...

🚀 Próximos Passos                     ← CTA box
```

---

## ✅ **Checklist de Uso**

### **Antes de Enviar:**
- [ ] `.env` configurado com credenciais
- [ ] `SENDER_PASSWORD` é senha de app (Gmail)
- [ ] `EXECUTIVE_RECIPIENTS` com emails corretos
- [ ] Testar com `python preview_email.py` primeiro

### **Para Enviar:**
```bash
# 1. Testar design (abre navegador)
python preview_email.py

# 2. Se estiver OK, enviar de verdade
python enviar_plano.py
```

### **Resultado Esperado:**
- ✅ Email HTML premium
- ✅ 2 anexos (plano + resumo)
- ✅ Múltiplos destinatários
- ✅ Log de sucesso no console

---

## 🆘 **Troubleshooting**

### **Erro: "SENDER_PASSWORD não configurado"**
**Solução:** Configure `SENDER_PASSWORD` no `.env` com senha de app do Gmail

### **Erro: "Authentication failed"**
**Solução:** 
1. Use senha de app (não senha normal)
2. Verifique se 2FA está ativo no Gmail
3. Gere nova senha de app em: https://myaccount.google.com/apppasswords

### **Erro: "Connection timeout"**
**Solução:**
1. Verifique conexão internet
2. Firewall pode estar bloqueando porta 587
3. Tente com VPN desligada

### **Email não chegou**
**Solução:**
1. Verifique pasta SPAM
2. Confirme email destinatário no `.env`
3. Veja logs do console (sucesso = "✅ EMAIL ENVIADO")

---

## 📊 **Comparação com Versões Antigas**

| Feature | Versão Antiga | Versão Nova ⭐ |
|---------|---------------|----------------|
| Interação console | ❌ Pergunta "s/n" | ✅ Zero perguntas |
| Template HTML | ❌ Simples | ✅ Premium gradientes |
| Anexos | ❌ Manual | ✅ Automático (2 docs) |
| Configuração | ❌ Hardcoded | ✅ 100% .env |
| Preview | ❌ Não tinha | ✅ Script dedicado |
| Log | ❌ Básico | ✅ Detalhado colorido |
| Erro handling | ❌ Genérico | ✅ Mensagens específicas |

---

## 🎯 **Casos de Uso**

### **1. Envio Executivo Formal**
```bash
# Configure EXECUTIVE_RECIPIENTS no .env
EXECUTIVE_RECIPIENTS=nicolas@avilaops.com,ceo@avilaops.com

python enviar_plano.py
```

### **2. Envio para Equipe Técnica**
```bash
# Configure TEAM_RECIPIENTS no .env
TEAM_RECIPIENTS=dev@avilaops.com,ops@avilaops.com

# Edite enviar_plano.py linha 256:
# msg['To'] = ', '.join(config.team_recipients)

python enviar_plano.py
```

### **3. Teste Local (sem enviar)**
```bash
python preview_email.py
# Abre navegador com preview
```

---

## 💡 **Próximas Melhorias**

- [ ] Agendamento automático (cronjob)
- [ ] Dashboard de tracking (emails abertos)
- [ ] A/B testing de templates
- [ ] Notificação Slack pós-envio
- [ ] Versionamento de emails enviados

---

## 📞 **Suporte**

**Problemas?** Entre em contato:
- 📧 Email: reports@avilaops.com
- 🤖 GitHub Copilot: Estou sempre aqui!

---

**🌟 "Zero cliques. Zero perguntas. Apenas resultados."**

---

**Última atualização:** 12 de novembro de 2025  
**Versão:** 2.0 - Totalmente Automatizado
