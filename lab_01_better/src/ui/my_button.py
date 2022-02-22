from tkinter import Button

from src.settings.settings import Settings

class MyButton(Button):
    def __init__(self, parent, text, command):
        super(MyButton, self).__init__(parent, text=text, command=command)

        self.settings = Settings()

        self.config(
            width=self.settings.ui.button.width,
            height=self.settings.ui.button.height,
            bg=self.settings.ui.button.bg,
            font=self.settings.ui.button.font,
            activebackground=self.settings.ui.button.activebackground
        )
