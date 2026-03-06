from parameters import *

class Visualize_Data(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text='Teste').pack(pady=10)