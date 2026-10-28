
import streamlit as st
import pandas as pd
import sqlglot

from src.assistente import gerar_sql_validado
from src.dados import consultar_censo_com_custo


st.set_page_config(
    page_title="Assistente do Censo Escolar",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Assistente de Dados — Censo Escolar 2024")
st.write(
    "Faça perguntas em português sobre os dados da educação básica "
    "e consulte os resultados usando inteligência artificial local."
)

st.info(
    "As consultas são validadas antes da execução. "
    "Os resultados estão limitados a 1.000 linhas."
)

pergunta = st.text_area(
    "O que você deseja descobrir?",
    placeholder="Ex.: Quantas escolas existem por estado?",
    height=100,
)

executar = st.button("Consultar dados", type="primary")

if executar:
    if not pergunta.strip():
        st.warning("Digite uma pergunta antes de consultar.")
    else:
        try:
            with st.spinner("Gerando e validando a consulta SQL..."):
                sql = gerar_sql_validado(pergunta)

            st.subheader("Consulta SQL aprovada")
            st.code(sql, language="sql")

            with st.spinner("Consultando os dados do Censo Escolar..."):
                resposta = consultar_censo_com_custo(sql)

            resultado = resposta["resultado"]
            estimativa = resposta["estimativa_custo"]

            st.subheader("Estimativa de custo")
            col1, col2 = st.columns(2)

            col1.metric("Nível estimado", estimativa["nivel"].capitalize())
            col2.metric("Pontuação heurística", estimativa["pontuacao"])

            st.caption(estimativa["aviso"])

            if estimativa["fatores"]:
                st.write("Fatores considerados:", ", ".join(estimativa["fatores"]))

            st.subheader("Resultados")

            if not resultado:
                st.info("A consulta não retornou registros.")
            else:
                arvore = sqlglot.parse_one(sql, read="duckdb")
                colunas = [
                    expressao.alias_or_name
                    for expressao in arvore.expressions
                ]

                df = pd.DataFrame(resultado, columns=colunas)

                st.dataframe(df, use_container_width=True)
                st.caption(f"Linhas exibidas: {len(df)}")

                # Gráfico automático quando existem colunas numéricas.
                colunas_numericas = df.select_dtypes(
                    include="number"
                ).columns.tolist()

                if len(df.columns) >= 2 and colunas_numericas:
                    coluna_valor = colunas_numericas[0]
                    coluna_categoria = next(
                        (
                            coluna
                            for coluna in df.columns
                            if coluna != coluna_valor
                        ),
                        None,
                    )

                    if coluna_categoria:
                        grafico_df = df[
                            [coluna_categoria, coluna_valor]
                        ].copy()

                        grafico_df[coluna_valor] = pd.to_numeric(
                            grafico_df[coluna_valor],
                            errors="coerce",
                        )

                        grafico_df = grafico_df.dropna(
                            subset=[coluna_valor]
                        )

                        if not grafico_df.empty:
                            st.subheader("Visualização gráfica")
                            st.bar_chart(
                                grafico_df.set_index(coluna_categoria)[
                                    coluna_valor
                                ]
                            )
                else:
                    st.caption(
                        "Não foi possível identificar automaticamente "
                        "uma coluna numérica para montar o gráfico."
                    )

        except Exception as erro:
            st.error(f"Não foi possível concluir a consulta: {erro}")
            st.caption(
                "Confira se o Ollama está em execução e se o modelo "
                "qwen2.5:3b está disponível."
            )
