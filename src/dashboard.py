
import streamlit as st
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import plotly.express as px
from vectors import chat_assistente

st.title("Análise da Câmara de Deputados")

tab1, tab2, tab3 = st.tabs(["Overview", "Despesas", "Proposições"])

with tab1:
    st.title("Visão Geral")
    st.write("Este dashboard apresenta uma análise dos dados da Câmara dos Deputados referentes ao mês de Agosto de 2024.")

    # Carregar e exibir a imagem
    image = mpimg.imread("docs/distribuicao_deputados.png")
    st.image(image, use_container_width=True)

    # Carregar e exibir os insights
    with open("data/insights_distribuicao_deputados.json", "r") as f:
        insights = json.load(f)
    for insight in insights:
        st.write(f"- {insight['analise']}")

with tab2:
    st.title("Despesas")

    # Carregar e exibir os insights das despesas
    with open("data/insights_despesas_deputados.json", "r") as f:
        insights_despesas = json.load(f)
    for insight in insights_despesas:
        st.write(f"- {insight['analise']}")

    # Carregar dados de despesas
    despesas_df = pd.read_parquet("data/despesas_deputados.parquet")

    # Selecionar deputado
    deputados = despesas_df["nomeDeputado"].unique()
    selected_deputado = st.selectbox("Selecione um Deputado:", deputados)

    # Filtrar dados para o deputado selecionado
    deputado_df = despesas_df[despesas_df["nomeDeputado"] == selected_deputado]

    # Criar gráfico de barras
    fig = px.bar(deputado_df, x="dataDocumento", y="valorLiquido", color="tipoDespesa", 
                 title=f"Série Temporal de Despesas - {selected_deputado}")
    st.plotly_chart(fig)


with tab3:
    st.title("Proposições")

    # Interface do chat
    st.write("### Assistente Virtual")
    pergunta = st.text_input("Digite sua pergunta:")
    if pergunta:
        resposta = chat_assistente(pergunta)
        st.write("Resposta do Assistente:")
        st.write(resposta)

    # Carregar e exibir dados das proposições
    proposicoes_df = pd.read_parquet("data/proposicoes_deputados.parquet")
    st.dataframe(proposicoes_df)

    # Carregar e exibir o resumo das proposições
    with open("data/sumarizacao_proposicoes.json", "r") as f:
        sumarizacao_proposicoes = json.load(f)
    for item in sumarizacao_proposicoes:
        st.write(f"**Tema:** {item['tema']}")
        st.write(f"**Sumarização:** {item['sumarizacao']}")


