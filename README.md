
# Assistente de Dados — Censo Escolar

## 1. Sobre o projeto

Este projeto tem como objetivo desenvolver um assistente de dados capaz de interpretar perguntas em linguagem natural, gerar consultas SQL seguras e apresentar resultados com base em dados públicos do Censo Escolar 2024.

A proposta faz parte de um projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas (ADS).

## 2. Objetivo

Facilitar a consulta de informações educacionais por meio de perguntas em português, reduzindo a necessidade de conhecimento prévio em SQL.

## 3. Fonte de dados

A base de dados prevista para o projeto é o conjunto de microdados do Censo Escolar 2024, disponibilizado pelo Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP).

Os dados serão analisados e preparados antes de serem utilizados pelo sistema.

## 4. Funcionalidades previstas

- Consultar o total de matrículas da educação básica por estado.
- Identificar os dez municípios com maior quantidade de escolas.
- Comparar o número de matrículas entre estados.
- Consultar a quantidade de turmas da educação básica em Jundiaí.
- Consultar a quantidade de escolas por dependência administrativa em São Paulo.
- Interpretar perguntas em linguagem natural e gerar consultas SQL.
- Validar as consultas antes da execução.
- Apresentar os resultados em tabelas e, quando adequado, gráficos.

## 5. Tecnologias em estudo

- Python
- SQL
- DuckDB ou PostgreSQL
- Streamlit
- SQLGlot
- Ollama para execução local de modelos de linguagem

A seleção definitiva das tecnologias será documentada durante o desenvolvimento.

## 6. Segurança

O sistema deverá validar as consultas SQL antes de executá-las, restringir as operações permitidas e limitar a quantidade de resultados retornados.

Também serão realizados testes para verificar o bloqueio de comandos destrutivos e tentativas de injeção de SQL.

## 7. Status do projeto

**Etapa atual:** configuração do repositório e preparação do ambiente de desenvolvimento.

As funcionalidades descritas neste documento são objetivos previstos e ainda precisam ser implementadas e testadas.

## 8. Execução

As instruções de instalação e execução serão adicionadas após a definição e implementação do ambiente do projeto.
