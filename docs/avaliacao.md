# Avaliação do Sistema

## 1. Objetivo da avaliação

A avaliação foi realizada para verificar se o assistente consegue interpretar perguntas em linguagem natural, gerar consultas SQL válidas e retornar os resultados esperados a partir dos microdados do Censo Escolar 2024.

Também foi feita uma comparação com um método mais simples, utilizado como baseline.

## 2. Avaliação do modelo

Foram utilizadas 50 perguntas para testar o modelo Qwen 2.5 3B, executado localmente pelo Ollama.

O modelo acertou 47 das 50 perguntas, alcançando uma acurácia de 94%.

Os resultados foram comparados com consultas SQL de referência, considerando se a execução retornava os mesmos resultados esperados.

## 3. Comparação com o baseline

O baseline foi submetido às mesmas 50 perguntas utilizadas na avaliação do sistema principal, utilizando o modelo Qwen 2.5 3B e um prompt simplificado, com informações básicas sobre a fonte de dados e as colunas disponíveis.

Os resultados foram:

- Perguntas testadas: 50
- Consultas bloqueadas pelo validador: 46
- Erros de execução: 2
- Consultas executadas corretamente: 2
- Acurácia entre as consultas executadas: 100%
- Taxa de acerto considerando as 50 perguntas: 4%

As duas consultas executadas corretamente foram as perguntas 37 e 38. A maioria das consultas foi bloqueada porque o modelo informou caminhos de arquivos diretamente, em vez de utilizar o parâmetro esperado pelo sistema. Também ocorreram tentativas de utilizar funções e colunas não autorizadas.

Embora a acurácia entre as consultas executadas tenha sido de 100%, esse percentual considera apenas duas consultas. Para a comparação geral, considerando as 50 perguntas, o baseline apresentou taxa de acerto de 4%, enquanto o sistema principal alcançou 94%.

Os resultados indicam que o prompt simplificado teve desempenho inferior ao prompt completo utilizado pelo sistema principal.

## 4. Avaliação das explicações

Também foram analisadas 10 explicações geradas pelo sistema para verificar se os resultados das consultas eram apresentados de maneira compreensível.

Dessas explicações, 2 foram consideradas boas e 8 parcialmente adequadas. Foram identificadas algumas imprecisões nas descrições de aspectos como limite de linhas, leitura do CSV e tratamento de valores nulos.

## 5. Considerações sobre os resultados

Os testes mostram que o modelo Qwen 2.5 3B conseguiu responder corretamente à maior parte das perguntas utilizadas na avaliação.

Apesar do resultado de 94%, ainda existem casos em que a consulta gerada não corresponde exatamente ao resultado esperado. As explicações também podem apresentar imprecisões, indicando pontos que precisam ser melhorados.

Os resultados completos e os arquivos utilizados na avaliação estão disponíveis na pasta `evidencias/` do projeto.
