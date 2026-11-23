# Assistente de Dados Educacionais do Brasil com Text-to-SQL Seguro

**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Projeto Integrador

---

## 1. Sobre o projeto

Neste projeto, desenvolvi um assistente de dados que permite consultar informações do Censo Escolar 2024 por meio de perguntas em português.

A proposta é facilitar o acesso aos dados sem que o usuário precise saber escrever SQL. Basta fazer uma pergunta, e o sistema utiliza um modelo de inteligência artificial para gerar a consulta, verificar se ela é segura e apresentar o resultado.

## 2. Objetivo

O objetivo é utilizar inteligência artificial para transformar perguntas feitas em linguagem natural em consultas SQL.

Além de gerar as consultas, também implementei verificações para impedir comandos que não são permitidos e evitar que uma consulta gerada pelo modelo seja executada sem passar pelas regras de segurança do projeto.

## 3. Fonte de dados

Utilizei os microdados do Censo Escolar 2024, disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

O arquivo utilizado é `microdados_ed_basica_2024.csv`.

Para consultar os dados, utilizei o DuckDB. A leitura do arquivo considera o ponto e vírgula como delimitador, codificação Latin-1 e as colunas como texto.

## 4. Tecnologias utilizadas

As tecnologias utilizadas no desenvolvimento foram:

- **Python:** linguagem utilizada para desenvolver o projeto.
- **DuckDB:** utilizado para consultar os microdados do Censo Escolar.
- **SQLGlot:** utilizado para analisar e validar as consultas SQL.
- **Ollama:** utilizado para executar o modelo de inteligência artificial localmente.
- **Qwen 2.5 3B:** modelo utilizado para interpretar as perguntas e gerar as consultas SQL.
- **Streamlit:** utilizado para criar a interface da aplicação.

## 5. Funcionalidades desenvolvidas

Durante o desenvolvimento, implementei as seguintes funcionalidades:

- Fazer perguntas sobre os dados utilizando linguagem natural.
- Gerar consultas SQL com o Qwen 2.5 3B.
- Identificar perguntas que precisam de mais informações antes de gerar a consulta.
- Validar o SQL antes de executar.
- Bloquear comandos que possam modificar ou excluir dados.
- Restringir as fontes de dados e as colunas utilizadas.
- Limitar os resultados a 1.000 linhas.
- Estimar o custo das consultas com base nos critérios definidos no projeto.
- Exibir os resultados em tabelas e gráficos.
- Apresentar uma explicação da consulta em linguagem simples.

## 6. Segurança das consultas

Uma das partes que exigiu mais atenção foi a segurança das consultas geradas pela inteligência artificial.

Para isso, utilizei o SQLGlot para analisar a estrutura do SQL antes de permitir sua execução.

As regras implementadas incluem:

- Permitir somente consultas do tipo `SELECT`.
- Bloquear comandos como `DELETE`, `UPDATE`, `DROP`, `INSERT` e `ALTER`.
- Impedir a execução de várias consultas na mesma instrução.
- Restringir as fontes de dados utilizadas.
- Verificar se as colunas solicitadas são permitidas.
- Controlar a leitura do arquivo CSV.
- Limitar os resultados a 1.000 linhas.

Também criei testes automatizados para verificar se essas regras estão funcionando. Nos testes realizados, os 29 casos de segurança foram aprovados.

A documentação dessas regras está em [`docs/seguranca.md`](docs/seguranca.md).

## 7. Análise exploratória dos dados

Antes de começar a desenvolver as consultas, analisei os microdados para entender melhor a estrutura do arquivo e algumas características da base.

O arquivo apresentou:

- 215.545 registros.
- 426 colunas.

Também verifiquei alguns campos utilizados no projeto. O `CO_ENTIDADE` apresentou 215.545 valores únicos e nenhum valor vazio.

Na variável `QT_MAT_BAS`, encontrei 36.259 valores vazios. Os mesmos registros também apresentam valores vazios em `QT_TUR_BAS` e `QT_DOC_BAS`.

A distribuição desses registros por situação de funcionamento foi:

- Em atividade: 1.779 registros.
- Paralisada: 31.321 registros.
- Extinta no ano do Censo: 3.159 registros.

Com essa análise, percebi que os valores vazios aparecem principalmente em escolas paralisadas, mas também estão presentes em escolas em atividade e extintas no ano do Censo.

Por isso, não considerei correto substituir esses valores automaticamente por zero ou simplesmente excluir os registros.

**Limitação:** os dados mostram onde estão concentrados os valores vazios, mas não permitem afirmar qual foi a causa dessas ausências.

## 8. Variáveis utilizadas

Consultei o dicionário dos microdados do Censo Escolar 2024, disponibilizado pelo INEP, para verificar o significado das variáveis utilizadas.

As principais foram:

