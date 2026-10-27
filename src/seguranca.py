
import sqlglot
from sqlglot import exp


def validar_sql(sql: str) -> tuple[bool, str]:
    """Permite SELECT com leitura parametrizada do Censo Escolar."""

    try:
        consultas = sqlglot.parse(sql, read="duckdb")
    except sqlglot.errors.ParseError:
        return False, "A consulta SQL possui uma sintaxe inválida."

    if len(consultas) != 1 or consultas[0] is None:
        return False, "Envie apenas uma consulta SQL por vez."

    consulta = consultas[0]

    if not isinstance(consulta, exp.Select):
        return False, "Apenas consultas SELECT são permitidas."

    if consulta.args.get("into") is not None:
        return False, "Consultas que gravam resultados não são permitidas."

    tabelas = list(consulta.find_all(exp.Table))

    if len(tabelas) > 1:
        return False, "A consulta pode usar apenas uma fonte de dados."

    if not tabelas:
        funcoes = list(consulta.find_all(exp.Func))

        if funcoes:
            return False, "Funções SQL sem fonte de dados não são permitidas."

        return True, "Consulta aprovada na validação inicial."

    for funcao in consulta.find_all(exp.Anonymous):
        if funcao.name.upper() != "READ_CSV":
            return False, "Função SQL não autorizada."

    for tabela in tabelas:
        fonte = tabela.this

        if isinstance(fonte, exp.Func):
            nome_funcao = fonte.sql_name().upper()
        else:
            nome_funcao = ""

        if nome_funcao != "READ_CSV":
            return False, "Apenas a fonte de dados autorizada é permitida."

        caminho = fonte.this

        if not isinstance(caminho, exp.Placeholder):
            return False, "O caminho do arquivo deve ser parametrizado."

    return True, "Consulta aprovada na validação inicial."
