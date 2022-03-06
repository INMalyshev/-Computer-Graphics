from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror
from src.settings.settings import Settings

from src.vector import Vector

from math import fabs

class MyScaleForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.kx = StringVar()
        self.ky = StringVar()

        self.x = StringVar()
        self.y = StringVar()

        label = Label(self, text="scale")

        entry_kx = Entry(self, textvariable=self.kx)
        entry_ky = Entry(self, textvariable=self.ky)

        entry_x = Entry(self, textvariable=self.x)
        entry_y = Entry(self, textvariable=self.y)

        self.btn_change = Button(self, text="scale")

        label.grid(row=0, columnspan=2)

        Label(self, text="kx").grid(row=1, column=0)
        Label(self, text="ky").grid(row=2, column=0)
        entry_kx.grid(row=1, column=1)
        entry_ky.grid(row=2, column=1)

        Label(self, text="x").grid(row=3, column=0)
        Label(self, text="y").grid(row=4, column=0)
        entry_x.grid(row=3, column=1)
        entry_y.grid(row=4, column=1)

        self.btn_change.grid(row=5, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_scale(self, event, buffer):
        kx = self.kx.get()
        ky = self.ky.get()

        x = self.x.get()
        y = self.x.get()

        buffer.append(kx)
        buffer.append(ky)

        buffer.append(x)
        buffer.append(y)

        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_change.bind("<ButtonRelease-1>", lambda event: self._handle_scale(event, buffer))
        self.open()

        if len(buffer) != 4:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0 or len(buffer[2]) == 0 or len(buffer[3]) == 0:
            showerror("blanc input", "you entered a blanc string")
            return None

        try:
            kx = float(buffer[0])

            if fabs(kx) < self.settings.math.eps:
                showerror("kx error", "kx should be bigger than 0")
                return None

        except:
            showerror("kx error", "kx is not a float number")
            return None

        try:
            ky = float(buffer[1])

            if fabs(ky) < self.settings.math.eps:
                showerror("ky error", "ky should be bigger than 0")
                return None
        except:
            showerror("ky error", "ky is not a float number")
            return None

        try:
            x = float(buffer[2])

        except:
            showerror("x error", "x is not a float number")
            return None

        try:
            y = float(buffer[3])

        except:
            showerror("y error", "y is not a float number")
            return None

        return (kx, ky, Vector(x, y))