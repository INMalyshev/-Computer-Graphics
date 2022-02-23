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
        self.btn = Button(self, text="add")

        label.grid(row=0, columnspan=2)
        Label(self, text="x").grid(row=1, column=0)
        Label(self, text="y").grid(row=2, column=0)
        entry_x.grid(row=1, column=1)
        entry_y.grid(row=2, column=1)
        self.btn.grid(row=3, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_add(self, event, buffer):
        x = self.x.get()
        y = self.y.get()

        print(f"Buffer set ({x}, {y})")
        buffer.append(x)
        buffer.append(y)
        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn.bind("<ButtonRelease-1>", lambda event: self._handle_add(event, buffer))
        self.open()
        print(buffer)
        if len(buffer) != 2:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0:
            return None

        try:
            x = float(buffer[0])
        except:
            showerror("x error", "x is not a float number")
            return None

        try:
            y = float(buffer[1])
        except:
            showerror("y error", "y is not a float number")
            return None

        return Vector(x, y)
