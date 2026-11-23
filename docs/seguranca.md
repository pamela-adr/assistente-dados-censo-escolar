# Segurança das Consultas SQL

## 1. Validação das consultas

Como o sistema utiliza inteligência artificial para gerar consultas SQL a partir de perguntas em linguagem natural, é necessário verificar cada consulta antes de executá-la.

Essa validação é feita com a biblioteca SQLGlot, por meio das regras implementadas no arquivo `src/seguranca.py`.

## 2. Regras de segurança

O sistema aplica algumas restrições para evitar consultas que possam comprometer os dados:

- Permite somente consultas do tipo SELECT.
- Bloqueia comandos como DELETE, UPDATE, DROP, INSERT e ALTER.
- Impede a execução de múltiplas instruções SQL na mesma consulta.
- Restringe as fontes de dados utilizadas.
- Verifica se as colunas solicitadas pertencem ao conjunto de dados autorizado.
- Bloqueia o uso de SELECT * fora de funções de contagem, como COUNT(*).
- Define um limite de 1.000 linhas para os resultados.

## 3. Acesso aos dados

Os dados são consultados por meio do DuckDB, utilizando os microdados do Censo Escolar 2024.

O acesso ao arquivo CSV é restrito à fonte autorizada pelo projeto. Na configuração com Docker, o volume que disponibiliza os dados ao container é montado como somente leitura.

## 4. Testes de segurança

Foram desenvolvidos testes automatizados para verificar se as regras estão sendo respeitadas.

Os testes contemplam consultas permitidas, comandos que devem ser bloqueados, tentativas de injeção SQL, utilização de fontes não autorizadas e consultas com colunas inválidas.

Até o momento, os testes de segurança do projeto apresentam 29 casos aprovados.

## 5. Limitações

As validações reduzem os riscos relacionados à execução de consultas geradas pela inteligência artificial, mas não significam que o sistema esteja livre de qualquer vulnerabilidade.

Por isso, as consultas passam pelas verificações antes de serem executadas, e os testes automatizados ajudam a identificar possíveis falhas nas regras implementadas.