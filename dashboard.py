import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pandas as pd
import sqlite3

from src.database import delete_gastos, load_gastos, load_param
from src.transform_db import prepare_data
from src.metrics import total_salary, total_expenses, get_total_save, get_wise_expenses
from src.charts import *
from src.figures import *

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

def add_line_gastos(conn, date, local, valor):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO gastos (data, local, valor)
        VALUES (?, ?, ?)
        """,
        (date, local, valor)
    )

    conn.commit()

def render_delete_table(df, key_prefix):
    df_delete = df[['id', 'Data', 'Local', 'Valor', 'Categoria', 'Saldo']].copy()
    df_delete['Remover'] = False

    confirm_ids_key = f'{key_prefix}_confirm_delete_ids'

    edited_df = st.data_editor(
        df_delete,
        hide_index=True,
        disabled=['id', 'Data', 'Local', 'Valor', 'Categoria', 'Saldo'],
        column_config={
            'id': st.column_config.NumberColumn('ID', disabled=True),
            'Data': st.column_config.DateColumn('Data'),
            'Local': st.column_config.TextColumn('Local'),
            'Valor': st.column_config.NumberColumn('Valor', format='%.2f CHF'),
            'Categoria': st.column_config.TextColumn('Categoria'),
            'Saldo': st.column_config.NumberColumn('Saldo', format='%.2f CHF'),
            'Remover': st.column_config.CheckboxColumn('Remover')
        },
        key=f'{key_prefix}_delete_editor'
    )

    ids_to_delete = edited_df.loc[edited_df['Remover'], 'id'].tolist()

    if st.button('Excluir selecionados', key=f'{key_prefix}_delete_button'):
        if not ids_to_delete:
            st.warning('Selecione pelo menos uma linha para remover.')
        else:
            st.session_state[confirm_ids_key] = ids_to_delete

    pending_delete_ids = st.session_state.get(confirm_ids_key, [])

    if pending_delete_ids:
        st.warning(f'Tem certeza que deseja remover {len(pending_delete_ids)} registro(s)?')

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button('Confirmar exclusão', key=f'{key_prefix}_confirm_delete_button'):
                deleted_rows = delete_gastos(pending_delete_ids)
                st.session_state.pop(confirm_ids_key, None)
                st.success(f'{deleted_rows} registro(s) removido(s) com sucesso.')
                st.rerun()

        with cancel_col:
            if st.button('Cancelar', key=f'{key_prefix}_cancel_delete_button'):
                st.session_state.pop(confirm_ids_key, None)
                st.info('Exclusão cancelada.')
                st.rerun()


def days_until_25():
    today = datetime.today()
    year = today.year
    month = today.month

    if today.day > 25:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

    next_25 = datetime(year, month, 25)
    return (next_25 - today).days

def create_date_table():
    df_date = pd.DataFrame({
        'Data': pd.date_range(
            start='07/02/2025',
            end='31/12/2026',
            freq='D'
        )
    })
    df_date['Mes_Ano'] = df_date['Data'].dt.to_period('M') 

    return df_date
def main():

    # Loading data frames
    df_raw = load_gastos()
    df_param = load_param()
    df = prepare_data(df_raw, df_param)

    df_date = create_date_table()

    df = df_date.merge(df, how='left', on='Data')


    

    # personalize_metric()

    st.title("Finance App")
    
    tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Dia', 'Tabela', 'Adicionar Dados'])

    st.sidebar.header('Filtros')

    # list all options for columns
    categoria_options = df['Categoria'].unique()
    reset_filtros = st.sidebar.button('Resetar Filtros')

    if reset_filtros:
        st.session_state['categoria'] = 'Todos'
        st.session_state['mes_pag_atual'] = False
        st.session_state['ano_pag_atual'] = True
        st.session_state['mes_pag'] = 'Todos'

    mes_pagamento_atual = st.sidebar.checkbox(
        'Mês Pagamento Atual?', 
        key='mes_pag_atual'
    )

    ano_pagamento_atual = st.sidebar.checkbox(
        'Ano Pagamento Atual?', 
        key='ano_pag_atual'
    )

    df_datas_disponiveis = df.copy()
    if mes_pagamento_atual:
        df_datas_disponiveis = df_datas_disponiveis[df_datas_disponiveis['Mês Pagamento Atual?'] == 'Sim']
    if ano_pagamento_atual:
        df_datas_disponiveis = df_datas_disponiveis[df_datas_disponiveis['Ano Pagamento Atual?'] == 'Sim']

    mes_options = pd.Index(df_datas_disponiveis['Mês Pagamento'].unique()).sort_values()
    mes_options_list = list(mes_options)
    mes_select_options = ['Todos', *mes_options_list]

    mes_selecionado = st.session_state.get('mes_pag', 'Todos')
    if reset_filtros or mes_selecionado not in mes_select_options:
        st.session_state['mes_pag'] = 'Todos'

    categoria = st.sidebar.selectbox(
        "Categoria",
        ['Todos', *categoria_options],
        key='categoria'
    )

    mes_pagamento = st.sidebar.selectbox(
        "Mês do Pagamento",
        mes_select_options,
        key='mes_pag'
    )

    filtro_categoria = pd.Series(True, index=df.index) if categoria == 'Todos' else df['Categoria'] == categoria
    filtro_mes = pd.Series(True, index=df.index) if mes_pagamento == 'Todos' else df['Mês Pagamento'] == mes_pagamento
    df_filtrado = df[
        filtro_categoria &
        filtro_mes
    ]

    if mes_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Mês Pagamento Atual?'] == 'Sim']

    if ano_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Ano Pagamento Atual?'] == 'Sim']

    # df_filtrado['Data'] = df_filtrado['Data'].dt.strftime('%d/%m/%y')
    df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'])

    # =========================================== PAGINA 1 ===========================================
    with tab1:
        df_gastos = df_filtrado[(df_filtrado['Pagamento?'] == 'Não') & (df_filtrado['Local'] != 'Wise Save')]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label='Salário', value=f'{total_salary(df_filtrado):,.0f} CHF')

        with col2:
            st.metric(label='Gastos', value=f'{total_expenses(df_gastos):,.2f} CHF')

        with col3:
            st.metric(label='Save' ,value=f'{get_total_save(df_filtrado):,.2f} CHF')

        # st.success(f'Enviar {get_wise_expenses(df_filtrado):,.2f} CHF para a Wise')

        

        saldo_atual = df_gastos['Saldo'].iloc[-1]
        st.metric(label='Saldo', value= f'{saldo_atual:,.2f} CHF')

        st.metric(label='Gastos Previsto por Dia', value=f'{saldo_atual/days_until_25():,.2f} CHF')
        
        

        
        
        # ------------------- Gastos por Mês -------------------
        # exp_month, exp_mean_month = expenses_per_column(df_gastos, column='Mês Pagamento')
        # st.plotly_chart(fig_expenses_per_column(exp_month, mean=exp_mean_month, column='Mês Pagamento'), use_container_width=True)

        # # # ------------------- Gastos por Categoria -------------------
        # exp_category, _ = expenses_per_column(df_gastos, column='Categoria')
        # st.plotly_chart(fig_expenses_per_column(exp_category, column='Categoria'), use_container_width=True)

        # # ------------------- Gastos por Local -------------------
        # exp_local, _ = expenses_per_column(df_gastos, column='Local')
        # st.plotly_chart(fig_expenses_per_column(exp_local, column='Local'), use_container_width=True)


    # =========================================== PAGINA 2 ===========================================
    with tab2:
        # ------------------- Gastos por Dia -------------------
        exp_day, exp_mean_day = expenses_per_column(df_gastos, column='Data')
        st.plotly_chart(fig_expenses_per_column(exp_day, column='Data', mean=exp_mean_day), use_container_width=True)

    
    # =========================================== PAGINA 3 ===========================================
    with tab3:
        st.write('Tabela')
        render_delete_table(df_filtrado, 'tab2')

    # =========================================== PAGINA 4 ===========================================
    with tab4:
        st.write('Adicionar Dados')

        date = st.date_input('Data')
        local = st.text_input('Local')
        valor = st.number_input('Valor (CHF)')

        bt_add = st.button('Adicionar')

        if bt_add:
            if date and local and valor > 0:
                st.markdown(f'''
                ## Adicionados:
                - Data: {date}
                - Local: {local}
                - Valor: {valor}            
                ''')
                add_line_gastos(sqlite3.connect('./db/finance_control.db'), date, local, valor)

            else:
                print('Preencha os campos corretamente')



if __name__ == "__main__":
    main()
