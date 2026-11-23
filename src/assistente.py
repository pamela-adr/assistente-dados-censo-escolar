
import os
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
EXEMPLO OBRIGATÓRIO — CONTAGEM DE REGISTROS DE UM ESTADO:

Pergunta: Quantos registros existem no estado do Paraná?

SQL esperado:
SELECT COUNT(*) AS quantidade_registros
FROM read_csv(?, delim=';', encoding='latin-1',
              header=true, all_varchar=true)
WHERE SG_UF = 'PR'
LIMIT 1000

Nesse tipo de pergunta:
- Não selecione SG_UF.
- Não utilize GROUP BY.
- Utilize a sigla correspondente do estado em SG_UF.
- Gere somente SELECT.
- A cláusula FROM deve conter a função read_csv completa:
  FROM read_csv(?, delim=';', encoding='latin-1',
                header=true, all_varchar=true)
- Nunca escreva FROM `?`, FROM '?', FROM file.csv
  ou FROM seguido de um caminho literal.
- O símbolo ? deve aparecer somente como primeiro argumento
  de read_csv, sem aspas nem crases.
- A chamada read_csv deve sempre começar exatamente assim:
  read_csv(?, delim=';', encoding='latin-1',
           header=true, all_varchar=true)
- Nunca omita a vírgula depois do argumento ?.
- Nunca altere os nomes das colunas autorizadas.
- Nunca invente nomes de colunas ou substitua letras
  dos nomes existentes.
- Não coloque read_csv entre crases.
- Use somente estas colunas:
  NO_UF, SG_UF, NO_MUNICIPIO, CO_MUNICIPIO, CO_ENTIDADE,
  TP_DEPENDENCIA, QT_MAT_BAS, QT_MAT_FUND, QT_MAT_MED,
  QT_MAT_INF, QT_TUR_BAS, QT_DOC_BAS,
  TP_SITUACAO_FUNCIONAMENTO, NO_REGIAO, TP_LOCALIZACAO,
  IN_INTERNET, IN_BIBLIOTECA, IN_QUADRA_ESPORTES,
  IN_AGUA_REDE_PUBLICA, IN_ENERGIA_REDE_PUBLICA,
  IN_BANDA_LARGA.
- ATENÇÃO: o nome correto é QT_MAT_FUND, começando por QT.
- Nunca escreva TQ_MAT_FUND. Essa coluna não existe.
- Antes de gerar o SQL, confira se cada nome de coluna
  está escrito exatamente como na lista autorizada.
- Os nomes das colunas devem ser copiados exatamente como
  aparecem na lista autorizada.
- Para matrículas da educação básica, utilize QT_MAT_BAS.
- Para matrículas do ensino fundamental, utilize QT_MAT_FUND.
- Para matrículas do ensino médio, utilize QT_MAT_MED.
- Para matrículas da educação infantil, utilize QT_MAT_INF.
- Sempre que a pergunta solicitar a soma ou o total de matrículas,
  utilize obrigatoriamente SUM() sobre a coluna correspondente.
- Educação básica: SUM(TRY_CAST(NULLIF(QT_MAT_BAS, '') AS BIGINT)).
- Ensino fundamental: SUM(TRY_CAST(NULLIF(QT_MAT_FUND, '') AS BIGINT)).
- Ensino médio: SUM(TRY_CAST(NULLIF(QT_MAT_MED, '') AS BIGINT)).
- Educação infantil: SUM(TRY_CAST(NULLIF(QT_MAT_INF, '') AS BIGINT)).
- Nunca retorne os valores individuais da coluna quando a pergunta
  solicitar a soma total.
- Não adicione GROUP BY quando a pergunta solicitar o total geral.
- As colunas QT_MAT_BAS, QT_MAT_FUND, QT_MAT_MED e QT_MAT_INF
  são lidas como texto. Antes de usar SUM, converta os valores
  com TRY_CAST(NULLIF(nome_da_coluna, '') AS BIGINT).
