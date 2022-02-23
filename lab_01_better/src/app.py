import tkinter
from tkinter.messagebox import showwarning

from src.position import Position
from src.ui.my_canvas import MyCanvas
from src.ui.my_button import MyButton
from src.ui.my_menu import MyMenu
from src.ui.my_frame import MyFrame
from src.ui.add_dot_form import AddDotForm
from src.ui.my_change_form import MyChangeForm
from src.settings.settings import Settings
from src.vector import Vector
from src.calculations.task import solution
from src.calculations.analitic_geometry import distance

class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()
        self.dots = [
        Vector(100, 100),
        Vector(100, 300),
        Vector(300, 100),
        Vector(300, 300),
        Vector(200, 200),
        Vector(200, 400),
        Vector(400, 200),
        Vector(400, 400),
        ]
        self.solution = False
        self.circles = list()
        self.position = Position(None, None, self.dots.copy(), self.solution, self.circles.copy())

        super(App, self).__init__()

        self.bind("<Configure>", self._set_position)
        self.bind("<Control-z>", self._backward, "+")
        self.bind("<Shift-Control-Z>", self._forward, "+")
        self.bind("<Control-w>", lambda event: self.quit(), "+")

        self.bind("<d>", lambda event: self._handle_pull(Vector(self.settings.move_len, 0)), "+")
        self.bind("<Right>", lambda event: self._handle_pull(Vector(self.settings.move_len, 0)), "+")

        self.bind("<a>", lambda event: self._handle_pull(Vector(-self.settings.move_len, 0)), "+")
        self.bind("<Left>", lambda event: self._handle_pull(Vector(-self.settings.move_len, 0)), "+")

        self.bind("<w>", lambda event: self._handle_pull(Vector(0, self.settings.move_len)), "+")
        self.bind("<Up>", lambda event: self._handle_pull(Vector(0, self.settings.move_len)), "+")

        self.bind("<s>", lambda event: self._handle_pull(Vector(0, -self.settings.move_len)), "+")
        self.bind("<Down>", lambda event: self._handle_pull(Vector(0, -self.settings.move_len)), "+")

        self.menu = MyMenu(self)
        self.menu.filemenu.add_command(label="add", command=None)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="exit", command=self.quit)

        self.config(menu=self.menu)

        self.canvas = MyCanvas(self)
        self.canvas.bind("<MouseWheel>", self._handle_zoom)
        self.canvas.bind("<Button-1>", self._handle_touch, "+")
        self.canvas.bind("<Button-3>", self._handle_right_touch, "+")
        self.canvas.pack(fill="both", expand=True)

        self.tool_frame = MyFrame(self)
        self.tool_frame.pack()
        self.tool_frame.add_button.bind("<ButtonRelease-1>", self._handle_add_dot_button)
        self.tool_frame.solution_button.bind("<ButtonRelease-1>", self._solution)
        self.tool_frame.rewind_button.bind("<ButtonRelease-1>", self._rewind)

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
        self.position = self.position.add(self.dots.copy(), self.solution, self.circles.copy())

    def _set_position(self, event): #TODO
        self.canvas.set_position(self.position)

        s = ""
        for vector in self.position.dots:
            s += f"{vector}\n"
        self.tool_frame.text.settext(s)

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
            self.solution = False
            self._make_record()

        self._set_position(event)

        print(f"after touch operation {len(self.position.dots)}")

    def _handle_right_touch(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if len(item) == 0:
            return

        id = item[0]

        if self.settings.ui.dot.tag in self.canvas.gettags(id):
            r = self.settings.ui.dot.radius
            x, y = self.canvas.coords(id)[0] + r, self.canvas.coords(id)[1] + r

            if distance(Vector(x, y), Vector(event.x, event.y)) <= self.settings.grabradius:
                converted_old = self.canvas.canvasCoordinates2vector(Vector(x, y))

                #todo!!!
                if converted_old in self.dots:
                    window = MyChangeForm(self)
                    answer = window.handle_open()

                    if answer is not None:
                        self._delete_dot(event, converted_old)
                        if isinstance(answer, Vector):
                            self._add_dot(answer)
                        self._make_record()
                        self._set_position(event)

                # self.data.remove(old)
                # self.field.delete(id)
                # self.showSolution = False
                # self.field.delete(self.settings.solutiontag)

    def _backward(self, event):
        self.position = self.position.backward()
        self.dots = self.position.dots.copy()
        self.solution = self.solution

        self._set_position(event)

        print(f"after backward operation solution is {self.position.solution}")
        print(f"after backward operation {len(self.position.dots)}")

    def _forward(self, event):
        self.position = self.position.forward()
        self.dots = self.position.dots.copy()
        self.solution = self.solution

        self._set_position(event)

        print(f"after forward operation solution is {self.position.solution}")
        print(f"after forward operation {len(self.position.dots)}")

    def _delete_dot(self, event, dot):
        if not isinstance(dot, Vector):
            return NotImplemented

        if dot in self.dots:
            self.dots.remove(dot)
            self.solution = False

    def _handle_add_dot_button(self, event):
        window = AddDotForm(self)
        result = window.handle_open()
        if result is not None:
            if self._add_dot(result):
                self.solution = False
                self._make_record()

            self._set_position(event)

    def _handle_pull(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented
        self.canvas.pull(vector)
        self._set_position(None)

    def _solution(self, event):
        answer = solution(self.position.dots)
        if answer is not None:
            self.solution = True
            self.circles = list(answer)
        else:
            self.solution = False
        self._make_record()
        self._set_position(event)

    def _rewind(self, event):
        self.dots = list()
        self.solution = False
        self.circles = list()
        self._make_record()
        self._set_position(event)
