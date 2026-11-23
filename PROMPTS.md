# Registro de uso de inteligência artificial

Este documento reúne interações com ferramentas de inteligência artificial utilizadas durante o desenvolvimento do Assistente de Dados Educacionais. O objetivo é registrar como essas ferramentas auxiliaram na implementação, nos testes e na análise do projeto.

## 1. Leitura dos microdados do Censo Escolar

**Prompt (resumo):** Como localizar e ler o arquivo CSV dos microdados do Censo Escolar 2024 utilizando Python e DuckDB?

**Resumo da resposta:** Foi apresentada uma solução para localizar o arquivo na pasta Downloads e realizar a leitura utilizando DuckDB.

**Decisão:** Aceita e adaptada. A abordagem foi aproveitada porque permitiu realizar a leitura dos microdados, mas o caminho do arquivo foi ajustado à estrutura utilizada no projeto.

## 2. Contagem de registros

**Prompt (resumo):** Como contar os registros do arquivo do Censo Escolar utilizando DuckDB?

**Resumo da resposta:** Foi apresentada uma consulta SQL com `COUNT(*)` para obter a quantidade total de registros.

**Decisão:** Aceita. A consulta foi utilizada por atender à necessidade de contar os registros do conjunto de dados.

## 3. Validação de consultas SQL

**Prompt (resumo):** Como utilizar SQLGlot para permitir apenas consultas SELECT e bloquear comandos que possam modificar os dados?

**Resumo da resposta:** Foi apresentada uma validação da estrutura da consulta antes da execução.

**Decisão:** Aceita e ampliada. A estrutura foi aproveitada, mas recebeu validações adicionais para atender aos requisitos de segurança do projeto, incluindo testes para comandos proibidos.

## 4. Criação de testes automatizados

**Prompt (resumo):** Como criar testes para verificar se a validação SQL aceita consultas permitidas e bloqueia comandos proibidos?

**Resumo da resposta:** Foram apresentados exemplos utilizando `unittest`.

**Decisão:** Aceita e adaptada. Os exemplos foram utilizados como base e ajustados às funções e à estrutura do projeto para verificar os comportamentos esperados.

## 5. Integração com o modelo local

**Prompt (resumo):** Como utilizar o Ollama com o modelo Qwen 2.5 3B para transformar perguntas em linguagem natural em consultas SQL?

**Resumo da resposta:** Foi apresentada uma estrutura de comunicação com o modelo e orientações para organizar o prompt.

**Decisão:** Aceita e adaptada. A abordagem foi incorporada ao assistente, com ajustes realizados durante os testes para adequar a geração de consultas ao esquema dos dados.

## 6. Interface com Streamlit

**Prompt (resumo):** Como apresentar as consultas geradas e os resultados em uma interface utilizando Streamlit?

**Resumo da resposta:** Foram apresentadas orientações para exibir tabelas e gráficos.

**Decisão:** Aceita e adaptada. A solução foi utilizada porque atendia à necessidade de apresentar os resultados de forma visual, com ajustes à interface do projeto.

## 7. Tratamento de perguntas ambíguas

**Prompt (resumo):** Como identificar perguntas que precisam de esclarecimento antes da geração da consulta SQL?

**Resumo da resposta:** Foi sugerida uma verificação de termos na pergunta para identificar situações ambíguas.

**Decisão:** Parcialmente aceita e adaptada. A ideia foi aproveitada, mas a lógica foi ajustada para identificar situações específicas e solicitar esclarecimentos antes de gerar a consulta.

## 8. Estimativa de custo das consultas

**Prompt (resumo):** Como estimar o custo de uma consulta SQL e apresentar essa estimativa junto com o resultado?

**Resumo da resposta:** Foi apresentada uma estrutura para calcular uma estimativa e retorná-la junto aos dados consultados.

**Decisão:** Aceita e adaptada. A estrutura foi ajustada ao funcionamento do DuckDB para apresentar uma estimativa relacionada à execução da consulta.

## 9. Avaliação das consultas geradas

**Prompt (resumo):** Como comparar as consultas produzidas pelo modelo com consultas SQL de referência e calcular a acurácia?

**Resumo da resposta:** Foram apresentadas orientações para executar perguntas de teste, comparar resultados e registrar as divergências.

**Decisão:** Aceita e adaptada. A estrutura foi utilizada na avaliação experimental, permitindo comparar os resultados do modelo com as consultas de referência e identificar divergências.

## 10. Testes de segurança e integração contínua

**Prompt (resumo):** Como organizar os testes automatizados no GitHub Actions para executá-los a cada alteração no repositório?

**Resumo da resposta:** Foi apresentado um workflow para instalar as dependências e executar os testes com `unittest`.

**Decisão:** Aceita e adaptada. O workflow foi ajustado à estrutura do projeto e sua execução foi confirmada com sucesso no GitHub Actions.

---

**Observação:** As sugestões das ferramentas de inteligência artificial foram analisadas e adaptadas. A implementação, os testes e as decisões finais foram realizados e conferidos durante o desenvolvimento do projeto.