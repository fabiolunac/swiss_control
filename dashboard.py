import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pandas as pd
import sqlite3
import requests

from src.database import delete_gastos, load_gastos, load_param, update_gasto, load_param_with_id, add_param, update_param, delete_param
from src.transform_db import prepare_data
from src.metrics import total_salary, total_expenses, get_total_save, get_wise_expenses
from src.charts import *
from src.figures import *

GRAPH_COLOR = '#b82b30'
# GRAPH_COLOR = '#ffffff'

SALARIO = 3486
MERCADO_META = 550
FIXO_META = 1256
SAVE_META = 800
EXTRA_META = SALARIO - FIXO_META - SAVE_META - MERCADO_META

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

def add_line_gastos(conn, date, local, valor, banco='yuh', tipo='Gasto'):
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO gastos (data, local, valor, banco, tipo)
        VALUES (?, ?, ?, ?, ?)
        """,
        (date, local, valor, banco, tipo)
    )

    conn.commit()

def render_delete_table(df, key_prefix):
    df_delete = df[['id', 'Data', 'Local', 'Valor', 'Banco', 'Tipo', 'Categoria', 'Categoria Geral', 'Saldo']].copy()
    df_delete['Remover'] = False

    confirm_ids_key = f'{key_prefix}_confirm_delete_ids'

    edited_df = st.data_editor(
        df_delete,
        hide_index=True,
        disabled=['id', 'Categoria', 'Saldo'],
        column_config={
            'id': st.column_config.NumberColumn('ID', disabled=True),
            'Data': st.column_config.DateColumn('Data'),
            'Local': st.column_config.TextColumn('Local'),
            'Valor': st.column_config.NumberColumn('Valor', format='%.2f CHF'),
            'Banco': st.column_config.SelectboxColumn('Banco', options=['yuh', 'wise']),
            'Tipo': st.column_config.SelectboxColumn('Tipo', options=['Gasto', 'Input', 'Transferência']),
            'Categoria': st.column_config.TextColumn('Categoria', disabled=True),
            'Categoria Geral': st.column_config.TextColumn('Categoria Geral', disabled=True),
            'Saldo': st.column_config.NumberColumn('Saldo', format='%.2f CHF', disabled=True),
            'Remover': st.column_config.CheckboxColumn('Remover')
        },
        key=f'{key_prefix}_delete_editor'
    )

    edit_col, delete_col = st.columns(2)

    with edit_col:
        if st.button('Salvar alterações', key=f'{key_prefix}_save_button'):
            compare_cols = ['Data', 'Local', 'Valor', 'Banco', 'Tipo']
            original = df_delete[compare_cols].copy()
            edited = edited_df[compare_cols].copy()
            original['Data'] = pd.to_datetime(original['Data']).dt.date
            edited['Data'] = pd.to_datetime(edited['Data']).dt.date
            changed_mask = (original != edited).any(axis=1)
            changed_rows = edited_df[changed_mask]
            if changed_rows.empty:
                st.info('Nenhuma alteração detectada.')
            else:
                for _, row in changed_rows.iterrows():
                    update_gasto(row['id'], row['Data'], row['Local'], row['Valor'], row['Banco'], row['Tipo'])
                st.success(f'{len(changed_rows)} registro(s) atualizado(s) com sucesso.')
                st.rerun()

    ids_to_delete = edited_df.loc[edited_df['Remover'], 'id'].tolist()

    with delete_col:
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


def render_param_table():
    EDIT_COLS = ['Local', 'Categoria', 'Categoria Geral']

    st.subheader('Adicionar novo registro')
    col1, col2, col3 = st.columns(3)
    with col1:
        novo_local = st.text_input('Local', key='param_new_local')
    with col2:
        nova_categoria = st.text_input('Categoria', key='param_new_categoria')
    with col3:
        nova_cat_geral = st.text_input('Categoria Geral', key='param_new_cat_geral')

    if st.button('Adicionar', key='param_add_button'):
        if novo_local and nova_categoria:
            add_param(novo_local, nova_categoria, nova_cat_geral or None)
            st.success(f'"{novo_local}" adicionado.')
            st.rerun()
        else:
            st.warning('Preencha Local e Categoria antes de adicionar.')

    st.divider()

    df_param = load_param_with_id()
    df_edit = df_param.copy()
    df_edit['Remover'] = False

    confirm_ids_key = 'param_confirm_delete_ids'

    edited_df = st.data_editor(
        df_edit,
        hide_index=True,
        disabled=['id'],
        column_config={
            'id': st.column_config.NumberColumn('ID', disabled=True),
            'Local': st.column_config.TextColumn('Local'),
            'Categoria': st.column_config.TextColumn('Categoria'),
            'Categoria Geral': st.column_config.TextColumn('Categoria Geral'),
            'Remover': st.column_config.CheckboxColumn('Remover'),
        },
        key='param_editor'
    )

    save_col, delete_col = st.columns(2)

    with save_col:
        if st.button('Salvar alterações', key='param_save_button'):
            original = df_edit[EDIT_COLS].fillna('')
            edited = edited_df[EDIT_COLS].fillna('')
            changed_mask = (edited != original).any(axis=1)
            changed_rows = edited_df[changed_mask]
            if changed_rows.empty:
                st.info('Nenhuma alteração detectada.')
            else:
                for _, row in changed_rows.iterrows():
                    update_param(row['id'], row['Local'], row['Categoria'], row['Categoria Geral'] or None)
                st.success(f'{len(changed_rows)} registro(s) atualizado(s).')
                st.rerun()

    with delete_col:
        ids_to_delete = edited_df.loc[edited_df['Remover'], 'id'].tolist()
        if st.button('Excluir selecionados', key='param_delete_button'):
            if not ids_to_delete:
                st.warning('Selecione pelo menos uma linha para remover.')
            else:
                st.session_state[confirm_ids_key] = ids_to_delete

    pending_delete_ids = st.session_state.get(confirm_ids_key, [])
    if pending_delete_ids:
        st.warning(f'Tem certeza que deseja remover {len(pending_delete_ids)} registro(s)?')
        confirm_col, cancel_col = st.columns(2)
        with confirm_col:
            if st.button('Confirmar exclusão', key='param_confirm_delete_button'):
                delete_param(pending_delete_ids)
                st.session_state.pop(confirm_ids_key, None)
                st.success('Registro(s) removido(s) com sucesso.')
                st.rerun()
        with cancel_col:
            if st.button('Cancelar', key='param_cancel_delete_button'):
                st.session_state.pop(confirm_ids_key, None)
                st.info('Exclusão cancelada.')
                st.rerun()



def days_until_next_payment(df):
    today = datetime.today()

    pagamentos = df[(df['Local'] == 'CERN') & (df['Valor'] > 3000)].copy()
    dia_pag = int(pagamentos['Data'].dt.day.iloc[-1]) if not pagamentos.empty else 25

    year = today.year
    month = today.month

    if today.day >= dia_pag:
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1

    next_payment = datetime(year, month, dia_pag)
    return (next_payment - today).days


def chf_to_brl():
    url = "https://api.frankfurter.app/latest?from=CHF&to=BRL"
    response = requests.get(url)
    data = response.json()
    
    return data["rates"]["BRL"]

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

def generate_prog_bar(df, type):
    mapping_type = {
        'Mercado': MERCADO_META,
        'Extra': EXTRA_META,
        'Fixo': FIXO_META,
        'Save': SAVE_META
    }
    gastos = df[df['Categoria Geral'] == type]['Valor'].sum()
    meta = mapping_type.get(type)
    pct = gastos / meta
    restante = meta - gastos

    if pct >= 1.0:
        color = '#B82B30'
    elif pct >= 0.8:
        color = '#F5A623'
    else:
        color = '#28a745'

    st.markdown(f'### {type}')
    st.markdown(f"""
