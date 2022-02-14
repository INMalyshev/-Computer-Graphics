import tkinter
import DotObject
import tkinter.messagebox

class UserForm(tkinter.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.x = tkinter.StringVar()
        self.y = tkinter.StringVar()

        label = tkinter.Label(self, text="add dot")
        entry_x = tkinter.Entry(self, textvariable=self.x)
        entry_y = tkinter.Entry(self, textvariable=self.y)
        btn = tkinter.Button(self, text="add", command=self.destroy)

        label.grid(row=0, columnspan=2)
        tkinter.Label(self, text="x").grid(row=1, column=0)
        tkinter.Label(self, text="y").grid(row=2, column=0)
        entry_x.grid(row=1, column=1)
        entry_y.grid(row=2, column=1)
        btn.grid(row=3, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()
        x = self.x.get()
        y = self.y.get()

        if not x.isdigit():
            if '-' in x:
                x = x[1:]
                if not x.isdigit():
                    tkinter.messagebox.showerror('error', 'x is not digit')
                    return None
                x = '-' + x
            else:
                tkinter.messagebox.showerror('error', 'x is not digit')
                return None
        x = int(x)

        if not y.isdigit():
            if '-' in y:
                y = y[1:]
                if not y.isdigit():
                    tkinter.messagebox.showerror('error', 'y is not digit')
                    return None
                y = '-' + y
            else:
                tkinter.messagebox.showerror('error', 'y is not digit')
                return None
        y = int(y)

        return DotObject.DotObject(x, y, None)
