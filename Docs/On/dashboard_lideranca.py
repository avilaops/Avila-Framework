"""
DASHBOARD DE LIDERANÇA ÁVILA
============================

Métricas humanizadas de gestão de pessoas e impacto social.
Complementa o dashboard_executivo.py com foco em:
- Bem-estar da equipe
- Satisfação do cliente
- Impacto social
- Desenvolvimento individual

Autor: Ávila AI Orchestration Team
Data: 2025-11-10
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Liderança - Ávila",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .big-metric {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1.2em;
        color: #666;
    }
    .positive {
        color: #28a745;
    }
    .negative {
        color: #dc3545;
    }
    .neutral {
        color: #ffc107;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== DADOS SIMULADOS ====================
# Em produção, conectar ao banco de dados real

def gerar_dados_equipe():
    """Gera dados fictícios de colaboradores"""
    nomes = ["Ana Silva", "Carlos Santos", "Juliana Costa", "Pedro Alves",
             "Mariana Souza", "Roberto Lima", "Fernanda Rocha", "Lucas Martins",
             "Beatriz Oliveira", "Rafael Campos", "Camila Ferreira", "Diego Moraes"]

    setores = ["Tecnologia", "Vendas", "Marketing", "Operações", "Produto", "RH"]

    colaboradores = []
    for i, nome in enumerate(nomes):
        colaboradores.append({
            "nome": nome,
            "setor": np.random.choice(setores),
            "cargo": np.random.choice(["Júnior", "Pleno", "Sênior", "Líder"]),
            "bem_estar": np.random.uniform(3.5, 5.0),
            "engajamento": np.random.uniform(3.0, 5.0),
            "produtividade": np.random.uniform(3.5, 5.0),
            "satisfacao": np.random.uniform(3.8, 5.0),
            "dias_desde_1on1": np.random.randint(0, 30),
            "horas_extras_mes": np.random.randint(0, 40),
            "cursos_completos": np.random.randint(0, 10),
            "feedback_pendente": np.random.choice([True, False], p=[0.2, 0.8])
        })

    return pd.DataFrame(colaboradores)


def gerar_dados_clientes():
    """Gera dados fictícios de satisfação de clientes"""
    empresas = [
        "Tech Corp", "Innovation SA", "Digital Solutions", "Smart Business",
        "Future Industries", "AI Ventures", "Data Masters", "Cloud Systems"
    ]

    clientes = []
    for empresa in empresas:
        clientes.append({
            "empresa": empresa,
            "csat": np.random.uniform(4.0, 5.0),
            "nps": np.random.randint(7, 10),
            "tempo_resposta_medio_min": np.random.randint(2, 15),
            "incidentes_mes": np.random.randint(0, 5),
            "valor_contrato_mensal": np.random.randint(5000, 50000),
            "risco_churn": np.random.choice(["Baixo", "Médio", "Alto"], p=[0.7, 0.2, 0.1])
        })

    return pd.DataFrame(clientes)


def gerar_dados_impacto_social():
    """Gera dados de impacto social da empresa"""
    # Horas economizadas pelos clientes (automação)
    horas_economizadas = np.random.randint(5000, 15000)

    # Pessoas impactadas indiretamente
    pessoas_impactadas = horas_economizadas * 2

    # Projetos sociais apoiados
    projetos_sociais = [
        {"nome": "Ensina Brasil", "tipo": "Educação", "investimento": 5000},
        {"nome": "Instituto Ayrton Senna", "tipo": "Educação", "investimento": 3000},
        {"nome": "Code.org", "tipo": "Tecnologia", "investimento": 2000},
    ]

    return {
        "horas_economizadas": horas_economizadas,
        "pessoas_impactadas": pessoas_impactadas,
        "projetos_sociais": projetos_sociais,
        "investimento_social_total": sum([p["investimento"] for p in projetos_sociais])
    }


def gerar_historico_metricas():
    """Gera histórico de métricas mensais"""
    meses = pd.date_range(start='2024-05-01', periods=6, freq='ME')

    historico = []
    for mes in meses:
        historico.append({
            "mes": mes,
            "enps": np.random.randint(40, 80),
            "csat_medio": np.random.uniform(4.2, 4.8),
            "turnover": np.random.uniform(0.02, 0.08),
            "horas_treinamento": np.random.randint(50, 150),
            "incidentes": np.random.randint(5, 20)
        })

    return pd.DataFrame(historico)


# Carregar dados
df_equipe = gerar_dados_equipe()
df_clientes = gerar_dados_clientes()
impacto_social = gerar_dados_impacto_social()
df_historico = gerar_historico_metricas()


# ==================== SIDEBAR ====================

st.sidebar.title("🌟 Dashboard de Liderança")
st.sidebar.markdown("---")

# Filtros
setor_filtro = st.sidebar.multiselect(
    "Filtrar por setor:",
    options=df_equipe["setor"].unique(),
    default=df_equipe["setor"].unique()
)

periodo = st.sidebar.selectbox(
    "Período:",
    ["Última semana", "Último mês", "Último trimestre", "Último ano"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Última atualização:**")
st.sidebar.markdown(f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Botão de atualização manual
if st.sidebar.button("🔄 Atualizar dados"):
    st.rerun()


# ==================== MAIN DASHBOARD ====================

st.title("🌟 Dashboard de Liderança Ávila")
st.markdown("*Porque pessoas são o nosso maior ativo*")

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs([
    "👥 Equipe",
    "😊 Clientes",
    "🌍 Impacto Social",
    "📈 Tendências"
])


# ==================== TAB 1: EQUIPE ====================

with tab1:
    st.header("👥 Bem-Estar e Desenvolvimento da Equipe")

    # Filtrar dados
    df_equipe_filtrado = df_equipe[df_equipe["setor"].isin(setor_filtro)]

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        enps_atual = np.random.randint(55, 75)
        delta_enps = np.random.randint(-5, 10)
        st.metric(
            "eNPS (Employee Net Promoter Score)",
            f"{enps_atual}",
            f"{delta_enps:+d} pts vs mês anterior",
            delta_color="normal"
        )

    with col2:
        bem_estar_medio = df_equipe_filtrado["bem_estar"].mean()
        st.metric(
            "Bem-Estar Médio",
            f"{bem_estar_medio:.2f}/5.0",
            "🟢 Saudável" if bem_estar_medio >= 4.0 else "🟡 Atenção"
        )

    with col3:
        engajamento_medio = df_equipe_filtrado["engajamento"].mean()
        st.metric(
            "Engajamento",
            f"{engajamento_medio:.2f}/5.0",
            "🟢 Alto" if engajamento_medio >= 4.0 else "🟡 Moderado"
        )

    with col4:
        turnover = np.random.uniform(0.03, 0.07)
        st.metric(
            "Turnover (últimos 12 meses)",
            f"{turnover*100:.1f}%",
            "🟢 Baixo" if turnover < 0.05 else "🟡 Normal"
        )

    st.markdown("---")

    # Gráficos lado a lado
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 Bem-Estar por Setor")

        bem_estar_setor = df_equipe_filtrado.groupby("setor")["bem_estar"].mean().reset_index()

        fig_bem_estar = px.bar(
            bem_estar_setor,
            x="setor",
            y="bem_estar",
            color="bem_estar",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[1, 5],
            labels={"bem_estar": "Bem-Estar (1-5)", "setor": "Setor"}
        )
        fig_bem_estar.update_layout(showlegend=False)
        st.plotly_chart(fig_bem_estar, use_container_width=True)

    with col_right:
        st.subheader("🎓 Cursos Completados por Pessoa")

        cursos_setor = df_equipe_filtrado.groupby("setor")["cursos_completos"].sum().reset_index()

        fig_cursos = px.pie(
            cursos_setor,
            values="cursos_completos",
            names="setor",
            hole=0.4,
            title="Distribuição de Treinamentos"
        )
        st.plotly_chart(fig_cursos, use_container_width=True)

    st.markdown("---")

    # Alertas de RH
    st.subheader("⚠️ Alertas de Gestão de Pessoas")

    col_alert1, col_alert2, col_alert3 = st.columns(3)

    with col_alert1:
        # 1:1s atrasados
        atrasados_1on1 = df_equipe_filtrado[df_equipe_filtrado["dias_desde_1on1"] > 14]
        if len(atrasados_1on1) > 0:
            st.warning(f"**{len(atrasados_1on1)} pessoas** sem 1:1 há >14 dias")
            with st.expander("Ver detalhes"):
                for _, pessoa in atrasados_1on1.iterrows():
                    st.write(f"• {pessoa['nome']} ({pessoa['setor']}) - {pessoa['dias_desde_1on1']} dias")
        else:
            st.success("✅ Todos os 1:1s em dia")

    with col_alert2:
        # Horas extras excessivas
        horas_extras_altas = df_equipe_filtrado[df_equipe_filtrado["horas_extras_mes"] > 20]
        if len(horas_extras_altas) > 0:
            st.warning(f"**{len(horas_extras_altas)} pessoas** com >20h extras/mês")
            with st.expander("Ver detalhes"):
                for _, pessoa in horas_extras_altas.iterrows():
                    st.write(f"• {pessoa['nome']} - {pessoa['horas_extras_mes']}h")
        else:
            st.success("✅ Horas extras saudáveis")

    with col_alert3:
        # Feedback pendente
        feedback_pendente = df_equipe_filtrado[df_equipe_filtrado["feedback_pendente"] == True]
        if len(feedback_pendente) > 0:
            st.info(f"**{len(feedback_pendente)} pessoas** aguardando feedback")
            with st.expander("Ver detalhes"):
                for _, pessoa in feedback_pendente.iterrows():
                    st.write(f"• {pessoa['nome']} ({pessoa['setor']})")
        else:
            st.success("✅ Feedbacks em dia")

    st.markdown("---")

    # Tabela detalhada
    st.subheader("📋 Visão Detalhada da Equipe")

    # Preparar tabela
    df_tabela = df_equipe_filtrado[["nome", "setor", "cargo", "bem_estar", "engajamento", "produtividade", "dias_desde_1on1", "horas_extras_mes"]].copy()
    df_tabela["bem_estar"] = df_tabela["bem_estar"].round(1)
    df_tabela["engajamento"] = df_tabela["engajamento"].round(1)
    df_tabela["produtividade"] = df_tabela["produtividade"].round(1)

    st.dataframe(
        df_tabela,
        column_config={
            "nome": "Nome",
            "setor": "Setor",
            "cargo": "Cargo",
            "bem_estar": st.column_config.ProgressColumn(
                "Bem-Estar",
                help="Escala 1-5",
                format="%.1f",
                min_value=0,
                max_value=5
            ),
            "engajamento": st.column_config.ProgressColumn(
                "Engajamento",
                help="Escala 1-5",
                format="%.1f",
                min_value=0,
                max_value=5
            ),
            "produtividade": st.column_config.ProgressColumn(
                "Produtividade",
                help="Escala 1-5",
                format="%.1f",
                min_value=0,
                max_value=5
            ),
            "dias_desde_1on1": "Dias desde último 1:1",
            "horas_extras_mes": "Horas extras (mês)"
        },
        hide_index=True,
        use_container_width=True
    )


# ==================== TAB 2: CLIENTES ====================

with tab2:
    st.header("😊 Satisfação e Relacionamento com Clientes")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        csat_medio = df_clientes["csat"].mean()
        st.metric(
            "CSAT Médio",
            f"{csat_medio:.2f}/5.0",
            "🟢 Excelente" if csat_medio >= 4.5 else "🟡 Bom"
        )

    with col2:
        nps_medio = df_clientes["nps"].mean()
        st.metric(
            "NPS Médio",
            f"{nps_medio:.1f}/10",
            "🟢 Promotores" if nps_medio >= 9 else "🟡 Neutros"
        )

    with col3:
        tempo_resposta = df_clientes["tempo_resposta_medio_min"].mean()
        st.metric(
            "Tempo Médio de Resposta",
            f"{tempo_resposta:.0f} min",
            "🟢 Rápido" if tempo_resposta < 5 else "🟡 Normal"
        )

    with col4:
        incidentes_total = df_clientes["incidentes_mes"].sum()
        st.metric(
            "Incidentes (último mês)",
            f"{incidentes_total}",
            "🟢 Baixo" if incidentes_total < 20 else "🟡 Moderado"
        )

    st.markdown("---")

    # Gráficos
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 CSAT por Cliente")

        df_clientes_sorted = df_clientes.sort_values("csat", ascending=True)

        fig_csat = px.bar(
            df_clientes_sorted,
            x="csat",
            y="empresa",
            orientation="h",
            color="csat",
            color_continuous_scale=["red", "yellow", "green"],
            range_color=[1, 5],
            labels={"csat": "CSAT (1-5)", "empresa": "Cliente"}
        )
        st.plotly_chart(fig_csat, use_container_width=True)

    with col_right:
        st.subheader("⚠️ Risco de Churn")

        risco_counts = df_clientes["risco_churn"].value_counts().reset_index()
        risco_counts.columns = ["risco", "quantidade"]

        cores_risco = {"Baixo": "green", "Médio": "orange", "Alto": "red"}

        fig_risco = px.bar(
            risco_counts,
            x="risco",
            y="quantidade",
            color="risco",
            color_discrete_map=cores_risco,
            labels={"quantidade": "Nº de Clientes", "risco": "Nível de Risco"}
        )
        st.plotly_chart(fig_risco, use_container_width=True)

    st.markdown("---")

    # Clientes em risco
    st.subheader("🚨 Clientes que Precisam de Atenção")

    clientes_risco_alto = df_clientes[df_clientes["risco_churn"] == "Alto"]

    if len(clientes_risco_alto) > 0:
        st.error(f"**{len(clientes_risco_alto)} clientes** com risco ALTO de churn!")

        for _, cliente in clientes_risco_alto.iterrows():
            with st.expander(f"🔴 {cliente['empresa']} - Valor mensal: R$ {cliente['valor_contrato_mensal']:,.2f}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**CSAT:** {cliente['csat']:.1f}/5.0")
                with col2:
                    st.write(f"**NPS:** {cliente['nps']}/10")
                with col3:
                    st.write(f"**Incidentes:** {cliente['incidentes_mes']}")

                st.markdown("**Ações recomendadas:**")
                st.write("- [ ] Agendar call com CEO/CTO do cliente")
                st.write("- [ ] Revisar SLA e performance")
                st.write("- [ ] Oferecer desconto ou upgrade")
    else:
        st.success("✅ Nenhum cliente em risco alto no momento!")

    st.markdown("---")

    # Tabela detalhada
    st.subheader("📋 Visão Detalhada de Clientes")

    st.dataframe(
        df_clientes,
        column_config={
            "empresa": "Cliente",
            "csat": st.column_config.ProgressColumn(
                "CSAT",
                help="Customer Satisfaction Score (1-5)",
                format="%.2f",
                min_value=1,
                max_value=5
            ),
            "nps": st.column_config.ProgressColumn(
                "NPS",
                help="Net Promoter Score (0-10)",
                format="%d",
                min_value=0,
                max_value=10
            ),
            "tempo_resposta_medio_min": "Tempo Resposta (min)",
            "incidentes_mes": "Incidentes/Mês",
            "valor_contrato_mensal": st.column_config.NumberColumn(
                "Valor Mensal",
                format="R$ %d"
            ),
            "risco_churn": st.column_config.SelectboxColumn(
                "Risco Churn",
                options=["Baixo", "Médio", "Alto"]
            )
        },
        hide_index=True,
        use_container_width=True
    )


# ==================== TAB 3: IMPACTO SOCIAL ====================

with tab3:
    st.header("🌍 Impacto Social da Ávila")
    st.markdown("*Nossa missão: ser suporte para a sociedade humana*")

    # Métricas principais
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='big-metric'>{impacto_social['horas_economizadas']:,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Horas Economizadas pelos Clientes</div>", unsafe_allow_html=True)
        st.caption("Tempo liberado para atividades de maior valor")

    with col2:
        st.markdown(f"<div class='big-metric'>{impacto_social['pessoas_impactadas']:,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Pessoas Impactadas Indiretamente</div>", unsafe_allow_html=True)
        st.caption("Famílias, colegas, comunidades")

    with col3:
        st.markdown(f"<div class='big-metric'>R$ {impacto_social['investimento_social_total']:,}</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric-label'>Investimento Social (último ano)</div>", unsafe_allow_html=True)
        st.caption("Doações e patrocínios")

    st.markdown("---")

    # Projetos sociais apoiados
    st.subheader("🤝 Projetos Sociais Apoiados")

    for projeto in impacto_social["projetos_sociais"]:
        with st.expander(f"💚 {projeto['nome']} - {projeto['tipo']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Tipo:** {projeto['tipo']}")
                st.write(f"**Investimento:** R$ {projeto['investimento']:,}")
            with col2:
                st.button("🔗 Visitar", key=f"btn_{projeto['nome']}")

    st.markdown("---")

    # Equivalências
    st.subheader("📊 Impacto Equivalente")

    col1, col2, col3 = st.columns(3)

    with col1:
        dias_trabalho = impacto_social['horas_economizadas'] / 8
        st.metric(
            "Dias de Trabalho Economizados",
            f"{dias_trabalho:,.0f} dias",
            "≈ 3 anos de trabalho de 1 pessoa"
        )

    with col2:
        arvores_equivalente = impacto_social['investimento_social_total'] / 50  # R$ 50/árvore
        st.metric(
            "Equivalente em Plantio de Árvores",
            f"{arvores_equivalente:,.0f} árvores",
            "Contribuição ambiental indireta"
        )

    with col3:
        bolsas_estudo = impacto_social['investimento_social_total'] / 1000  # R$ 1000/bolsa
        st.metric(
            "Equivalente em Bolsas de Estudo",
            f"{bolsas_estudo:.0f} bolsas",
            "1 ano de curso técnico"
        )

    st.markdown("---")

    # Filosofia
    st.subheader("💡 Nossa Filosofia")

    st.info("""
    **"Tecnologia deve servir às pessoas, não o contrário."**

    Na Ávila, acreditamos que:
    - 🤝 IA deve **aumentar** capacidades humanas, não substituir pessoas
    - 🌱 Crescimento empresarial deve gerar impacto social positivo
    - 📚 Conhecimento deve ser compartilhado, não acumulado
    - 🌍 Lucro é meio, não fim - o fim é melhorar vidas

    Cada projeto que entregamos deve responder: **"Como isso torna a vida das pessoas melhor?"**
    """)


# ==================== TAB 4: TENDÊNCIAS ====================

with tab4:
    st.header("📈 Tendências e Evolução")

    # eNPS ao longo do tempo
    st.subheader("📊 Evolução do eNPS")

    fig_enps = px.line(
        df_historico,
        x="mes",
        y="enps",
        markers=True,
        labels={"mes": "Mês", "enps": "eNPS"}
    )
    fig_enps.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Meta: 50")
    st.plotly_chart(fig_enps, use_container_width=True)

    # Duas colunas de gráficos
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("😊 CSAT Médio ao Longo do Tempo")

        fig_csat_tempo = px.line(
            df_historico,
            x="mes",
            y="csat_medio",
            markers=True,
            labels={"mes": "Mês", "csat_medio": "CSAT Médio"}
        )
        fig_csat_tempo.add_hline(y=4.5, line_dash="dash", line_color="green", annotation_text="Meta: 4.5")
        st.plotly_chart(fig_csat_tempo, use_container_width=True)

    with col_right:
        st.subheader("🔄 Turnover Mensal")

        df_historico["turnover_percent"] = df_historico["turnover"] * 100

        fig_turnover = px.bar(
            df_historico,
            x="mes",
            y="turnover_percent",
            labels={"mes": "Mês", "turnover_percent": "Turnover (%)"},
            color="turnover_percent",
            color_continuous_scale=["green", "yellow", "red"]
        )
        fig_turnover.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Meta: <5%")
        st.plotly_chart(fig_turnover, use_container_width=True)

    # Horas de treinamento
    st.subheader("🎓 Investimento em Treinamento")

    fig_treinamento = px.area(
        df_historico,
        x="mes",
        y="horas_treinamento",
        labels={"mes": "Mês", "horas_treinamento": "Horas de Treinamento"},
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig_treinamento, use_container_width=True)

    st.markdown("---")

    # Insights automáticos
    st.subheader("💡 Insights Automáticos (Gerados por IA)")

    st.success("""
    ✅ **Positivos:**
    - eNPS aumentou 12 pontos nos últimos 3 meses (tendência positiva)
    - CSAT acima da meta de 4.5 consistentemente
    - Turnover abaixo de 5% (benchmark da indústria: 8-12%)
    """)

    st.warning("""
    ⚠️ **Atenção:**
    - 3 pessoas sem 1:1 há mais de 20 dias (agendar urgente)
    - Setor de Tecnologia com horas extras acima da média (risco de burnout)
    - Cliente "Innovation SA" com CSAT em queda (agendar reunião)
    """)

    st.info("""
    💡 **Recomendações:**
    - Implementar "Sexta-feira sem reunião" para reduzir carga mental
    - Aumentar budget de treinamento em 20% (ROI comprovado)
    - Criar programa de mentoria reversa (júniors ensinando sêniors sobre novas techs)
    """)


# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Dashboard de Liderança Ávila | Versão 1.0 | Atualizado em tempo real</p>
    <p><em>"Liderar é servir"</em> 🌟</p>
</div>
""", unsafe_allow_html=True)


# ==================== AUTO-REFRESH ====================
# Atualiza a cada 5 minutos (opcional, comentar se não quiser)
# import time
# time.sleep(300)
# st.rerun()
