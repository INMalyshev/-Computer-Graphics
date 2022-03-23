import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import *

class MyBarForm(Toplevel):
    def __init__(self, parent, x_arr=[1, 2, 3], y_arr=[3, 2, 1]):
        super(MyBarForm, self).__init__(parent)

        self.title("bar")

        f = Figure(figsize=(5, 4), dpi=100) # типа фигура из матплотлиба
        f_plot = f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(f, self)

        f_plot.bar(x_arr, y_arr, width=3)
        # f_plot.set_xticks(x_arr)

        self.canvas.draw()

        # canvas = FigureCanvasTkAgg(f, self)

        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def open(self):
        # self.grab_set()
        # self.wait_window()
        self.mainloop()
