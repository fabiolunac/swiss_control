import sqlite3
import pandas as pd

PATH = "/Users/fabioluna/OneDrive - CERN/Swiss Control.xlsx"
PATH_OLD = "/Users/fabioluna/Downloads/ControleMensal_v2.xlsx"

transfer = False
transfer_param = False
transfer_old = True

if transfer:
    df = pd.read_excel(PATH)

    conn = sqlite3.connect('../db/finance_control.db')

    df.to_sql('gastos', conn, if_exists='replace', index=False)

    conn.close()

if transfer_param:
    df = pd.read_excel(PATH, sheet_name='Parâmetros')

    conn = sqlite3.connect('../db/local_param.db')

    df.to_sql('param', conn, if_exists='replace', index=False)

    conn.close()

if transfer_old:
    df = pd.read_excel(PATH_OLD, sheet_name='Controle')
    
    conn = sqlite3.connect('../db/finance_control.db')

    df.to_sql('gastos', conn, if_exists='append', index=False)

    conn.close()


# conn = sqlite3.connect('../db/old_data.db')

# df = pd.read_sql_query("SELECT * from gastos", conn)

# print(df)