Exemplo obrigatório de soma de matrículas:
SELECT NO_UF,
       SUM(TRY_CAST(NULLIF(QT_MAT_FUND, '') AS BIGINT)) AS total_matriculas
FROM read_csv(?, delim=';', encoding='latin-1',
              header=true, all_varchar=true)
GROUP BY NO_UF
ORDER BY total_matriculas DESC
LIMIT 5

Sempre use esse padrão de conversão ao somar QT_MAT_FUND.
- Nunca utilize TQ_MAT_BAS, TQ_MAT_FUND,
  TQ_MAT_MED ou TQ_MAT_INF.
- NO_REGIAO armazena o nome da região geográfica,
  como 'Norte', 'Nordeste', 'Sudeste', 'Sul' e 'Centro-Oeste'.
- TP_LOCALIZACAO identifica a localização da escola:
  '1' representa urbana e '2' representa rural.
- NO_UF armazena o nome completo do estado, por exemplo:
  'São Paulo', 'Minas Gerais' e 'Bahia'.
- SG_UF armazena a sigla da unidade federativa, por exemplo:
  'SP', 'MG' e 'BA'.
- Quando a pergunta solicitar a quantidade de siglas de estados
  diferentes, utilize COUNT(DISTINCT SG_UF).
- Quando a pergunta solicitar a quantidade de municípios
  diferentes, utilize obrigatoriamente
  COUNT(DISTINCT CO_MUNICIPIO).
- Não utilize NO_MUNICIPIO para essa contagem.
- Nesse cálculo, utilize exclusivamente SG_UF.
- Nunca utilize NO_UF para contar siglas de estados.
- Nunca utilize CAST ou TRY_CAST em SG_UF.
- Quando a pergunta mencionar o nome completo de um estado,
  utilize NO_UF com o nome completo correspondente.
- Quando a pergunta mencionar a sigla de um estado,
  utilize SG_UF com a sigla correspondente.
- Nunca compare o nome completo do estado com SG_UF.
- Nunca compare a sigla do estado com NO_UF.
  utilize SG_UF e a sigla informada.
- Não utilize NO_UF para filtrar estados.
- Nunca utilize OR para combinar NO_UF e SG_UF em um mesmo filtro.
- Nunca tente combinar NO_UF e SG_UF em um mesmo filtro.
- Utilize exclusivamente SG_UF para filtrar estados.
- Quando receber o nome completo, converta-o para a sigla correspondente.
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
- Em perguntas que solicitam agrupamento por uma categoria,
  utilize exatamente a coluna dessa categoria no SELECT e GROUP BY.
- TP_DEPENDENCIA representa a dependência administrativa:
  '1' = Federal, '2' = Estadual, '3' = Municipal e '4' = Privada.
- Quando a pergunta solicitar registros por dependência administrativa,
  utilize COUNT(*) e GROUP BY TP_DEPENDENCIA.
- Quando a pergunta solicitar registros por localização,
  utilize COUNT(*) e GROUP BY TP_LOCALIZACAO.
- Quando a pergunta solicitar registros por região,
  utilize COUNT(*) e GROUP BY NO_REGIAO.
- Quando a pergunta solicitar quantas regiões diferentes existem,
  utilize COUNT(DISTINCT NO_REGIAO).
- Nesse caso, retorne somente a contagem de regiões distintas.
- Não utilize GROUP BY nessa consulta.
- EXEMPLO OBRIGATÓRIO — CONTAGEM DE REGISTROS POR REGIÃO:

Pergunta: Quantos registros existem por região do Brasil?

SQL esperado:
SELECT NO_REGIAO, COUNT(*) AS quantidade_registros
FROM read_csv(?, delim=';', encoding='latin-1',
              header=true, all_varchar=true)
GROUP BY NO_REGIAO
LIMIT 1000

