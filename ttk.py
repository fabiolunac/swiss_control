from parameters import *

class App():

    def __init__(self, root):
        self.root = root
        self.root.title('Teste TTK')
        self.root.geometry("360x300")

        self.root.bind("<Return>", lambda event: self.salvar())
        self.root.bind("<Escape>", lambda event: root.destroy())

        self.criar_widgets()
        self.configurar_estilo()

    def configurar_estilo(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("aqua")

        self.style.configure("TLabel", font=("Arial", 14))
        self.style.configure("TButton", font=("Arial", 14, "bold"), padding=10)
        self.style.configure("TEntry", padding=6)
    

    def criar_widgets(self):
        self.frame = ttk.Frame(self.root, padding=16)
        self.frame.pack(fill='both', expand=True)

        ttk.Label(self.frame, text='Salvar Valores').grid(row=0, column=0, sticky='ew', columnspan=2, pady=6)

        # ----------- Campo de Data -----------
        ttk.Label(self.frame, text="Data").grid(row=1, column=0, sticky='w', pady=6)

        self.data_var = tk.StringVar(value=today)
        self.data_entry = ttk.Entry(self.frame, width=20, textvariable=self.data_var)
        self.data_entry.grid(row=1, column=1, sticky='ew', pady=6)

        # ----------- Campo de Local -----------
        ttk.Label(self.frame, text="Local").grid(row=2, column=0, sticky='w', pady=6)
        self.local_var = tk.StringVar()
        self.local_entry = ttk.Entry(self.frame, width=20, textvariable=self.local_var)
        self.local_entry.grid(row=2, column=1, sticky='ew', pady=6)

        # ----------- Campo de Valor -----------
        ttk.Label(self.frame, text="Valor (CHF)").grid(row=3, column=0, sticky='w', pady=6)
        self.valor_var = tk.StringVar()
        self.valor_entry = ttk.Entry(self.frame, width=20, textvariable=self.valor_var)
        self.valor_entry.grid(row=3, column=1, sticky='ew', pady=6)

        # ----------- Botão para salvar -----------
        self.btn_salvar = ttk.Button(self.frame, text='Salvar Valores', command=self.salvar)
        self.btn_salvar.grid(row=4, column=0, columnspan=2, sticky='ew', pady=6)


        self.frame.columnconfigure(1, weight=1)

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

        wb = load_workbook(path)

        ws = wb[sheet_name] if sheet_name else wb.active
        ws.append(dados)
        ws.cell(row=ws.max_row, column=1).number_format = "DD/MM/YYYY"
        wb.save(path)

        print(f'Valores adicionados! {dados}')

        self.local_var.set("")
        self.valor_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


#teste