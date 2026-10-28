
import ollama

try:
    from .seguranca import validar_sql
except ImportError:
    from seguranca import validar_sql

try:
    from .dados import consultar_censo_com_custo
except ImportError:
    from dados import consultar_censo_com_custo

MODELO = "qwen2.5:3b"

PROMPT_SISTEMA = """
Você transforma perguntas sobre o Censo Escolar 2024 em SQL DuckDB.

Retorne somente uma consulta SQL, sem Markdown ou explicações.

Regras:
- Gere somente SELECT.
- A cláusula FROM deve conter a função read_csv completa:
  FROM read_csv(?, delim=';', encoding='latin-1',
                header=true, all_varchar=true)
- Nunca escreva FROM `?`, FROM '?', FROM file.csv
  ou FROM seguido de um caminho literal.
- O símbolo ? deve aparecer somente como primeiro argumento
  de read_csv, sem aspas nem crases.
- Não coloque read_csv entre crases.
- Use somente estas colunas:
  NO_UF, SG_UF, NO_MUNICIPIO, CO_MUNICIPIO, CO_ENTIDADE,
  TP_DEPENDENCIA, QT_MAT_BAS, QT_TUR_BAS, QT_DOC_BAS,
  TP_SITUACAO_FUNCIONAMENTO.
- Para cálculos numéricos, use:
  TRY_CAST(NULLIF(NOME_DA_COLUNA, '') AS BIGINT)
- Trate valores vazios como NULL, não como zero.
- Use LIMIT 1000 ou menos.
- Não use outras tabelas ou fontes de dados.
- Para contar escolas por estado, selecione NO_UF e COUNT(*),
  agrupe por NO_UF e use o alias quantidade_escolas.
- Escreva FROM apenas uma vez. Nunca gere FROM FROM.
- A estrutura correta da consulta é:
  SELECT NO_UF, COUNT(*) AS quantidade_escolas
  FROM read_csv(?, delim=';', encoding='latin-1',
                header=true, all_varchar=true)
  GROUP BY NO_UF
  LIMIT 1000
- Para contar todas as escolas por estado, não adicione filtro
  por TP_DEPENDENCIA.
- TP_DEPENDENCIA contém os códigos '1', '2', '3' e '4',
  não as letras E, M ou P.
- Não invente filtros que não foram solicitados.
- Não confunda contagem de registros com quantidade de matrículas.
16. A chamada read_csv deve ser uma função SQL, nunca um nome entre crases.
17. O primeiro argumento de read_csv deve ser exatamente ? sem aspas.
18. Não use nomes como file.csv, caminho_do_arquivo ou qualquer caminho literal.
19. Inclua obrigatoriamente delim=';', encoding='latin-1',
    header=true e all_varchar=true.
20. Se não conseguir seguir exatamente essas regras, gere novamente
    uma consulta que respeite todas elas.
"""


def perguntar_ao_modelo(pergunta: str) -> str:
    """Gera uma consulta SQL usando o modelo local."""
    resposta = ollama.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": pergunta},
        ],
    )

    return resposta.message.content.strip()


import re


def corrigir_parametro_csv(sql: str) -> str:
    """Corrige apenas o parâmetro ? entre aspas no read_csv."""
    return re.sub(
        r"""(read_csv\s*\(\s*)['"]\?['"]""",
        r"\1?",
        sql,
        flags=re.IGNORECASE,
    )


def gerar_sql_validado(pergunta: str) -> str:
    """Gera SQL e verifica as regras de segurança e a intenção da pergunta."""
    sql = perguntar_ao_modelo(pergunta)

    print("\nSQL bruto gerado pelo modelo:")
    print(repr(sql))

    sql = corrigir_parametro_csv(sql)

    print("\nSQL após corrigir o parâmetro:")
    print(sql)

    valido, mensagem = validar_sql(sql)

    if not valido:
        raise ValueError(f"SQL rejeitado: {mensagem}")

    pergunta_normalizada = pergunta.casefold()

    if "quantas escolas" in pergunta_normalizada and "estado" in pergunta_normalizada:
        sql_normalizado = sql.casefold()

        if "count(" not in sql_normalizado:
            raise ValueError(
                "SQL rejeitado: a pergunta pede uma contagem, "
                "mas o modelo não gerou uma função COUNT."
            )

        if "no_uf" not in sql_normalizado or "group by" not in sql_normalizado:
            raise ValueError(
                "SQL rejeitado: a contagem por estado precisa agrupar por NO_UF."
            )

    return sql


if __name__ == "__main__":
    pergunta = input("Faça uma pergunta sobre o Censo Escolar: ")

    try:
        sql = gerar_sql_validado(pergunta)

        print("\nSQL aprovado:")
        print(sql)

        resultado = consultar_censo_com_custo(sql)

        print("\nEstimativa de custo:")
        print(resultado["estimativa_custo"])

        print("\nResultado da consulta:")
        for linha in resultado["resultado"]:
            print(linha)

        if not resultado["resultado"]:
            print("A consulta não retornou registros.")

    except Exception as erro:
        print(f"\nNão foi possível concluir a consulta: {erro}")
