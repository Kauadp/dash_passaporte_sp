"""
Cálculo de todas as KPIs e datasets de gráfico do Dashboard Passaporte Exagerado.
Recebe os DataFrames já carregados por `database.db.load_data()` — nenhuma
função aqui abre conexão com o banco, só transforma o que já veio em memória.

Schema real: cada formulário é uma tabela `interacoes_<etapa>` própria
(uma linha por visitante, `visitante_id` UNIQUE), pontos já vêm calculados
em `users.pontos_atuais`, e pontuação por loja mora em `pontuacoes`.
"""

from __future__ import annotations

import pandas as pd

# ordem da jornada — cada nome bate com a chave usada em database.TABELAS
ETAPAS_JORNADA = [
    "boas_vindas",
    "entrada_juquita",
    "acao_guerrilha",
    "lounge_vip",
    "estacionamento",
    "cenografia",
    "dentro_lojas",
    "saida_juquita",
    "saida_nps",
]
TOTAL_ETAPAS_COM_PONTO = 8  # todas menos o nps, que não pontua

# colunas de pergunta (categóricas) de cada formulário, pra aba "Formulários"
FORM_PERGUNTAS = {
    "boas_vindas": ["quem_eh_voce", "qual_foco", "regiao"],
    "entrada_juquita": ["item_ritmo", "faixa_etaria", "ficou_sabendo_onde"],
    "acao_guerrilha": ["oque_trouxe", "regiao"],
    "lounge_vip": ["prioridade", "quantas_sacolas"],
    "estacionamento": ["como_veio", "quanto_tempo"],
    "cenografia": ["oque_mais_garimpou", "qual_marca_deixou_louco"],
    "dentro_lojas": ["melhor_dia", "forma_pagamento"],
    "saida_juquita": ["qual_renda", "quanto_pretende_gastar", "com_quem_veio"],
    "saida_nps": ["maior_destaque", "te_vejo_proxima_edicao"],  # quanto_recomenda vai à parte (é a nota NPS)
}


def get_total_cadastros(data: dict[str, pd.DataFrame]) -> int:
    return len(data["users"])


def get_funil_conversao(data: dict[str, pd.DataFrame], total_cadastros: int) -> pd.DataFrame:
    """% de cadastrados que respondeu cada formulário, na ordem da jornada.
    Cada interacoes_<etapa> tem 1 linha por visitante (visitante_id é UNIQUE),
    então o tamanho da tabela já é o número de respondentes daquela etapa."""
    if total_cadastros == 0:
        return pd.DataFrame(columns=["etapa", "respondentes", "pct"])

    linhas = []
    for etapa in ETAPAS_JORNADA:
        respondentes = len(data[etapa])
        linhas.append(
            {"etapa": etapa, "respondentes": respondentes, "pct": respondentes / total_cadastros}
        )
    return pd.DataFrame(linhas)


def get_taxa_jornada_completa(data: dict[str, pd.DataFrame], total_cadastros: int) -> float:
    """% de cadastrados que aparecem nas 8 tabelas de interação que dão ponto
    (todas exceto saida_nps) — interseção dos visitante_id entre elas."""
    if total_cadastros == 0:
        return 0.0
    etapas_com_ponto = [e for e in ETAPAS_JORNADA if e != "saida_nps"]
    conjuntos = [set(data[e]["visitante_id"]) for e in etapas_com_ponto if not data[e].empty]
    if len(conjuntos) < len(etapas_com_ponto):
        return 0.0  # alguma etapa ainda não tem nenhuma resposta
    completos = len(set.intersection(*conjuntos))
    return completos / total_cadastros


def get_pontuacao(data: dict[str, pd.DataFrame]) -> tuple[float, pd.Series]:
    """Pontuação já vem calculada em users.pontos_atuais — não recalculamos aqui."""
    df = data["users"]
    if df.empty:
        return 0.0, pd.Series(dtype=int)
    serie = df["pontos_atuais"]
    return float(serie.mean()), serie


def get_nps_medio(data: dict[str, pd.DataFrame]) -> float | None:
    df = data["saida_nps"]
    if df.empty or "quanto_recomenda" not in df:
        return None
    return float(df["quanto_recomenda"].mean())


def get_ranking_brindes(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    resgates, brindes = data["resgates"], data["brindes"]
    if resgates.empty or brindes.empty:
        return pd.DataFrame(columns=["brinde_nome", "resgates"])
    merged = resgates.merge(brindes[["id", "nome"]], left_on="brinde_id", right_on="id")
    return (
        merged.groupby("nome").size().reset_index(name="resgates")
        .rename(columns={"nome": "brinde_nome"})
        .sort_values("resgates", ascending=False)
    )


def get_heatmap_horarios(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Junta o created_at de todas as tabelas de interação pra montar o heatmap
    dia da semana x hora — cada linha ali é uma resposta de formulário."""
    frames = [data[etapa][["created_at"]] for etapa in ETAPAS_JORNADA if not data[etapa].empty]
    if not frames:
        return pd.DataFrame(columns=["dia_semana", "hora", "respostas"])
    todas = pd.concat(frames, ignore_index=True)
    todas["created_at"] = pd.to_datetime(todas["created_at"])
    todas["dia_semana"] = todas["created_at"].dt.day_name()
    todas["hora"] = todas["created_at"].dt.hour
    return todas.groupby(["dia_semana", "hora"]).size().reset_index(name="respostas")


def get_ranking_lojas(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """pontos = soma de pontuacoes.pontos por loja; scans = nº de visitantes
    distintos que pontuaram naquela loja (a constraint UNIQUE(visitante_id, loja_id)
    garante que cada visitante conta só 1x por loja)."""
    pontuacoes, lojas = data["pontuacoes"], data["lojas"]
    if pontuacoes.empty or lojas.empty:
        return pd.DataFrame(columns=["loja_nome", "pontos", "scans"])
    merged = pontuacoes.merge(lojas[["id", "nome"]], left_on="loja_id", right_on="id")
    ranking = (
        merged.groupby("nome")
        .agg(pontos=("pontos", "sum"), scans=("visitante_id", "nunique"))
        .reset_index()
        .rename(columns={"nome": "loja_nome"})
        .sort_values("pontos", ascending=False)
    )
    return ranking


def get_resultados_formulario(data: dict[str, pd.DataFrame], tipo_formulario: str) -> pd.DataFrame:
    """Proporção de respostas por opção, pra cada pergunta categórica do formulário escolhido."""
    perguntas = FORM_PERGUNTAS.get(tipo_formulario, [])
    df = data.get(tipo_formulario)
    if df is None or df.empty or not perguntas:
        return pd.DataFrame(columns=["pergunta", "resposta", "pct"])
    melted = df[perguntas].melt(var_name="pergunta", value_name="resposta")
    contagem = melted.groupby(["pergunta", "resposta"]).size().reset_index(name="n")
    contagem["pct"] = contagem["n"] / contagem.groupby("pergunta")["n"].transform("sum")
    return contagem