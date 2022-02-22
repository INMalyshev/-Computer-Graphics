from tkinter import Frame

from src.settings.settings import Settings
from src.ui.my_button import MyButton

class MyFrame(Frame):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyFrame, self).__init__(parent)

        self.config(
        bg=self.settings.ui.frame.bg
        )

        self.add_button = MyButton(self, "add dot", None)
        self.add_button.grid(row=0, column=0)

        self.solution_button = MyButton(self, "find solution", None)
        self.solution_button.grid(row=0, column=1)

        self.rewind_button = MyButton(self, "rewind", None)
        self.rewind_button.grid(row=0, column=2)
