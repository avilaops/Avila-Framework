# Automação — Relatório Executivo Semanal

## Objetivo
Gerar e-mail semanal a partir dos templates `marketing/templates/email/dashboard_report.md` (Markdown) e `marketing/templates/email/dashboard_report.html` (HTML) com métricas consolidadas dos dashboards gerenciais.

## Entradas esperadas
- `data/dashboard_metrics.json`: snapshot agregado (receita, CAC, FRT etc.) produzido pelos dashboards ou por job ETL.
- `data/dashboard_alerts.json`: alertas (descrição, responsável, status) calculados automaticamente.
- `data/dashboard_actions.json`: próximos passos com responsável e prazo.
- Templates Markdown/HTML em `marketing/templates/email/` (permitem customizar branding e copy).

## Saída
- Arquivos `out/executive_email.md` e `out/executive_email.html` contendo o e-mail preenchido
- Opcional: envio via SMTP/Graph (fora do escopo inicial)

## Processo
1. Carregar dados agregados.
2. Calcular indicadores derivados (ex.: LTV/CAC) se não vierem prontos.
3. Preencher templates substituindo placeholders `{{chave}}`.
4. Exportar Markdown em `out/executive_email.md` e HTML em `out/executive_email.html`.
5. Logar caminhos gerados para revisão humana antes do envio.

## Requisitos
- Python 3.13+ (conforme ambiente configurado)
- Dependências opcionais: `pyyaml`, `jinja2` (caso migremos para templates avançados). Implementação atual usa substituição simples.
- Garantir privacidade: nenhum dado sensível individual; apenas agregados k≥20.
- Atualizar branding ajustando os templates Markdown/HTML em vez do script sempre que possível.

## Próximos passos
- Manter script `analytics/reporting/generate_dashboard_email.py` como fonte única de geração Markdown/HTML.
- Definir pipeline (GitHub Actions ou tarefa agendada) para executar semanalmente.
- Integrar com serviço de e-mail (Mailgun, SES, Outlook) após validação humana.
- Monitorar consistência de dados e atualizar templates quando houver mudança de branding ou KPIs.
