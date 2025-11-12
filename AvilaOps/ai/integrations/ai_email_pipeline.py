#!/usr/bin/env python3
"""
Integração: Lumen → Atlas → Vox → Email Automation
Pipeline de insights executivos automatizados com IA

Fluxo:
1. Lumen analisa métricas (ON, Geolocation, sync-center)
2. Atlas consolida insights estratégicos
3. Vox personaliza comunicação
4. Email enviado via generate_dashboard_email.py (AvilaInc)

Integração com: AvilaInc email automation + On.Core EventBus
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações
PROJECT_ROOT = Path(__file__).parent.parent
DATASETS_PATH = PROJECT_ROOT / "datasets"
AVILAOPS_ROOT = PROJECT_ROOT.parent.parent

class AgentPipeline:
    """Pipeline de integração entre agentes AI e email automation"""
    
    def __init__(self):
        self.insights = []
        self.timestamp = datetime.now()
        
    def lumen_analyze_metrics(self):
        """LUMEN: Analisa datasets e gera insights de ML"""
        print("🔬 LUMEN: Analisando métricas...")
        
        insights = []
        
        # Analisar ON (onboarding)
        on_data_path = DATASETS_PATH / "on" / "onboarding_events.json"
        if on_data_path.exists():
            with open(on_data_path, 'r') as f:
                on_data = json.load(f)
            
            # Análise simples: TTV médio
            ttv_values = [u['ttv_days'] for u in on_data if u.get('ttv_days') is not None]
            if ttv_values:
                avg_ttv = sum(ttv_values) / len(ttv_values)
                insights.append({
                    'source': 'Lumen',
                    'product': 'ON',
                    'metric': 'TTV Médio',
                    'value': round(avg_ttv, 1),
                    'unit': 'dias',
                    'insight': f"Time-to-Value médio é {avg_ttv:.1f} dias. {'✅ Abaixo da meta (<7 dias)' if avg_ttv < 7 else '⚠️ Acima da meta - investigar fricções'}"
                })
            
            # Churn risk
            active_users = sum(1 for u in on_data if u.get('onboarding_status') in ['active', 'champion'])
            churn_risk = sum(1 for u in on_data if u.get('support_tickets_open', 0) > 2)
            
            insights.append({
                'source': 'Lumen',
                'product': 'ON',
                'metric': 'Risco de Churn',
                'value': churn_risk,
                'total': len(on_data),
                'percentage': round(churn_risk / len(on_data) * 100, 1) if on_data else 0,
                'insight': f"{churn_risk}/{len(on_data)} usuários com risco (>2 tickets). Taxa: {churn_risk/len(on_data)*100:.1f}%"
            })
        
        # Analisar Geolocation
        geo_data_path = DATASETS_PATH / "geolocation" / "gps_samples.json"
        if geo_data_path.exists():
            with open(geo_data_path, 'r') as f:
                geo_data = json.load(f)
            
            # Análise de acurácia
            accuracies = [g['accuracy_meters'] for g in geo_data]
            avg_accuracy = sum(accuracies) / len(accuracies)
            
            insights.append({
                'source': 'Lumen',
                'product': 'Geolocation',
                'metric': 'Acurácia GPS',
                'value': round(avg_accuracy, 1),
                'unit': 'metros',
                'insight': f"Acurácia média de {avg_accuracy:.1f}m. {'✅ Excelente (<10m)' if avg_accuracy < 10 else '⚠️ Requer calibração'}"
            })
            
            # Compliance LGPD
            with_consent = sum(1 for g in geo_data if 'consent_id' in g)
            insights.append({
                'source': 'Lumen',
                'product': 'Geolocation',
                'metric': 'Compliance LGPD',
                'value': with_consent,
                'total': len(geo_data),
                'percentage': round(with_consent / len(geo_data) * 100, 1),
                'insight': f"{with_consent}/{len(geo_data)} amostras com consentimento. Compliance: {with_consent/len(geo_data)*100:.1f}%"
            })
        
        self.insights.extend(insights)
        print(f"   ✅ {len(insights)} insights gerados")
        return insights
    
    def atlas_consolidate_strategy(self):
        """ATLAS: Consolida insights em estratégia executiva"""
        print("🗺️  ATLAS: Consolidando estratégia...")
        
        # Agrupar por produto
        by_product = {}
        for insight in self.insights:
            product = insight.get('product', 'Geral')
            if product not in by_product:
                by_product[product] = []
            by_product[product].append(insight)
        
        # Identificar prioridades
        strategic_summary = {
            'timestamp': self.timestamp.isoformat(),
            'products': {},
            'priorities': [],
            'kpis': {}
        }
        
        for product, product_insights in by_product.items():
            # Calcular score de saúde (0-100)
            health_score = 100
            issues = []
            wins = []
            
            for insight in product_insights:
                # Detectar problemas (⚠️)
                if '⚠️' in insight['insight']:
                    health_score -= 15
                    issues.append(insight['metric'])
                # Detectar sucessos (✅)
                elif '✅' in insight['insight']:
                    wins.append(insight['metric'])
            
            strategic_summary['products'][product] = {
                'health_score': max(0, health_score),
                'total_metrics': len(product_insights),
                'issues': issues,
                'wins': wins
            }
            
            # Adicionar às prioridades se houver problemas
            if issues:
                strategic_summary['priorities'].append({
                    'product': product,
                    'urgency': 'high' if health_score < 70 else 'medium',
                    'issues': issues
                })
        
        # Calcular KPIs agregados
        for insight in self.insights:
            metric = insight['metric']
            strategic_summary['kpis'][metric] = {
                'value': insight['value'],
                'unit': insight.get('unit', ''),
                'insight': insight['insight']
            }
        
        self.strategic_summary = strategic_summary
        print(f"   ✅ Estratégia consolidada para {len(by_product)} produtos")
        return strategic_summary
    
    def vox_personalize_communication(self):
        """VOX: Personaliza comunicação para stakeholders"""
        print("📢 VOX: Personalizando comunicação...")
        
        summary = self.strategic_summary
        
        # Email executivo (CEO)
        email_executive = {
            'to': 'nicolas@avila.inc',
            'subject': f"📊 Insights Executivos - {self.timestamp.strftime('%d/%m/%Y')}",
            'template': 'executive_summary'
        }
        
        # Corpo do email
        body_parts = []
        
        # Saudação personalizada
        hour = self.timestamp.hour
        greeting = "Bom dia" if hour < 12 else "Boa tarde" if hour < 18 else "Boa noite"
        
        body_parts.append(f"{greeting}, Nícolas.\n")
        body_parts.append("Seu resumo diário de IA chegou.\n")
        
        # Resumo por produto
        body_parts.append("\n## 📊 Visão Geral dos Produtos\n")
        for product, data in summary['products'].items():
            health = data['health_score']
            icon = "🟢" if health >= 80 else "🟡" if health >= 60 else "🔴"
            
            body_parts.append(f"\n### {icon} {product}")
            body_parts.append(f"**Saúde:** {health}/100")
            
            if data['wins']:
                body_parts.append(f"**✅ Sucessos:** {', '.join(data['wins'])}")
            
            if data['issues']:
                body_parts.append(f"**⚠️ Atenção:** {', '.join(data['issues'])}")
        
        # KPIs chave
        body_parts.append("\n\n## 📈 KPIs Principais\n")
        for metric, data in summary['kpis'].items():
            value_str = f"{data['value']} {data['unit']}".strip()
            body_parts.append(f"**{metric}:** {value_str}")
            body_parts.append(f"  _{data['insight']}_\n")
        
        # Prioridades estratégicas
        if summary['priorities']:
            body_parts.append("\n\n## 🎯 Prioridades\n")
            for i, priority in enumerate(summary['priorities'], 1):
                urgency_icon = "🔥" if priority['urgency'] == 'high' else "⚡"
                body_parts.append(f"{i}. {urgency_icon} **{priority['product']}**: {', '.join(priority['issues'])}")
        
        # Rodapé
        body_parts.append("\n\n---")
        body_parts.append("_Gerado automaticamente por: Lumen (análise) → Atlas (estratégia) → Vox (comunicação)_")
        body_parts.append(f"_Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}_")
        
        email_executive['body_markdown'] = '\n'.join(body_parts)
        
        self.email_content = email_executive
        print("   ✅ Email personalizado gerado")
        return email_executive
    
    def send_email_via_smtp(self):
        """Envia email via SMTP (integração com AvilaInc email automation)"""
        print("📧 Enviando email...")
        
        email = self.email_content
        
        # Configuração SMTP (mesmo do AvilaInc)
        smtp_server = "smtp.porkbun.com"
        smtp_port = 587
        smtp_user = "dev@avila.inc"
        smtp_password = "1NcybeT#QpNn"  # Mesmo do send_jobs_email.py
        
        # Criar mensagem
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = email['to']
        msg['Subject'] = email['subject']
        
        # Versão texto
        text_part = MIMEText(email['body_markdown'], 'plain', 'utf-8')
        msg.attach(text_part)
        
        # Versão HTML (converter markdown simples)
        html_body = email['body_markdown']
        html_body = html_body.replace('\n## ', '\n<h2>').replace('\n### ', '\n<h3>')
        html_body = html_body.replace('\n**', '\n<strong>').replace('**', '</strong>')
        html_body = html_body.replace('\n_', '\n<em>').replace('_', '</em>')
        html_body = html_body.replace('\n', '<br>\n')
        
        html_template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
                h2 {{ color: #0066cc; }}
                h3 {{ color: #333; }}
                strong {{ color: #000; }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        html_part = MIMEText(html_template, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Enviar
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            
            print(f"   ✅ Email enviado para {email['to']}")
            print(f"   📧 Assunto: {email['subject']}")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao enviar email: {e}")
            return False
    
    def run_pipeline(self):
        """Executa pipeline completo"""
        print("\n" + "=" * 60)
        print("🚀 PIPELINE DE INTEGRAÇÃO AI → EMAIL AUTOMATION")
        print("=" * 60)
        print()
        
        try:
            # 1. Lumen: Análise
            self.lumen_analyze_metrics()
            
            # 2. Atlas: Estratégia
            self.atlas_consolidate_strategy()
            
            # 3. Vox: Comunicação
            self.vox_personalize_communication()
            
            # 4. Email: Envio
            success = self.send_email_via_smtp()
            
            print()
            print("=" * 60)
            if success:
                print("✅ PIPELINE CONCLUÍDO COM SUCESSO")
            else:
                print("⚠️ PIPELINE CONCLUÍDO COM AVISOS")
            print("=" * 60)
            
            # Salvar log da execução
            log_path = PROJECT_ROOT / "logs" / f"pipeline_{self.timestamp.strftime('%Y-%m-%d_%H%M%S')}.json"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': self.timestamp.isoformat(),
                    'insights': self.insights,
                    'strategic_summary': self.strategic_summary,
                    'email_sent': success
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n📝 Log salvo: {log_path}")
            
        except Exception as e:
            print(f"\n❌ ERRO NO PIPELINE: {e}")
            import traceback
            traceback.print_exc()

def main():
    pipeline = AgentPipeline()
    pipeline.run_pipeline()

if __name__ == "__main__":
    main()
