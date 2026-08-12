"""
Conexão com o Supabase (Postgres) via SQLAlchemy + psycopg-binary.
Centraliza engine e carregamento das tabelas em um único objeto `db`,
instanciado no fim deste arquivo — dashboard.py e utils.py só consomem
`db.load_data()`, nenhum dos dois abre conexão diretamente.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

# chave usada no dashboard -> nome real da tabela no Supabase
TABELAS = {
    "users": "users",
    "lojas": "lojas",
    "pontuacoes": "pontuacoes",
    "brindes": "brindes",
    "resgates": "resgates",
    "boas_vindas": "interacoes_boas_vindas",
    "entrada_juquita": "interacoes_entrada_juquita",
    "acao_guerrilha": "interacoes_acao_guerrilha",
    "lounge_vip": "interacoes_lounge_vip",
    "estacionamento": "interacoes_estacionamento",
    "cenografia": "interacoes_cenografia",
    "dentro_lojas": "interacoes_dentro_lojas",
    "saida_juquita": "interacoes_saida_juquita",
    "saida_nps": "interacoes_saida_nps",
}

COLUNAS_REQUERIDAS = {
    "users": ["visitante_id", "pontos_atuais"],
    "lojas": ["id", "nome"],
    "pontuacoes": ["visitante_id", "loja_id", "pontos"],
    "brindes": ["id", "nome"],
    "resgates": ["brinde_id"],
    "boas_vindas": ["visitante_id", "created_at", "quem_eh_voce", "qual_foco", "regiao"],
    "entrada_juquita": ["visitante_id", "created_at", "item_ritmo", "faixa_etaria", "ficou_sabendo_onde"],
    "acao_guerrilha": ["visitante_id", "created_at", "oque_trouxe", "regiao"],
    "lounge_vip": ["visitante_id", "created_at", "prioridade", "quantas_sacolas"],
    "estacionamento": ["visitante_id", "created_at", "como_veio", "quanto_tempo"],
    "cenografia": ["visitante_id", "created_at", "oque_mais_garimpou", "qual_marca_deixou_louco"],
    "dentro_lojas": ["visitante_id", "created_at", "melhor_dia", "forma_pagamento"],
    "saida_juquita": ["visitante_id", "created_at", "qual_renda", "quanto_pretende_gastar", "com_quem_veio"],
    "saida_nps": ["visitante_id", "created_at", "quanto_recomenda", "maior_destaque", "te_vejo_proxima_edicao"],
}


class DataBaseManager:
    """Gerencia a conexão com o banco e o carregamento das tabelas em DataFrames."""

    def __init__(self, secrets_key: str = "supabase") -> None:
        self._secrets_key = secrets_key
        self._engine: Engine | None = None
        self.data: dict[str, pd.DataFrame] = {}

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = self._criar_conexao(self._secrets_key)
        return self._engine

    @staticmethod
    @st.cache_resource(show_spinner=False)
    def _criar_conexao(secrets_key: str) -> Engine:
        """Lê a URI de .streamlit/secrets.toml, ex.:

        [connections.supabase]
        uri = "postgresql+psycopg2://user:senha@host:5432/postgres"
        """
        uri = st.secrets["connections"][secrets_key]["uri"]
        return create_engine(uri, pool_pre_ping=True)

    def load_data(self) -> dict[str, pd.DataFrame]:
        """Carrega (com cache de 5 min) todas as tabelas usadas pelo dash."""
        self.data = self._carregar_tabelas(self.engine)
        return self.data

    @staticmethod
    @st.cache_data(ttl=300, show_spinner="Carregando dados do Supabase...")
    def _carregar_tabelas(_engine: Engine) -> dict[str, pd.DataFrame]:
        # _engine com underscore: instrui o st.cache_data a não tentar
        # hashear o objeto engine, só o restante dos argumentos (nenhum aqui)
        dados: dict[str, pd.DataFrame] = {}
        for chave, tabela in TABELAS.items():
            colunas_requeridas = COLUNAS_REQUERIDAS.get(chave, [])
            colunas_disponiveis = {col["name"] for col in inspect(_engine).get_columns(tabela)}
            colunas = [col for col in colunas_requeridas if col in colunas_disponiveis]

            if not colunas:
                dados[chave] = pd.read_sql_table(tabela, _engine)
            else:
                dados[chave] = pd.read_sql_table(tabela, _engine, columns=colunas)
        return dados


db = DataBaseManager()