# Assistente de Dados Educacionais do Brasil com Text-to-SQL Seguro

**Curso:** EAD_PROINT_100.DD-ADS-PI-10-74.2026.74  
**Disciplina:** Projeto Integrador  
**Integrante:** Pamela Adrielly — RA: 2408194

---

## 1. Sobre o projeto

Neste projeto, desenvolvi um assistente de dados educacionais que permite consultar informações do Censo Escolar 2024 por meio de perguntas feitas em linguagem natural.

A ideia surgiu da possibilidade de facilitar o acesso aos dados educacionais, permitindo que uma pessoa faça perguntas em português sem precisar conhecer SQL. A partir dessas perguntas, o sistema utiliza um modelo de linguagem para gerar consultas, verifica se elas seguem as regras de segurança e apresenta os resultados.

## 2. Objetivo

O objetivo é desenvolver uma ferramenta que facilite a consulta aos microdados do Censo Escolar 2024, utilizando inteligência artificial para transformar perguntas em consultas SQL.

Além de gerar as consultas, procurei implementar mecanismos para evitar operações não permitidas e reduzir os riscos relacionados à execução de comandos SQL.

## 3. Fonte de dados

Utilizei os microdados do Censo Escolar 2024, disponibilizados pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

O arquivo principal utilizado no projeto é `microdados_ed_basica_2024.csv`.

A leitura dos dados é feita com o DuckDB, utilizando o ponto e vírgula como delimitador, codificação Latin-1 e leitura das colunas como texto.

## 4. Tecnologias utilizadas

Durante o desenvolvimento, utilizei as seguintes tecnologias:

- **Python:** linguagem utilizada para desenvolver a aplicação e organizar suas funcionalidades.
- **DuckDB:** utilizado para consultar os microdados do Censo Escolar.
- **SQLGlot:** utilizado na análise e validação das consultas SQL.
- **Ollama:** utilizado para executar localmente o modelo de linguagem.
- **Qwen 2.5 3B:** modelo utilizado para interpretar as perguntas e gerar consultas SQL.
- **Streamlit:** utilizado para desenvolver a interface da aplicação.

## 5. Funcionalidades desenvolvidas

Ao longo do desenvolvimento, implementei as seguintes funcionalidades:

- Recebimento de perguntas em linguagem natural.
- Geração de consultas SQL utilizando o modelo Qwen 2.5 3B.
- Validação das consultas antes da execução.
- Restrição das operações SQL permitidas.
- Bloqueio de comandos que podem modificar ou excluir dados.
- Limitação da quantidade de linhas retornadas.
- Estimativa de custo das consultas com base em critérios definidos na aplicação.
- Apresentação dos resultados em tabelas.
- Exibição de gráficos quando o resultado permite esse tipo de visualização.
- Explicação das consultas SQL em linguagem simples.

## 6. Segurança das consultas

Uma das partes que exigiu atenção durante o desenvolvimento foi a segurança das consultas geradas pelo modelo.

Para isso, utilizei o SQLGlot na análise da estrutura das consultas e implementei regras para permitir apenas operações autorizadas.

Entre os controles desenvolvidos estão:

- Permissão apenas para consultas do tipo `SELECT`.
- Bloqueio de comandos como `DELETE`, `UPDATE`, `DROP`, `INSERT` e `ALTER`.
- Bloqueio de múltiplas consultas enviadas na mesma instrução.
- Restrição das fontes de dados e das colunas permitidas.
- Controle sobre a leitura do arquivo CSV.
- Limitação das linhas retornadas.

Também desenvolvi testes automatizados para verificar se essas regras estão funcionando.

Até o momento, foram executados 29 testes relacionados à segurança, todos aprovados.

## 7. Análise exploratória dos dados

Antes de desenvolver as consultas, realizei uma análise inicial dos microdados para conhecer melhor a estrutura do arquivo e identificar características importantes da base.

O arquivo principal apresentou:

- 215.545 registros.
- 426 colunas.

Também analisei alguns campos utilizados no projeto. O campo `CO_ENTIDADE` apresentou 215.545 valores únicos e nenhum valor vazio.

Na variável `QT_MAT_BAS`, identifiquei 36.259 valores vazios. Os mesmos registros também apresentam valores vazios em `QT_TUR_BAS` e `QT_DOC_BAS`.

A distribuição desses registros por situação de funcionamento foi:

- Em atividade: 1.779 registros.
- Paralisada: 31.321 registros.
- Extinta no ano do Censo: 3.159 registros.

Essa análise mostrou que os valores ausentes estão concentrados principalmente em escolas paralisadas, mas também aparecem em escolas em atividade e extintas no ano do Censo.

