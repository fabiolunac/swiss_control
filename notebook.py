from parameters import *

root = tk.Tk()

notebook = ttk.Notebook(root)

aba1 = ttk.Frame(notebook)
aba2 = ttk.Frame(notebook)

notebook.add(aba1, text='Adicionar Dados')
notebook.add(aba2, text='Leitura dos Dados')

notebook.pack(expand=True, fill='both')

ttk.Label(aba1, text="App Financeiro").pack(pady=20)
ttk.Button(aba1, text="Adicionar Linha").pack()

# --- Conteúdo da Aba 2 ---
ttk.Label(aba2, text="App de Calibração").pack(pady=20)
ttk.Entry(aba2).pack()



root.mainloop()