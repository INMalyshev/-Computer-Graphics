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

class MyAddBunchForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.center_x = StringVar()
        self.center_y = StringVar()

        self.line_len = StringVar()
        self.angle_step = StringVar()

        self.mod = IntVar()
        self.mod.set(0)

        label = Label(self, text="draw bunch")

        entry_center_x = Entry(self, textvariable=self.center_x)
        entry_center_y = Entry(self, textvariable=self.center_y)

        entry_line_len = Entry(self, textvariable=self.line_len)
        entry_angle_step = Entry(self, textvariable=self.angle_step)

        default_mod = Radiobutton(self, text="default", variable=self.mod, value=0)
        dda_mod = Radiobutton(self, text="dda", variable=self.mod, value=1)
        br_mod = Radiobutton(self, text="bresenham", variable=self.mod, value=2)
        br_int_mod = Radiobutton(self, text="int bresenham", variable=self.mod, value=3)
        br_ang_mod = Radiobutton(self, text="no angle bresenham", variable=self.mod, value=4)
        wu_mod = Radiobutton(self, text="wu", variable=self.mod, value=5)

        self.btn_draw = Button(self, text="draw")

        label.grid(row=0, columnspan=2)

        Label(self, text="center x").grid(row=1, column=0)
        Label(self, text="center y").grid(row=2, column=0)

        Label(self, text="line len").grid(row=3, column=0)
        Label(self, text="angle_step").grid(row=4, column=0)

        entry_center_x.grid(row=1, column=1)
        entry_center_y.grid(row=2, column=1)

        entry_line_len.grid(row=3, column=1)
        entry_angle_step.grid(row=4, column=1)

        default_mod.grid(row=5, column=0)
        dda_mod.grid(row=5, column=1)
        br_mod.grid(row=6, column=0)
        br_int_mod.grid(row=6, column=1)
        br_ang_mod.grid(row=7, column=0)
        wu_mod.grid(row=7, column=1)

        self.btn_draw.grid(row=8, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_draw(self, event, buffer):
        buffer.append(self.center_x.get())
        buffer.append(self.center_y.get())
        buffer.append(self.line_len.get())
        buffer.append(self.angle_step.get())
        buffer.append(self.mod.get())

        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_draw.bind("<ButtonRelease-1>", lambda event: self._handle_draw(event, buffer))
        self.open()

        if len(buffer) != 5:
            return None

        if len(buffer[0]) == 0 or len(buffer[1]) == 0 or len(buffer[2]) == 0 or len(buffer[3]) == 0:
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
            line_len = float(buffer[2])

            if line_len == 0:
                showerror("line len error", "line len cannot be equal to zero")
                return None


        except:
            showerror("line len error", "line len is not a float number")
            return None

        try:
            angle_step = int(buffer[3])

            if angle_step == 0:
                showerror("angle step error", "angle step cannot be equal to zero")
                return None

        except:
            showerror("angle step error", "angle step is not a float number")
            return None

        color = colorchooser.askcolor()


        if None in color:
            return None

        return {
            "type": "bunch",
            "center": Vector(x, y),
            "line_len": line_len,
            "angle_step": angle_step,
            "mod": buffer[4],
            "color": color[1],
        }
