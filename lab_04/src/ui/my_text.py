from tkinter import Text, Scrollbar, RIGHT, Y, END

from src.settings.settings import Settings

class MyText(Text):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyText, self).__init__(parent)
        # self.configure(font=self.settings.ui.text.font)
        self.configure(height=self.settings.ui.text.height)
        self.configure(width=self.settings.ui.text.width)
        self.configure(bg=self.settings.ui.text.bg)
        self.configure(state="disabled")

        self.scroll = Scrollbar(command=self.yview)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.config(yscrollcommand=self.scroll.set)

    def set_text(self, text):
        self.configure(state="normal")
        self.delete(1.0, END)
        self.insert(1.0, text)
        self.configure(state="disabled")
