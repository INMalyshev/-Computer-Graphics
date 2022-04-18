from tkinter import Toplevel
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Radiobutton
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import colorchooser
from tkinter.messagebox import showerror
from src.settings.settings import Settings
from src.vector import Vector


class MyAddCircleForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.center_x = StringVar()
        self.center_y = StringVar()

        self.radius = StringVar()

        self.mod = IntVar()
        self.mod.set(0)

        label = Label(self, text="draw circle")

        entry_center_x = Entry(self, textvariable=self.center_x)
        entry_center_y = Entry(self, textvariable=self.center_y)

        entry_radius = Entry(self, textvariable=self.radius)

        default_mod = Radiobutton(self, text="default", variable=self.mod, value=0)
        canonical_mod = Radiobutton(self, text="canonical", variable=self.mod, value=1)
        parametric_mod = Radiobutton(self, text="parametric", variable=self.mod, value=2)
        bresenham_mod = Radiobutton(self, text="bresenham", variable=self.mod, value=3)
        middle_dot_mod = Radiobutton(self, text="middle dot", variable=self.mod, value=4)   #?

        self.btn_draw = Button(self, text="draw")

        label.grid(row=0, columnspan=2)

        Label(self, text="center x").grid(row=1, column=0)
        Label(self, text="center y").grid(row=2, column=0)

        Label(self, text="radius").grid(row=3, column=0)

        entry_center_x.grid(row=1, column=1)
        entry_center_y.grid(row=2, column=1)

        entry_radius.grid(row=3, column=1)

        default_mod.grid(row=5, column=0)
        canonical_mod.grid(row=5, column=1)
        parametric_mod.grid(row=6, column=0)
        bresenham_mod.grid(row=6, column=1)
        middle_dot_mod.grid(row=7, column=0)

        self.btn_draw.grid(row=8, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_draw(self, event, buffer):
        buffer.append(self.center_x.get())
        buffer.append(self.center_y.get())
        buffer.append(self.radius.get())
        buffer.append(self.mod.get())

        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_draw.bind("<ButtonRelease-1>", lambda event: self._handle_draw(event, buffer))
        self.open()

        if len(buffer) != 4:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0 or len(buffer[2]) == 0:
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

        try:
            radius = float(buffer[2])

            if radius <= 0:
                showerror("radius error", "radius cannot be less or equal than zero")
                return None

        except:
            showerror("radius error", "radius is not a float number")
            return None

        color = colorchooser.askcolor()

        if None in color:
            return None

        return {
            "type": "circle",
            "center": Vector(x, y),
            "radius": radius,
            "mod": buffer[3],
            "color": color[1],
        }
