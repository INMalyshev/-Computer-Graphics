from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror

from src.vector import Vector

class AddDotForm(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.x = StringVar()
        self.y = StringVar()

        label = Label(self, text="add dot")
        entry_x = Entry(self, textvariable=self.x)
        entry_y = Entry(self, textvariable=self.y)
        btn = Button(self, text="add", command=self.destroy)

        label.grid(row=0, columnspan=2)
        Label(self, text="x").grid(row=1, column=0)
        Label(self, text="y").grid(row=2, column=0)
        entry_x.grid(row=1, column=1)
        entry_y.grid(row=2, column=1)
        btn.grid(row=3, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()
        x = self.x.get()
        y = self.y.get()

        return (x, y)

    def handle_open(self):
        result = self.open()

        if len(result[0]) == 0 or len(result[0]) == 0:
            return None

        if result is not None:
            try:
                x = float(result[0])
            except:
                showerror("x error", "x is not a float number")
                return None

            try:
                y = float(result[1])
            except:
                showerror("y error", "y is not a float number")
                return None

            return Vector(x, y)

        else:
            return None
