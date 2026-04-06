import pandas as pd


def expenses_per_column(df, column):

    if column != 'Data' and column != 'Mês Pagamento':
        exp = df.groupby(column)['Valor'].sum().reset_index().sort_values(by='Valor', ascending=False)
    else:
        exp = df.groupby(column)['Valor'].sum().reset_index()


    if column == 'Mês Pagamento':
        exp['Mês Pagamento'] = exp['Mês Pagamento'].dt.to_timestamp().dt.strftime('%m/%y')

    mean = exp['Valor'].mean()

    return exp, mean



