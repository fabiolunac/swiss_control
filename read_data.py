import pandas as pd
import sqlite3

conn1 = sqlite3.connect('finance_control.db')
conn2 = sqlite3.connect('local_param.db')

df = pd.read_sql_query("SELECT * from gastos", conn1)
df_param = pd.read_sql_query("SELECT * from param", conn2)

print(df)

print(df_param)