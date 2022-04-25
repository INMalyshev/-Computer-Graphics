from tkinter import Menu
from tkinter.messagebox import showinfo

from src.settings.settings import Settings

class MyMenu(Menu):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyMenu, self).__init__(parent)

        self.filemenu = Menu(self, tearoff=0)

        self.faqmenu = Menu(self, tearoff=0)

        self.faqmenu.add_command(label="abaut the program", command=self.program)
        self.faqmenu.add_command(label="about the autor", command=self.autor)

        self.add_cascade(label="file", menu=self.filemenu)
        self.add_cascade(label="f&q", menu=self.faqmenu)

    def autor(self):
        showinfo("About the autor", self.settings.ui.menu.autor)

    def program(self):
        showinfo("About the program", self.settings.ui.menu.programinfo)
