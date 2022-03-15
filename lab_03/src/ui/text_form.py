from tkinter import Toplevel
from src.settings.settings import Settings

from src.ui.my_text import MyText

class MyTextForm(Toplevel):
    def __init__(self, parent, text='hello, world'):
        self.settings = Settings()

        super().__init__(parent)

        self.text = MyText(self)
        self.text.configure(width=50, height=25)
        self.text.pack(fill="both", expand=True)
        self.text.set_text(text)


    def open(self):
        self.grab_set()
        self.wait_window()
