from tkinter import Toplevel
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Radiobutton
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror
from src.settings.settings import Settings
from src.vector import Vector

class MtAddLineForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.start_x = StringVar()
        self.start_y = StringVar()

        self.finish_x = StringVar()
        self.finish_y = StringVar()

        self.mod = IntVar()
        self.mod.set(0)

        label = Label(self, text="Draw line")

        entry_start_x = Entry(self, textvariable=self.start_x)
        entry_start_y = Entry(self, textvariable=self.start_y)

        entry_finish_x = Entry(self, textvariable=self.finish_x)
        entry_finish_y = Entry(self, textvariable=self.finish_y)

        default_mod = Radiobutton(self, text="default", variable=self.mod, value=0)
        dda_mod = Radiobutton(self, text="dda", variable=self.mod, value=1)
        br_mod = Radiobutton(self, text="bresenham", variable=self.mod, value=2)
        br_int_mod = Radiobutton(self, text="int bresenham", variable=self.mod, value=3)
        br_ang_mod = Radiobutton(self, text="no angle bresenham", variable=self.mod, value=4)
        wu_mod = Radiobutton(self, text="wu", variable=self.mod, value=5)

        self.btn_draw = Button(self, text="draw")

        label.grid(row=0, columnspan=2)

        Label(self, text="start x").grid(row=1, column=0)
        Label(self, text="start y").grid(row=2, column=0)

        Label(self, text="finish x").grid(row=3, column=0)
        Label(self, text="finish y").grid(row=4, column=0)

        entry_start_x.grid(row=1, column=1)
        entry_start_y.grid(row=2, column=1)

        entry_finish_x.grid(row=3, column=1)
        entry_finish_y.grid(row=4, column=1)

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
        buffer.append(self.start_x.get())
        buffer.append(self.start_y.get())
        buffer.append(self.finish_x.get())
        buffer.append(self.finish_y.get())
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
            start_x = float(buffer[0])

        except:
            showerror("start x error", "start x is not a float number")
            return None

        try:
            start_y = float(buffer[1])

        except:
            showerror("start y error", "start y is not a float number")
            return None

        try:
            finish_x = float(buffer[2])

        except:
            showerror("finish x error", "finish x is not a float number")
            return None

        try:
            finish_y = float(buffer[3])

        except:
            showerror("finish y error", "finish y is not a float number")
            return None

        return {
            "type": "line",
            "start": Vector(start_x, start_y),
            "finish": Vector(finish_x, finish_y),
            "mod": buffer[4],
            "color": "red",
        }