- Gere somente uma consulta SQL.
- Utilize somente um FROM.
- Nunca acrescente outro FROM depois de LIMIT.
REGRAS OBRIGATÓRIAS DE FIDELIDADE À PERGUNTA:

- Utilize somente os filtros explicitamente solicitados pelo usuário.
- Nunca invente condições WHERE.
- Nunca exclua categorias que não foram solicitadas.
- Em perguntas sobre as categorias com MAIOR quantidade,
  agrupe todas as categorias, ordene por quantidade DESC
  e aplique LIMIT somente ao número solicitado.
- Em perguntas sobre as categorias com MENOR quantidade,
  agrupe todas as categorias, ordene por quantidade ASC
  e aplique LIMIT somente ao número solicitado.
- Em perguntas que solicitem agrupamento por estado,
  utilize NO_UF para identificar os estados no resultado.
- Para filtrar um estado específico, utilize SG_UF
  com sua sigla correspondente.
- Não confunda agrupamento por categoria com filtro por categoria.
- Antes de gerar o SQL, identifique quais filtros foram
  realmente solicitados na pergunta.
- Para agrupamentos por categoria, não inclua NO_UF ou SG_UF
  se a pergunta não solicitar informações por estado.
- Não inclua NO_UF ou SG_UF quando a pergunta não solicitar
  agrupamento ou filtro por estado.
- Em perguntas com ordenação, utilize obrigatoriamente:
  GROUP BY, ORDER BY e LIMIT, nessa ordem.
- Nunca coloque LIMIT antes de ORDER BY.
- Utilize somente um FROM com read_csv por consulta.
- Nunca acrescente outro FROM depois do LIMIT.
- DIFERENÇA ENTRE REGISTROS E ESCOLAS DISTINTAS:

- Quando a pergunta solicitar quantidade de registros,
  utilize COUNT(*).
- Quando solicitar quantidade de escolas distintas,
  utilize COUNT(DISTINCT CO_ENTIDADE).
- Quando solicitar escolas distintas por estado,
  utilize NO_UF e COUNT(DISTINCT CO_ENTIDADE),
  agrupando por NO_UF.
- Nunca utilize COUNT(*) para responder perguntas
  que solicitem explicitamente escolas distintas.
- Quando a pergunta solicitar quantidade de registros,
  utilize COUNT(*).
- Quando a pergunta solicitar somente a quantidade de registros
  que possuem determinado valor em uma categoria,
  retorne apenas COUNT(*) no SELECT.
- Nesse caso, aplique o valor solicitado no WHERE,
  sem selecionar a coluna da categoria e sem utilizar GROUP BY.
- Exemplo: para contar registros com TP_DEPENDENCIA igual a 3,
  utilize WHERE TP_DEPENDENCIA = '3'.
- Quando a pergunta solicitar a quantidade de registros de um
  único estado, utilize COUNT(*) e filtre pela coluna NO_UF
  ou SG_UF, conforme a pergunta.
- Nesse caso, não selecione a coluna do estado junto com COUNT(*).
- Não utilize GROUP BY quando a consulta contar registros
  de apenas um estado e não selecionar outra coluna.
- Quando utilizar COUNT(*) e selecionar também uma coluna
  não agregada, inclua essa coluna no GROUP BY.
- Quando solicitar total ou quantidade de matrículas,
  utilize SUM(TRY_CAST(NULLIF(QT_MAT_BAS, '') AS BIGINT)).
  A sintaxe de conversão é obrigatoriamente:
TRY_CAST(NULLIF(coluna, '') AS BIGINT).
Nunca substitua AS por vírgula.
- Nunca utilize COUNT(*) para responder perguntas sobre
  o total de matrículas.
- Quando a pergunta mencionar o nome completo de um estado,
  utilize SG_UF com a sigla correspondente.
