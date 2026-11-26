import unittest

from src.assistente import identificar_ambiguidade


class TestarIdentificacaoAmbiguidade(unittest.TestCase):

    def test_identifica_pergunta_ambigua(self):
        pergunta = "Quantas escolas existem?"

        resultado = identificar_ambiguidade(pergunta)

        self.assertIsNotNone(resultado)
        self.assertIn("CO_ENTIDADE", resultado)

    def test_nao_identifica_agrupamento_por_estado(self):
        pergunta = "Quantas escolas existem por estado?"

        resultado = identificar_ambiguidade(pergunta)

        self.assertIsNone(resultado)

    def test_nao_identifica_agrupamento_por_municipio(self):
        pergunta = "Quantas escolas existem por município?"

        resultado = identificar_ambiguidade(pergunta)

        self.assertIsNone(resultado)

    def test_nao_identifica_agrupamento_sem_acento(self):
        pergunta = "Quantas escolas existem por municipio?"

        resultado = identificar_ambiguidade(pergunta)

        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()