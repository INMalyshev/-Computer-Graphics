import tkinter

from src.ui.my_canvas import MyCanvas
from src.ui.my_menu import MyMenu
from src.settings.settings import Settings
from src.vector import Vector
from src.cadre import Cadre
from src.ui.my_button import MyButton
from src.ui.add_line_form import MtAddLineForm

import copy


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
        self.menu.filemenu.add_command(label="rewind", command=self._rewind)
        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="exit", command=self.quit)

        self.config(menu=self.menu)

        # Настройки канвы

        self.canvas = MyCanvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Кнопки

        self.add_line_button = MyButton(self, "add line", self.__handle_add_line_button)
        self.add_line_button.pack(fill="both")

        # Бинды чисто для лабы



    def start(self):
        self.mainloop()

    def _set_position(self):
        self.canvas._set_position(self.position)
        # print(self.position._data)

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
        print("backward")
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

    def __handle_add_line_button(self, event=None):
        new_window = MtAddLineForm(self)
        answer = new_window.handle_open()

        # print(answer)

        if answer is not None:
            self._make_record()
            self.position._data.append(answer)
            self._set_position()
