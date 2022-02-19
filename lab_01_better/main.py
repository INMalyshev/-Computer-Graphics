from src.dot import Dot
from src.calculations.analitic_geometry import equal
import tkinter as tk
from src.ui.my_button import MyButton

a = Dot(1, 2)
b = Dot(1, 2)

print(equal(a, b))


root = tk.Tk()

btn = MyButton(root, "test", lambda: print("test"))
btn.pack()

root.mainloop()