<div style="background-color: #e0e0e0; border-radius: 8px; height: 18px; margin-bottom: 4px;">
    <div style="width: {min(pct, 1.0)*100:.1f}%; background-color: {color}; height: 18px; border-radius: 8px;"></div>
</div>
""", unsafe_allow_html=True)

    if restante > 0:
        st.caption(f'{gastos:.2f} / {meta} CHF  ({pct*100:.1f}%) — Sobram **{restante:.2f} CHF**')
    else:
        st.caption(f'{gastos:.2f} / {meta} CHF  ({pct*100:.1f}%) — **Ultrapassou {abs(restante):.2f} CHF**')


def main():

    # Loading data frames
    df_raw = load_gastos()
    df_param = load_param()
    df = prepare_data(df_raw, df_param)

    df_date = create_date_table()

    df = df_date.merge(df, how='left', on='Data')

    st.title("Controle Financeiro")
    
    tab1, tab2, tab3, tab5, tab6 = st.tabs(
        [
            'Controle', 
            'Tabela', 
            'Adicionar Dados', 
            'Parâmetros',
            'Dia'
        ]
    )

    st.sidebar.header('Filtros')

    # list all options for columns
    categoria_options = df['Categoria'].unique()
    categoria_geral_options = df['Categoria Geral'].unique()
    reset_filtros = st.sidebar.button('Resetar Filtros')

    if reset_filtros:
        st.session_state['categoria'] = 'Todos'
        st.session_state['mes_pag_atual'] = False
        st.session_state['ano_pag_atual'] = True
        st.session_state['mes_pag'] = 'Todos'
        st.session_state['categoria_geral'] = 'Todos'

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

    categoria_geral = st.sidebar.selectbox(
        'Categoria Geral',
        ['Todos', *categoria_geral_options],
        key='categoria_geral'
    )

    mes_pagamento = st.sidebar.selectbox(
        "Mês do Pagamento",
        mes_select_options,
        key='mes_pag'
    )

    filtro_categoria = pd.Series(True, index=df.index) if categoria == 'Todos' else df['Categoria'] == categoria
    filtro_categoria_geral = pd.Series(True, index=df.index) if categoria_geral == 'Todos' else df['Categoria Geral'] == categoria_geral
    filtro_mes = pd.Series(True, index=df.index) if mes_pagamento == 'Todos' else df['Mês Pagamento'] == mes_pagamento
    df_filtrado = df[
        filtro_categoria &
        filtro_mes &
        filtro_categoria_geral
    ]

    if mes_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Mês Pagamento Atual?'] == 'Sim']

    if ano_pagamento_atual:
        df_filtrado = df_filtrado[df_filtrado['Ano Pagamento Atual?'] == 'Sim']

    # df_filtrado['Data'] = df_filtrado['Data'].dt.strftime('%d/%m/%y')
    df_filtrado['Data'] = pd.to_datetime(df_filtrado['Data'])

    df_gastos = df_filtrado[(df_filtrado['Pagamento?'] == 'Não') & (df_filtrado['Local'] != 'Wise Save')]

    with tab1:
        today = datetime.today()
        days_remaining = days_until_next_payment(df_raw)

        categorias_controle = ['Fixo', 'Save', 'Extra', 'Mercado']
        total_orcado = FIXO_META + SAVE_META + EXTRA_META + MERCADO_META
        total_gasto = df_gastos[df_gastos['Categoria Geral'].isin(categorias_controle)]['Valor'].sum()
        gasto_diario_medio = total_gasto / today.day if today.day > 0 else 0
        projecao_pagamento = total_gasto + gasto_diario_medio * days_remaining
        delta_val = total_gasto - total_orcado

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric('Salário', f'{total_orcado:,.0f} CHF')
        with col_s2:
            st.metric('Total Gasto', f'{total_gasto:,.2f} CHF', delta=f'{delta_val:+.2f} CHF', delta_color='inverse')
        with col_s3:
            st.metric(
                'Dias até Pagamento',
                f'{days_remaining} dias',
                help=f'Média diária: {gasto_diario_medio:.2f} CHF/dia · Projeção até pagamento: {projecao_pagamento:.2f} CHF'
            )

        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            generate_prog_bar(df_gastos, 'Fixo')
            generate_prog_bar(df_gastos, 'Extra')
        with col_b:
            generate_prog_bar(df_gastos, 'Save')
            generate_prog_bar(df_gastos, 'Mercado')

    # =========================================== PAGINA 2 ===========================================
    with tab6:
        # ------------------- Waterfall Saldo -------------------
        st.plotly_chart(fig_waterfall_saldo(df_filtrado, df_gastos), use_container_width=True)

        # ------------------- Gastos por Dia -------------------
        exp_day, exp_mean_day = expenses_per_column(df_gastos, column='Data')
        st.plotly_chart(fig_expenses_per_column(exp_day, column='Data', mean=exp_mean_day), use_container_width=True)

        exp_type, exp_mean_type = expenses_per_column(df_gastos, column='Categoria')
        st.plotly_chart(fig_expenses_per_column(exp_type, column='Categoria', mean=exp_mean_type), use_container_width=True)

        exp_categ, exp_mean_categ = expenses_per_column(df_gastos, column='Categoria Geral')
        st.plotly_chart(fig_expenses_per_column(exp_categ, column='Categoria Geral', mean=exp_mean_categ), use_container_width=True)
        
    
    # =========================================== PAGINA 3 ===========================================
    with tab2:
        st.write('Tabela')
        render_delete_table(df_filtrado, 'tab2')
        # st.dataframe(df_filtrado)
        st.download_button(
            label='Baixar CSV',
            data=df_raw.to_csv(index=False).encode('utf-8'),
            file_name='gastos.csv',
            mime='text/csv'
        )
    # =========================================== PAGINA 4 ===========================================
    with tab3:
        st.write('Adicionar Dados')

        date = st.date_input('Data')
        local = st.text_input('Local')
        valor = st.number_input('Valor (CHF)')
        banco = st.selectbox('Banco', ['yuh', 'wise'], index=0)
        tipo = st.selectbox('Tipo', ['Gasto', 'Input', 'Transferência'], index=0)

        bt_add = st.button('Adicionar')

        if bt_add:
            if date and local and valor > 0:
                st.markdown(f'''
                ## Adicionados:
                - Data: {date}
                - Local: {local}
                - Valor: {valor}
                - Banco: {banco}
                - Tipo: {tipo}
                ''')
                add_line_gastos(sqlite3.connect('./db/finance_control.db'), date, local, valor, banco, tipo)

            else:
                print('Preencha os campos corretamente')

    with tab5:
        st.subheader('Parâmetros')
        render_param_table()




if __name__ == "__main__":
    main()
