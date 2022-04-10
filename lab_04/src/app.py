import tkinter
from tkinter import colorchooser

from src.ui.my_canvas import MyCanvas
from src.ui.my_menu import MyMenu
from src.ui.my_text import MyText
from src.settings.settings import Settings
from src.vector import Vector
from src.cadre import Cadre
from src.ui.my_button import MyButton
from src.ui.del_with_id_form import MyDelWithIdForm
from src.ui.add_circle_form import MyAddCircleForm
from src.ui.add_circle_bunch_form import MyAddCircleBunchForm
from src.ui.add_ellipse_form import MyAddEllipseForm
from src.ui.add_ellipse_bunch_form import MyAddEllipseBunchForm

import copy

from math import acos, degrees
from src.calculations.analitic_geometry import distance

from tkinter.messagebox import showerror

from src.utils.graphs import graph_scatter


class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()

        self.position = Cadre(None, None, list())

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

        # Настройки отката действия

        self.bind("<Control-z>", lambda event: self._backward(None), "+")
        self.bind("<Shift-Control-Z>", lambda event: self._forward(None), "+")

        # Подключение и настройка меню

        self.menu = MyMenu(self)
        self.menu.filemenu.add_command(label="background color", command=self.__handle_choose_bg_color_button)
        self.menu.filemenu.add_command(label="rewind", command=self._rewind)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="exit", command=self.quit)

        self.config(menu=self.menu)

        # Настройки канвы

        self.canvas = MyCanvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Кнопки
        self.add_circle_button = MyButton(self, 'add circle', self.__handle_add_circle_button)
        self.add_circle_button.pack(fill="both")

        self.add_circle_bunch_button = MyButton(self, 'add circle bunch', self.__handle_add_circle_bunch_button)
        self.add_circle_bunch_button.pack(fill="both")

        self.add_ellipse_button = MyButton(self, 'add ellipse', self.__handle_add_ellipse_button)
        self.add_ellipse_button.pack(fill="both")

        self.add_ellipse_bunch_button = MyButton(self, 'add ellipse bunch', self.__handle_add_ellipse_bunch_button)
        self.add_ellipse_bunch_button.pack(fill="both")

        self.del_with_id_button = MyButton(self, 'del with id', self.__handle_del_with_id_button)
        self.del_with_id_button.pack(fill="both")

        self.gget_stat_with_id_button = MyButton(self, 'get stat with id', self.__handle_get_stat_with_id_button)
        self.gget_stat_with_id_button.pack(fill="both")

        # Text

        self.text_list = MyText(self)
        self.text_list.pack(fill="both")

        # Бинды чисто для лабы


    def start(self):
        self.mainloop()

    def _set_position(self):
        self.canvas._set_position(self.position)
        self.text_list.set_text(self.___gen_text())

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

    def _make_record(self):
        self.position = self.position.add(copy.deepcopy(self.position._data))


    def _backward(self, event):
        self.position = self.position.backward()

        self._set_position()

    def _forward(self, event):
        self.position = self.position.forward()

        self._set_position()

    def _rewind(self):
        self._make_record()

        self.position._data = copy.deepcopy(list())

        self._set_position()

    """ lab functions """

    def __handle_choose_bg_color_button(self, event=None):
        color = colorchooser.askcolor()
        self.canvas.configure(bg=color[1])

    def __handle_del_with_id_button(self, event=None):
        new_window = MyDelWithIdForm(self)
        id = new_window.handle_open()

        if id is None:
            return

        if id >= 0 and id < len(self.position._data):
            self._make_record()
            del self.position._data[id]
            self._set_position()

    def __handle_get_stat_with_id_button(self, event=None):
        new_window = MyDelWithIdForm(self)
        id = new_window.handle_open()

        if id is None:
            return

        if id >= 0 and id < len(self.position._data):
            graph_scatter(self.position._data[id]['time_data'])

    def __handle_add_circle_button(self, event=None):
        new_window = MyAddCircleForm(self)
        answer = new_window.handle_open()

        if answer is not None:
            self._make_record()
            self.position._data.append(answer)
            self._set_position()

    def __handle_add_ellipse_button(self, event=None):
        new_window = MyAddEllipseForm(self)
        answer = new_window.handle_open()

        if answer is not None:
            self._make_record()
            self.position._data.append(answer)
            self._set_position()

    def __handle_add_circle_bunch_button(self, event=None):
        new_window = MyAddCircleBunchForm(self)
        answer = new_window.handle_open()

        if answer is not None:
            self._make_record()
            self.position._data.append(answer)
            self._set_position()

    def __handle_add_ellipse_bunch_button(self, event=None):
        new_window = MyAddEllipseBunchForm(self)
        answer = new_window.handle_open()

        if answer is not None:
            self._make_record()
            self.position._data.append(answer)
            self._set_position()


    def ___gen_text(self):
        text = ''
        for i in range(len(self.position._data)):
            if self.position._data[i]['type'] == 'circle':
                text += f"id: {i}, {self.position._data[i]['type']}, center: {self.position._data[i]['center']}, radius: {self.position._data[i]['radius']}\n"

            elif self.position._data[i]['type'] == 'circle_bunch':
                text += f"id: {i}, {self.position._data[i]['type']}, center: {self.position._data[i]['center']}, circles: {int(self.position._data[i]['circle_amount'])}\n"

            elif self.position._data[i]['type'] == 'ellipse':
                text += f"id: {i}, {self.position._data[i]['type']}, center: {self.position._data[i]['center']}, a: {self.position._data[i]['x_radius']}, b: {self.position._data[i]['y_radius']}\n"

            elif self.position._data[i]['type'] == 'ellipse_bunch':
                text += f"id: {i}, {self.position._data[i]['type']}, center: {self.position._data[i]['center']}, a: {self.position._data[i]['min_radius_x']} - {self.position._data[i]['max_radius_x']}, b: {self.position._data[i]['min_radius_y']} - {self.position._data[i]['max_radius_y']}, ellipses: {int(self.position._data[i]['ellipse_amount'])}\n"

        return text
