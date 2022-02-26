import tkinter

from src.ui.my_canvas import MyCanvas
from src.ui.my_menu import MyMenu
from src.settings.settings import Settings
from src.vector import Vector
from src.cadre import Cadre
from src.face import get_face

import src.calculations.rsp as rsp


class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()

        self.position = Cadre(None, None, get_face())

        super(App, self).__init__()

        # Настройка некоторых горячих клавиш приложения

        self.bind("<Configure>", lambda event: self._set_position())
        self.bind("<Control-w>", lambda event: self.quit(), "+")

        # Настройка области видимости конвы

        self.bind("<d>", lambda event: self._handle_pull(Vector(self.settings.move_len, 0)), "+")
        self.bind("<Right>", lambda event: self._handle_pull(Vector(self.settings.move_len, 0)), "+")

        self.bind("<a>", lambda event: self._handle_pull(Vector(-self.settings.move_len, 0)), "+")
        self.bind("<Left>", lambda event: self._handle_pull(Vector(-self.settings.move_len, 0)), "+")

        self.bind("<w>", lambda event: self._handle_pull(Vector(0, self.settings.move_len)), "+")
        self.bind("<Up>", lambda event: self._handle_pull(Vector(0, self.settings.move_len)), "+")

        self.bind("<s>", lambda event: self._handle_pull(Vector(0, -self.settings.move_len)), "+")
        self.bind("<Down>", lambda event: self._handle_pull(Vector(0, -self.settings.move_len)), "+")

        self.bind("<MouseWheel>", self._handle_zoom, "+")

        # Подключение и настройка меню

        self.menu = MyMenu(self)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="exit", command=self.quit)

        self.config(menu=self.menu)

        # Настройки канвы

        self.canvas = MyCanvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Бинды чисто для лабы

        self.bind("<Shift-MouseWheel>", self.__handle_rotate, "+")
        self.bind("<Alt-MouseWheel>", self.__handle_scale, "+")

        self.bind("<Shift-Right>", lambda event: self.__handle_push(Vector(self.settings.move_len, 0)), "+")

        self.bind("<Shift-Left>", lambda event: self.__handle_push(Vector(-self.settings.move_len, 0)), "+")

        self.bind("<Shift-Up>", lambda event: self.__handle_push(Vector(0, self.settings.move_len)), "+")

        self.bind("<Shift-Down>", lambda event: self.__handle_push(Vector(0, -self.settings.move_len)), "+")

    def start(self):
        self.mainloop()

    def _set_position(self):
        self.canvas._set_position(self.position)

    def _handle_zoom(self, event):
        if (event.delta > 0):
            self.canvas.zoom(self.settings.estange)
        elif (event.delta < 0):
            self.canvas.zoom(self.settings.approach)
        self._set_position()

    def _handle_pull(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented
        self.canvas.pull(vector)
        self._set_position()

    """ lab functions """

    def __handle_rotate(self, event):
        phi = self.settings.math.pi
        if event.delta > 0:
            phi *= self.settings.estange - 1
        elif event.delta < 0:
            phi *= self.settings.approach - 1

        for i in range(len(self.position._couples)):
            for j in range(len(self.position._couples[i])):
                self.position._couples[i][j] = rsp.rotate(self.position._couples[i][j], phi, Vector(0, 0))

        self._set_position()

    def __handle_scale(self, event):
        k = 0
        if event.delta > 0:
            k = self.settings.estange
        elif event.delta < 0:
            k = self.settings.approach

        for i in range(len(self.position._couples)):
            for j in range(len(self.position._couples[i])):
                self.position._couples[i][j] = rsp.scale(self.position._couples[i][j], k)

        self._set_position()

    def __handle_push(self, vec):
        for i in range(len(self.position._couples)):
            for j in range(len(self.position._couples[i])):
                self.position._couples[i][j] = rsp.push(self.position._couples[i][j], vec)

        self._set_position()