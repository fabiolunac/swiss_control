import sqlite3
import pandas as pd

# Conectar aos banco de dados

DB_GASTOS = './db/finance_control.db'
DB_PARAM  = './db/local_param.db'

def get_connection(path):
    return sqlite3.connect(path)

def load_gastos():
    with get_connection(DB_GASTOS) as conn:
        df = pd.read_sql_query("SELECT * from gastos ORDER BY Data ASC", conn)

        return df
    
def load_param():
    with get_connection(DB_PARAM) as conn:
        df_param = pd.read_sql_query("SELECT * from param", conn)

        return df_param
