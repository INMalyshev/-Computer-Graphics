# from src.vector import Vector
# from src.position import Position
#
# from src.calculations.analitic_geometry import equal
# import tkinter as tk
# from src.ui.my_button import MyButton
# from src.ui.my_canvas import MyCanvas
#
# # a = Vector(1, 2)
# # b = Vector(1, 2)
# #
# # print(equal(a, b))
#
# def zoom(event):
#     print("zoom")
#     if (event.delta > 0):
#         canv.zoom(1.1)
#     elif (event.delta < 0):
#         canv.zoom(0.9)
#     canv.set_position(position)
#
# position = Position(None, None, [Vector(30, 30), Vector(90, 90), Vector(150, 150)], False)
#
# root = tk.Tk()
# root.bind("<Configure>", lambda event: canv.set_position(position))
#
# canv = MyCanvas(root)
# canv.bind("<MouseWheel>", zoom)
# # btn = MyButton(root, "test", lambda: print(canv.winfo_height()))
# # canv.bind("<Button-1>", lambda event: print(canv.vector2canvasCoordinates(Vector(0, 0))))
# # btn.pack()
# canv.pack(fill="both", expand=True)
#
# # a = Vector(0.5, 0)
# # b = canv.vector2canvasCoordinates(a)
# # c = canv.canvasCoordinates2vector(b)
# # print(a)
# # print(b)
# # print(c)
#
# root.mainloop()

from src.app import App

app = App()
app.start()
