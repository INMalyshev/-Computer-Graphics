from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror

from src.vector import Vector

class MyChangeForm(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.x = StringVar()
        self.y = StringVar()

        label = Label(self, text="change dot")
        entry_x = Entry(self, textvariable=self.x)
        entry_y = Entry(self, textvariable=self.y)
        self.btn_change = Button(self, text="change")
        self.btn_delete = Button(self, text="delete")

        label.grid(row=0, columnspan=2)
        Label(self, text="x").grid(row=1, column=0)
        Label(self, text="y").grid(row=2, column=0)
        entry_x.grid(row=1, column=1)
        entry_y.grid(row=2, column=1)
        self.btn_change.grid(row=3, column=0)
        self.btn_delete.grid(row=3, column=1)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_change(self, event, buffer):
        x = self.x.get()
        y = self.y.get()

        buffer.append(x)
        buffer.append(y)
        self.destroy()

    def _handle_delete(self, event, buffer):
        buffer.append("del")
        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_change.bind("<ButtonRelease-1>", lambda event: self._handle_change(event, buffer))
        self.btn_delete.bind("<ButtonRelease-1>", lambda event: self._handle_delete(event, buffer))
        self.open()

        if len(buffer) == 1 and buffer[0] == 'del':
            return 'del'

        if len(buffer) != 2:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0:
            showerror("blanc input", "you entered a blanc string")
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