Por esse motivo, não considerei adequado transformar automaticamente os valores ausentes em zero ou excluir esses registros sem uma investigação adicional.

**Limitação:** essa análise descreve o comportamento observado nos dados, mas não determina, por si só, a causa dos valores ausentes.

## 8. Variáveis utilizadas e definições

As definições das variáveis foram consultadas no dicionário dos microdados do Censo Escolar 2024, disponibilizado pelo INEP.

As principais variáveis analisadas foram:

- `QT_MAT_BAS`: número de matrículas da educação básica, incluindo as etapas e modalidades descritas pelo INEP e excluindo matrículas em turmas exclusivamente de atividade complementar e exclusivamente de Atendimento Educacional Especializado (AEE).
- `QT_TUR_BAS`: número de turmas da educação básica.
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

Para avaliar o funcionamento do assistente, preparei um conjunto de 50 perguntas com consultas SQL de referência.

As consultas geradas pelo Qwen foram comparadas com os resultados obtidos pelas consultas de referência.

Na avaliação registrada, o assistente apresentou:

- Perguntas avaliadas: 50.
- Acertos: 50.
- Acurácia: 100%.

Esse resultado corresponde ao conjunto de perguntas utilizado na avaliação e não representa uma garantia de precisão para qualquer pergunta que possa ser feita ao sistema.

### 9.1 Comparação entre os prompts

Também realizei uma comparação utilizando o mesmo modelo, mas com uma instrução simplificada, sem as orientações detalhadas do prompt principal.

O resultado foi:

- Perguntas avaliadas: 50.
- Consultas bloqueadas pela validação: 50.
- Consultas executadas: 0.

Nesse experimento, o modelo não conseguiu gerar consultas compatíveis com as fontes de dados e as colunas autorizadas pelo projeto.

Como nenhuma consulta foi executada, não foi possível calcular a acurácia do baseline.

A comparação foi utilizada para observar a importância das instruções específicas sobre a estrutura dos dados na geração das consultas.

## 10. Explicação das consultas

Além da geração do SQL, implementei uma funcionalidade para explicar o que cada consulta realiza em linguagem simples.

A intenção é permitir que a pessoa entenda quais informações estão sendo buscadas, quais filtros foram utilizados e como os resultados são organizados.

Para verificar essa funcionalidade, gerei uma amostra de dez explicações, registrada no arquivo `evidencias/avaliacao_explicacoes.json`.

A amostra foi gerada para verificar a qualidade das explicações. A revisão do conteúdo ainda faz parte das etapas de validação do projeto.

## 11. Estrutura das evidências

Durante o desenvolvimento, organizei os resultados dos testes e das avaliações na pasta `evidencias`.

Os arquivos registrados até o momento são:

- `resultado_avaliacao.txt`: resultado da avaliação do assistente principal.
- `resultado_baseline.json`: resultados do experimento baseline.
- `comparacao_modelos.json`: comparação entre os experimentos.
- `catalogo_testes_seguranca.md`: registro dos testes de segurança.
- `avaliacao_explicacoes.json`: amostra de explicações das consultas.
- `requirements.txt`: lista as dependências e suas versões utilizadas no projeto.

## 12. Execução do projeto

Para executar o projeto, é necessário ter o Python 3.13 e o Ollama instalados. Também é necessário disponibilizar os microdados do Censo Escolar 2024 no caminho configurado no arquivo `src/dados.py`.

Primeiro, instale as dependências do projeto:

```powershell
python -m pip install -r requirements.txt
```

Em seguida, baixe o modelo utilizado pelo assistente:

```powershell
ollama pull qwen2.5:3b
```

Com o Ollama em execução, inicie a interface:

```powershell
python -m streamlit run app.py
```

A aplicação será aberta no navegador e permitirá enviar perguntas sobre os dados do Censo Escolar 2024.

## 13. Considerações finais

O desenvolvimento deste projeto permitiu trabalhar com geração de consultas SQL utilizando inteligência artificial, análise de dados educacionais e validação de segurança.

Durante o processo, precisei ajustar as instruções utilizadas pelo modelo, testar diferentes perguntas e verificar se as consultas geradas correspondiam aos resultados esperados.

A avaliação realizada apresentou 50 acertos nas 50 perguntas registradas, enquanto o experimento com o prompt simplificado mostrou dificuldades para gerar consultas compatíveis com a estrutura da base.

Com as principais funcionalidades implementadas e os primeiros testes realizados, estou avançando na revisão das evidências, na documentação e na preparação do projeto para a entrega final.