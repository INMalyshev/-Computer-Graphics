DOTS = list()
DOTR = 2

from tkinter import *

def clickOnCanvas(event):
    global DOTS, DOTR, c
    x = event.x
    y = event.y
    new = 1
    for elem in DOTS:
        if elem[1] == x and elem[2] == y:
            new = 0
    if new:
        id = c.create_oval(x-DOTR, y-DOTR, x+DOTR, y+DOTR, fill='red')
        DOTS.append([id, x, y])

def undo(event):
    global DOTS, c
    if len(DOTS) > 0:
        c.delete(DOTS[len(DOTS)-1][0])
        del DOTS[len(DOTS)-1]

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

root.mainloop()
