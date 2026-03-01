from parameters import *


class App():


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

        # Limpar os dados
        self.local_var.set("")  
        self.valor_var.set("")  


    def __init__(self, root):
        self.root = root
        self.root.title('Minha Janela')
        self.root.geometry('400x500')

        self.style = ttk.Style(root)
        self.style.theme_use("clam")

        # Teclas de atalho
        self.root.bind("<Return>", lambda event: self.salvar())
        self.root.bind("<Escape>", lambda event: root.destroy())

        # ---------------- Campo de data ----------------
        self.data_label = tk.Label(root, text=f'Data')
        self.data_label.pack()

        self.data_var = tk.StringVar(value=today)
        self.data_entry = tk.Entry(root, textvariable=self.data_var)
        self.data_entry.pack(pady=20)

        # ---------------- Campo de Local ----------------
        self.local_label = tk.Label(root, text=f'Local')
        self.local_label.pack()
        
        # Declarar StringVar pra armazenar o valor
        self.local_var = tk.StringVar()
        self.local_entry = tk.Entry(root, textvariable=self.local_var)
        self.local_entry.pack(pady=20)

        # ---------------- Campo de Valor ----------------
        self.valor_label = tk.Label(root, text=f'Valor (CHF)')
        self.valor_label.pack()

        self.valor_var = tk.StringVar()
        self.valor_entry = tk.Entry(root, textvariable=self.valor_var)
        self.valor_entry.pack(pady=20)

        # ---------------- Botão pra adicionar ----------------
        self.add_button = tk.Button(root, text='Adicionar Valores', command=self.salvar)
        self.add_button.pack(pady=20)


root = tk.Tk()
app = App(root)
root.mainloop()