- `QT_MAT_BAS`: quantidade de matrículas da educação básica, considerando as etapas e modalidades descritas pelo INEP e excluindo matrículas em turmas exclusivamente de atividade complementar e exclusivamente de Atendimento Educacional Especializado (AEE).
- `QT_TUR_BAS`: quantidade de turmas da educação básica.
- `TP_DEPENDENCIA`: código da dependência administrativa da escola:
  - `1`: Federal.
  - `2`: Estadual.
  - `3`: Municipal.
  - `4`: Privada.
- `TP_SITUACAO_FUNCIONAMENTO`: situação de funcionamento da escola:
  - `1`: Em atividade.
  - `2`: Paralisada.
  - `3`: Extinta no ano do Censo.
  - `4`: Extinta em anos anteriores.

## 9. Avaliação do assistente

Para testar o assistente, preparei um conjunto de 50 perguntas com consultas SQL de referência.

Depois, comparei os resultados das consultas geradas pelo Qwen 2.5 3B com os resultados esperados.

O resultado foi:

- Perguntas avaliadas: 50.
- Acertos: 47.
- Acurácia: 94%.

As três perguntas em que houve divergência foram mantidas na avaliação. Não fiz alterações nos resultados para aumentar a porcentagem de acertos.

### 9.1 Comparação com o baseline

Também fiz um teste utilizando o mesmo modelo, mas com uma instrução mais simples, sem as orientações detalhadas do prompt principal.

O resultado foi:

- Perguntas avaliadas: 50.
- Consultas executadas: 0.
- Consultas bloqueadas: 50.
- Acurácia: não calculável.

Nenhuma das consultas geradas nesse teste passou pelas regras de segurança. Como nenhuma chegou a ser executada, não foi possível calcular a acurácia do baseline.

Essa comparação mostrou a importância de informar ao modelo quais são as fontes de dados e as colunas disponíveis, além de explicar como a base está organizada.

### 9.2 Avaliação das explicações

Também testei a funcionalidade que explica as consultas SQL em linguagem simples.

Para isso, analisei 10 explicações geradas pelo modelo. O resultado foi:

- 2 explicações boas.
- 8 explicações parcialmente adequadas.

Durante a revisão, encontrei algumas imprecisões relacionadas ao uso de `LIMIT`, ao delimitador do CSV, aos valores nulos e ao significado de `header=true`.

Os resultados dessa análise estão registrados em `evidencias/avaliacao_explicacoes.md`.

A avaliação completa do sistema está documentada em [`docs/avaliacao.md`](docs/avaliacao.md).

## 10. Evidências

Guardei os resultados dos testes e das avaliações na pasta `evidencias/`.

Os principais arquivos são:

- `resultado_avaliacao.txt`: resultado dos testes realizados com o assistente.
- `resultado_baseline.json`: registro das consultas geradas pelo baseline.
- `comparacao_modelos.json`: comparação entre os dois experimentos.
- `catalogo_testes_seguranca.md`: registro dos testes de segurança.
- `avaliacao_explicacoes.json`: explicações utilizadas na revisão.
- `analise_avaliacao.md`: análise das divergências encontradas nas perguntas.
- `avaliacao_explicacoes.md`: resultado da revisão das dez explicações.

## 11. Como executar o projeto

Para executar o projeto localmente, é necessário ter o Python 3.13, o Ollama e os microdados do Censo Escolar 2024.

Primeiro, instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

Depois, baixe o modelo utilizado:

```powershell
ollama pull qwen2.5:3b
```

Com o Ollama em execução, inicie a aplicação:

```powershell
python -m streamlit run app.py
```

A interface será aberta no navegador, permitindo fazer perguntas sobre os dados do Censo Escolar.

### 11.1 Execução com Docker

Também é possível executar o projeto utilizando Docker Compose.

Com o Docker instalado e os microdados disponíveis no caminho configurado no `docker-compose.yml`, execute:

```powershell
docker compose up --build
```

Depois que a aplicação iniciar, acesse `http://localhost:8501` no navegador.

Nessa configuração, o Ollama continua sendo executado na máquina, enquanto a aplicação roda dentro do container.

## 12. Arquitetura do sistema

O funcionamento acontece nesta ordem:

1. O usuário envia uma pergunta pela interface do Streamlit.
2. O assistente verifica se a pergunta precisa de algum esclarecimento.
3. O Qwen 2.5 3B, executado pelo Ollama, gera a consulta SQL.
4. O SQLGlot verifica se a consulta segue as regras de segurança.
5. O DuckDB executa a consulta nos dados autorizados.
6. O resultado aparece na interface em forma de tabela, gráfico ou explicação.

A descrição mais detalhada está em [`docs/arquitetura.md`](docs/arquitetura.md).

## 13. Licenças utilizadas

As principais tecnologias utilizadas possuem as seguintes licenças:

- DuckDB: MIT.
- SQLGlot: MIT.
- Streamlit: Apache 2.0.
- Ollama: código aberto.

Os microdados utilizados são públicos e foram disponibilizados pelo INEP.