# Arquitetura do Sistema

## 1. Como o sistema funciona

O Assistente de Dados Educacionais foi desenvolvido para facilitar a consulta aos microdados do Censo Escolar 2024. Em vez de escrever uma consulta SQL, o usuário pode fazer uma pergunta em português e receber os resultados pela aplicação.

Para isso, o sistema utiliza algumas tecnologias que trabalham em conjunto, desde a interpretação da pergunta até a apresentação dos dados.

## 2. Etapas do funcionamento

O processo começa quando o usuário digita uma pergunta na interface do Streamlit.

Antes de gerar a consulta, o sistema verifica se a pergunta precisa de algum esclarecimento. Quando identifica uma possível ambiguidade, solicita que o usuário especifique o que deseja consultar.

Se a pergunta estiver clara, o modelo Qwen 2.5 3B, executado pelo Ollama, gera uma consulta SQL.

Essa consulta passa pela validação do SQLGlot, que verifica se ela respeita as regras de segurança definidas no projeto. Somente depois dessa verificação a consulta é encaminhada ao DuckDB, responsável por acessar os microdados do Censo Escolar.

Por fim, os resultados são apresentados na interface. Além da tabela, o sistema também pode exibir gráficos e uma explicação sobre o que foi consultado.

## 3. Tecnologias utilizadas

**Python:** utilizado no desenvolvimento e na integração das funcionalidades do projeto.

**Streamlit:** responsável pela interface, onde o usuário envia perguntas e visualiza os resultados.

**Ollama e Qwen 2.5 3B:** utilizados para interpretar as perguntas e gerar as consultas SQL localmente.

**SQLGlot:** utilizado para analisar e validar as consultas antes de sua execução.

**DuckDB:** responsável por realizar as consultas nos microdados do Censo Escolar 2024.

## 4. Cuidados com a segurança

Como as consultas são geradas por um modelo de inteligência artificial, foi necessário implementar verificações antes de permitir sua execução.

O sistema aceita apenas consultas do tipo SELECT e bloqueia comandos que possam alterar ou excluir dados. Também verifica as fontes e colunas utilizadas, impede o envio de múltiplas consultas na mesma instrução e limita o resultado a 1.000 linhas.

Essas verificações são realizadas antes de o DuckDB acessar o arquivo CSV.

## 5. Execução com Docker

O projeto também possui uma configuração com Docker Compose, que permite executar a aplicação em um container.

A interface fica disponível na porta 8501. Os microdados são disponibilizados ao container por meio de um volume configurado como somente leitura.

O Ollama continua sendo executado na máquina hospedeira, e o container acessa o serviço pelo endereço definido no arquivo `docker-compose.yml`.

## 6. Organização do sistema

A separação entre interface, geração de SQL, validação e consulta aos dados facilita a manutenção e os testes do projeto.

Dessa forma, cada parte possui uma responsabilidade específica, desde o recebimento da pergunta até a apresentação do resultado.