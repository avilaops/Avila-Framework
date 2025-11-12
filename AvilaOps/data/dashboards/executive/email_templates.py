#!/usr/bin/env python3
"""
ÁVILA EXECUTIVE EMAIL TEMPLATES
==============================
Templates premium para relatórios executivos em HTML
Autor: Nicolas Avila - Ávila Framework
Data: 2025-11-11
"""

class AvilaEmailTemplates:
    """Templates de email premium para dashboards executivos"""
    
    @staticmethod
    def get_executive_template() -> str:
        """Template executivo premium com design responsivo"""
        return """
<!DOCTYPE html>
<html lang="pt-BR" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="x-apple-disable-message-reformatting">
    <title>{company_name} - Dashboard Executivo</title>
    
    <!--[if mso]>
    <noscript>
        <xml>
            <o:OfficeDocumentSettings>
                <o:AllowPNG/>
                <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
    </noscript>
    <![endif]-->
    
    <style>
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0 !important;
            padding: 0 !important;
            background-color: #f6f9fc !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif !important;
            line-height: 1.6 !important;
            color: #2d3748 !important;
        }}
        
        table {{
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }}
        
        table table table {{
            table-layout: auto;
        }}
        
        img {{
            -ms-interpolation-mode: bicubic;
            border: 0;
            outline: none;
            text-decoration: none;
        }}
        
        /* Main container */
        .email-container {{
            max-width: 680px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        /* Header */
        .header {{
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            padding: 40px 20px;
            text-align: center;
            position: relative;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100"><polygon fill="rgba(255,255,255,0.05)" points="0,0 1000,0 1000,80 0,100"/></svg>');
            background-size: cover;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .logo {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin: 0 auto 20px;
            border: 3px solid rgba(255, 255, 255, 0.2);
            display: block;
        }}
        
        .header h1 {{
            color: #ffffff !important;
            font-size: 32px;
            font-weight: 700;
            margin: 0 0 10px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .subtitle {{
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 16px;
            margin: 0;
            font-weight: 300;
        }}
        
        /* Report metadata */
        .report-meta {{
            background-color: #f7fafc;
            padding: 25px 30px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .meta-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 0;
        }}
        
        .meta-item {{
            color: #718096;
            font-size: 14px;
            margin: 0;
        }}
        
        .meta-item.highlight {{
            color: #38a169;
            font-weight: 600;
        }}
        
        /* Content sections */
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            color: #1a202c !important;
            font-size: 22px;
            font-weight: 700;
            margin: 0 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        /* Metrics grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .metric-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 25px 20px;
            text-align: center;
            position: relative;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, #3182ce 0%, #2b6cb0 100%);
            border-radius: 12px 12px 0 0;
        }}
        
        .metric-icon {{
            font-size: 24px;
            margin-bottom: 10px;
            display: block;
        }}
        
        .metric-value {{
            font-size: 28px;
            font-weight: 700;
            color: #3182ce !important;
            margin: 5px 0;
            line-height: 1;
        }}
        
        .metric-label {{
            color: #4a5568 !important;
            font-size: 14px;
            font-weight: 600;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .metric-change {{
            font-size: 12px;
            margin-top: 8px;
            padding: 4px 8px;
            border-radius: 6px;
            font-weight: 500;
        }}
        
        .metric-change.positive {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .metric-change.negative {{
            background: #fed7d7;
            color: #742a2a;
        }}
        
        /* Lists */
        .achievement-list, .alert-list {{
            list-style: none;
            padding: 0;
            margin: 15px 0;
        }}
        
        .achievement-item, .alert-item {{
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
            border-left: 4px solid;
        }}
        
        .achievement-item {{
            background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%);
            color: #22543d !important;
            border-left-color: #38a169;
        }}
        
        .alert-item {{
            background: linear-gradient(135deg, #fef5e7 0%, #fde8b2 100%);
            color: #744210 !important;
            border-left-color: #d69e2e;
        }}
        
        /* Charts placeholder */
        .chart-container {{
            background: #f7fafc;
            border: 2px dashed #cbd5e0;
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            margin: 20px 0;
        }}
        
        .chart-placeholder {{
            color: #718096 !important;
            font-size: 16px;
            font-weight: 500;
        }}
        
        /* Insights section */
        .insights-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff !important;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin: 30px 0;
        }}
        
        .insights-card h3 {{
            color: #ffffff !important;
            font-size: 20px;
            margin: 0 0 15px 0;
            font-weight: 600;
        }}
        
        .insights-card p {{
            color: rgba(255, 255, 255, 0.95) !important;
            font-size: 15px;
            line-height: 1.6;
            margin: 0;
        }}
        
        /* Team section */
        .team-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .team-card {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
        }}
        
        .team-card h4 {{
            color: #3182ce !important;
            font-size: 16px;
            margin: 0 0 12px 0;
            font-weight: 600;
        }}
        
        .team-metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        
        .team-metric-label {{
            color: #4a5568 !important;
        }}
        
        .team-metric-value {{
            color: #2d3748 !important;
            font-weight: 600;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3182ce 0%, #2b6cb0 100%);
            border-radius: 3px;
        }}
        
        /* Footer */
        .footer {{
            background: #1a202c;
            padding: 30px;
            text-align: center;
        }}
        
        .footer h4 {{
            color: #ffffff !important;
            font-size: 18px;
            margin: 0 0 15px 0;
            font-weight: 600;
        }}
        
        .footer p {{
            color: rgba(255, 255, 255, 0.8) !important;
            font-size: 14px;
            line-height: 1.6;
            margin: 0 0 15px 0;
        }}
        
        .footer .copyright {{
            color: rgba(255, 255, 255, 0.6) !important;
            font-size: 12px;
            margin: 0;
        }}
        
        /* Mobile responsiveness */
        @media only screen and (max-width: 600px) {{
            .email-container {{
                margin: 10px !important;
                border-radius: 8px !important;
            }}
            
            .header {{
                padding: 30px 15px !important;
            }}
            
            .header h1 {{
                font-size: 24px !important;
            }}
            
            .content {{
                padding: 20px !important;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr !important;
                gap: 15px !important;
            }}
            
            .metric-value {{
                font-size: 24px !important;
            }}
            
            .section-title {{
                font-size: 18px !important;
            }}
            
            .team-grid {{
                grid-template-columns: 1fr !important;
            }}
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            .email-container {{
                background-color: #1a202c !important;
            }}
            
            .content {{
                background-color: #1a202c !important;
            }}
            
            .metric-card {{
                background: #2d3748 !important;
                border-color: #4a5568 !important;
            }}
            
            .section-title {{
                color: #f7fafc !important;
                border-bottom-color: #4a5568 !important;
            }}
        }}
        
        /* Outlook specific fixes */
        <!--[if mso]>
        .metric-card {{
            width: 200px !important;
        }}
        
        .team-card {{
            width: 250px !important;
        }}
        <![endif]-->
    </style>
</head>
<body>
    <div style="background-color: #f6f9fc; padding: 20px 0;">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
            <tr>
                <td align="center">
                    <div class="email-container">
                        <!-- Header -->
                        <div class="header">
                            <div class="header-content">
                                <img src="{company_logo}" alt="Logo da {company_name}" class="logo" width="80" height="80">
                                <h1>{company_name}</h1>
                                <p class="subtitle">Dashboard Executivo - Relatório Gerencial</p>
                            </div>
                        </div>
                        
                        <!-- Report Metadata -->
                        <div class="report-meta">
                            <div class="meta-row">
                                <p class="meta-item">📅 Período: {period_start} - {period_end}</p>
                                <p class="meta-item highlight">🕒 Gerado: {report_date} às {report_time}</p>
                            </div>
                        </div>
                        
                        <!-- Content -->
                        <div class="content">
                            <!-- Executive Summary -->
                            <div class="section">
                                <h2 class="section-title">📊 Resumo Executivo</h2>
                                <div class="metrics-grid">
                                    <div class="metric-card">
                                        <span class="metric-icon">🚀</span>
                                        <div class="metric-value">{total_products}</div>
                                        <p class="metric-label">Produtos Ativos</p>
                                        <div class="metric-change positive">
                                            {healthy_products}/{total_products_detail} saudáveis
                                        </div>
                                    </div>
                                    
                                    <div class="metric-card">
                                        <span class="metric-icon">📈</span>
                                        <div class="metric-value">{revenue_growth}%</div>
                                        <p class="metric-label">Crescimento</p>
                                        <div class="metric-change positive">
                                            Receita mensal
                                        </div>
                                    </div>
                                    
                                    <div class="metric-card">
                                        <span class="metric-icon">⭐</span>
                                        <div class="metric-value">{customer_satisfaction}</div>
                                        <p class="metric-label">Satisfação</p>
                                        <div class="metric-change positive">
                                            Score NPS
                                        </div>
                                    </div>
                                    
                                    <div class="metric-card">
                                        <span class="metric-icon">👥</span>
                                        <div class="metric-value">{team_size}</div>
                                        <p class="metric-label">Equipe</p>
                                        <div class="metric-change positive">
                                            Velocidade: {overall_velocity}%
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Financial Overview -->
                            <div class="section">
                                <h2 class="section-title">💰 Visão Financeira</h2>
                                <div class="metrics-grid">
                                    <div class="metric-card">
                                        <span class="metric-icon">💵</span>
                                        <div class="metric-value">R$ {current_revenue:,.0f}</div>
                                        <p class="metric-label">Receita Atual</p>
                                        <div class="metric-change positive">
                                            +{revenue_growth_rate}% vs anterior
                                        </div>
                                    </div>
                                    
                                    <div class="metric-card">
                                        <span class="metric-icon">📊</span>
                                        <div class="metric-value">{gross_margin}%</div>
                                        <p class="metric-label">Margem Bruta</p>
                                        <div class="metric-change positive">
                                            Líquida: {net_margin}%
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Key Achievements -->
                            <div class="section">
                                <h2 class="section-title">🏆 Principais Conquistas</h2>
                                <ul class="achievement-list">
                                    {achievements}
                                </ul>
                            </div>
                            
                            <!-- Critical Alerts -->
                            <div class="section">
                                <h2 class="section-title">⚠️ Alertas Críticos</h2>
                                <ul class="alert-list">
                                    {critical_alerts}
                                </ul>
                            </div>
                            
                            <!-- Team Performance -->
                            <div class="section">
                                <h2 class="section-title">👥 Performance das Equipes</h2>
                                <div class="team-grid">
                                    <div class="team-card">
                                        <h4>Atlas Squad</h4>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Membros:</span>
                                            <span class="team-metric-value">2</span>
                                        </div>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Produtividade:</span>
                                            <span class="team-metric-value">92%</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: 92%"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="team-card">
                                        <h4>Forge Squad</h4>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Membros:</span>
                                            <span class="team-metric-value">2</span>
                                        </div>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Produtividade:</span>
                                            <span class="team-metric-value">88%</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: 88%"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="team-card">
                                        <h4>Lumen Squad</h4>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Membros:</span>
                                            <span class="team-metric-value">2</span>
                                        </div>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Produtividade:</span>
                                            <span class="team-metric-value">90%</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: 90%"></div>
                                        </div>
                                    </div>
                                    
                                    <div class="team-card">
                                        <h4>Sigma Squad</h4>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Membros:</span>
                                            <span class="team-metric-value">2</span>
                                        </div>
                                        <div class="team-metric">
                                            <span class="team-metric-label">Produtividade:</span>
                                            <span class="team-metric-value">86%</span>
                                        </div>
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: 86%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Charts Section -->
                            <div class="section">
                                <h2 class="section-title">📈 Análise Visual</h2>
                                <div class="chart-container">
                                    <p class="chart-placeholder">
                                        📊 Gráficos interativos disponíveis na versão web do dashboard<br>
                                        Acesse o relatório completo em: dashboard.avilaops.com
                                    </p>
                                </div>
                            </div>
                            
                            <!-- AI Insights -->
                            <div class="insights-card">
                                <h3>🧠 Insights Inteligentes</h3>
                                <p>
                                    Com base na análise dos dados, recomendamos focar na otimização do Roncav Budget 
                                    e monitorar de perto a capacidade do Bárbara Core. O crescimento de 23% na receita 
                                    está alinhado com nossas metas estratégicas. A produtividade das equipes mantém-se 
                                    acima de 85%, indicando excelente engajamento.
                                </p>
                            </div>
                        </div>
                        
                        <!-- Footer -->
                        <div class="footer">
                            <h4>🏛️ {company_name} - Dashboard Executivo</h4>
                            <p>
                                Este relatório foi gerado automaticamente pelo sistema de analytics executivo.
                                Os dados são atualizados em tempo real e refletem o estado atual da operação.
                                Para dúvidas ou análises específicas, entre em contato com a equipe de dados.
                            </p>
                            <p class="copyright">
                                © 2025 Ávila Framework. Todos os direitos reservados. | Confidencial - Uso Interno
                            </p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def get_mobile_template() -> str:
        """Template otimizado para mobile"""
        return """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{company_name} - Dashboard Mobile</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            margin: 0;
            padding: 15px;
            background: #f6f9fc;
            color: #2d3748;
            line-height: 1.5;
        }}
        
        .container {{
            max-width: 100%;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .header {{
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
            padding: 20px;
            text-align: center;
            color: white;
        }}
        
        .header h1 {{
            font-size: 20px;
            margin: 0 0 5px 0;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 20px 15px;
        }}
        
        .metric {{
            background: #f7fafc;
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
            border-left: 4px solid #3182ce;
        }}
        
        .metric-value {{
            font-size: 24px;
            font-weight: 700;
            color: #3182ce;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            color: #4a5568;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .list-item {{
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 6px;
            font-size: 14px;
            line-height: 1.4;
        }}
        
        .achievement {{
            background: #c6f6d5;
            color: #22543d;
            border-left: 3px solid #38a169;
        }}
        
        .alert {{
            background: #fef5e7;
            color: #744210;
            border-left: 3px solid #d69e2e;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #1a202c;
            margin: 20px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .footer {{
            background: #1a202c;
            color: white;
            padding: 20px 15px;
            text-align: center;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{company_name}</h1>
            <p class="subtitle">Dashboard Executivo</p>
        </div>
        
        <div class="content">
            <div class="metric">
                <div class="metric-value">{total_products}</div>
                <div class="metric-label">Produtos Ativos</div>
            </div>
            
            <div class="metric">
                <div class="metric-value">{revenue_growth}%</div>
                <div class="metric-label">Crescimento</div>
            </div>
            
            <div class="metric">
                <div class="metric-value">R$ {current_revenue:,.0f}</div>
                <div class="metric-label">Receita Atual</div>
            </div>
            
            <h2 class="section-title">🏆 Conquistas</h2>
            {achievements_mobile}
            
            <h2 class="section-title">⚠️ Alertas</h2>
            {alerts_mobile}
        </div>
        
        <div class="footer">
            <p>© 2025 {company_name} | Confidencial</p>
        </div>
    </div>
</body>
</html>
        """
    
    @staticmethod
    def format_achievements_mobile(achievements: list) -> str:
        """Formatar conquistas para template mobile"""
        return '\n'.join([
            f'<div class="list-item achievement">{achievement}</div>'
            for achievement in achievements
        ])
    
    @staticmethod
    def format_alerts_mobile(alerts: list) -> str:
        """Formatar alertas para template mobile"""
        return '\n'.join([
            f'<div class="list-item alert">{alert}</div>'
            for alert in alerts
        ])
    
    @staticmethod
    def format_achievement_items(achievements: list) -> str:
        """Formatar itens de conquista para template principal"""
        return '\n'.join([
            f'<li class="achievement-item">{achievement}</li>'
            for achievement in achievements
        ])
    
    @staticmethod
    def format_alert_items(alerts: list) -> str:
        """Formatar itens de alerta para template principal"""
        return '\n'.join([
            f'<li class="alert-item">{alert}</li>'
            for alert in alerts
        ])