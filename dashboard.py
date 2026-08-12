import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import utils
from database import db
from labels import rotular_etapa
from theme import CHART_SEQUENCE, PALETTE, PLOTLY_LAYOUT, inject_css, kpi_card, render_footer_accent, render_header

st.set_page_config(
    page_title="Passaporte Exagerado · Dashboard",
    page_icon="🎪",
    layout="wide",
)

inject_css()
render_header()

data = db.load_data()

tab_geral, tab_comportamento, tab_lojas, tab_formularios = st.tabs(
    ["Visão geral", "Comportamento", "Lojas", "Formulários"]
)

# ---------------------------------------------------------------------------
# Visão geral
# ---------------------------------------------------------------------------
with tab_geral:
    total_cadastros = utils.get_total_cadastros(data)
    taxa_jornada = utils.get_taxa_jornada_completa(data, total_cadastros)
    pontuacao_media, pontuacao_serie = utils.get_pontuacao(data)
    ranking_brindes = utils.get_ranking_brindes(data)
    brinde_top = ranking_brindes.iloc[0]["brinde_nome"] if not ranking_brindes.empty else "—"
    nps = utils.get_nps_medio(data)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Cadastros", f"{total_cadastros:,}".replace(",", "."), "purple"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Jornada completa", f"{taxa_jornada:.0%}", "coral", "elegíveis ao ecocopo"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Pontuação média", f"{pontuacao_media:.0f} pts", "amber"), unsafe_allow_html=True)
    with c4:
        sub = f"NPS médio: {nps:.1f}" if nps is not None else None
        st.markdown(kpi_card("Brinde mais resgatado", brinde_top, "pink", sub), unsafe_allow_html=True)

    st.write("")
    col_funil, col_dist = st.columns([3, 2])

    with col_funil:
        st.markdown("##### Funil de conversão por etapa")
        funil = utils.get_funil_conversao(data, total_cadastros)
        if not funil.empty:
            fig = go.Figure(
                go.Funnel(
                    y=funil["etapa"],
                    x=funil["respondentes"],
                    marker=dict(color=PALETTE["purple"]),
                    textinfo="value+percent initial",
                )
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=340)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem respostas suficientes ainda para montar o funil.")

    with col_dist:
        st.markdown("##### Distribuição de pontuação")
        if not pontuacao_serie.empty:
            fig = px.histogram(pontuacao_serie, nbins=10, color_discrete_sequence=[PALETTE["coral"]])
            fig.update_layout(**PLOTLY_LAYOUT, height=340, showlegend=False, yaxis_title="usuários", xaxis_title="pontos")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de pontuação ainda.")

    render_footer_accent()

# ---------------------------------------------------------------------------
# Comportamento
# ---------------------------------------------------------------------------
with tab_comportamento:
    st.markdown("##### Respostas por dia da semana e horário")
    heatmap_df = utils.get_heatmap_horarios(data)
    if not heatmap_df.empty:
        dias_ordem = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        pivot = (
            heatmap_df.pivot_table(
                index="dia_semana",
                columns="hora",
                values="respostas",
                aggfunc="sum",
                fill_value=0,
            )
            .reindex(index=dias_ordem, columns=range(0, 24), fill_value=0)
        )

        fig = px.imshow(
            pivot,
            color_continuous_scale=[PALETTE["off_white"], PALETTE["coral"], PALETTE["purple"]],
            aspect="auto",
            labels=dict(x="Horário", y="Dia da semana", color="Respostas"),
            origin="lower",
        )

        tickvals = list(range(0, 24, 2))
        fig.update_xaxes(
            tickmode="array",
            tickvals=tickvals,
            ticktext=[f"{h:02d}:00" for h in tickvals],
            title_text="Horário",
        )
        fig.update_yaxes(title_text="Dia da semana")
        layout = dict(PLOTLY_LAYOUT)
        layout["height"] = 380
        layout["coloraxis_colorbar"] = dict(title="respostas")
        layout["margin"] = dict(l=10, r=10, t=10, b=10)
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem respostas registradas ainda.")

    render_footer_accent()

# ---------------------------------------------------------------------------
# Lojas
# ---------------------------------------------------------------------------
with tab_lojas:
    st.markdown("##### Ranking de lojas por pontos gerados")
    lojas_df = utils.get_ranking_lojas(data)
    if not lojas_df.empty:
        fig = px.bar(
            lojas_df.head(15),
            x="pontos",
            y="loja_nome",
            orientation="h",
            color_discrete_sequence=[PALETTE["amber"]],
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=460)
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(lojas_df, use_container_width=True, hide_index=True)
    else:
        st.info("Sem dados de loja ainda.")

    render_footer_accent()

# ---------------------------------------------------------------------------
# Formulários
# ---------------------------------------------------------------------------
with tab_formularios:
    st.markdown("##### Resultado por formulário")
    formulario_escolhido = st.selectbox(
        "Formulário", utils.ETAPAS_JORNADA, format_func=rotular_etapa
    )
    resultados_df = utils.get_resultados_formulario(data, formulario_escolhido)
    if not resultados_df.empty:
        fig = px.bar(
            resultados_df,
            x="pct",
            y="resposta",
            color="pergunta",
            orientation="h",
            barmode="group",
            color_discrete_sequence=CHART_SEQUENCE,
        )
        fig.update_layout(**PLOTLY_LAYOUT, height=420, xaxis_tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Esse formulário ainda não tem respostas com pergunta/resposta estruturadas.")

    if formulario_escolhido == "cenografia":
        st.markdown("##### Marcas mais citadas (resposta livre)")
        marcas_df = utils.get_ranking_marcas_citadas(data)
        if not marcas_df.empty:
            fig = px.bar(
                marcas_df, x="mencoes", y="marca", orientation="h",
                color_discrete_sequence=[PALETTE["pink"]],
            )
            fig.update_layout(**PLOTLY_LAYOUT, height=380)
            fig.update_yaxes(autorange="reversed")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem menções de marca registradas ainda.")

    render_footer_accent()