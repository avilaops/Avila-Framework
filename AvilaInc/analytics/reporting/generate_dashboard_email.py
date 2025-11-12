from __future__ import annotations

import argparse
import json
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable, List, Mapping, TypeVar

try:
    from .env_loader import load_env
    load_env()
except ImportError:
    pass  # env_loader é opcional

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "dashboard_report.md"
HTML_TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "dashboard_report.html"
MARKETING_TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "marketing_plan.md"
MARKETING_HTML_TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "marketing_plan.html"
HIRING_TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "hiring_plan.md"
HIRING_HTML_TEMPLATE_PATH = REPO_ROOT / "marketing" / "templates" / "email" / "hiring_plan.html"

DEFAULT_METRICS = REPO_ROOT / "data" / "dashboard_metrics.json"
DEFAULT_ALERTS = REPO_ROOT / "data" / "dashboard_alerts.json"
DEFAULT_ACTIONS = REPO_ROOT / "data" / "dashboard_actions.json"
MARKETING_METRICS = REPO_ROOT / "data" / "marketing_plan.json"
MARKETING_ALERTS = REPO_ROOT / "data" / "marketing_alerts.json"
MARKETING_ACTIONS = REPO_ROOT / "data" / "marketing_actions.json"
HIRING_METRICS = REPO_ROOT / "data" / "hiring_plan.json"
HIRING_ALERTS = REPO_ROOT / "data" / "hiring_alerts.json"
HIRING_ACTIONS = REPO_ROOT / "data" / "hiring_actions.json"

OUTPUT_PATH = REPO_ROOT / "out" / "executive_email.md"
OUTPUT_HTML_PATH = REPO_ROOT / "out" / "executive_email.html"

MONTH_NAMES_PT = [
    "jan",
    "fev",
    "mar",
    "abr",
    "mai",
    "jun",
    "jul",
    "ago",
    "set",
    "out",
    "nov",
    "dez",
]


@dataclass
class Alert:
    description: str
    owner: str
    status: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, str]) -> "Alert":
        return cls(
            description=str(data.get("descricao", "")),
            owner=str(data.get("responsavel", "")),
            status=str(data.get("status", "")),
        )

    def render(self) -> str:
        if self.owner and self.status:
            return f"{self.description} — {self.owner} ({self.status})"
        if self.owner:
            return f"{self.description} — {self.owner}"
        return self.description


@dataclass
class Action:
    action: str
    owner: str
    due_date: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, str]) -> "Action":
        return cls(
            action=str(data.get("acao", "")),
            owner=str(data.get("responsavel", "")),
            due_date=str(data.get("prazo", "")),
        )

    def as_tuple(self) -> tuple[str, str, str]:
        return self.action, self.owner, self.due_date


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def format_currency_brl(value: float) -> str:
    formatted = f"{value:,.2f}"
    return formatted.replace(",", "_").replace(".", ",").replace("_", ".")


