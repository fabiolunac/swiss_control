import sqlite3
import pandas as pd

# Conectar aos banco de dados

DB_GASTOS = './db/finance_control.db'
DB_PARAM  = './db/local_param.db'

def get_connection(path):
    return sqlite3.connect(path)

def load_gastos():
    with get_connection(DB_GASTOS) as conn:
        df = pd.read_sql_query(
            "SELECT rowid AS id, * from gastos ORDER BY Data ASC",
            conn
        )
        df = df.rename(columns={'banco': 'Banco', 'tipo': 'Tipo'})

        return df
    
def load_param():
    with get_connection(DB_PARAM) as conn:
        df_param = pd.read_sql_query("SELECT * from param", conn)
        return df_param

def load_param_with_id():
    with get_connection(DB_PARAM) as conn:
        return pd.read_sql_query("SELECT rowid AS id, * FROM param ORDER BY Local ASC", conn)

def add_param(local, categoria, categoria_geral=None):
    with get_connection(DB_PARAM) as conn:
        conn.execute(
            "INSERT INTO param (Local, Categoria, \"Categoria Geral\") VALUES (?, ?, ?)",
            (local, categoria, categoria_geral)
        )
        conn.commit()

def update_param(id, local, categoria, categoria_geral=None):
    with get_connection(DB_PARAM) as conn:
        conn.execute(
            "UPDATE param SET Local=?, Categoria=?, \"Categoria Geral\"=? WHERE rowid=?",
            (local, categoria, categoria_geral, int(id))
        )
        conn.commit()

def delete_param(ids):
    if not ids:
        return 0
    placeholders = ",".join("?" for _ in ids)
    with get_connection(DB_PARAM) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM param WHERE rowid IN ({placeholders})", ids)
        conn.commit()
        return cursor.rowcount

def update_gasto(id, data, local, valor, banco, tipo):
    with get_connection(DB_GASTOS) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE gastos SET data=?, local=?, valor=?, banco=?, tipo=? WHERE rowid=?",
            (str(data), local, float(valor), banco, tipo, int(id))
        )
        conn.commit()
        return cursor.rowcount


def delete_gastos(ids):
    if not ids:
        return 0

    placeholders = ",".join("?" for _ in ids)

    with get_connection(DB_GASTOS) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM gastos WHERE rowid IN ({placeholders})",
            ids
        )
        conn.commit()

        return cursor.rowcount
