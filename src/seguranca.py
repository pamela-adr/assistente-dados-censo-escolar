import sqlglot
from sqlglot import exp


def validar_sql(sql:str) -> tuple[bool, str]:
    """Permite apenas consultas SELECT simples."""

    try:
        consultas = sqlglot.parse(sql, read="duckdb")
    except sqlglot.errors.ParseError:
        return False, "A consulta SQL possui uma sintaxe inválida"
    
    if len(consultas) != 1 or consultas[0] is None:
        return False, "Envie apenas uma consulta SQL por vez."

    consulta = consultas[0]

    if not isinstance(consulta, exp.Select):
        return False, "Apenas consultas SELECT são permitidas."

    if consulta.args.get("into") is not None:
        return False, "Consultas que gravam resultados não são permitidas."

    return True, "Consulta aprovada na validação inicial"