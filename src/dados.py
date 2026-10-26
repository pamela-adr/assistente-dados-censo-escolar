import os
from pathlib import Path

import duckdb


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


if __name__ == "__main__":
    print("Total de registros:", contar_registros())