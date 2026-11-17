# Catálogo de testes de segurança

**Projeto:** Assistente de dados educacionais do Brasil com text-to-SQL seguro.

## Objetivo

Registrar os testes automatizados realizados para verificar a validação das consultas SQL antes da execução.

## Casos testados

| Categoria | Caso testado | Resultado |
|---|---|---|
| Comandos destrutivos | DELETE, DROP, UPDATE, INSERT, ALTER e TRUNCATE | Bloqueado |
| Injeção SQL | Tentativa de executar duas instruções na mesma consulta | Bloqueado |
| Múltiplas consultas | Duas instruções SQL separadas por ponto e vírgula | Bloqueado |
| Fonte de dados | Leitura de arquivo diferente do Censo Escolar | Bloqueado |
| Fonte de dados | Leitura de JSON, Parquet e read_csv_auto | Bloqueado |
| Fontes múltiplas | JOIN e subconsulta utilizando outra fonte | Bloqueado |
| Tabelas | Tabelas não autorizadas | Bloqueado |
| Colunas | Colunas não autorizadas | Bloqueado |
| Funções | Funções SQL não autorizadas | Bloqueado |
| Consulta | SELECT * | Bloqueado |
| Sintaxe | SQL inválido e FROM duplicado | Bloqueado |
| Limite | LIMIT negativo | Bloqueado |
| Limite | Resultado limitado a 1.000 registros | Aplicado |
| Consulta permitida | SELECT com leitura parametrizada do Censo | Permitido |
| Consulta permitida | Funções agregadas autorizadas | Permitido |

## Resultado da execução

- Arquivo de testes: `tests/test_seguranca.py`
- Total de testes executados: 29
- Testes aprovados: 29
- Testes reprovados: 0
- Resultado: OK

