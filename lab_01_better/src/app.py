import tkinter

from src.position import Position
from src.ui.my_canvas import MyCanvas
from src.ui.my_button import MyButton
from src.ui.my_menu import MyMenu
from src.settings.settings import Settings
from src.vector import Vector

class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()
        self.dots = list()
        self.solution = False
        self.position = Position(None, None, self.dots.copy(), self.solution)

        super(App, self).__init__()

        self.bind("<Configure>", self._set_position)
        self.bind("<Control-z>", self._backward, "+")
        self.bind("<Shift-Control-Z>", self._forward, "+")

        self.config(menu=MyMenu(self))

        self.canvas = MyCanvas(self)
        self.canvas.bind("<MouseWheel>", self._handle_zoom)
        self.canvas.bind("<Button-1>", self._handle_touch, "+")
        self.canvas.pack(fill="both", expand=True)

        self.add_dot_button = MyButton(self, "add dot", None)
        self.add_dot_button.pack()

    def start(self):
        self.mainloop()

    def _add_dot(self, dot):
        if not isinstance(dot, Vector):
            return NotImplemented

        if dot not in self.dots:
            self.dots.append(dot)
            return True

        return False

    def _make_record(self):
        self.position = self.position.add(self.dots.copy(), self.solution)

    def _set_position(self, event):
        self.canvas.set_position(self.position)

    def _handle_zoom(self, event):
        if (event.delta > 0):
            self.canvas.zoom(self.settings.estange)
        elif (event.delta < 0):
            self.canvas.zoom(self.settings.approach)
        self._set_position(self.position)

    def _handle_touch(self, event):
        canvas_coordinates = Vector(event.x, event.y)
        absolute_coordinates = self.canvas.canvasCoordinates2vector(canvas_coordinates)

        if self._add_dot(absolute_coordinates):
            self._make_record()

        self._set_position(event)

        print(f"after touch operation {len(self.position.dots)}")

    def _backward(self, event):
        self.position = self.position.backward()
        self.dots = self.position.dots.copy()
        self.solution = self.solution

        self._set_position(event)

        print(f"after backward operation {len(self.position.dots)}")

    def _forward(self, event):
        self.position = self.position.forward()
        self.dots = self.position.dots.copy()
        self.solution = self.solution

        self._set_position(event)
        print(f"after forward operation {len(self.position.dots)}")
