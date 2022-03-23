from tkinter import Toplevel
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter.messagebox import showerror
from src.settings.settings import Settings

class MyDelWithIdForm(Toplevel):
    def __init__(self, parent):
        self.settings = Settings()

        super().__init__(parent)
        self.id = StringVar()

        label = Label(self, text="input id")

        entry_id = Entry(self, textvariable=self.id)

        self.btn_del = Button(self, text="ok")

        label.grid(row=0, columnspan=2)

        Label(self, text="id").grid(row=1, column=0)

        entry_id.grid(row=1, column=1)

        self.btn_del.grid(row=2, column=0, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()

    def _handle_draw(self, event, buffer):
        buffer.append(self.id.get())

        self.destroy()

    def handle_open(self):
        buffer = list()
        self.btn_del.bind("<ButtonRelease-1>", lambda event: self._handle_draw(event, buffer))
        self.open()

        if len(buffer) != 1:
            return None

        if len(buffer[0]) == 0:
            showerror("blanc input", "you entered a blanc string")
            return None

        try:
            id = int(buffer[0])

        except:
            showerror("id error", "id is not an int number")
            return None

        return id
