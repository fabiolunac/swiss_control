import streamlit as st
import pandas as pd
import numpy as np
from excel_utils import prepare_data
import plotly.express as px

GRAPH_COLOR = '#b82b30'
PATH = "/Users/fabioluna/OneDrive - CERN/Swiss Control.xlsx"

def prepare_data():
    df = pd.read_excel(PATH)
    df_parametros = pd.read_excel(PATH, sheet_name='Parâmetros')

    df['Data'] = pd.to_datetime(df['Data'])

    #Criacao das novas colunas
    df['Categoria'] = df['Local'].map(
        df_parametros.set_index('Local')['Categoria']
    ).fillna('Extra')

    df['Pagamento?'] = np.where(
        (df['Local'] == "CERN") & (df['Valor'] > 3000),
        "Sim",
        "Não"
    )
    df['Mês Pagamento'] = np.where(
        df['Data'].dt.day >= 25, 
        (df['Data'] + pd.DateOffset(months=1)), 
        df['Data']
    )
    df['Mês Pagamento'] = df['Mês Pagamento'].dt.strftime('%m/%y')


    saldo = []
    for i, row in df.iterrows():
        if i == 0:
            saldo_atual = 3486

        elif row['Pagamento?'] == 'Sim':
            saldo_atual = 3486

        else:
            saldo_atual = saldo[-1] - row['Valor']
        
        saldo.append(saldo_atual)

    df['Saldo'] = saldo

    df['Mês Pagamento Atual?'] = np.where(df['Mês Pagamento'] == MES_ATUAL, 'Sim', 'Não')

    return df

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
    personalize_metric()

    st.title("Finance App")
    df = prepare_data()
    
    tab1, tab2 = st.tabs(['Gráficos', 'Tabela'])

    btn_filter = st.sidebar.header('Filtros')

    st.sidebar.button('Resetar Filtros')

    categoria = st.sidebar.multiselect(
        "Categoria",
        df["Categoria"].unique(),
        default=df["Categoria"].unique()
    )

    mes_pagamento_atual = st.sidebar.multiselect(
        "Mês do Pagamento Atual?",
        df["Mês Pagamento Atual?"].unique(),
        default=df["Mês Pagamento Atual?"].unique()
    )

    mes_pagamento = st.sidebar.multiselect(
        "Mês do Pagamento",
        df["Mês Pagamento"].unique(),
        default=df["Mês Pagamento"].unique()
    )

    df_filtrado = df[
        df['Categoria'].isin(categoria) &
        df["Mês Pagamento Atual?"].isin(mes_pagamento_atual) &
        df['Mês Pagamento'].isin(mes_pagamento)
    ]

    # PAGINA 1
    with tab1:
        df_gastos = df_filtrado[(df_filtrado['Pagamento?'] == 'Não') & (df_filtrado['Local'] != 'Wise Save')]
        df_gastos['Data'] = pd.to_datetime(df_gastos['Data'])

        col1, col2, col3 = st.columns(3)

        with col1:
            gastos_totais = df_gastos['Valor'].sum()

            st.metric(
                label='Gasto Total',
                value=f'{gastos_totais:.2f} CHF'
            )
        with col2:
            saldo_guardado = df_filtrado[df_filtrado['Local'] == 'Wise Save']['Valor'].sum()

            st.metric(
                label='Saldo Guardado',
                value=f'{saldo_guardado:.2f} CHF'
            )
        with col3:
            saldo_atual = df['Saldo'].iloc[-1]

            st.metric(
                label='Saldo Atual',
                value=f'{saldo_atual:.2f} CHF'
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