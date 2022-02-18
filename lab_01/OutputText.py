import tkinter

class OutputText(tkinter.Text):
    def __init__(self, parent):
        super(OutputText, self).__init__(parent)
        self.configure(state=tkinter.DISABLED)
        self.configure(width=15, height=25)

    def settext(self, text):
        self.configure(state=tkinter.NORMAL)
        self.delete(1.0, tkinter.END)
        self.insert(1.0, text)
        self.configure(state=tkinter.DISABLED)
