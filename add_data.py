from functions import *
from tkinter import ttk
import tkinter as tk
import sqlite3

class Add_Data(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()
        self.create_database()

    def create_widgets(self):
        # ttk.Label(self, text='Salvar Valores', anchor='center').grid(row=0, column=0, sticky='ew', columnspan=2, pady=6)

        # ----------- Campo de Data -----------
        ttk.Label(self, text="Data").grid(row=1, column=0, sticky='w', pady=6)

        self.data_entry = DateEntry(
            self,
            width=18,
            date_pattern='dd/MM/yyyy'
        )
        self.data_entry.grid(row=1, column=1, stick='ew', pady=6)

        # ----------- Campo de Local -----------
        ttk.Label(self, text="Local").grid(row=2, column=0, sticky='w', pady=6)
        self.local_var = tk.StringVar()
        self.local_entry = ttk.Entry(self, width=20, textvariable=self.local_var)
        self.local_entry.grid(row=2, column=1, sticky='ew', pady=6)

        # ----------- Campo de Valor -----------
        ttk.Label(self, text="Valor").grid(row=3, column=0, sticky='w', pady=6)
        self.valor_var = tk.StringVar()
        self.valor_entry = ttk.Entry(self, width=20, textvariable=self.valor_var)
        self.valor_entry.grid(row=3, column=1, sticky='ew', pady=6)

        # ----------- Campo de Moeda -----------
        ttk.Label(self, text="Moeda").grid(row=4, column=0, sticky='w', pady=6)
        self.moeda_var = tk.StringVar(value='CHF')
        self.moeda_box = ttk.Combobox(
            self,
            textvariable=self.moeda_var,
            values=["CHF", "EUR"],
            state="readonly",
            width=17
        )
        self.moeda_box.grid(row=4, column=1, sticky='ew', pady=6)

        # ----------- Botão para salvar -----------
        self.btn_salvar = ttk.Button(self, text='Salvar Valores', command=self.salvar)
        self.btn_salvar.grid(row=5, column=0, columnspan=2, sticky='ew', pady=6)

        # ----------- Botão para mostrar saldo -----------
        self.btn_lastdata= ttk.Button(self, text='Últimos Dados', command=self.read_last_line_method)
        self.btn_lastdata.grid(row=6, column=0, columnspan=2, sticky='ew', pady=6)

        # ----------- Label para últimos dados -----------
        self.lastdados_var = tk.StringVar()
        ttk.Label(self, textvariable=self.lastdados_var).grid(
            row=7, column=0, sticky='w', pady=6, columnspan=2
            )

        # ----------- Label para dados adicionados -----------
        self.dadosadd = tk.StringVar()
        ttk.Label(self, textvariable=self.dadosadd).grid(
            row=8, column=0, sticky='w', pady=6, columnspan=2
            )
    

        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)

    def create_database(self):
        self.conn = sqlite3.connect('./db/finance_control.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            local TEXT NOT NULL,
            valor REAL NOT NULL
        )
        """)
        self.conn.commit()

    def salvar(self):
        try:
            data = parse_date_input(self.data_entry.get())
        except ValueError as exc:
            print(str(exc))
            return

        valor_raw = self.valor_entry.get()

        try:
            valor = float(valor_raw.replace(",", "."))
        except ValueError:
            valor = valor_raw

        moeda = self.moeda_var.get()
        if moeda == 'EUR':
            rate = eur_chf()
            valor_eur = valor * rate
            valor_chf = valor_eur
        else:
            valor_chf = valor


        dados = [data, self.local_entry.get(), valor_chf]

        # salvar_dados(PATH, dados)
        # trocar pra adicionar linhas na DB
        self.cursor.execute("""
            INSERT INTO gastos (data, local, valor)
            VALUES (?, ?, ?)
            """, (data, self.local_entry.get(), valor_chf))
        self.conn.commit()


        dados_line = f"Dados adicionados: \n{data.strftime('%d/%m')} | {self.local_entry.get()} | {valor_chf} CHF"

        self.local_var.set("")
        self.valor_var.set("")

        self.dadosadd.set(dados_line)

    def read_last_line_method(self):
        data, local, valor = read_last_line(PATH)

        last_line = f"{data.strftime('%d/%m')} | {local} | {valor} CHF"

        self.lastdados_var.set(last_line)