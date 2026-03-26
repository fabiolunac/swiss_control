import pandas as pd

def expenses_per_month(df):
    ex =  df.groupby('Mês Pagamento')['Valor'].sum().reset_index()
    ex['Mês Pagamento'] = ex['Mês Pagamento'].dt.to_timestamp().dt.strftime('%m/%y')

    mean = ex['Valor'].mean()
    
    return ex, mean



def expense_category(df):
    return df.groupby('Categoria')['Valor'].sum().sort_values(ascending=False).reset_index()


def expenses_per_local(df):
    return df.groupby('Local')['Valor'].sum().sort_values(ascending=False).reset_index()

def expenses_per_category(df, category):
    data = df[df['Categoria'] == category].groupby('Mês Pagamento')['Valor'].sum().reset_index()

    data['Mês Pagamento'] = data['Mês Pagamento'].dt.to_timestamp().dt.strftime('%m/%y')

    mean = data['Valor'].mean()

    return data, mean



