from parameters import *

class Visualize_Data(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.create_widgets()
        self.create_figure()

    def create_figure(self):
        self.fig = Figure(figsize=(4,4))
        self.ax = self.fig.add_subplot(111)

        x = [1, 2, 3, 4]
        y = [100, 150, 120, 180]

        self.ax.plot(x, y)
        self.ax.set_title("Exemplo de gráfico")
        self.ax.set_xlabel("Pontos")
        self.ax.set_ylabel("Valor")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def create_widgets(self):
        ttk.Label(self, text='Teste').pack(pady=10)
        