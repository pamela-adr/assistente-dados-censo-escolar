# Avaliação do Sistema

## 1. Objetivo da avaliação

A avaliação foi realizada para verificar se o assistente consegue interpretar perguntas em linguagem natural, gerar consultas SQL válidas e retornar os resultados esperados a partir dos microdados do Censo Escolar 2024.

Também foi feita uma comparação com um método mais simples, utilizado como baseline.

## 2. Avaliação do modelo

Foram utilizadas 50 perguntas para testar o modelo Qwen 2.5 3B, executado localmente pelo Ollama.

O modelo acertou 47 das 50 perguntas, alcançando uma acurácia de 94%.

Os resultados foram comparados com consultas SQL de referência, considerando se a execução retornava os mesmos resultados esperados.

## 3. Comparação com o baseline

O baseline foi submetido às mesmas 50 perguntas. Entretanto, nenhuma das consultas foi executada: as 50 foram bloqueadas.

Por esse motivo, não foi possível calcular sua acurácia. O resultado demonstra que o método utilizado como baseline não conseguiu atender às perguntas avaliadas.

## 4. Avaliação das explicações

Também foram analisadas 10 explicações geradas pelo sistema para verificar se os resultados das consultas eram apresentados de maneira compreensível.

Dessas explicações, 2 foram consideradas boas e 8 parcialmente adequadas. Foram identificadas algumas imprecisões nas descrições de aspectos como limite de linhas, leitura do CSV e tratamento de valores nulos.

## 5. Considerações sobre os resultados

Os testes mostram que o modelo Qwen 2.5 3B conseguiu responder corretamente à maior parte das perguntas utilizadas na avaliação.

Apesar do resultado de 94%, ainda existem casos em que a consulta gerada não corresponde exatamente ao resultado esperado. As explicações também podem apresentar imprecisões, indicando pontos que precisam ser melhorados.

Os resultados completos e os arquivos utilizados na avaliação estão disponíveis na pasta `evidencias/` do projeto.
