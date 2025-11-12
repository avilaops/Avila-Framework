#!/usr/bin/env python3
"""
Envia o Sumário Executivo de IA por email
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Configuração
SMTP_HOST = "smtp.porkbun.com"
SMTP_PORT = 587
SMTP_USER = "dev@avila.inc"
SMTP_PASSWORD = "7Aciqgr7@3278579"
FROM_EMAIL = "dev@avila.inc"
TO_EMAIL = "nicolas@avila.inc"

# Lê o sumário
sumario_path = Path(__file__).parent / "docs" / "SUMARIO_EXECUTIVO_IA.md"
content = sumario_path.read_text(encoding="utf-8")

# Cria mensagem
msg = MIMEMultipart("alternative")
msg["Subject"] = "✅ Estratégia de IA para Produtos Ávila - Fase 1 Completa"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL

# Texto puro
text_part = MIMEText(content, "plain", "utf-8")
msg.attach(text_part)

# HTML básico
html_content = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        pre {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            background: #e8e8e8;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
    </style>
</head>
<body>
    <pre>{content}</pre>
</body>
</html>
"""

html_part = MIMEText(html_content, "html", "utf-8")
msg.attach(html_part)

# Envia
print("📧 Conectando ao servidor SMTP...")
server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
server.starttls()

print("🔐 Autenticando...")
server.login(SMTP_USER, SMTP_PASSWORD)

print("📨 Enviando email...")
server.send_message(msg)
server.quit()

print(f"✅ Email enviado com sucesso para {TO_EMAIL}!")
print(f"📄 Arquivo: {sumario_path.name}")
print(f"📊 Tamanho: {len(content)} caracteres")
