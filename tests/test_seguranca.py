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

if __name__ == "__main__":
    unittest.main()    