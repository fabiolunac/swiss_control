from parameters import *

class Add_Data(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text='Salvar Valores').grid(row=0, column=0, sticky='ew', columnspan=2, pady=6)

        # ----------- Campo de Data -----------
        ttk.Label(self, text="Data").grid(row=1, column=0, sticky='w', pady=6)

        self.data_var = tk.StringVar(value=TODAY)
        self.data_entry = ttk.Entry(self, width=20, textvariable=self.data_var)
        self.data_entry.grid(row=1, column=1, sticky='ew', pady=6)

        # ----------- Campo de Local -----------
        ttk.Label(self, text="Local").grid(row=2, column=0, sticky='w', pady=6)
        self.local_var = tk.StringVar()
        self.local_entry = ttk.Entry(self, width=20, textvariable=self.local_var)
        self.local_entry.grid(row=2, column=1, sticky='ew', pady=6)

        # ----------- Campo de Valor -----------
        ttk.Label(self, text="Valor (CHF)").grid(row=3, column=0, sticky='w', pady=6)
        self.valor_var = tk.StringVar()
        self.valor_entry = ttk.Entry(self, width=20, textvariable=self.valor_var)
        self.valor_entry.grid(row=3, column=1, sticky='ew', pady=6)

        # ----------- Botão para salvar -----------
        self.btn_salvar = ttk.Button(self, text='Salvar Valores', command=self.salvar)
        self.btn_salvar.grid(row=4, column=0, columnspan=2, sticky='ew', pady=6)

        # ----------- Botão para mostrar saldo -----------
        self.btn_lastdata= ttk.Button(self, text='Últimos Dados', command=self.read_last_line)
        self.btn_lastdata.grid(row=5, column=0, columnspan=2, sticky='ew', pady=6)

        # ----------- Label para últimos dados -----------
        self.lastdados_var = tk.StringVar()
        ttk.Label(self, textvariable=self.lastdados_var).grid(
            row=6, column=0, sticky='w', pady=6, columnspan=2
            )

        # ----------- Label para dados adicionados -----------
        self.dadosadd = tk.StringVar()
        ttk.Label(self, textvariable=self.dadosadd).grid(
            row=7, column=0, sticky='w', pady=6, columnspan=2
            )

        self.columnconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)

    def salvar(self, sheet_name=None):
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

        dados = [data, self.local_entry.get(), valor]

        wb = load_workbook(PATH)

        ws = wb[sheet_name] if sheet_name else wb.active
        ws.append(dados)
        ws.cell(row=ws.max_row, column=1).number_format = "DD/MM/YYYY"
        wb.save(PATH)

        dados_line = f"Dados adicionados: \n{data.strftime('%d/%m')} | {self.local_entry.get()} | {valor} CHF"

        self.local_var.set("")
        self.valor_var.set("")

        self.dadosadd.set(dados_line)

    def read_last_line(self):
        self.df = pd.read_excel(PATH)

        last_values = self.df.iloc[-1].to_dict()

        last_data = last_values['Data']

        last_local = last_values['Local']

        last_valor = last_values['Valor']

        last_line = f"{last_data.strftime('%d/%m')} | {last_local} | {last_valor} CHF"

        self.lastdados_var.set(last_line)