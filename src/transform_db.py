import pandas as pd
import numpy as np
from datetime import datetime

def add_categoria(df, df_param):
    df['Categoria'] = df['Local'].map(
        df_param.set_index('Local')['Categoria']
    ).fillna('Extra')
    return df

def add_pagamento(df):
    df['Pagamento?'] = np.where(
        (df['Local'] == "CERN") & (df['Valor'] > 3000),
        "Sim",
        "Não"
    )
    return df

def add_mes_pagamento(df):
    df['Mês Pagamento'] = np.where(
        df['Data'].dt.day >= 25, 
        (df['Data'] + pd.DateOffset(months=1)), 
        df['Data']
    )
    df['Mês Pagamento'] = df['Mês Pagamento'].dt.strftime('%m/%y')
    return df

def add_saldo(df):
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
    return df

def add_mes_atual(df):
    mes_atual = datetime.now().strftime('%m/%y')
    df['Mês Pagamento Atual?'] = np.where(df['Mês Pagamento'] == mes_atual, 'Sim', 'Não')
    return df


def prepare_data(df, df_param):
    df['Data'] = pd.to_datetime(df['Data'])
    df['Data'].dt.strftime('%d/%m/%y')

    df = add_categoria(df, df_param)
    df = add_pagamento(df)
    df = add_mes_pagamento(df)
    df = add_saldo(df)
    df = add_mes_atual(df)
    return df