def format_percentage(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def format_hours(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def ensure_out_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def format_date_friendly(report_date: date) -> str:
    month = MONTH_NAMES_PT[report_date.month - 1]
    return f"{report_date.day:02d} {month} {report_date.year}"


def split_front_matter(content: str) -> tuple[str, str]:
    if not content.startswith("---"):
        raise ValueError("Template must start with front matter delimiter '---'")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Template must contain both front matter and body")
    _, front_matter, body = parts
    return front_matter.strip(), body.lstrip()


def update_date(front_matter: str, new_date: str) -> str:
    pattern = re.compile(r"date:\s*\"?[^\n\r]*\"?")
    replacement = f'date: "{new_date}"'
    if pattern.search(front_matter):
        return pattern.sub(replacement, front_matter, count=1)
    return f"{front_matter}\n{replacement}"


T = TypeVar("T")


def pad_list(values: Iterable[T], size: int, filler: T) -> List[T]:
    items = list(values)
    while len(items) < size:
        items.append(filler)
    return items[:size]


def build_replacements(
    metrics: Mapping[str, object],
    alerts: List[Alert],
    actions: List[Action],
    report_date: date,
) -> Mapping[str, str]:
    ltv = float(metrics.get("ltv", 0) or 0)
    cac = float(metrics.get("cac", 0) or 0.0001)
    ltv_cac = ltv / cac if cac else 0

    insights = metrics.get("insights", []) or []
    insight_values = pad_list([str(item) for item in insights], 3, "Sem insight registrado")

    alert_values = pad_list([alert.render() for alert in alerts if alert.description], 2, "Sem alertas ativos")
    raw_actions = [action.as_tuple() for action in actions if action.action]
    action_values = pad_list(raw_actions, 2, ("Sem novas ações", "", ""))

    return {
        "periodo": str(metrics.get("periodo", "semana não informada")),
        "data_relatorio": format_date_friendly(report_date),
        "receita_incremental": format_currency_brl(float(metrics.get("receita_incremental", 0) or 0)),
        "custos_otimizados": format_currency_brl(float(metrics.get("custos_otimizados", 0) or 0)),
        "margem_projetada": format_percentage(float(metrics.get("margem_projetada", 0) or 0)),
        "frt_medio": format_hours(float(metrics.get("frt_medio", 0) or 0)),
        "resolucao_24h": format_percentage(float(metrics.get("resolucao_24h", 0) or 0)),
        "csat": str(metrics.get("csat", "n/d")),
        "nps": str(metrics.get("nps", "n/d")),
        "execucao_plano": format_percentage(float(metrics.get("execucao_plano", 0) or 0)),
        "leads_qualificados": str(metrics.get("leads_qualificados", "n/d")),
        "win_rate": format_percentage(float(metrics.get("win_rate", 0) or 0)),
        "cac": format_currency_brl(float(metrics.get("cac", 0) or 0)),
        "ltv_cac": format_percentage(ltv_cac),
        "insight_1": insight_values[0],
        "insight_2": insight_values[1],
        "insight_3": insight_values[2],
        "alerta_1": alert_values[0],
        "alerta_2": alert_values[1],
    "acao_1": action_values[0][0],
    "responsavel_1": action_values[0][1],
    "prazo_1": action_values[0][2],
    "acao_2": action_values[1][0],
    "responsavel_2": action_values[1][1],
    "prazo_2": action_values[1][2],
        "link_dashboard": metrics.get("link_dashboard", "https://intranet.avila/dashboard"),
        "nome_destinatario": metrics.get("destinatario", "time"),
        "assinatura": metrics.get("assinatura", "Time Ávila"),
    }


def apply_replacements(body: str, replacements: Mapping[str, str]) -> str:
    rendered = body
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def escape_replacements_for_html(replacements: Mapping[str, str]) -> Mapping[str, str]:
    return {key: escape(str(value), quote=True) for key, value in replacements.items()}


def generate_email(
    metrics_path: Path,
    alerts_path: Path,
    actions_path: Path,
    template_path: Path,
    output_path: Path,
) -> tuple[Path, Mapping[str, str]]:
    metrics = load_json(metrics_path)
    raw_alerts = load_json(alerts_path)
    raw_actions = load_json(actions_path)

    alerts = [Alert.from_mapping(item) for item in raw_alerts]
    actions = [Action.from_mapping(item) for item in raw_actions]

    template_content = template_path.read_text(encoding="utf-8")
    front_matter, body = split_front_matter(template_content)
    today = date.today()
    front_matter = update_date(front_matter, today.isoformat())

    replacements = build_replacements(metrics, alerts, actions, today)
    rendered_body = apply_replacements(body, replacements)

    ensure_out_dir(output_path)
    output_path.write_text(f"---\n{front_matter}\n---\n\n{rendered_body}", encoding="utf-8")
    return output_path, replacements


def generate_html_email(
    replacements: Mapping[str, str],
    template_path: Path,
    output_path: Path,
) -> Path:
    template = template_path.read_text(encoding="utf-8")
    escaped_replacements = escape_replacements_for_html(replacements)
    rendered_html = apply_replacements(template, escaped_replacements)
    ensure_out_dir(output_path)
    output_path.write_text(rendered_html, encoding="utf-8")
    return output_path


def send_email_smtp(
    to_email: str,
    from_email: str,
    subject: str,
    html_content: str,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
) -> None:
    """Send HTML email via SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    
    html_part = MIMEText(html_content, "html", "utf-8")
    msg.attach(html_part)
    
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        print(f"✅ Email enviado com sucesso para {to_email}")
    except Exception as e:
        print(f"❌ Erro ao enviar email: {e}")
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate executive dashboard email")
    parser.add_argument("--report-type", type=str, default="dashboard", choices=["dashboard", "marketing_plan", "hiring_plan"], help="Type of report to generate")
    parser.add_argument("--metrics", type=Path, help="Path to metrics JSON (auto-selected based on report type)")
    parser.add_argument("--alerts", type=Path, help="Path to alerts JSON (auto-selected based on report type)")
    parser.add_argument("--actions", type=Path, help="Path to actions JSON (auto-selected based on report type)")
    parser.add_argument("--template", type=Path, help="Path to markdown template (auto-selected based on report type)")
    parser.add_argument("--html-template", type=Path, help="Path to HTML template (auto-selected based on report type)")
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH, help="Output markdown path")
    parser.add_argument("--html-output", type=Path, default=OUTPUT_HTML_PATH, help="Output HTML path")
    parser.add_argument("--skip-html", action="store_true", help="Skip HTML generation")
    
    # Email sending options
    parser.add_argument("--send-email", action="store_true", help="Send email after generating")
    parser.add_argument("--to", type=str, help="Recipient email address")
    parser.add_argument("--from-email", type=str, help="Sender email address (defaults to SMTP_USER env var)")
    parser.add_argument("--subject", type=str, help="Email subject (defaults to template subject)")
    parser.add_argument("--smtp-host", type=str, help="SMTP server host (defaults to SMTP_HOST env var)")
    parser.add_argument("--smtp-port", type=int, help="SMTP server port (defaults to SMTP_PORT env var or 587)")
    parser.add_argument("--smtp-user", type=str, help="SMTP username (defaults to SMTP_USER env var)")
    parser.add_argument("--smtp-password", type=str, help="SMTP password (defaults to SMTP_PASSWORD env var)")
    
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    # Auto-select paths based on report type
    if args.report_type == "marketing_plan":
        metrics_path = args.metrics or MARKETING_METRICS
        alerts_path = args.alerts or MARKETING_ALERTS  
        actions_path = args.actions or MARKETING_ACTIONS
        template_path = args.template or MARKETING_TEMPLATE_PATH
        html_template_path = args.html_template or MARKETING_HTML_TEMPLATE_PATH
    elif args.report_type == "hiring_plan":
        metrics_path = args.metrics or HIRING_METRICS
        alerts_path = args.alerts or HIRING_ALERTS
        actions_path = args.actions or HIRING_ACTIONS
        template_path = args.template or HIRING_TEMPLATE_PATH
        html_template_path = args.html_template or HIRING_HTML_TEMPLATE_PATH
    else:  # dashboard
        metrics_path = args.metrics or DEFAULT_METRICS
        alerts_path = args.alerts or DEFAULT_ALERTS
        actions_path = args.actions or DEFAULT_ACTIONS
        template_path = args.template or TEMPLATE_PATH
        html_template_path = args.html_template or HTML_TEMPLATE_PATH
    
    markdown_path, replacements = generate_email(
        metrics_path=metrics_path,
        alerts_path=alerts_path,
        actions_path=actions_path,
        template_path=template_path,
        output_path=args.output,
    )
    print(f"Relatório Markdown gerado em: {markdown_path}")

    html_path = None
    if not args.skip_html:
        html_path = generate_html_email(
            replacements=replacements,
            template_path=html_template_path,
            output_path=args.html_output,
        )
        print(f"Relatório HTML gerado em: {html_path}")
    
    # Send email if requested
    if args.send_email:
        if not html_path:
            print("❌ Erro: --send-email requer geração de HTML (não use --skip-html)")
            return
        
        # Get email configuration from args or environment
        to_email = args.to
        from_email = args.from_email or os.getenv("SMTP_USER")
        smtp_host = args.smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = args.smtp_port or int(os.getenv("SMTP_PORT", "587"))
        smtp_user = args.smtp_user or os.getenv("SMTP_USER")
        smtp_password = args.smtp_password or os.getenv("SMTP_PASSWORD")
        
        # Validate required fields
        if not to_email:
            print("❌ Erro: especifique destinatário com --to ou variável TO_EMAIL")
            return
        if not from_email:
            print("❌ Erro: especifique remetente com --from-email ou variável SMTP_USER")
            return
        if not smtp_user or not smtp_password:
            print("❌ Erro: configure SMTP_USER e SMTP_PASSWORD (variáveis de ambiente ou argumentos)")
            return
        
        # Default subject from template front-matter or use argument
        subject = args.subject or f"Relatório Executivo Semanal — {replacements.get('periodo', 'Semana')}"
        
        # Read HTML content
        html_content = html_path.read_text(encoding="utf-8")
        
        # Send email
        send_email_smtp(
            to_email=to_email,
            from_email=from_email,
            subject=subject,
            html_content=html_content,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_user=smtp_user,
            smtp_password=smtp_password,
        )


if __name__ == "__main__":
    main()
