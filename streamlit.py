import streamlit as st
import pandas as pd
import numpy as np
from excel_utils import prepare_data
from parameters import *
import plotly.express as px


def main():
    st.title("Dashboard de Gastos")

    df = prepare_data()

    btn_filter = st.sidebar.header('Filtros')
    if btn_filter:
        print(1)

    st.sidebar.button('Resetar Filtros')

    categoria = st.sidebar.multiselect(
        "Categoria",
        df["Categoria"].unique(),
        default=df["Categoria"].unique()
    )

    mes_pagamento_atual = st.sidebar.multiselect(
        "Mês Pagamento Atual?",
        df["Mês Pagamento Atual?"].unique(),
        default=df["Mês Pagamento Atual?"].unique()
    )

    df_filtrado = df[
        df['Categoria'].isin(categoria) &
        df["Mês Pagamento Atual?"].isin(mes_pagamento_atual)
    ]

    st.write('Table')
    st.dataframe(df_filtrado)
    # ------------------- Gastos por dia -------------------
    # df_gastos = df[(df['Pagamento?'] == 'Não') & (df['Local'] != 'Wise Save')]
    
    # gastos_por_dia = df_gastos[df_gastos['Mês Pagamento Atual?'] == "Sim"].groupby('Data')['Valor'].sum().reset_index()
    # # gastos_por_dia.index = gastos_por_dia.index.strftime('%d/%m')

    # fig1 = px.bar(
    #     gastos_por_dia, 
    #     x="Data",
    #     y="Valor",
    #     text="Valor"
    # )
    # fig1.update_traces(
    #     texttemplate='%{text:.2f} CHF',
    #     textposition='outside', 
    #     marker_color='darkred'
    # )

    # fig1.update_layout(
    #     title="Gastos por Dia - Mês Atual",
    #     xaxis_title="Data",
    #     yaxis_title="CHF",
    #     showlegend=False
    # )
    # st.plotly_chart(fig1, use_container_width=True)

    # # ------------------- Gastos por Categoria -------------------
    # gastos_categoria = df_gastos[df_gastos['Mês Pagamento Atual?'] == "Sim"].groupby('Categoria')['Valor'].sum().sort_values(ascending=True).reset_index()

    # fig2 = px.bar(gastos_categoria, x='Categoria', y='Valor', text='Valor')
    # fig2.update_traces(texttemplate='%{text:.2f} CHF', textposition='outside', marker_color='darkred')
    # fig2.update_layout(
    #     title="Gastos por Categoria - Mês Atual",
    #     xaxis_title="Categoria",
    #     yaxis_title="CHF",
    #     showlegend=False
    # )

    # st.plotly_chart(fig2, use_container_width=True)




if __name__ == "__main__":
    main()