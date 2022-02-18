import tkinter
import tkinter.messagebox
import Settings
import CanvasObject
import DotObject
import Dot
import UserForm
import task
import Record
import AnaliticGeometry
import ChangeDotForm
import OutputText

class Gui(tkinter.Tk):
    def __init__(self):
        self.settings = Settings.Settings()

        self.log = list()
        self.showSolution = False
        self.delmode = False

        self.data = list()

        super(Gui, self).__init__()
        self.configure(bg=self.settings.maincolor)
        self.title(self.settings.title)
        self.geometry(self.settings.geometry)
        self.resizable(width=False, height=False)
        self.config(menu=self.mainmenu())

        self.field = CanvasObject.CanvasObject(self)
        self.field.bind("<Button-1>", self.clickOnCanvas)
        self.field.bind("<Button-3>", self.changeDot, "+")
        self.field.grid(row=0, column=0, columnspan=100)

        self.undoButton = tkinter.Button(self, text='undo')
        self.undoButton.bind("<Button-1>", self.undo)
        self.undoButton.grid(row=10, column=0)
        self.rewindButton = tkinter.Button(self, text='rewind')
        self.rewindButton.bind("<Button-1>", self.rewind)
        self.rewindButton.grid(row=10, column=10)

        self.addDotButton = tkinter.Button(self, text='add dot')
        self.addDotButton.bind("<Button-1>", self.addDot)
        self.addDotButton.grid(row=10, column=20)

        self.findSolutionButton = tkinter.Button(self, text='find solution')
        self.findSolutionButton.bind("<Button-1>", self.findSolution)
        self.findSolutionButton.grid(row=10, column=30)

        self.findSolutionButton = tkinter.Button(self, text='del dot')
        self.findSolutionButton.bind("<Button-1>", self.delmodeOnOff)
        self.findSolutionButton.grid(row=10, column=40)

        self.txt = OutputText.OutputText(self)
        self.txt.grid(row=20, column=0)
        self.txt.settext('hello')

    def delmodeOnOff(self, event=None):
        self.delmode = not self.delmode

    def refreshText(self):
        s = ''
        for dot in self.data:
            s += f"{dot}\n"
        self.txt.settext(s)

    def start(self):
        self.mainloop()

    def mainmenu(self):
        mainmenu = tkinter.Menu(self)

        filemenu = tkinter.Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="add new dot", command=self.addDot)
        filemenu.add_command(label="undo", command=self.undo)
        filemenu.add_command(label="rewinnd", command=self.rewind)
        filemenu.add_command(label="find solution", command=self.findSolution)
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
        self.makeRecord() # Сохранение состояния для отката действий
        # Удалить все, кроме того, что было при запуске
        self.data.clear()
        self.field.rewind()
        self.refreshText()

    def clickOnCanvas(self, event):
        if self.delmode == False:
            # Обработка нажатия на canvas
            x = event.x
            y = event.y
            # Создаю объект класса DotObject
            new = DotObject.DotObject(x, y, None)
            if new not in self.data:
                # Если эта точка новая то рисую ее и запоминаю
                self.makeRecord() # Сохранение состояния для отката действий
                self.showSolution = False
                self.field.delete(self.settings.solutiontag)
                r = self.settings.dotradius
                new.id = self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)
                self.data.append(new)
        else:
            item = self.field.find_closest(event.x, event.y)
            if len(item) == 0:
                return

            id = item[0]

            if self.settings.useritemtag in self.field.gettags(id):
                r = self.settings.dotradius
                x, y = self.field.coords(id)[0] + r, self.field.coords(id)[1] + r
                if AnaliticGeometry.distance(Dot.Dot(x, y), Dot.Dot(event.x, event.y)) <= self.settings.grabradius:
                    old = DotObject.DotObject(x, y, None)
                    self.makeRecord() # Сохранение состояния для отката действий
                    self.data.remove(old)
                    self.field.delete(id)
                    self.showSolution = False
                    self.field.delete(self.settings.solutiontag)
        self.refreshText()

    def undo(self, event=None):
        if self.settings.logOn:
            print(f"in log len {len(self.log)}")
            print(f"in data len {len(self.data)}")
            # print(self.data)
            # print(self.log[-1].data)

        if len(self.log) == 0:
            if self.settings.logOn:
                print("empty log")
            return

        # self.rewind()
        self.data.clear()
        self.field.rewind()

        position = self.log[len(self.log)-1]

        if self.settings.logOn:
            print(f"position len {len(position.data)}")

        # print(position)

        # self.data = position.data.copy()
        self.showSolution = position.flag

        for i in range(len(position.data)):
            x, y, r = position.data[i].x, position.data[i].y, self.settings.dotradius
            self.data.append(DotObject.DotObject(x, y, self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)))
        if self.showSolution:
            solution = task.solution(self.data)
            x1, y1, r1 = solution[0].x, solution[0].y, solution[1]
            self.field.create_oval(x1-r1, y1-r1, x1+r1, y1+r1, width=2, outline="yellow", tag=self.settings.solutiontag)
            x2, y2, r2 = solution[2].x, solution[2].y, solution[3]
            self.field.create_oval(x2-r2, y2-r2, x2+r2, y2+r2, width=2, outline="green", tag=self.settings.solutiontag)

        del self.log[len(self.log)-1]

        if self.settings.logOn:
            print(f"out log len {len(self.log)}")
            print(f"out data len {len(self.data)}")

        self.refreshText()

    def addDot(self, event=None):
        self.field.delete("all")
        for i in range(len(self.data)):
            x, y, r = self.data[i].x, self.data[i].y, self.settings.dotradius
            self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)

        userForm = UserForm.UserForm(self)
        newDot = userForm.open()
        if newDot is not None:
            if newDot not in self.data:
                self.makeRecord() # Сохранение состояния для отката действий
                self.showSolution = False
                self.field.delete(self.settings.solutiontag)
                r = self.settings.dotradius
                x = newDot.x
                y = newDot.y
                newDot.id = self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)
                self.data.append(newDot)
            else:
                tkinter.messagebox.showwarning("already exists", "try to add sth else")
        self.refreshText()

    def findSolution(self, event=None):
        solution = task.solution(self.data)
        if solution is None:
            tkinter.messagebox.showwarning("no solution found", "try to add more dots or change any")
            return
        self.makeRecord() # Сохранение состояния для отката действий
        self.showSolution = True
        x1, y1, r1 = solution[0].x, solution[0].y, solution[1]
        self.field.create_oval(x1-r1, y1-r1, x1+r1, y1+r1, width=2, outline="yellow", tag=self.settings.solutiontag)
        x2, y2, r2 = solution[2].x, solution[2].y, solution[3]
        self.field.create_oval(x2-r2, y2-r2, x2+r2, y2+r2, width=2, outline="green", tag=self.settings.solutiontag)

        tkinter.messagebox.showinfo("solution", f"circle1 - {Dot.Dot(x1, y1)}, r1 - {r1:.1}\n\
        circle1 - {Dot.Dot(x2, y2)}, r2 - {r2:.1}")

        self.refreshText()

    def makeRecord(self):
        if self.settings.logOn:
            print(f"   in adding record log len {len(self.log)}")

        if self.settings.loglen is None:
            self.log.append(Record.Record(self.data, self.showSolution))
            if self.settings.logOn:
                print(f"   out adding record log len {len(self.log)}")
            return

        if len(self.log) < self.settings.loglen:
            self.log.append(Record.Record(self.data, self.showSolution))

            if self.settings.logOn:
                print(f"   out adding record log len {len(self.log)}")

            return

        self.log = self.log[1:]
        self.log.append(Record.Record(self.data, self.showSolution))

        if self.settings.logOn:
            print(f"   out adding record log len {len(self.log)}")

    def changeDot(self, event):
        item = self.field.find_closest(event.x, event.y)
        if len(item) == 0:
            return

        id = item[0]

        if self.settings.useritemtag in self.field.gettags(id):
            r = self.settings.dotradius
            x, y = self.field.coords(id)[0] + r, self.field.coords(id)[1] + r
            if AnaliticGeometry.distance(Dot.Dot(x, y), Dot.Dot(event.x, event.y)) <= self.settings.grabradius:
                old = DotObject.DotObject(x, y, None)
                form = ChangeDotForm.ChangeDotForm(self)
                newDot = form.open()
                if newDot is not None:
                    if newDot not in self.data:
                        self.makeRecord() # Сохранение состояния для отката действий
                        self.showSolution = False
                        self.field.delete(self.settings.solutiontag)
                        r = self.settings.dotradius
                        x = newDot.x
                        y = newDot.y
                        newDot.id = self.field.create_oval(x-r, y-r, x+r, y+r, fill=self.settings.dotcolor, tag=self.settings.useritemtag)
                        self.data.append(newDot)
                        self.data.remove(old)
                        self.field.delete(id)
                    else:
                        tkinter.messagebox.showwarning("already exists", "try to add sth else")
        self.refreshText()
