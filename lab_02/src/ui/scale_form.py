from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror
from src.settings.settings import Settings

from math import fabs

class MyScaleForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.kx = StringVar()
        self.ky = StringVar()

        label = Label(self, text="scale")
        entry_x = Entry(self, textvariable=self.kx)
        entry_y = Entry(self, textvariable=self.ky)
        self.btn_change = Button(self, text="scale")

        label.grid(row=0, columnspan=2)
        Label(self, text="x").grid(row=1, column=0)
        Label(self, text="y").grid(row=2, column=0)
        entry_x.grid(row=1, column=1)
        entry_y.grid(row=2, column=1)
        self.btn_change.grid(row=3, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_scale(self, event, buffer):
        x = self.kx.get()
        y = self.ky.get()

        buffer.append(x)
        buffer.append(y)
        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_change.bind("<ButtonRelease-1>", lambda event: self._handle_scale(event, buffer))
        self.open()

        if len(buffer) != 2:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0:
            showerror("blanc input", "you entered a blanc string")
            return None

        try:
            kx = float(buffer[0])

            if fabs(kx) < self.settings.math.eps:
                showerror("x error", "x should be bigger than 0")
                return None

        except:
            showerror("x error", "x is not a float number")
            return None

        try:
            ky = float(buffer[1])

            if fabs(ky) < self.settings.math.eps:
                showerror("y error", "y should be bigger than 0")
                return None
        except:
            showerror("y error", "y is not a float number")
            return None

        return (kx, ky)