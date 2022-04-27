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

import copy

from math import acos, degrees
from src.calculations.analitic_geometry import distance

from tkinter.messagebox import showerror

from src.utils.graphs import graph_scatter

from tkinter import IntVar
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Radiobutton


class App(tkinter.Tk):
    def __init__(self):
        self.settings = Settings()

        self.position = Cadre(None, None, list())

        super(App, self).__init__()

        # Настройка некоторых горячих клавиш приложения

        self.bind("<Configure>", lambda event: self._set_position())
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
        # self.canvas.pack(fill="both", expand=True)
        self.canvas.place(relx=0, rely=0, relheight=1.0, relwidth=0.8)

        # Кнопки
        self.process_button = MyButton(self, 'make with hands', self.___start_make_figure_process)
        self.process_button.place(relx=0.8, rely=0, relheight=0.05, relwidth=0.2)

        self.slowly_button = MyButton(self, 'draw scene slowly', lambda: self._set_position(animated=True))
        self.slowly_button.place(relx=0.8, rely=0.05, relheight=0.05, relwidth=0.2)

        self.fill_mod = IntVar()
        self.fill_mod.set(0)
        self.filling_mod = Radiobutton(self, text="fill", variable=self.fill_mod, value=0)
        self.erasing_mod = Radiobutton(self, text="erase", variable=self.fill_mod, value=1)
        self.filling_mod.place(relx=0.8, rely=0.1, relheight=0.05, relwidth=0.1)
        self.erasing_mod.place(relx=0.9, rely=0.1, relheight=0.05, relwidth=0.1)

        self.del_with_id_button = MyButton(self, 'del with id', self.__handle_del_with_id_button)
        self.del_with_id_button.place(relx=0.8, rely=0.15, relheight=0.05, relwidth=0.2)

        self.change_color_button = MyButton(self, 'change fill color', self.__handle_choose_fill_color_button)
        self.change_color_button.place(relx=0.8, rely=0.2, relheight=0.05, relwidth=0.2)

        self.new_figure_button = MyButton(self, 'new figure', self.___handle_new_figure_button)
        self.new_figure_button.place(relx=0.8, rely=0.45, relheight=0.05, relwidth=0.2)

        self.finish_figure_button = MyButton(self, 'finish figure', self.___handle_finish_figure_button)
        self.finish_figure_button.place(relx=0.8, rely=0.5, relheight=0.05, relwidth=0.2)

        self.text_x = StringVar()
        self.text_y = StringVar()

        Label(self, text='x:').place(relx=0.8, rely=0.55, relheight=0.05, relwidth=0.05)
        self.x_entry = Entry(self, textvariable=self.text_x)
        self.x_entry.place(relx=0.85, rely=0.55, relheight=0.05, relwidth=0.15)

        Label(self, text='y:').place(relx=0.8, rely=0.6, relheight=0.05, relwidth=0.05)
        self.y_entry = Entry(self, textvariable=self.text_y)
        self.y_entry.place(relx=0.85, rely=0.6, relheight=0.05, relwidth=0.15)

        self.add_dot_button = MyButton(self, 'add dot', self.___handle_add_dot_button)
        self.add_dot_button.place(relx=0.8, rely=0.65, relheight=0.05, relwidth=0.2)

        # Text

        self.text_list = MyText(self)
        self.text_list.place(relx=0.8, rely=0.25, relheight=0.2, relwidth=0.2)


        # Бинды чисто для лабы

        self.hand_mod = False

    def start(self):
        self.mainloop()

    def _set_position(self, animated=False):
        self.canvas._set_position(self.position, animated)
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
        d = min(self.canvas.field.finish.x - self.canvas.field.start.x, self.canvas.field.finish.y - self.canvas.field.start.y) / 10
        self.canvas.pull(vector * d)
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
        if color is not None:
            self.canvas.change_bg_color(color[1])

    def __handle_choose_fill_color_button(self, event=None):
        color = colorchooser.askcolor()
        if color is not None:
            self.canvas.change_fill_color(color[1])

    def __handle_del_with_id_button(self, event=None):
        new_window = MyDelWithIdForm(self)
        id = new_window.handle_open()

        if id is None:
            return

        if id >= 0 and id < len(self.position._data):
            self._make_record()
            del self.position._data[id]
            self._set_position()

    def ___gen_text(self):
        text = ''

        for ind, figure in enumerate(self.position._data):
            state = 'finished' if figure['finished'] else 'not finished'
            text += f'id: {ind}, state: {state}\n'

            for dot in figure['dots']:
                text += f'  {dot}\n'

        text += '\n'

        return text

    def ___handle_new_figure_button(self, event=None):
        if self.hand_mod:
            return

        if self.position._data:
            if not self.position._data[-1]['finished']:
                del self.position._data[-1]

        new_figure = {
            'dots': [],
            'finished': False,
            'erase': self.fill_mod.get() == 1,
            'color': self.canvas.fill_color,
        }

        self._make_record()
        self.position._data.append(new_figure)
        self._set_position()

    def ___handle_finish_figure_button(self, event=None):
        if self.hand_mod:
            return

        if self.position._data:
            if self.position._data[-1]['finished']:
                return

            if len(self.position._data[-1]['dots']) < 3:
                del self.position._data[-1]

                self._set_position()
                return

            self.position._data[-1]['finished'] = True
            self._set_position()

    def ___handle_add_dot_button(self, event=None):
        if self.hand_mod:
            return

        str_x = self.text_x.get()
        str_y = self.text_y.get()
        self.text_x.set('')
        self.text_y.set('')

        if self.position._data:
            if self.position._data[-1]['finished']:
                return

        x, y = None, None

        try:
            x = float(str_x)
        except Exception:
            if len(str_x) > 0:
                showerror('x error', 'x not a float number')

            return

        try:
            y = float(str_y)
        except Exception:
            if len(str_y) > 0:
                showerror('y error', 'y not a float number')

            return

        dot = Vector(x, y)

        if self.position._data:
            self.position._data[-1]['dots'].append(dot)

            self._set_position()

    def ___start_make_figure_process(self, event=None):
        if self.position._data:
            if not self.position._data[-1]['finished']:
                del self.position._data[-1]

        self.hand_mod = True

        binds = []
        line_width = 2

        def add_dot(self, event=None):
            on_canvas = Vector(event.x, event.y)
            on_real = self.canvas.canvasCoordinates2vector(on_canvas)
            self.position._data[-1]['dots'].append(on_real)
            # print(self.position._data)
            self._set_position()

        def add_perpendicular_dot(self,  event=None):
            on_canvas = Vector(event.x, event.y)
            on_real = self.canvas.canvasCoordinates2vector(on_canvas)

            if len(self.position._data[-1]['dots']) > 0:
                last_dot = self.position._data[-1]['dots'][-1]
                delta = on_real - last_dot
                if abs(delta.x) >= abs(delta.y):
                    on_real = last_dot + Vector(delta.x, 0)
                else:
                    on_real = last_dot + Vector(0, delta.y)

            self.position._data[-1]['dots'].append(on_real)
            # print(self.position._data)
            self._set_position()

        def create_prompt_line(self, event):
            if len(self.position._data[-1]['dots']) > 0:
                self._set_position()
                # self.canvas.delete('to_del')

                on_canvas = Vector(event.x, event.y)
                on_real = self.canvas.canvasCoordinates2vector(on_canvas)
                last_dot = self.position._data[-1]['dots'][-1]
                self.canvas.draw_line(last_dot, on_real, fill='red', width=line_width)
                # self.canvas.draw_line(last_dot, on_real, fill='red', width=line_width, tag='to_del')


        def create_perpendicular_prompt_line(self, event):
            if len(self.position._data[-1]['dots']) > 0:
                self._set_position()

                on_canvas = Vector(event.x, event.y)
                on_real = self.canvas.canvasCoordinates2vector(on_canvas)
                last_dot = self.position._data[-1]['dots'][-1]

                delta = on_real - last_dot
                if abs(delta.x) >= abs(delta.y):
                    on_real = last_dot + Vector(delta.x, 0)
                else:
                    on_real = last_dot + Vector(0, delta.y)

                self.canvas.draw_line(last_dot, on_real, fill='red', width=line_width)

        def finish_make_figure_process(self, event=None):
            if len(self.position._data[-1]['dots']) < 3:
                del self.position._data[-1]
            else:
                self.position._data[-1]['finished'] = True

            self.unbind("<Return>", binds[0])
            self.canvas.unbind("<Button-1>", binds[1])
            self.canvas.unbind("<Motion>", binds[2])
            self.canvas.unbind("<Shift-Button-1>", binds[3])
            self.canvas.unbind("<Shift-Motion>", binds[4])

            self.hand_mod = False

            self._set_position()

        new_figure = {
            'dots': [],
            'finished': False,
            'erase': self.fill_mod.get() == 1,
            'color': self.canvas.fill_color,
        }

        self._make_record()
        self.position._data.append(new_figure)

        binds.append(self.bind("<Return>", lambda event: finish_make_figure_process(self, event)))
        binds.append(self.canvas.bind("<Button-1>", lambda event: add_dot(self, event)))
        binds.append(self.canvas.bind("<Motion>", lambda event: create_prompt_line(self, event)))
        binds.append(self.canvas.bind("<Shift-Button-1>", lambda event: add_perpendicular_dot(self, event)))
        binds.append(self.canvas.bind("<Shift-Motion>", lambda event: create_perpendicular_prompt_line(self, event)))
