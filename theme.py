"""
Estilização do Dashboard Passaporte Exagerado.
Toda cor/CSS/tema de gráfico fica centralizado aqui — dashboard.py e
utils.py não devem ter nenhuma string de cor solta.
"""

import base64
from pathlib import Path

import streamlit as st

ASSETS_DIR = Path(__file__).parent / "assets"
HEADER_BANNER = ASSETS_DIR / "header_banner.png"

# ---------------------------------------------------------------------------
# Paleta — extraída da identidade visual (LP / material de marketing)
# ---------------------------------------------------------------------------
PALETTE = {
    "off_white": "#F5F2EA",
    "purple": "#3C3489",
    "purple_light": "#EEEDFE",
    "purple_text": "#26215C",
    "coral": "#D85A30",
    "coral_light": "#FAECE7",
    "coral_text": "#4A1B0C",
    "amber": "#EF9F27",
    "amber_light": "#FAEEDA",
    "amber_text": "#412402",
    "pink": "#D4537E",
    "pink_light": "#FBEAF0",
    "pink_text": "#4B1528",
    "white": "#FFFFFF",
    "muted": "#8A8578",
}

# ordem de cores pra série categórica em gráficos (funil, ranking, formulários)
CHART_SEQUENCE = [
    PALETTE["purple"],
    PALETTE["coral"],
    PALETTE["amber"],
    PALETTE["pink"],
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="sans-serif", color=PALETTE["purple_text"], size=13),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor="#E5E1D6", zeroline=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)


def _img_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def inject_css() -> None:
    """Injeta CSS global: fundo, header com a arte, tabs horizontais estilizadas,
    cards de KPI. Chamar uma vez, logo após set_page_config."""

    banner_b64 = _img_base64(HEADER_BANNER) if HEADER_BANNER.exists() else ""

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-color: {PALETTE["off_white"]};
        }}
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
        }}
        .block-container {{
            padding-top: 0rem;
            max-width: 1200px;
        }}

        /* faixa de topo com a arte original */
        .exagerado-header {{
            width: 100%;
            height: 190px;
            border-radius: 0 0 18px 18px;
            background-image: url("data:image/png;base64,{banner_b64}");
            background-size: cover;
            background-position: center top;
            margin-bottom: 1.6rem;
            box-shadow: 0 2px 10px rgba(60,52,137,0.15);
        }}

        /* quadriculado de assinatura no rodapé, ecoando o header */
        .exagerado-footer-check {{
            height: 14px;
            width: 100%;
            background-image: repeating-linear-gradient(
                90deg, {PALETTE["coral"]} 0 14px, transparent 14px 28px
            );
            opacity: 0.5;
            border-radius: 8px;
            margin-top: 2rem;
        }}

        /* tabs nativas do Streamlit viram um menu horizontal em pílula */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
            border-bottom: none;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 42px;
            border-radius: 999px;
            padding: 0 20px;
            background-color: {PALETTE["white"]};
            border: 1px solid #E5E1D6;
            color: {PALETTE["muted"]};
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {PALETTE["purple"]} !important;
            color: {PALETTE["purple_light"]} !important;
            border: 1px solid {PALETTE["purple"]} !important;
        }}

        /* cards de kpi custom (substituem o st.metric padrão) */
        .kpi-card {{
            border-radius: 14px;
            padding: 1rem 1.2rem;
            height: 100%;
        }}
        .kpi-label {{
            font-size: 12.5px;
            font-weight: 500;
            margin: 0 0 4px 0;
            opacity: 0.85;
        }}
        .kpi-value {{
            font-size: 26px;
            font-weight: 700;
            margin: 0;
        }}
        .kpi-sub {{
            font-size: 11.5px;
            margin: 4px 0 0 0;
            opacity: 0.7;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown('<div class="exagerado-header"></div>', unsafe_allow_html=True)


def render_footer_accent() -> None:
    st.markdown('<div class="exagerado-footer-check"></div>', unsafe_allow_html=True)


# combinações (fundo claro, texto escuro) prontas pra usar no kpi_card()
KPI_STYLES = {
    "purple": (PALETTE["purple_light"], PALETTE["purple_text"]),
    "coral": (PALETTE["coral_light"], PALETTE["coral_text"]),
    "amber": (PALETTE["amber_light"], PALETTE["amber_text"]),
    "pink": (PALETTE["pink_light"], PALETTE["pink_text"]),
}


def kpi_card(label: str, value: str, style: str = "purple", sub: str | None = None) -> str:
    bg, fg = KPI_STYLES[style]
    sub_html = f'<p class="kpi-sub" style="color:{fg}">{sub}</p>' if sub else ""
    return f"""
    <div class="kpi-card" style="background-color:{bg}; color:{fg};">
        <p class="kpi-label" style="color:{fg}">{label}</p>
        <p class="kpi-value" style="color:{fg}">{value}</p>
        {sub_html}
    </div>
    """