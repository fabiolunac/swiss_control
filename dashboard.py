import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pandas as pd
# import sqlite3

from src.database import load_gastos, load_param
from src.transform_db import prepare_data
from src.metrics import total_salary, total_expenses, get_total_save, get_wise_expenses
from src.charts import *

GRAPH_COLOR = '#b82b30'
# GRAPH_COLOR = '#ffffff'

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

    # Loading data frames
    df_raw = load_gastos()
    df_param = load_param()
    df = prepare_data(df_raw, df_param)

    # personalize_metric()

    st.title("Finance App")
    
    tab1, tab2 = st.tabs(['Gráficos', 'Tabela'])

    st.sidebar.header('Filtros')

    # list all options for columns
    categoria_options = df['Categoria'].unique()
    mes_options = df['Mês Pagamento'].unique()

    if st.sidebar.button('Resetar Filtros'):
        st.session_state['categoria'] = list(categoria_options)
        st.session_state['mes_pag_atual'] = False
        st.session_state['ano_pag_atual'] = False
        st.session_state['mes_pag'] = list(mes_options)

    mes_pagamento_atual = st.sidebar.checkbox(
        'Mês Pagamento Atual?', 
        key='mes_pag_atual'
    )

    ano_pagamento_atual = st.sidebar.checkbox(
        'Ano Pagamento Atual?', 
        key='ano_pag_atual'
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

    if ano_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Ano Pagamento Atual?'] == 'Sim']

    df_filtrado['Data'] = df_filtrado['Data'].dt.strftime('%d/%m/%y')

    # PAGINA 1
    with tab1:
        df_gastos = df_filtrado[(df_filtrado['Pagamento?'] == 'Não') & (df_filtrado['Local'] != 'Wise Save')]
        df_gastos['Data'] = pd.to_datetime(df_gastos['Data'])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label='Salário', value=f'{total_salary(df_filtrado):,.0f} CHF')

        with col2:
            st.metric(label='Gastos', value=f'{total_expenses(df_gastos):,.2f} CHF')

        with col3:
            st.metric(label='Save' ,value=f'{get_total_save(df_filtrado):,.2f} CHF')

        st.success(f'Enviar {get_wise_expenses(df_filtrado):,.2f} CHF para a Wise')

        
        # ------------------- Gastos por dia -------------------
        exp_month, exp_mean_month = expenses_per_month(df_gastos)

        fig1 = px.bar(
            exp_month, 
            x="Mês Pagamento",
            y="Valor",
            text="Valor"
        )
        fig1.add_hline(
            y=exp_mean_month,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Média: {exp_mean_month:.2f} CHF",
            annotation_position="bottom left"
        )
        fig1.update_traces(
            texttemplate='%{text:.2f} CHF',
            textposition='outside', 
            marker_color=GRAPH_COLOR
        )
        fig1.update_layout(
            title="Gastos por Mês",
            xaxis_title="Mês",
            yaxis_title="CHF",
            showlegend=False,
            xaxis=dict(
                tickformat="%d/%m"
            )
        )
        st.plotly_chart(fig1, use_container_width=True)

        # # ------------------- Gastos por Categoria -------------------
        fig2 = px.bar(
            expense_category(df_gastos), 
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
        fig3 = px.bar(
            expenses_per_local(df_gastos), 
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

        # ------------------- Gastos Mercado por Dia -------------------
        # gm = df_gastos[df_gastos['Categoria'] == 'Mercado'].groupby('Mês Pagamento')['Valor'].sum().reset_index()

        # gm['Mês Pagamento'] = gm['Mês Pagamento'].astype(str)

        exp_categ, mean_categ = expenses_per_category(df_gastos, 'Mercado')

        fig4 = px.bar(
            exp_categ,
            x='Mês Pagamento',
            y='Valor', 
            text='Valor'  
        )

        fig4.add_hline(
            y=mean_categ,
            line_dash="dash",
            line_color="white",
            annotation_text=f"Média: {mean_categ:.2f} CHF",
            annotation_position="bottom left"
        )

        fig4.update_traces(
            texttemplate='%{text:.2f} CHF', 
            textposition='outside', 
            marker_color=GRAPH_COLOR
        )
        fig4.update_layout(
            title="Gastos Mercado por Mês de Pagamento",
            xaxis_title="Mês de Pagamento",
            yaxis_title="CHF",
            showlegend=False
        )

        st.plotly_chart(fig4, use_container_width=True)
    
    # PAGINA 2
    with tab2:
        st.write('Tabela')
        st.dataframe(df_filtrado[['Data', 'Local', 'Valor', 'Categoria', 'Saldo']])
        # st.dataframe(df_filtrado)

if __name__ == "__main__":
    main()