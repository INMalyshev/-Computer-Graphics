from src.vector import Vector
from src.calculations.analitic_geometry import equal
import tkinter as tk
from src.ui.my_button import MyButton
from src.ui.my_canvas import MyCanvas

a = Vector(1, 2)
b = Vector(1, 2)

print(equal(a, b))


root = tk.Tk()

canv = MyCanvas(root)
# btn = MyButton(root, "test", lambda: print(canv.winfo_height()))
# canv.bind("<Button-1>", lambda event: print(canv.vector2canvasCoordinates(Vector(0, 0))))
canv.bind("<Button-1>", lambda event: print(canv.draw_cross()))
# btn.pack()
canv.pack(fill="both", expand=True)

root.mainloop()
