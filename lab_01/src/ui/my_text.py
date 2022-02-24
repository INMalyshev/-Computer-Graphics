import tkinter

class MyText(tkinter.Text):
    def __init__(self, parent):
        super(MyText, self).__init__(parent)
        self.configure(state=tkinter.DISABLED)
        self.configure(width=20, height=5)

    def settext(self, text):
        self.configure(state=tkinter.NORMAL)
        self.delete(1.0, tkinter.END)
        self.insert(1.0, text)
        self.configure(state=tkinter.DISABLED)
