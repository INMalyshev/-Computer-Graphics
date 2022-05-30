import tkinter
from tkinter import colorchooser

from src.ui.my_canvas import MyCanvas
from src.ui.my_menu import MyMenu
from src.settings.settings import Settings
from src.vector import Vector
from src.cadre import Cadre

import copy


class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()

        self.position = Cadre(None, None, list())

        super(App, self).__init__()

        # Настройка некоторых горячих клавиш приложения

        self.bind("<Configure>", lambda event: self.set_position())
        self.bind("<Control-w>", lambda event: self.quit(), "+")

        # Настройка области видимости конвы

        self.bind("<d>", lambda event: self._handle_pull(Vector(1, 0)), "+")
        self.bind("<Right>", lambda event: self._handle_pull(Vector(1, 0)), "+")

        self.bind("<a>", lambda event: self._handle_pull(Vector(-1, 0)), "+")
        self.bind("<Left>", lambda event: self._handle_pull(Vector(-1, 0)), "+")

        self.bind("<w>", lambda event: self._handle_pull(Vector(0, 1)), "+")
        self.bind("<Up>", lambda event: self._handle_pull(Vector(0, 1)), "+")

        self.bind("<s>", lambda event: self._handle_pull(Vector(0, -1)), "+")
        self.bind("<Down>", lambda event: self._handle_pull(Vector(0, -1)), "+")

        # self.bind("<MouseWheel>", self._handle_zoom, "+")

        # Настройки отката действия

        self.bind("<Control-z>", lambda event: self._backward(None), "+")
        self.bind("<Shift-Control-Z>", lambda event: self._forward(None), "+")

        # Подключение и настройка меню

        self.menu = MyMenu(self)
        self.menu.filemenu.add_command(label="Изменить цвет фона", command=self._handle_choose_bg_color_button)
        self.menu.filemenu.add_command(label="Сбросить", command=self._rewind)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="Откатить на шаг вперед", command=self._forward)
        self.menu.filemenu.add_command(label="Откатить на шаг назад", command=self._backward)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="Выход", command=self.quit)

        self.config(menu=self.menu)

    def start(self):
        self.mainloop()

    # def _handle_zoom(self, event=None):
    #     if (event.delta > 0):
    #         self.canvas.zoom(self.settings.estange)
    #     elif (event.delta < 0):
    #         self.canvas.zoom(self.settings.approach)
    #     self.set_position()

    def _handle_pull(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented
        d = min(self.canvas.field.finish.x - self.canvas.field.start.x, self.canvas.field.finish.y - self.canvas.field.start.y) / 10
        self.canvas.pull(vector * d)
        self.set_position()

    def _make_record(self):
        # self.position = self.position.add(copy.deepcopy(self.position.data))
        self.position = self.position.add(self.position.data.copy())

    def _backward(self, event=None):
        self.position = self.position.backward()

        self.set_position()

    def _forward(self, event=None):
        self.position = self.position.forward()

        self.set_position()

    def _rewind(self, event=None):
        self._make_record()

        self.position.data = copy.deepcopy(list())

        self.set_position()

    def _handle_choose_bg_color_button(self, event=None):
        color = colorchooser.askcolor()
        if color is not None:
            self.canvas.change_bg_color(color[1])
