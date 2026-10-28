from pathlib import Path

import duckdb
import sqlglot
from sqlglot import exp
try:
    from .seguranca import validar_sql
except ImportError:
    from seguranca import validar_sql

def localizar_arquivo_censo() -> Path:
    """Localiza o CSV do Censo Escolar 2024 na pasta Downloads."""
    pasta_usuario = Path.home()

    arquivo = (
        pasta_usuario
        / "Downloads"
        / "microdados_censo_escolar_2024_defeso"
        / "dados"
        / "microdados_ed_basica_2024.csv"
    )

    if not arquivo.is_file():
        raise FileNotFoundError(
            f"Arquivo do Censo Escolar não encontrado: {arquivo}"
        )

    return arquivo

   
def conectar_duckdb() -> duckdb.DuckDBPyConnection:
    """Cria uma conexão DuckDB em memória"""
    return duckdb.connect()

def obter_esquema_censo() -> list[str]:
    """Retorna os nomes das colunas do Censo Escolar."""
    arquivo = localizar_arquivo_censo()

    with conectar_duckdb() as conexao:
        resultado = conexao.execute(
            """
            DESCRIBE
            SELECT *
            FROM read_csv(
                ?, delim=';', encoding='latin-1',
                header=true, all_varchar=true
            )
            """,
            [str(arquivo)],
        ).fetchall()

    return [coluna[0] for coluna in resultado]

def estimar_custo_consulta(sql: str) -> dict:
    """Estima a complexidade estrutural de uma consulta SQL."""

    valido, mensagem = validar_sql(sql)

    if not valido:
        raise ValueError(mensagem)

    consultas = sqlglot.parse(sql, read="duckdb")
    consulta = consultas[0]

    pontos = 1
    fatores = ["custo básico da consulta"]

    # A leitura da fonte de dados exige processamento.
    if list(consulta.find_all(exp.Table)):
        pontos += 2
        fatores.append("leitura da fonte de dados")

    # Agrupar registros pode exigir processamento adicional.
    if consulta.args.get("group") is not None:
        pontos += 2
        fatores.append("agrupamento de registros")

    # Ordenar resultados também pode exigir processamento.
    if consulta.args.get("order") is not None:
        pontos += 2
        fatores.append("ordenação dos resultados")

    # DISTINCT pode exigir comparação entre registros.
    if consulta.args.get("distinct") is not None:
        pontos += 1
        fatores.append("remoção de duplicados")

    if pontos <= 3:
        nivel = "baixo"
    elif pontos <= 5:
        nivel = "médio"
    else:
        nivel = "alto"

    return {
        "pontuacao": pontos,
        "nivel": nivel,
        "fatores": fatores,
        "aviso": (
            "Estimativa heurística; não representa o custo real "
            "de execução do DuckDB."
        ),
    }


def contar_registros() -> int:
    """Conta as linhas do arquivo do Censo Escolar."""
    arquivo = localizar_arquivo_censo()

    with conectar_duckdb() as conexao:
        resultado = conexao.execute(
            """
            SELECT COUNT(*)
            FROM read_csv(
                ?, delim=';', encoding='latin-1',
                header=true, all_varchar=true
            )
            """,
            [str(arquivo)],
        ).fetchone()

    return resultado[0]


def consultar_censo(sql: str) -> list:
    """Executa uma consulta SQL validada, limitada a 1.000 resultados."""
    valido, mensagem = validar_sql(sql)

    if not valido:
        raise ValueError(mensagem)

    consultas = sqlglot.parse(sql, read="duckdb")
    consulta = consultas[0]

    # Adiciona o limite usando a estrutura do SQL.
    limite = consulta.args.get("limit")

    if limite is None:
        consulta = consulta.limit(1000)
    else:
        expressao_limite = limite.expression

        if (
            not isinstance(expressao_limite, exp.Literal)
            or not expressao_limite.is_int
        ):
            raise ValueError("O limite da consulta deve ser um número inteiro.")

        quantidade = int(expressao_limite.this)

        if quantidade > 1000:
            consulta = consulta.limit(1000)

    sql_seguro = consulta.sql(dialect="duckdb")
    arquivo = localizar_arquivo_censo()

    with conectar_duckdb() as conexao:
        resultado = conexao.execute(
            sql_seguro,
            [str(arquivo)],
        ).fetchall()

    return resultado

def consultar_censo_com_custo(sql: str):
    """Executa uma consulta e retorna também sua estimativa de custo."""

    estimativa = estimar_custo_consulta(sql)
    resultado = consultar_censo(sql)

    return {
        "resultado": resultado,
        "estimativa_custo": estimativa,
    }




if __name__ == "__main__":
    sql = """
        SELECT
            NO_UF,
            COUNT(*) AS quantidade_registros
        FROM read_csv(
            ?, delim=';', encoding='latin-1',
            header=true, all_varchar=true
        )
        GROUP BY NO_UF
        ORDER BY quantidade_registros DESC
        LIMIT 5
    """

    resultado = consultar_censo(sql)

    for linha in resultado:
        print(linha)
