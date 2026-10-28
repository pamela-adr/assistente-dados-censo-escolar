import re
import sqlglot
from sqlglot import exp
COLUNAS_PERMITIDAS = {
    "NO_UF",
    "SG_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "CO_ENTIDADE",
    "TP_DEPENDENCIA",
    "QT_MAT_BAS",
    "QT_TUR_BAS",
    "QT_DOC_BAS",
    "TP_SITUACAO_FUNCIONAMENTO",
}

def validar_sql(sql: str) -> tuple[bool, str]:
    """Permite SELECT com leitura parametrizada do Censo Escolar."""

    if re.search(r"\bFROM\s+FROM\b", sql, re.IGNORECASE):
        return False, "A consulta contém FROM duplicado."

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

    for estrela in consulta.find_all(exp.Star):
        if not isinstance(estrela.parent, exp.Count):
            return False, (
                "SELECT * não é permitido; "
                "use apenas colunas autorizadas."
            )

    colunas = list(consulta.find_all(exp.Column))

    for funcao in consulta.find_all(exp.Func):
        nome_funcao = funcao.sql_name().upper()

        if nome_funcao not in {
            "READ_CSV",
            "COUNT",
            "SUM",
            "AVG",
            "MIN",
            "MAX",
            "TRY_CAST",
            "NULLIF",
        }:
            return False, f"Função SQL não autorizada: {nome_funcao}"

    aliases_permitidos = {
        alias.alias.upper()
        for alias in consulta.find_all(exp.Alias)
        if alias.alias
    }

    for coluna in colunas:
        # Ignora os parâmetros internos da função read_csv.
        ancestral = coluna.parent

        dentro_de_read_csv = False

        while ancestral is not None:
            if (
                isinstance(ancestral, exp.Func)
                and ancestral.sql_name().upper() == "READ_CSV"
            ):
                dentro_de_read_csv = True
                break

            ancestral = ancestral.parent

        if dentro_de_read_csv:
            continue
        nome_coluna = coluna.name.upper()

        if (
            nome_coluna not in COLUNAS_PERMITIDAS
            and nome_coluna not in aliases_permitidos
        ):
            return False, f"Coluna SQL não autorizada: {coluna.name}"



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
