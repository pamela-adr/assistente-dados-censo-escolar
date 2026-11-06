
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
- NO_UF armazena o nome completo do estado, por exemplo:
  'São Paulo', 'Minas Gerais' e 'Bahia'.
- SG_UF armazena a sigla da unidade federativa, por exemplo:
  'SP', 'MG' e 'BA'.
- Quando a pergunta mencionar o nome de um estado,
  utilize NO_UF.
- Quando a pergunta mencionar a sigla de um estado,
  utilize SG_UF.
- Nunca compare uma sigla com a coluna NO_UF.
- Nunca compare o nome completo de um estado com SG_UF.
- NO_UF e SG_UF são colunas textuais.
- Nunca utilize TRY_CAST ou CAST nessas duas colunas.
- Nunca converta nomes ou siglas de estados para números.
- Para cálculos numéricos, converta a coluna numérica utilizada
na consulta com:
TRY_CAST(NULLIF(COLUNA_NUMERICA_AUTORIZADA, '') AS BIGINT)

COLUNA_NUMERICA_AUTORIZADA é apenas um marcador de posição.
Substitua-o pelo nome real de uma coluna numérica autorizada.
Nunca utilize literalmente esse marcador ou NOME_DA_COLUNA
como se fossem colunas existentes.
Não converta nomes ou siglas de estados para números.
- Trate valores vazios como NULL, não como zero.
- Use LIMIT 1000 ou menos.
- Respeite sempre esta ordem das cláusulas SQL:
  SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY e LIMIT.
- Nunca coloque WHERE depois de GROUP BY, ORDER BY ou LIMIT.
- Todos os filtros solicitados devem aparecer antes de GROUP BY.
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
- DIFERENÇA ENTRE REGISTROS E MATRÍCULAS:

- Quando a pergunta solicitar quantidade de registros,
  utilize COUNT(*).
- Quando solicitar total ou quantidade de matrículas,
  utilize SUM(TRY_CAST(NULLIF(QT_MAT_BAS, '') AS BIGINT)).
  A sintaxe de conversão é obrigatoriamente:
TRY_CAST(NULLIF(coluna, '') AS BIGINT).
Nunca substitua AS por vírgula.
- Nunca utilize COUNT(*) para responder perguntas sobre
  o total de matrículas.
- Se a pergunta mencionar o nome completo de um estado,
  utilize NO_UF com o nome completo.
- Não utilize SG_UF quando a pergunta informar o nome
  completo do estado.
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

    cliente = ollama.Client(timeout=180)

    resposta = cliente.chat(
        model=MODELO,
        messages=[
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": pergunta},
        ],
    )

    return resposta.message.content.strip()

import re


def corrigir_parametro_csv(sql: str) -> str:
    """Corrige erros comuns nos parâmetros do read_csv."""

    # Corrige o parâmetro ? quando aparece entre aspas.
    sql = re.sub(
        r"""(read_csv\s*\(\s*)['"]\?['"]""",
        r"\1?",
        sql,
        flags=re.IGNORECASE,
    )

    # Corrige all_varchars para all_varchar.
    sql = re.sub(
        r"\ball_varchars\b",
        "all_varchar",
        sql,
        flags=re.IGNORECASE,
    )

    return sql


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
