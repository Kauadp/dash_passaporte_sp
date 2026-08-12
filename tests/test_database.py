import unittest
from unittest.mock import patch

import pandas as pd

import database


class TestDatabaseLoad(unittest.TestCase):
    @patch("database.inspect")
    @patch("database.pd.read_sql_table")
    def test_load_data_uses_requested_columns_only(self, mock_read_sql_table, mock_inspect):
        mock_read_sql_table.return_value = pd.DataFrame({"id": [1]})

        available = {
            "users": [{"name": "visitante_id"}, {"name": "pontos_atuais"}],
            "lojas": [{"name": "id"}, {"name": "nome"}],
            "pontuacoes": [{"name": "visitante_id"}, {"name": "loja_id"}, {"name": "pontos"}],
            "brindes": [{"name": "id"}, {"name": "nome"}],
            "resgates": [{"name": "brinde_id"}],
            "interacoes_boas_vindas": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "quem_eh_voce"}],
            "interacoes_entrada_juquita": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "item_ritmo"}],
            "interacoes_acao_guerrilha": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "oque_trouxe"}],
            "interacoes_lounge_vip": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "prioridade"}],
            "interacoes_estacionamento": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "como_veio"}],
            "interacoes_cenografia": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "qual_marca_deixou_louco"}],
            "interacoes_dentro_lojas": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "melhor_dia"}],
            "interacoes_saida_juquita": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "qual_renda"}],
            "interacoes_saida_nps": [{"name": "visitante_id"}, {"name": "created_at"}, {"name": "quanto_recomenda"}],
        }

        def fake_inspect(_engine):
            class FakeInspector:
                @staticmethod
                def get_columns(table_name):
                    return available.get(table_name, [])

            return FakeInspector()

        mock_inspect.side_effect = fake_inspect

        database.DataBaseManager._carregar_tabelas(object())

        for chave, tabela in database.TABELAS.items():
            expected_cols = [
                col for col in database.COLUNAS_REQUERIDAS.get(chave, []) if col in {item["name"] for item in available.get(tabela, [])}
            ]
            matches = [
                call for call in mock_read_sql_table.call_args_list
                if call.args[0] == tabela
            ]
            self.assertTrue(matches, f"Tabela {tabela} não foi carregada")
            if expected_cols:
                self.assertIn("columns", matches[0].kwargs)
                self.assertEqual(matches[0].kwargs["columns"], expected_cols)


if __name__ == "__main__":
    unittest.main()
