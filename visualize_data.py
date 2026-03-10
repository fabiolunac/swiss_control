from parameters import *
from excel_utils import *

class Visualize_Data(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_layout()
        self.show_graphs()

    def create_layout(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        self.frame_graf1 = ttk.Frame(self, width=400, height=250)
        self.frame_graf1.grid(row=0, column=0, padx=10, pady=10)
        self.frame_graf1.pack_propagate(False)

        # self.frame_graf2 = ttk.Frame(self, width=400, height=250)
        # self.frame_graf2.grid(row=0, column=1, padx=10, pady=10)
        # self.frame_graf2.pack_propagate(False)


    def show_graphs(self):
        # gera figura -> cria o canvas -> desenha -> pack
        fig1 = fig_gastos_por_dia()
        # fig2 = fig_gastos_categoria()

        self.canvas1 = FigureCanvasTkAgg(fig1, master=self.frame_graf1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack()

        # self.canvas2 = FigureCanvasTkAgg(fig2, master=self.frame_graf2)
        # self.canvas2.draw()
        # self.canvas2.get_tk_widget().pack()


        