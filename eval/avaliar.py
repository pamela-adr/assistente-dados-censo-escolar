import json
from pathlib import Path

from src.dados import consultar_censo
from src.assistente import gerar_sql_validado

def carregar_perguntas() -> list:
    """Carrega as perguntas de avaliação do arquivo JSON."""

    caminho = Path(__file__).parent / "perguntas.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        perguntas = json.load(arquivo)

    return perguntas

def carregar_resultados_qwen() -> list:
    """Carrega os resultados registrados do Qwen."""

    caminho = Path(__file__).parent / "resultados_qwen.json"

    with open(caminho, "r", encoding="utf-8") as arquivo:
        resultados = json.load(arquivo)

    return resultados

def salvar_resultados_qwen(resultados: list) -> None:
    """Salva os resultados da avaliação em JSON."""
    caminho = Path(__file__).parent / "resultados_qwen.json"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(
            resultados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )

def executar_pergunta_qwen(pergunta: dict) -> dict:
    """Gera, valida e executa o SQL de uma pergunta."""

    sql = gerar_sql_validado(pergunta["pergunta"])
    resultado = consultar_censo(sql)

    if pergunta["tipo"] in ("contagem", "soma"):
        resultado_qwen = resultado[0][0]

    elif pergunta["tipo"] == "agrupamento":
        resultado_qwen = [
            {
                "estado": linha[0],
                "registros": linha[1]
            }
            for linha in resultado
        ]

    elif pergunta["tipo"] == "ordenação":
        resultado_qwen = [
            [linha[0], linha[1]]
            for linha in resultado
        ]

    else:
        raise ValueError(
            f"Tipo de avaliação não reconhecido: {pergunta['tipo']}"
        )

    return {
        "id": pergunta["id"],
        "pergunta": pergunta["pergunta"],
        "sql_gerado": sql,
        "status": "executada",
        "resultado_qwen": resultado_qwen
    }

def executar_lote(tamanho_lote: int = 5) -> None:
    """Executa até cinco perguntas que ainda não foram concluídas."""

    perguntas = carregar_perguntas()
    resultados = carregar_resultados_qwen()

    ids_concluidos = {
        item["id"]
        for item in resultados
        if item["status"] == "executada"
    }

    pendentes = [
        pergunta
        for pergunta in perguntas
        if pergunta["id"] not in ids_concluidos
    ]

    lote = pendentes[:tamanho_lote]

    if not lote:
        print("Não existem perguntas pendentes.")
        return

    print(f"\nExecutando lote com {len(lote)} pergunta(s).")

    for pergunta in lote:
        print(f"\nProcessando pergunta {pergunta['id']}...")

        try:
            resultado = executar_pergunta_qwen(pergunta)

        except Exception as erro:
            resultado = {
                "id": pergunta["id"],
                "pergunta": pergunta["pergunta"],
                "status": "erro",
                "erro": str(erro)
            }

        resultados = [
            item
            for item in resultados
            if item["id"] != pergunta["id"]
        ]

        resultados.append(resultado)

        salvar_resultados_qwen(resultados)

        print("Status:", resultado["status"])

    print("\nLote finalizado.")

def localizar_resultado_qwen(
    resultados_qwen: list,
    id_pergunta: int
):
    """Localiza o resultado do Qwen pelo ID da pergunta."""

    for resultado in resultados_qwen:
        if resultado["id"] == id_pergunta:
            return resultado

    return None

def comparar_resultados(
    resultado_referencia,
    resultado_qwen
) -> bool:
    """Verifica se os resultados são iguais."""

    return resultado_referencia == resultado_qwen

def comparar_contagem(
    resultado_referencia,
    resultado_qwen
) -> bool:
    """Compara resultados de consultas de contagem."""

    total_referencia = resultado_referencia[0][0]

    return total_referencia == resultado_qwen

def comparar_soma(
    resultado_referencia,
    resultado_qwen
) -> bool:
    """Compara resultados de consultas de soma."""

    total_referencia = resultado_referencia[0][0]

    return total_referencia == resultado_qwen

def comparar_agrupamento(
    resultado_referencia,
    resultado_qwen
) -> bool:
    """Compara os registros agrupados por estado."""

    referencia = {
        estado: quantidade
        for estado, quantidade in resultado_referencia
    }

    qwen = {
        item["estado"]: item["registros"]
        for item in resultado_qwen
    }

    return referencia == qwen

def comparar_ordenacao(resultado_referencia, resultado_qwen):
    """Compara os estados e suas quantidades, respeitando a ordem."""

    referencia = [
        (estado, quantidade)
        for estado, quantidade in resultado_referencia
    ]

    if resultado_qwen and isinstance(resultado_qwen[0], dict):
        qwen = [
            (item["estado"], item["registros"])
            for item in resultado_qwen
        ]
    else:
        qwen = [
            (estado, quantidade)
            for estado, quantidade in resultado_qwen
        ]

    return referencia == qwen


def executar_referencia(sql: str):
    """Executa a consulta SQL de referência."""

    return consultar_censo(sql)


def avaliar_perguntas():
    """Executa e compara as consultas de referência."""

    perguntas = carregar_perguntas()
    resultados_qwen = carregar_resultados_qwen()
    resultados = []

    for pergunta in perguntas:
        resultado_referencia = executar_referencia(
            pergunta["sql_referencia"]
        )

        resultado_qwen = localizar_resultado_qwen(
            resultados_qwen,
            pergunta["id"]
        )

        comparacao = None
        valor_qwen = None

        if (
            resultado_qwen is not None
            and resultado_qwen.get("status") == "executada"
        ):
            valor_qwen = resultado_qwen["resultado_qwen"]

            if pergunta["tipo"] == "contagem":
                comparacao = comparar_contagem(
                    resultado_referencia, valor_qwen
                )

            elif pergunta["tipo"] == "soma":
                comparacao = comparar_soma(
                    resultado_referencia, valor_qwen
                )

            elif pergunta["tipo"] == "agrupamento":
                comparacao = comparar_agrupamento(
                    resultado_referencia, valor_qwen
                )

            elif pergunta["tipo"] == "ordenação":
                comparacao = comparar_ordenacao(
                    resultado_referencia, valor_qwen
                )

        resultados.append({
            "id": pergunta["id"],
            "pergunta": pergunta["pergunta"],
            "resultado_referencia": resultado_referencia,
            "resultado_qwen": valor_qwen,
            "comparacao": comparacao
        })

    avaliados = [
        resultado
        for resultado in resultados
        if resultado["comparacao"] is not None
    ]

    acertos = sum(
        resultado["comparacao"] is True
        for resultado in avaliados
    )

    total_avaliado = len(avaliados)

    acuracia = (
        acertos / total_avaliado * 100
        if total_avaliado > 0
        else 0
    )

    print(f"\nPerguntas avaliadas: {total_avaliado}")
    print(f"Acertos: {acertos}")
    print(f"Acurácia: {acuracia:.2f}%")

    return resultados

if __name__ == "__main__":
    executar_lote()

    resultados = avaliar_perguntas()
    for resultado in resultados:
        print(f"\nPergunta {resultado['id']}:")
        print(resultado["pergunta"])
        print("Resultado de referência:")
        print(resultado["resultado_referencia"])
        print("Comparação automática:", resultado["comparacao"])