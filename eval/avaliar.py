import json
from pathlib import Path

from src.dados import consultar_censo

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
    """Compara os cinco estados mais bem classificados."""

    referencia = [
        {"estado": estado, "registros": quantidade}
        for estado, quantidade in resultado_referencia
    ]

    return referencia == resultado_qwen


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

        if resultado_qwen is not None:
            valor_qwen = resultado_qwen["resultado_qwen"]

            if pergunta["tipo"] == "contagem":
                comparacao = comparar_contagem(
                    resultado_referencia,
                    valor_qwen
                )

            elif pergunta["tipo"] == "soma":
                comparacao = comparar_soma(
                    resultado_referencia,
                    valor_qwen
                )

            elif pergunta["tipo"] == "agrupamento":
                comparacao = comparar_agrupamento(
                    resultado_referencia,
                    valor_qwen
                )

            elif pergunta["tipo"] == "ordenação":
                comparacao = comparar_ordenacao(
                    resultado_referencia,
                    valor_qwen
                )

        resultados.append({
            "id": pergunta["id"],
            "pergunta": pergunta["pergunta"],
            "resultado_referencia": resultado_referencia,
            "resultado_qwen": resultado_qwen,
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
    resultados = avaliar_perguntas()

    for resultado in resultados:
        print(f"\nPergunta {resultado['id']}:")
        print(resultado["pergunta"])
        print("Resultado de referência:")
        print(resultado["resultado_referencia"])
        print("Comparação automática:", resultado["comparacao"])