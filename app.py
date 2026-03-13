from parameters import *

from add_data import Add_Data
from visualize_data import Visualize_Data
    
class App:
    def __init__(self, root):
        self.root = root
        self.root.title('FINANCE APP')
        self.root.geometry('400x500')

        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.bind("<Return>", lambda event: self.Add_Data.salvar())

        self.configurate_style()
        self.create_widgets()

    def create_widgets(self):
        # Create Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Instancia as abas
        self.Add_Data       = Add_Data(self.notebook)
        self.Visualize_Data = Visualize_Data(self.notebook)

        # Add abas no notebook
        self.notebook.add(self.Add_Data, text='Add Data')
        # self.notebook.add(self.Visualize_Data, text='Visualizar')

    def configurate_style(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("aqua")

        self.style.configure("TLabel", font=("Arial", 14))
        self.style.configure("TButton", font=("Arial", 14, "bold"), padding=1)
        self.style.configure("TEntry", padding=6)
        self.style.configure("TCombobox", padding=6)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