- Nunca utilize NO_UF para filtrar estados.
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

    cliente = ollama.Client(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        timeout=180
    )

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

        if (
            not any(coluna in sql_normalizado for coluna in ("no_uf", "sg_uf"))
            or "group by" not in sql_normalizado
        ):
            raise ValueError(
                "SQL rejeitado: a contagem por estado precisa agrupar "
                "por NO_UF ou SG_UF."
            )

    return sql

def gerar_sql_baseline(pergunta: str) -> str:
    """Gera SQL usando uma instrução simples, sem o prompt principal."""

    cliente = ollama.Client(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        timeout=180
    )

    resposta = cliente.chat(
        model=MODELO,
        messages=[
            {
                "role": "system",
                "content": (
                    "Transforme a pergunta em uma consulta SQL DuckDB. "
                    "Retorne somente o SQL, sem Markdown ou explicações. "
                    "Use apenas SELECT."
                ),
            },
            {"role": "user", "content": pergunta},
        ],
    )

    return resposta.message.content.strip()


def explicar_sql(sql: str) -> str:
    """Explica em linguagem simples o que a consulta SQL faz."""

    cliente = ollama.Client(
        host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        timeout=180
    )

    resposta = cliente.chat(
        model=MODELO,
        messages=[
            {
                "role": "system",
                "content": (
                    "LIMIT apenas restringe a quantidade de linhas retornadas.\n"
                    "LIMIT não ordena os resultados nem seleciona os maiores valores.\n"
                    "Só diga que os resultados estão ordenados quando existir ORDER BY.\n"
                    "Sem ORDER BY, não afirme que existe uma ordem específica.\n"
                    "É proibido atribuir qualquer ordem aos resultados quando não houver ORDER BY.\n"
                    "Não interprete LIMIT como os maiores, menores, primeiros ou últimos valores.\n"
                    "Se houver LIMIT sem ORDER BY, diga apenas que a consulta limita a quantidade de linhas retornadas.\n"
                    "Explique a consulta SQL em português simples e "
                    "de forma curta.\n"
                    "GROUP BY agrupa pelos campos que aparecem após GROUP BY, "
                    "nunca pela função COUNT.\n"
                    "Não descreva read_csv como filtro; ele lê os dados do arquivo.\n"
                    "Não repita informações na explicação.\n"
                    "Descreva somente o que realmente aparece no SQL.\n"
                    "Explique o que é selecionado, os filtros, "
                    "agrupamentos, ordenação e limite, quando existirem.\n"
                    "COUNT(*) conta todas as linhas que atendem aos filtros.\n"
                    "LIMIT limita a quantidade de linhas retornadas, "
                    "não o total contado por COUNT(*).\n"
                    "GROUP BY reúne registros com o mesmo valor.\n"
                    "ORDER BY organiza os resultados.\n"
                    "NO_UF representa o nome do estado.\n"
                    "SG_UF representa a sigla do estado.\n"
                    "Não invente filtros, ordenações ou informações.\n"
                    "Não diga que uma contagem é aproximada sem motivo.\n"
                    "Não explique os parâmetros técnicos do CSV, "
                    "a menos que sejam importantes para a pergunta."
                    
                ),
            },
            {
                "role": "user",
                "content": f"Explique esta consulta SQL:\n{sql}",
            },
        ],
    )

    return resposta.message.content.strip()
if __name__ == "__main__":
    pergunta = input("Faça uma pergunta sobre o Censo Escolar: ")

def identificar_ambiguidade(pergunta: str) -> str | None:
    """Identifica perguntas que precisam de esclarecimento."""

    pergunta_normalizada = pergunta.casefold().strip()

    if (
        "quantas escolas" in pergunta_normalizada
        and "por estado" not in pergunta_normalizada
        and "por município" not in pergunta_normalizada
        and "por municipio" not in pergunta_normalizada
    ):
        return (
            "Você deseja contar os registros da base ou contar "
            "as escolas distintas pelo código CO_ENTIDADE?"
        )

    return None

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
