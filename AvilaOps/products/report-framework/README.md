# 🏛️ Ávila Report Framework

## 📋 Visão Geral

O **Ávila Report Framework** é uma solução completa para geração, formatação e distribuição de relatórios corporativos. Desenvolvido para o ecossistema Ávila Framework, oferece múltiplos formatos de saída e canais de comunicação.

## ✨ Funcionalidades

### 📊 Geração de Relatórios
- **8 Tipos de Relatório**: Diário, Semanal, Mensal, Projetos, Financeiro, Performance, Governança, Personalizado
- **Múltiplos Formatos**: Markdown, Excel, PDF, HTML
- **Dados Dinâmicos**: Métricas automatizadas e personalizáveis
- **Templates Profissionais**: Formatação corporativa automática

### 📱 Distribuição Multi-Canal
- **📧 Email**: HTML formatado com anexos
- **📱 WhatsApp**: Mensagens formatadas via WhatsApp Web
- **💾 Arquivos**: Salvamento local em diversos formatos
- **🔄 Sincronização**: Integração com Obsidian e GitHub

### 🎯 Interface Gráfica
- **GUI Intuitiva**: Interface amigável em tkinter
- **👁️ Visualização**: Preview em tempo real
- **📊 Logs**: Monitoramento completo
- **⚙️ Configurações**: Personalização total

### 📈 Monitoramento
- **🔍 Sentry Integration**: Monitoramento de erros
- **📋 Logging**: Sistema de logs detalhado
- **📊 Métricas**: Acompanhamento de performance

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- Windows 10/11 (recomendado)
- Acesso à internet

### 1️⃣ Instalação
```bash
# Navegar para o diretório
cd AvilaOps/products/report-framework

# Executar setup automático
python setup.py
```

### 2️⃣ Configuração
```bash
# Executar aplicação
python main.py

# Ou usar o atalho
./launch_avila_reports.ps1
```

### 3️⃣ Configurações Personalizadas
Edite o arquivo `config.py` para:
- **WhatsApp**: Configurar número de destino
- **Email**: SMTP e credenciais
- **Sentry**: Token de monitoramento
- **Logs**: Localização e níveis

## 📊 Tipos de Relatório

| Tipo          | Ícone | Descrição                    | Frequência  |
| ------------- | ----- | ---------------------------- | ----------- |
| Diário        | 📅     | Resumo das atividades do dia | Diário      |
| Semanal       | 📊     | Consolidado da semana        | Semanal     |
| Mensal        | 📈     | Análise mensal completa      | Mensal      |
| Projetos      | 🏗️     | Status dos projetos ativos   | Sob demanda |
| Financeiro    | 💰     | Análise financeira           | Mensal      |
| Performance   | 🚀     | Métricas de desempenho       | Semanal     |
| Governança    | 🏛️     | Compliance e governança      | Trimestral  |
| Personalizado | ⚙️     | Relatório customizado        | Sob demanda |

## 🎯 Como Usar

### Gerar Relatório Markdown
```python
from exporters import MarkdownExporter

exporter = MarkdownExporter()
data = {
    'summary': 'Resumo do relatório',
    'metrics': {'Vendas': 'R$ 50.000'},
    'details': 'Detalhes completos'
}

filepath = exporter.export(data, 'financial')
```

### Enviar via WhatsApp
```python
from exporters import WhatsAppExporter

exporter = WhatsAppExporter()
exporter.export(data, 'daily', 'resumo')
```

### Enviar via Email
```python
from exporters import EmailExporter

exporter = EmailExporter()
exporter.export(data, 'weekly', attachments=['report.xlsx'])
```

### Excel Avançado
```python
from exporters import ExcelExporter

exporter = ExcelExporter()
exporter.export(data, 'financial')  # Com gráficos e formatação
```

## ⚙️ Configurações

### WhatsApp
```python
WHATSAPP_CONFIG = {
    "phone_number": "+5517997811471",
    "message_template": "🏛️ *Ávila Framework*\n{content}"
}
```

### Email
```python
EMAIL_CONFIG = {
    "to_email": "nicolas@avila.inc",
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587
}
```

### Sentry
```python
SENTRY_CONFIG = {
    "dsn": "sntrys_eyJpYXQi...",
    "environment": "production"
}
```

## 🔧 Estrutura do Projeto

```
report-framework/
├── 📄 main.py              # Interface principal
├── ⚙️ config.py            # Configurações
├── 📊 logger.py            # Sistema de logs
├── 📦 setup.py             # Instalador
├── 📋 requirements.txt     # Dependências
├── 📁 exporters/           # Módulos de exportação
│   ├── markdown_exporter.py
│   ├── excel_exporter.py
│   ├── whatsapp_exporter.py
│   └── email_exporter.py
├── 📁 logs/                # Logs do sistema
├── 📁 exports/             # Arquivos gerados
└── 📁 assets/              # Recursos (ícones, etc.)
```

## 📈 Funcionalidades Avançadas

### Relatório Financeiro
- Análise de receitas e despesas
- Gráficos automáticos no Excel
- Indicadores de performance
- Comparativos temporais

### Relatório de Projetos
- Status de todos os projetos
- Progresso visual
- Alertas de prazo
- Análise de recursos

### Sistema de Logs
- Logs rotativos automáticos
- Integração com Sentry
- Níveis configuráveis
- Visualização em tempo real

### Automação
- Scripts PowerShell incluídos
- Integração com Task Scheduler
- Sincronização automática
- Backup de dados

## 🛠️ Desenvolvimento

### Adicionar Novo Tipo de Relatório
1. Edite `config.py` → `REPORT_TYPES`
2. Implemente lógica específica nos exportadores
3. Teste via interface gráfica

### Adicionar Novo Exportador
1. Crie arquivo em `exporters/`
2. Herde da classe base apropriada
3. Implemente método `export()`
4. Registre em `__init__.py`

### Debug
```bash
# Logs detalhados
python main.py --debug

# Teste específico
python -c "from exporters import WhatsAppExporter; WhatsAppExporter().send_test_message()"
```

## 🚨 Troubleshooting

### Email não enviando
- Verificar credenciais SMTP
- Configurar "App Password" no Gmail
- Checar firewall/antivírus

### WhatsApp não abrindo
- Verificar formato do número
- WhatsApp Web deve estar disponível
- Navegador padrão configurado

### Erro no Excel
- Instalar: `pip install openpyxl xlsxwriter`
- Verificar permissões de escrita
- Fechar Excel se estiver aberto

### Logs não aparecendo
- Verificar permissões da pasta `logs/`
- Executar como administrador
- Checar configurações de nível de log

## 📞 Suporte

- **Email**: nicolas@avila.inc
- **GitHub**: https://github.com/avilaops/Avila-Framework
- **Documentação**: Ver pasta `AvilaOps/docs/`
- **Issues**: GitHub Issues

## 📄 Licença

Copyright © 2025 AvilaOps Team. Todos os direitos reservados.

Este software é propriedade do Ávila Framework e está licenciado para uso interno.

## 🎯 Roadmap

### v1.1 (Próxima Release)
- [ ] Integração com APIs externas
- [ ] Dashboard web
- [ ] Agendamento automático
- [ ] Relatórios em PDF nativos

### v1.2 (Futuro)
- [ ] Slack integration
- [ ] Teams integration
- [ ] Mobile app
- [ ] AI-powered insights

---

**🏛️ Desenvolvido com ❤️ pelo AvilaOps Team**
