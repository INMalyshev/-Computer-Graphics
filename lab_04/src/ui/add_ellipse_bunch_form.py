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


class MyAddEllipseBunchForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.center_x = StringVar()
        self.center_y = StringVar()

        self.min_radius_x = StringVar()
        self.max_radius_x = StringVar()
        self.min_radius_y = StringVar()
        self.max_radius_y = StringVar()
        self.ellipse_amount = StringVar()

        self.mod = IntVar()
        self.mod.set(0)

        label = Label(self, text="draw ellipse bunch")

        entry_center_x = Entry(self, textvariable=self.center_x)
        entry_center_y = Entry(self, textvariable=self.center_y)

        entry_min_radius_x = Entry(self, textvariable=self.min_radius_x)
        entry_max_radius_x = Entry(self, textvariable=self.max_radius_x)
        entry_min_radius_y = Entry(self, textvariable=self.min_radius_y)
        entry_max_radius_y = Entry(self, textvariable=self.max_radius_y)
        entry_ellipse_amount = Entry(self, textvariable=self.ellipse_amount)

        default_mod = Radiobutton(self, text="default", variable=self.mod, value=0)
        canonical_mod = Radiobutton(self, text="canonical", variable=self.mod, value=1)
        parametric_mod = Radiobutton(self, text="parametric", variable=self.mod, value=2)
        bresenham_mod = Radiobutton(self, text="bresenham", variable=self.mod, value=3)
        middle_dot_mod = Radiobutton(self, text="middle dot", variable=self.mod, value=4)

        self.btn_draw = Button(self, text="draw")

        label.grid(row=0, columnspan=2)

        Label(self, text="center x").grid(row=1, column=0)
        Label(self, text="center y").grid(row=2, column=0)

        Label(self, text="min x radius").grid(row=3, column=0)
        Label(self, text="max x radius").grid(row=4, column=0)
        Label(self, text="min y radius").grid(row=5, column=0)
        Label(self, text="max y radius").grid(row=6, column=0)
        Label(self, text="circle amount").grid(row=7, column=0)

        entry_center_x.grid(row=1, column=1)
        entry_center_y.grid(row=2, column=1)

        entry_min_radius_x.grid(row=3, column=1)
        entry_max_radius_x.grid(row=4, column=1)
        entry_min_radius_y.grid(row=5, column=1)
        entry_max_radius_y.grid(row=6, column=1)
        entry_ellipse_amount.grid(row=7, column=1)

        default_mod.grid(row=8, column=0)
        canonical_mod.grid(row=8, column=1)
        parametric_mod.grid(row=9, column=0)
        bresenham_mod.grid(row=9, column=1)
        middle_dot_mod.grid(row=10, column=0)

        self.btn_draw.grid(row=11, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_draw(self, event, buffer):
        buffer.append(self.center_x.get())
        buffer.append(self.center_y.get())
        buffer.append(self.min_radius_x.get())
        buffer.append(self.max_radius_x.get())
        buffer.append(self.min_radius_y.get())
        buffer.append(self.max_radius_y.get())
        buffer.append(self.ellipse_amount.get())
        buffer.append(self.mod.get())

        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_draw.bind("<ButtonRelease-1>", lambda event: self._handle_draw(event, buffer))
        self.open()

        if len(buffer) != 8:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0 or len(buffer[2]) == 0 or len(buffer[3]) == 0 or len(buffer[4]) == 0 or len(buffer[5]) == 0 or len(buffer[6]) == 0:
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
            min_radius_x = float(buffer[2])

            if min_radius_x <= 0:
                showerror("min x radius error", "radius cannot be less or equal than zero")
                return None

        except:
            showerror("radius error", "radius is not a float number")
            return None

        try:
            max_radius_x = float(buffer[3])

            if max_radius_x <= min_radius_x:
                showerror("max x radius error", "radius cannot be less or equal than min radius")
                return None

        except:
            showerror("radius error", "radius is not a float number")
            return None

        try:
            min_radius_y = float(buffer[4])

            if min_radius_y <= 0:
                showerror("min y radius error", "radius cannot be less or equal than zero")
                return None

        except:
            showerror("radius error", "radius is not a float number")
            return None

        try:
            max_radius_y = float(buffer[5])

            if max_radius_y <= min_radius_y:
                showerror("max y radius error", "radius cannot be less or equal than min radius")
                return None

        except:
            showerror("radius error", "radius is not a float number")
            return None

        try:
            ellipse_amount = int(buffer[6])

            if ellipse_amount < 2:
                showerror("ellipse amount error", "ellipse amount cannot be less than two")
                return None

        except:
            showerror("ellipse amount error", "ellipse amount is not a int number")
            return None

        color = colorchooser.askcolor()

        if None in color:
            return None

        return {
            "type": "ellipse_bunch",
            "center": Vector(x, y),
            "min_radius_x": min_radius_x,
            "max_radius_x": max_radius_x,
            "min_radius_y": min_radius_y,
            "max_radius_y": max_radius_y,
            "ellipse_amount": ellipse_amount,
            "mod": buffer[7],
            "color": color[1],
        }
