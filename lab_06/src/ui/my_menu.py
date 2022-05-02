from tkinter import Menu
from tkinter.messagebox import showinfo

from src.settings.settings import Settings

class MyMenu(Menu):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyMenu, self).__init__(parent)

        self.filemenu = Menu(self, tearoff=0)

        self.faqmenu = Menu(self, tearoff=0)

        self.faqmenu.add_command(label="О программе", command=self.program)
        self.faqmenu.add_command(label="Об авторе", command=self.autor)

        self.add_cascade(label="Файл", menu=self.filemenu)
        self.add_cascade(label="Прочее", menu=self.faqmenu)

    def autor(self):
        showinfo("Об авторе", self.settings.ui.menu.autor)

    def program(self):
        showinfo("О Программе", self.settings.ui.menu.programinfo)
