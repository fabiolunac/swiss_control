import streamlit as st
import pandas as pd
import numpy as np
from parameters import *

def prepare_data(path):
    df = pd.read_excel(path)
    df_parametros = pd.read_excel(path, sheet_name='Parâmetros')

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

def main():
    st.title("Dashboard de Gastos")

    st.button('Reset Filters')

    df = prepare_data(path=PATH)
    st.write('Table')
    st.dataframe(df)

    col1, col2 = st.columns(2)

    with col1:
        st.write('coluna 1')

    with col2:
        st.write('coluna 2')


if __name__ == "__main__":
    main()