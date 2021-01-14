import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from time import sleep


@st.cache
def carrega_dados(caminho):
    data = pd.read_csv(caminho)
    return data


def obtendo_dataframes(data_2019, data_2020, causa, estado="BRASIL"):
    if estado == "BRASIL":
        data_sel_2019 = data_2019.query(f"tipo_doenca == '{causa}'")
        data_sel_2020 = data_2020.query(f"tipo_doenca == '{causa}'")
    else:
        data_sel_2019 = data_2019.query(f"tipo_doenca == '{causa}' and uf == '{estado}'")
        data_sel_2020 = data_2020.query(f"tipo_doenca == '{causa}' and uf == '{estado}'")

    return data_sel_2019, data_sel_2020


def grafico_comparativo(data_2019, data_2020, causa, estado="BRASIL"):
    if estado == "BRASIL":
        total_2019 = data_2019.groupby("tipo_doenca").sum()
        total_2020 = data_2020.groupby("tipo_doenca").sum()
        lista = [int(total_2019.loc[causa]), int(total_2020.loc[causa])]
    else:
        total_2019 = data_2019.groupby(["uf","tipo_doenca"]).sum()
        total_2020 = data_2020.groupby(["uf", "tipo_doenca"]).sum()
        lista = [int(total_2019.loc[estado, causa]), int(total_2020.loc[estado, causa])]
    
    data = pd.DataFrame({"Total" : lista,
                            "Ano": [2019, 2020]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x="Ano", y="Total", data = data)
    ax.set_title(f"Óbitos por {causa} - {estado}")
   
    return fig


def main():
    obitos_2019 = carrega_dados("data/obitos-2019.csv")
    obitos_2020 = carrega_dados("data/obitos-2020.csv")
    tipo_doenca = obitos_2020["tipo_doenca"].unique()
    estado = np.append(obitos_2020["uf"].unique(), "BRASIL")

    st.title("Análise de Óbitos 2019-2020")
    st.markdown("Este trabalho analisa dados dos **óbitos 2019-2020**")  
    opcao_1 = st.sidebar.selectbox("Selecione o tipo de doença", tipo_doenca)
    opcao_2 = st.sidebar.selectbox("Selecione o Estado", estado)
    opcao_3 = st.sidebar.checkbox("Exibir os dados.")

    figura = grafico_comparativo(obitos_2019, obitos_2020,
                                opcao_1, opcao_2)

    st.pyplot(figura)

    if opcao_3:
        data_sel_2019, data_sel_2020 = obtendo_dataframes(obitos_2019, 
                                                       obitos_2020, 
                                                       opcao_1, 
                                                       opcao_2)
        st.write("Dados de 2019:")
        st.dataframe(data_sel_2019)
        st.write("Dados de 2020:")
        st.dataframe(data_sel_2020)


if __name__ == "__main__":
    main()
