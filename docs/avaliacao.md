# Avaliação do Sistema

## 1. Objetivo da avaliação

A avaliação foi realizada para verificar se o assistente consegue interpretar perguntas em linguagem natural, gerar consultas SQL válidas e retornar os resultados esperados a partir dos microdados do Censo Escolar 2024.

Também foi feita uma comparação com um método mais simples, utilizado como baseline.

## 2. Avaliação do modelo

Foram utilizadas 50 perguntas para testar o modelo Qwen 2.5 3B, executado localmente pelo Ollama.

O modelo acertou 47 das 50 perguntas, alcançando uma acurácia de 94%.

Os resultados foram comparados com consultas SQL de referência, considerando se a execução retornava os mesmos resultados esperados.

## 3. Comparação com o baseline

Para comparar os resultados, utilizei as mesmas 50 perguntas da avaliação principal, mas com o modelo Qwen 2.5 3B e um prompt mais simples, contendo informações básicas sobre os dados e as colunas disponíveis.

O resultado foi:

- Perguntas testadas: 50.
- Consultas bloqueadas: 43.
- Erros de execução: 4.
- Consultas executadas corretamente: 2.
- Consultas executadas incorretamente: 1.
- Taxa de acerto geral: 4%.

As perguntas que tiveram respostas corretas foram a 22 e a 36. A maior parte das consultas foi bloqueada porque o modelo informou diretamente o caminho dos arquivos, em vez de utilizar o parâmetro esperado pelo sistema. Também aconteceram erros durante a execução de algumas consultas.

Das três consultas que chegaram a ser executadas e tiveram resultado comparável, duas estavam corretas, o que representa 66,67% de acerto. Considerando todas as 50 perguntas, o baseline teve 4% de acerto, enquanto o sistema principal alcançou 94%.

Com essa comparação, foi possível observar que o prompt mais completo utilizado no sistema principal apresentou resultados melhores do que o prompt simplificado do baseline.

Os resultados indicam que o prompt simplificado teve desempenho inferior ao prompt completo utilizado pelo sistema principal.

## 4. Avaliação das explicações

Também foram analisadas 10 explicações geradas pelo sistema para verificar se os resultados das consultas eram apresentados de maneira compreensível.

Dessas explicações, 2 foram consideradas boas e 8 parcialmente adequadas. Foram identificadas algumas imprecisões nas descrições de aspectos como limite de linhas, leitura do CSV e tratamento de valores nulos.

## 5. Considerações sobre os resultados

Os testes mostram que o modelo Qwen 2.5 3B conseguiu responder corretamente à maior parte das perguntas utilizadas na avaliação.

Apesar do resultado de 94%, ainda existem casos em que a consulta gerada não corresponde exatamente ao resultado esperado. As explicações também podem apresentar imprecisões, indicando pontos que precisam ser melhorados.

Os resultados completos e os arquivos utilizados na avaliação estão disponíveis na pasta `evidencias/` do projeto.
