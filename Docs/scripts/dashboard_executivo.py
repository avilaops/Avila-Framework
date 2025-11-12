"""
ÁVILA - Dashboard Executivo (Streamlit)

Dashboard interativo em tempo real mostrando:
- Métricas principais (economia, tempo, deploys, OKRs)
- Alertas críticos (P0/P1)
- Oportunidades de alto impacto
- Tendências e gráficos
- Top performers

Uso:
    streamlit run dashboard_executivo.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
from typing import Dict, List

# Configuração da página
st.set_page_config(
    page_title="Ávila Intelligence Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .opportunity-card {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Dados mockados (em produção, vem do banco)
def get_mock_data():
    return {
        "metricas_principais": {
            "economia_identificada": 38500,
            "economia_variacao": 22,
            "tempo_economizado": 127,
            "tempo_variacao": 18,
            "deploy_frequency": 42,
            "deploy_variacao": 31,
            "okr_progress": 73,
            "okr_variacao": 8
        },
        "alertas_criticos": [
            {
                "tipo": "performance",
                "titulo": "Servidor prod-api-01: CPU 98% há 4h",
                "acao": "Auto-scale (+2 instances)",
                "prioridade": "P0"
            },
            {
                "tipo": "security",
                "titulo": 'CVE-2025-12345 em dependency "fastapi==0.104.0"',
                "acao": "Upgrade para 0.104.1 (patch disponível)",
                "prioridade": "P0"
            },
            {
                "tipo": "cost",
                "titulo": "Custo Azure: $12,300 (orçamento: $10,000)",
                "acao": "8 VMs não desligadas (dev/test)",
                "prioridade": "P1"
            }
        ],
        "oportunidades": [
            {
                "titulo": "Reserved Instances: Economia de $4,200/mês",
                "descricao": "12 VMs com uptime >90% sem commitment",
                "roi": 50400,
                "risco": "BAIXO",
                "impact": "HIGH"
            },
            {
                "titulo": "Chatbot Vendas: +2100% ROI esperado",
                "descricao": "Lead qualification automática (24/7)",
                "roi": 0,
                "setup": "1 semana",
                "custo": 800,
                "impact": "HIGH"
            },
            {
                "titulo": "Storage Tiering: Economia de $3,600/ano",
                "descricao": "2TB em Hot tier (50% raramente acessado)",
                "roi": 3600,
                "risco": "ZERO",
                "esforco": "15min",
                "impact": "MEDIUM"
            },
            {
                "titulo": "Zombie Resources: Economia de $3,732/ano",
                "descricao": "8 discos, 12 IPs, 45 snapshots não usados",
                "roi": 3732,
                "risco": "ZERO",
                "impact": "MEDIUM"
            },
            {
                "titulo": 'Runbook "Git Workflows": 6h/mês economizadas',
                "descricao": "Padrão detectado em 8 conversas Copilot",
                "roi": 0,
                "tempo_economizado": 6,
                "impact": "LOW"
            }
        ],
        "tendencias": {
            "meses": ["Ago", "Set", "Out", "Nov"],
            "economia_acumulada": [12000, 22000, 34000, 48500]
        },
        "top_performers": [
            {
                "nome": "Ana Costa",
                "tipo": "pessoa",
                "contribuicao": "3 otimizações",
                "valor": 8200
            },
            {
                "nome": "João Silva",
                "tipo": "pessoa",
                "contribuicao": "5 runbooks criados",
                "valor": 60  # horas
            },
            {
                "nome": "AI Auto-actions",
                "tipo": "bot",
                "contribuicao": "142 execuções",
                "valor": 100  # % sucesso
            }
        ]
    }

# Header
st.title("🎯 ÁVILA INTELLIGENCE DASHBOARD")
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**Visão Executiva em Tempo Real**")
with col2:
    st.markdown(f"🔴 **LIVE** - {datetime.now().strftime('%H:%M:%S')}")

st.divider()

# Carregar dados
data = get_mock_data()

# SEÇÃO 1: Métricas Principais
st.subheader("📊 Métricas Principais (Último mês vs Anterior)")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Economia Identificada",
        value=f"${data['metricas_principais']['economia_identificada']:,}",
        delta=f"{data['metricas_principais']['economia_variacao']}%"
    )

with col2:
    st.metric(
        label="⏱️ Tempo Economizado",
        value=f"{data['metricas_principais']['tempo_economizado']} horas",
        delta=f"{data['metricas_principais']['tempo_variacao']}%"
    )

with col3:
    st.metric(
        label="🚀 Deploy Frequency",
        value=f"{data['metricas_principais']['deploy_frequency']} deploys",
        delta=f"{data['metricas_principais']['deploy_variacao']}%"
    )

with col4:
    st.metric(
        label="🎯 OKRs Progress",
        value=f"{data['metricas_principals']['okr_progress']}%",
        delta=f"{data['metricas_principais']['okr_variacao']}%"
    )

st.divider()

# SEÇÃO 2: Alertas Críticos
st.subheader(f"🚨 Alertas Críticos ({len(data['alertas_criticos'])})")

for alerta in data['alertas_criticos']:
    emoji = "⚠️" if alerta['tipo'] == "performance" else "🔐" if alerta['tipo'] == "security" else "💸"
    
    with st.container():
        st.markdown(f"""
        <div class="alert-critical">
            <h4>{emoji} {alerta['titulo']}</h4>
            <p>└─ Ação recomendada: {alerta['acao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("APROVAR", key=f"approve_{alerta['titulo']}"):
                st.success("✅ Ação aprovada! Executando...")
        with col2:
            if st.button("ADIAR 1h", key=f"defer_{alerta['titulo']}"):
                st.info("⏰ Adiado por 1 hora")
        with col3:
            if st.button("DETALHES", key=f"details_{alerta['titulo']}"):
                st.info("📋 Abrindo detalhes...")

st.divider()

# SEÇÃO 3: Oportunidades de Alto Impacto
st.subheader("💡 Oportunidades de Alto Impacto (Top 5)")

for i, opp in enumerate(data['oportunidades'], 1):
    with st.container():
        st.markdown(f"""
        <div class="opportunity-card">
            <h4>{i}. {opp['titulo']}</h4>
            <p>└─ {opp['descricao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            if 'roi' in opp and opp['roi'] > 0:
                st.markdown(f"**ROI:** ${opp['roi']:,}/ano")
            if 'tempo_economizado' in opp:
                st.markdown(f"**Tempo:** {opp['tempo_economizado']}h/mês")
        with col2:
            if 'risco' in opp:
                st.markdown(f"**Risco:** {opp['risco']}")
        with col3:
            if 'esforco' in opp:
                st.markdown(f"**Esforço:** {opp['esforco']}")
        with col4:
            if st.button("IMPLEMENTAR", key=f"impl_{i}"):
                st.success(f"✅ Oportunidade {i} em implementação!")

st.divider()

# SEÇÃO 4: Tendências
st.subheader("📈 Tendências (90 dias)")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=data['tendencias']['meses'],
    y=data['tendencias']['economia_acumulada'],
    mode='lines+markers',
    name='Economia Acumulada',
    line=dict(color='#4CAF50', width=3),
    marker=dict(size=10)
))

fig.update_layout(
    title="Economia Acumulada ao Longo do Tempo",
    xaxis_title="Mês",
    yaxis_title="Economia ($)",
    hovermode='x unified',
    template='plotly_white',
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# SEÇÃO 5: Top Performers
st.subheader("🏆 Top Performers (Last 30 days)")

for performer in data['top_performers']:
    emoji = "👤" if performer['tipo'] == "pessoa" else "🤖"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"**{emoji} {performer['nome']}:** {performer['contribuicao']}")
    with col2:
        if performer['nome'] == "AI Auto-actions":
            st.markdown(f"**{performer['valor']}% sucesso**")
        elif "runbooks" in performer['contribuicao']:
            st.markdown(f"**{performer['valor']}h economizadas**")
        else:
            st.markdown(f"**${performer['valor']:,}**")

st.divider()

# Sidebar - Filtros e Configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.subheader("Período")
    periodo = st.selectbox(
        "Selecione o período:",
        ["Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Último ano"]
    )
    
    st.subheader("Setores")
    setores = st.multiselect(
        "Filtrar por setor:",
        ["Liderança", "Vendas & Marketing", "Produto", "Tecnologia", 
         "Operações", "Clientes", "Suporte"],
        default=["Tecnologia", "Vendas & Marketing"]
    )
    
    st.subheader("Prioridades")
    prioridades = st.multiselect(
        "Filtrar alertas:",
        ["P0 - Crítico", "P1 - Alto", "P2 - Médio", "P3 - Baixo"],
        default=["P0 - Crítico", "P1 - Alto"]
    )
    
    st.divider()
    
    st.subheader("🔄 Atualização")
    auto_refresh = st.checkbox("Auto-refresh (30s)", value=True)
    
    if st.button("🔄 Atualizar Agora"):
        st.rerun()
    
    st.divider()
    
    st.subheader("📥 Exportar")
    if st.button("Exportar Dashboard (PDF)"):
        st.info("📄 Gerando PDF...")
    
    if st.button("Exportar Dados (CSV)"):
        st.info("📊 Gerando CSV...")

# Auto-refresh
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    f"**Ávila Intelligence Platform** v1.0 | "
    f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
    f"[Documentação](https://docs.avila.com) | "
    f"[Suporte](mailto:support@avila.com)"
)
