import ollama

MODELO = "qwen2.5:3b"


def perguntar_ao_modelo(pergunta: str) -> str:
    """Envia uma pergunta ao modelo local e retorna a resposta."""
    resposta = ollama.chat(
        model=MODELO,
        messages=[
        {
            "role":"user",
            "content": pergunta,
        }

      ]

    )

    return resposta.message.content



if __name__ == "__main__":
    pergunta = input("Faça uma pergunta: ")
    resposta = perguntar_ao_modelo(pergunta)

    print("\nResposta do assistente:")
    print(resposta)

    