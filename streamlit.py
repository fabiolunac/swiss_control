import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pandas as pd
import sqlite3

from src.database import load_gastos, load_param
from src.transform_db import prepare_data

GRAPH_COLOR = '#b82b30'

def personalize_metric():
    st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #B82B30;
        border: 1px solid #B82B30;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetric"] > div {
        color: white;
    }

    div[data-testid="stMetricLabel"] p {
        color: white;
    }

    div[data-testid="stMetricValue"] {
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    df_raw = load_gastos()
    df_param = load_param()

    personalize_metric()

    st.title("Finance App")
    df = prepare_data(df_raw, df_param)
    
    tab1, tab2 = st.tabs(['Gráficos', 'Tabela'])

    st.sidebar.header('Filtros')

    # list all options for columns
    categoria_options = df['Categoria'].unique()
    mes_options = df['Mês Pagamento'].unique()

    if st.sidebar.button('Resetar Filtros'):
        st.session_state['categoria'] = list(categoria_options)
        st.session_state['mes_pag_atual'] = False
        st.session_state['mes_pag'] = list(mes_options)

    mes_pagamento_atual = st.sidebar.checkbox(
        'Mês Pagamento Atual?', 
        key='mes_pag_atual'
    )

    categoria = st.sidebar.multiselect(
        "Categoria",
        df["Categoria"].unique(),
        default=df["Categoria"].unique(),
        key='categoria'
    )

    mes_pagamento = st.sidebar.multiselect(
        "Mês do Pagamento",
        df["Mês Pagamento"].unique(),
        default=df["Mês Pagamento"].unique(),
        key='mes_pag'
    )


    df_filtrado = df[
        df['Categoria'].isin(categoria) &
        df['Mês Pagamento'].isin(mes_pagamento)
    ]

    if mes_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Mês Pagamento Atual?'] == 'Sim']

    # PAGINA 1
    with tab1:
        df_gastos = df_filtrado[(df_filtrado['Pagamento?'] == 'Não') & (df_filtrado['Local'] != 'Wise Save')]
        df_gastos['Data'] = pd.to_datetime(df_gastos['Data'])

        col1, col2, col3 = st.columns(3)

        with col1:
            salario_total = df_filtrado[df_filtrado['Pagamento?'] == 'Sim']['Valor'].sum()

            st.metric(
                label='Salário',
                value=f'{salario_total:.0f} CHF'
            )

        with col2:
            gastos_totais = df_gastos['Valor'].sum()

            st.metric(
                label='Gastos',
                value=f'{gastos_totais:.2f} CHF'
            )

        with col3:
            saldo_guardado = df_filtrado[df_filtrado['Local'] == 'Wise Save']['Valor'].sum()

            st.metric(
                label='Save',
                value=f'{saldo_guardado:.2f} CHF'
            )
        
        # ------------------- Gastos por dia -------------------
        
        # gastos_por_dia = df_gastos.groupby('Data')['Valor'].sum().reset_index()
        gastos_por_dia = (
            df_gastos
            .set_index('Data')
            .resample('D')['Valor']
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            gastos_por_dia, 
            x="Data",
            y="Valor",
            text="Valor"
        )
        fig1.update_traces(
            texttemplate='%{text:.2f} CHF',
            textposition='outside', 
            marker_color=GRAPH_COLOR
        )
        fig1.update_layout(
            title="Gastos por Dia",
            xaxis_title="Data",
            yaxis_title="CHF",
            showlegend=False,
            xaxis=dict(
                tickformat="%d/%m"
            )
        )
        st.plotly_chart(fig1, use_container_width=True)

        # # ------------------- Gastos por Categoria -------------------
        gastos_categoria = df_gastos.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).reset_index()

        fig2 = px.bar(
            gastos_categoria, 
            x='Categoria', 
            y='Valor', 
            text='Valor'
        )
        fig2.update_traces(
            texttemplate='%{text:.2f} CHF', 
            textposition='outside', 
            marker_color=GRAPH_COLOR
        )
        fig2.update_layout(
            title="Gastos por Categoria",
            xaxis_title="Categoria",
            yaxis_title="CHF",
            showlegend=False
        )

        st.plotly_chart(fig2, use_container_width=True)

        # ------------------- Gastos por Categoria -------------------
        gastos_por_local = df_gastos.groupby('Local')['Valor'].sum().sort_values(ascending=False).reset_index()

        fig3 = px.bar(
            gastos_por_local, 
            x='Local', 
            y='Valor', 
            text='Valor'
        )
        fig3.update_traces(
            texttemplate='%{text:.2f} CHF', 
            textposition='outside', 
            marker_color=GRAPH_COLOR
        )
        fig3.update_layout(
            title="Gastos por Local",
            xaxis_title="Local",
            yaxis_title="CHF",
            showlegend=False
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # PAGINA 2
    with tab2:
        st.write('Tabela')
        st.dataframe(df_filtrado[['Data', 'Local', 'Valor', 'Categoria', 'Saldo']])

if __name__ == "__main__":
    main()