import sys
import unittest
from pathlib import Path
from src.dados import consultar_censo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.seguranca import validar_sql


class TestarSegurancaSQL(unittest.TestCase):

    def test_aceita_select(self):
        valido, _ = validar_sql("SELECT 1")
        self.assertTrue(valido)

    def test_bloqueia_delete(self):
        valido, _ = validar_sql("DELETE FROM escolar")
        self.assertFalse(valido)
    
    def test_bloqueia_duas_consultas(self):
        valido, _ = validar_sql("SELECT 1; SELECT 2")
        self.assertFalse(valido)

    def test_bloqueia_sql_invalido(self):
        valido, _ = validar_sql("SELEC errado")
        self.assertFalse(valido)

    def test_consulta_censo_bloqueia_delete(self):
        with self.assertRaises(ValueError):
            consultar_censo("DELETE FROM escolas")

    def test_bloqueia_leitura_de_outro_arquivo(self):
        sql = "SELECT * FROM read_csv('outro_arquivo.csv')"
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_tabela_nao_autorizada(self):
        valido, _ = validar_sql("SELECT * FROM escolas")
        self.assertFalse(valido)

    def test_bloqueia_duas_fontes_de_dados(self):
        sql = """
        SELECT *
        FROM read_csv(?, delim=';') AS a
        JOIN read_csv('outro_arquivo.csv', delim=';') AS b
        ON TRUE
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_leitura_de_json(self):
        sql = "SELECT * FROM read_json('outro_arquivo.json')"
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_leitura_de_parquet(self):
        sql = "SELECT * FROM read_parquet('outro_arquivo.parquet')"
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_aceita_leitura_parametrizada_do_censo(self):
        sql = """
        SELECT NO_UF
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertTrue(valido)

    def test_bloqueia_funcao_nao_autorizada(self):
        sql = """
        SELECT current_setting('memory_limit')
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_subconsulta_com_outra_fonte(self):
        sql = """
        SELECT NO_UF
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        WHERE NO_UF IN (
            SELECT NO_UF
            FROM read_csv('outro_arquivo.csv')
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)
    
    def test_bloqueia_select_asterisco(self):
        sql = """
        SELECT *
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    
    def test_bloqueia_from_duplicado(self):
        sql = """
        SELECT NO_UF, COUNT(*) AS quantidade_escolas
        FROM FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        GROUP BY NO_UF
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_limita_resultado_a_mil_registros(self):
        from unittest.mock import patch

        resultado_falso = [(i,) for i in range(1000)]

        with patch(
            "src.dados.localizar_arquivo_censo"
        ), patch(
            "src.dados.conectar_duckdb"
        ) as mock_conectar:
            conexao = mock_conectar.return_value.__enter__.return_value
            conexao.execute.return_value.fetchall.return_value = resultado_falso

            resultado = consultar_censo("""
                SELECT NO_UF
                FROM read_csv(
                    ?, delim=';', encoding='latin-1',
                    header=true, all_varchar=true
                )
                LIMIT 5000
            """)

        self.assertLessEqual(len(resultado), 1000)
        sql_executado = conexao.execute.call_args.args[0]
        self.assertIn("LIMIT 1000", sql_executado.upper())
    
    def test_bloqueia_coluna_nao_autorizada(self):
        sql = """
        SELECT coluna_inventada
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_aceita_coluna_permitida_com_alias(self):
        sql = """
        SELECT NO_UF AS estado
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertTrue(valido)


    def test_aceita_funcao_agregada(self):
        sql = """
        SELECT COUNT(*), SUM(1), AVG(1)
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertTrue(valido)

    def test_bloqueia_limite_negativo(self):
        with self.assertRaises(ValueError):
            consultar_censo("""
                SELECT NO_UF
                FROM read_csv(
                    ?, delim=';', encoding='latin-1',
                    header=true, all_varchar=true
                )
                LIMIT -1
            """)
    def test_estimativa_custo_consulta_simples(self):
        from src.dados import estimar_custo_consulta

        resultado = estimar_custo_consulta("SELECT 1")

        self.assertEqual(resultado["nivel"], "baixo")
        self.assertIn("pontuacao", resultado)
        self.assertIn("fatores", resultado)

    def test_estimativa_custo_consulta_com_agrupamento(self):
        from src.dados import estimar_custo_consulta

        sql = """
            SELECT NO_UF, COUNT(*)
            FROM read_csv(
                ?, delim=';', encoding='latin-1',
                header=true, all_varchar=true
            )
            GROUP BY NO_UF
            ORDER BY COUNT(*) DESC
        """

        resultado = estimar_custo_consulta(sql)

        self.assertEqual(resultado["nivel"], "alto")
        self.assertIn("agrupamento de registros", resultado["fatores"])
        self.assertIn("ordenação dos resultados", resultado["fatores"])

    def test_estimativa_rejeita_sql_proibido(self):
        from src.dados import estimar_custo_consulta

        with self.assertRaises(ValueError):
            estimar_custo_consulta("DELETE FROM escolas")

    def test_consulta_censo_com_custo_retorna_resultado_e_estimativa(self):
        from unittest.mock import patch
        from src.dados import consultar_censo_com_custo

        resultado_falso = [("São Paulo", 100)]
        estimativa_falsa = {
            "pontuacao": 3,
            "nivel": "baixo",
            "fatores": ["custo básico da consulta"],
            "aviso": "Estimativa de teste.",
        }

        with patch(
            "src.dados.estimar_custo_consulta",
            return_value=estimativa_falsa,
        ), patch(
            "src.dados.consultar_censo",
            return_value=resultado_falso,
        ):
            resposta = consultar_censo_com_custo("SELECT 1")

        self.assertEqual(resposta["resultado"], resultado_falso)
        self.assertEqual(
            resposta["estimativa_custo"],
            estimativa_falsa,
        )
    def test_bloqueia_duas_fontes_parametrizadas(self):
        sql = """
        SELECT *
        FROM read_csv(?, delim=';') AS a
        JOIN read_csv(?, delim=';') AS b
        ON TRUE
        """

        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_read_csv_auto(self):
        sql = """
        SELECT NO_UF
        FROM read_csv_auto(
            ?, delim=';', header=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

    def test_bloqueia_informacao_do_usuario_sql(self):
        sql = """
        SELECT CURRENT_USER
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        """
        valido, _ = validar_sql(sql)
        self.assertFalse(valido)

if __name__ == "__main__":
    unittest.main()