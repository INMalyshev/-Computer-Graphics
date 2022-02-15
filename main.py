from tkinter import *
from DotObject import DotObject

DOTS = list()
DOTR = 2

def clickOnCanvas(event):
    # Обработка нажатия на canvas
    global DOTS, DOTR, c
    # Координаты нажатия мыши на canvas
    x = event.x
    y = event.y
    # Создаю объект класса DotObject
    new = DotObject(x, y, None)
    if new not in DOTS:
        # Если эта точка новая то рисую ее и запоминаю
        new.id = c.create_oval(x-DOTR, y-DOTR, x+DOTR, y+DOTR, fill='red')
        DOTS.append(new)

def undo(event):
    global DOTS, c
    if len(DOTS) > 0:
        c.delete(DOTS[-1].id)
        del DOTS[-1]

def clearAll(event=None):
    global DOTS, c
    DOTS.clear()
    c.delete("all")

root = Tk()

winK = 0.78
winW = int(root.winfo_screenwidth() * winK)
winH = int(root.winfo_screenheight() * winK)

root.title('lab_01')
root.geometry('{}x{}'.format(winW, winH))
root.resizable(width=False, height=False)

cRate = 1.0
cK = 0.01
cX = int(winW * cK)
cY = int(winH * cK)
cW = min(int(winW*cRate - 2*cX), int(winH*cRate - 2*cY))
cH = cW
c = Canvas(root, width=cW, height=cH, bg='yellow')
c.place(x=cX, y=cY)
c.bind('<Button-1>', clickOnCanvas)

toolFrameX = 2 * cX + cW
toolFrameY = cY
toolFrameW = winW - 3 * cX - cW
toolFrameH = cH
toolFrame = Frame(root, width=toolFrameW, height=toolFrameH, bg='darkred')
toolFrame.place(x=toolFrameX, y=toolFrameY)

undoButton = Button(toolFrame, text='undo')
undoButton.bind('<Button-1>', undo)
undoButton.grid(row=0, column=0)

refreshButton = Button(toolFrame, text='refresh')
refreshButton.bind('<Button-1>', clearAll)
refreshButton.grid(row=0, column=10)

root.mainloop()
