import sqlite3
import pandas as pd

PATH = "/Users/fabioluna/OneDrive - CERN/Swiss Control.xlsx"
transfer = False
transfer_param = True

if transfer:
    df = pd.read_excel(PATH)

    conn = sqlite3.connect('./db/finance_control.db')

    df.to_sql('gastos', conn, if_exists='replace', index=False)

    conn.close()

if transfer_param:
    df = pd.read_excel(PATH, sheet_name='Parâmetros')

    conn = sqlite3.connect('./db/local_param.db')

    df.to_sql('param', conn, if_exists='replace', index=False)

    conn.close()

### Criar tabela de parametros
