import sys
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()    