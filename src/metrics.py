import pandas as pd

"""
File to calculate metrics for dashboard, for example:
Calculate total expenses in the month
"""

def total_salary(df):
    return df[df['Pagamento?'] == 'Sim']['Valor'].sum()

def total_expenses(df):
    return df['Valor'].sum()

def get_total_save(df):
    return df[df['Local'] == 'Wise Save']['Valor'].sum()