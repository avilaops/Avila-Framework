#!/usr/bin/env python3
"""
Script wrapper para enviar diferentes tipos de relatórios
Uso:
    python send_scheduled_report.py daily
    python send_scheduled_report.py weekly
    python send_scheduled_report.py monthly
"""
import argparse
import os
import sys
from pathlib import Path

# Adiciona analytics/reporting ao path
sys.path.insert(0, str(Path(__file__).parent / "analytics" / "reporting"))

from generate_dashboard_email import generate_email, generate_html_email, send_email_smtp
from env_loader import load_env

# Carrega configurações
load_env()

REPORT_CONFIGS = {
    "daily": {
        "metrics": os.getenv("DAILY_METRICS", "data/daily_metrics.json"),
        "alerts": os.getenv("DAILY_ALERTS", "data/daily_alerts.json"),
        "actions": os.getenv("DAILY_ACTIONS", "data/daily_actions.json"),
        "template_md": "marketing/templates/email/dashboard_report.md",
        "template_html": os.getenv("DAILY_TEMPLATE", "marketing/templates/email/dashboard_report.html"),
        "subject": os.getenv("DAILY_SUBJECT", "Relatório Operacional Diário"),
        "to_email": os.getenv("DAILY_TO", os.getenv("TO_EMAIL")),
    },
    "weekly": {
        "metrics": os.getenv("WEEKLY_METRICS", "data/dashboard_metrics.json"),
        "alerts": os.getenv("WEEKLY_ALERTS", "data/dashboard_alerts.json"),
        "actions": os.getenv("WEEKLY_ACTIONS", "data/dashboard_actions.json"),
        "template_md": "marketing/templates/email/dashboard_report.md",
        "template_html": os.getenv("WEEKLY_TEMPLATE", "marketing/templates/email/dashboard_report.html"),
        "subject": os.getenv("WEEKLY_SUBJECT", "Relatório Executivo Semanal"),
        "to_email": os.getenv("WEEKLY_TO", os.getenv("TO_EMAIL")),
    },
    "monthly": {
        "metrics": os.getenv("MONTHLY_METRICS", "data/monthly_metrics.json"),
        "alerts": os.getenv("MONTHLY_ALERTS", "data/monthly_alerts.json"),
        "actions": os.getenv("MONTHLY_ACTIONS", "data/monthly_actions.json"),
        "template_md": "marketing/templates/email/dashboard_report.md",
        "template_html": os.getenv("MONTHLY_TEMPLATE", "marketing/templates/email/dashboard_report.html"),
        "subject": os.getenv("MONTHLY_SUBJECT", "Relatório Estratégico Mensal"),
        "to_email": os.getenv("MONTHLY_TO", os.getenv("TO_EMAIL")),
    },
}


def send_report(report_type: str, dry_run: bool = False):
    """Envia relatório do tipo especificado."""
    if report_type not in REPORT_CONFIGS:
        print(f"❌ Tipo de relatório inválido: {report_type}")
        print(f"   Tipos disponíveis: {', '.join(REPORT_CONFIGS.keys())}")
        sys.exit(1)
    
    config = REPORT_CONFIGS[report_type]
    repo_root = Path(__file__).parent
    
    # Valida se arquivos de dados existem
    metrics_path = repo_root / config["metrics"]
    if not metrics_path.exists():
        print(f"❌ Arquivo de métricas não encontrado: {metrics_path}")
        print(f"   Usando dados de exemplo: data/dashboard_metrics.json")
        metrics_path = repo_root / "data" / "dashboard_metrics.json"
    
    alerts_path = repo_root / config["alerts"]
    if not alerts_path.exists():
        alerts_path = repo_root / "data" / "dashboard_alerts.json"
    
    actions_path = repo_root / config["actions"]
    if not actions_path.exists():
        actions_path = repo_root / "data" / "dashboard_actions.json"
    
    print(f"📊 Gerando relatório: {report_type.upper()}")
    print(f"   Métricas: {metrics_path.name}")
    print(f"   Destinatário: {config['to_email']}")
    
    # Gera relatórios
    md_output = repo_root / "out" / f"{report_type}_email.md"
    html_output = repo_root / "out" / f"{report_type}_email.html"
    
    _, replacements = generate_email(
        metrics_path=metrics_path,
        alerts_path=alerts_path,
        actions_path=actions_path,
        template_path=repo_root / config["template_md"],
        output_path=md_output,
    )
    print(f"✅ Markdown: {md_output}")
    
    html_path = generate_html_email(
        replacements=replacements,
        template_path=repo_root / config["template_html"],
        output_path=html_output,
    )
    print(f"✅ HTML: {html_path}")
    
    if dry_run:
        print("🔍 Modo dry-run: email NÃO será enviado")
        return
    
    # Envia email
    smtp_config = {
        "smtp_host": os.getenv("SMTP_HOST", "smtp.porkbun.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "smtp_user": os.getenv("SMTP_USER"),
        "smtp_password": os.getenv("SMTP_PASSWORD"),
        "from_email": os.getenv("FROM_EMAIL") or os.getenv("SMTP_USER"),
    }
    
    if not smtp_config["smtp_user"] or not smtp_config["smtp_password"]:
        print("❌ Configure SMTP_USER e SMTP_PASSWORD no .env")
        sys.exit(1)
    
    html_content = html_path.read_text(encoding="utf-8")
    
    send_email_smtp(
        to_email=config["to_email"],
        from_email=smtp_config["from_email"],
        subject=config["subject"],
        html_content=html_content,
        smtp_host=smtp_config["smtp_host"],
        smtp_port=smtp_config["smtp_port"],
        smtp_user=smtp_config["smtp_user"],
        smtp_password=smtp_config["smtp_password"],
    )


def main():
    parser = argparse.ArgumentParser(description="Envio agendado de relatórios")
    parser.add_argument(
        "report_type",
        choices=["daily", "weekly", "monthly"],
        help="Tipo de relatório a enviar",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Gera relatórios sem enviar email",
    )
    
    args = parser.parse_args()
    send_report(args.report_type, args.dry_run)


if __name__ == "__main__":
    main()
