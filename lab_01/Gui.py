import tkinter
import tkinter.messagebox
import Settings
import CanvasObject
import DotObject
import UserForm

class Gui(tkinter.Tk):
    def __init__(self):
        self.settings = Settings.Settings()
        self.data = list()

        super(Gui, self).__init__()
        self.configure(bg=self.settings.maincolor)
        self.title(self.settings.title)
        self.geometry(self.settings.geometry)
        self.resizable(width=False, height=False)
        self.config(menu=self.mainmenu())

        self.field = CanvasObject.CanvasObject(self)
        self.field.bind("<Button-1>", self.clickOnCanvas)
        self.field.grid(row=0, column=0, columnspan=100)

        self.undoButton = tkinter.Button(self, text='undo')
        self.undoButton.bind("<Button-1>", self.undo)
        self.undoButton.grid(row=10, column=0)

        self.rewindButton = tkinter.Button(self, text='rewind')
        self.rewindButton.bind("<Button-1>", self.rewind)
        self.rewindButton.grid(row=20, column=0)

        self.addDotButton = tkinter.Button(self, text='add dot')
        self.addDotButton.bind("<Button-1>", self.addDot)
        self.addDotButton.grid(row=30, column=0)

    def start(self):
        self.mainloop()

    def mainmenu(self):
        mainmenu = tkinter.Menu(self)

        filemenu = tkinter.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="add new dot")
        filemenu.add_command(label="undo", command=self.undo)
        filemenu.add_command(label="rewinnd", command=self.rewind)
        filemenu.add_command(label="find solution")
        filemenu.add_separator()
        filemenu.add_command(label="exit", command=quit)

        faqmenu = tkinter.Menu(mainmenu, tearoff=0)
        faqmenu.add_command(label="abaut thr program", command=self.program)
        faqmenu.add_command(label="about the autor", command=self.autor)

        mainmenu.add_cascade(label="file", menu=filemenu)
        mainmenu.add_cascade(label="f&q", menu=faqmenu)

        return mainmenu

    def quit(self):
        self.quit

    def autor(self):
        tkinter.messagebox.showinfo("About the autor", self.settings.autor)

    def program(self):
        tkinter.messagebox.showinfo("About the program", self.settings.programinfo)

    def rewind(self, event=None):
        # Удалить все, кроме того, что было при запуске
        self.data.clear()
        self.field.rewind()

    def clickOnCanvas(self, event):
        # Обработка нажатия на canvas
        x = event.x
        y = event.y
        # Создаю объект класса DotObject
        new = DotObject.DotObject(x, y, None)
        if new not in self.data:
            # Если эта точка новая то рисую ее и запоминаю
            r = self.settings.dotradius
            new.id = self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)
            self.data.append(new)

    def undo(self, event=None):
        if len(self.data) > 0:
            self.field.delete(self.data[-1].id)
            del self.data[-1]

    def addDot(self, event):
        userForm = UserForm.UserForm(self)
        newDot = userForm.open()
        if newDot is not None:
            if newDot not in self.data:
                r = self.settings.dotradius
                x = newDot.x
                y = newDot.y
                newDot.id = self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)
                self.data.append(newDot)

app = Gui()
app.start()
