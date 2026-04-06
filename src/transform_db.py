import pandas as pd
import numpy as np
from datetime import datetime


def get_periodo_pagamento_atual():
    hoje = pd.Timestamp.today().normalize()
    if hoje.day >= 25:
        hoje = hoje + pd.DateOffset(months=1)
    return hoje.to_period('M')

def add_categoria(df, df_param):
    df['Categoria'] = np.where(
        (df['Local'] == 'CERN') & (df['Valor'] > 3000),
        'Pagamento',
        df['Local'].map(
            df_param.set_index('Local')['Categoria']
        ).fillna('Extra')
    )
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
    df['Mês Pagamento'] = df['Mês Pagamento'].dt.to_period('M')

    df['Ano Pagamento'] = df['Mês Pagamento'].dt.to_timestamp().dt.year

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
    periodo_pagamento_atual = get_periodo_pagamento_atual()
    df['Mês Pagamento Atual?'] = np.where(df['Mês Pagamento'] == periodo_pagamento_atual, 'Sim', 'Não')
    return df

def add_ano_atual(df):
    ano_atual = get_periodo_pagamento_atual().year
    df['Ano Pagamento Atual?'] = np.where(df['Ano Pagamento'] == ano_atual, 'Sim', 'Não')

    return df


def prepare_data(df, df_param):
    df['Data'] = pd.to_datetime(df['Data'], format='mixed')
    df['Data'].dt.strftime('%d/%m/%y')

    df = add_categoria(df, df_param)
    df = add_pagamento(df)
    df = add_mes_pagamento(df)
    df = add_saldo(df)
    df = add_mes_atual(df)
    df = add_ano_atual(df)

    return df
