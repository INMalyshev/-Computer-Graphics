import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

class MyBarForm(Toplevel):
    def __init__(self, parent, x_arr=[1, 2, 3], y_arr=[3, 2, 1]):
        super().__init__(parent)

        self.title("bar")

        f = Figure(figsize=(5, 4), dpi=100)
        f_plot = f.add_subplot(111)

        canvs = FigureCanvasTkAgg(f, self)

        f_plot.bar(x_arr, y_arr)
        canvs.draw()

        canvs = FigureCanvasTkAgg(f, self)
        canvs.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def open(self):
        self.grab_set()
        self.wait_window()
        self.mainloop()
