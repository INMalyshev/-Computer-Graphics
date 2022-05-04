from src.app import App
from src.ui.my_lab_canvas import MyLabCanvas
from src.figure import Figure
from src.vector import Vector

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


class LabApp(App):
    def __init__(self):
        super(LabApp, self).__init__()

        # Параметры
        self.line_width = 2
        self.line_color = 'red'
        self.inner_index = 0
        self.hand_mod = False
        self.fill_color = 'pink'
        self.init_coordinate = Vector(0, 0)

        # Настройки канвы

        self.canvas = MyLabCanvas(self)
        self.canvas.place(relx=0, rely=0, relheight=1.0, relwidth=0.8)

        # Кнопки
        self.process_button = MyButton(self, 'Задать отрезок руками', self._start_make_figure_process)
        self.process_button.place(relx=0.8, rely=0, relheight=0.05, relwidth=0.2)

        self.slowly_button = MyButton(self, 'Медленно отрисовать сцену', lambda: self.set_position(step_by_step=True))
        self.slowly_button.place(relx=0.8, rely=0.05, relheight=0.05, relwidth=0.2)

        self.fill_mod = IntVar()
        self.fill_mod.set(0)
        self.filling_mod = Radiobutton(self, text="Заполнение", variable=self.fill_mod, value=0)
        self.erasing_mod = Radiobutton(self, text="Вырезание", variable=self.fill_mod, value=1)
        self.filling_mod.place(relx=0.8, rely=0.1, relheight=0.05, relwidth=0.1)
        self.erasing_mod.place(relx=0.9, rely=0.1, relheight=0.05, relwidth=0.1)

        self.del_with_id_button = MyButton(self, 'Удалить по индексу', self._handle_del_with_id_button)
        self.del_with_id_button.place(relx=0.8, rely=0.15, relheight=0.05, relwidth=0.2)

        self.change_color_button = MyButton(self, 'Изменить цвет заполнения', self._handle_choose_fill_color_button)
        self.change_color_button.place(relx=0.8, rely=0.2, relheight=0.05, relwidth=0.2)

        self.new_figure_button = MyButton(self, 'Добавить фигуру', self._handle_new_figure_button)
        self.new_figure_button.place(relx=0.8, rely=0.45, relheight=0.05, relwidth=0.2)

        self.finish_figure_button = MyButton(self, 'Завершить фигуру', self._handle_finish_figure_button)
        self.finish_figure_button.place(relx=0.8, rely=0.5, relheight=0.05, relwidth=0.2)

        self.text_x = StringVar()
        self.text_y = StringVar()

        Label(self, text='x:').place(relx=0.8, rely=0.55, relheight=0.05, relwidth=0.05)
        self.x_entry = Entry(self, textvariable=self.text_x)
        self.x_entry.place(relx=0.85, rely=0.55, relheight=0.05, relwidth=0.15)

        Label(self, text='y:').place(relx=0.8, rely=0.6, relheight=0.05, relwidth=0.05)
        self.y_entry = Entry(self, textvariable=self.text_y)
        self.y_entry.place(relx=0.85, rely=0.6, relheight=0.05, relwidth=0.15)

        self.add_dot_button = MyButton(self, 'Добавить точку', self._handle_add_dot_button)
        self.add_dot_button.place(relx=0.8, rely=0.65, relheight=0.05, relwidth=0.2)

        self.change_center_button = MyButton(self, 'Изменить затравочные координаты', self._handle_set_center_button)
        self.change_center_button.place(relx=0.8, rely=0.7, relheight=0.05, relwidth=0.2)

        # Text

        self.text_list = MyText(self)
        self.text_list.place(relx=0.8, rely=0.25, relheight=0.2, relwidth=0.2)

    def set_position(self, event=None, **kwargs):
        self.inner_index += 1

        only_text = False if 'only_text' not in kwargs else kwargs['only_text']
        only_scene = False if 'only_scene' not in kwargs else kwargs['only_scene']

        if self.inner_index < 4:
            return

        # print(self.inner_index)

        if not only_text:
            self.canvas.set_position(self.position.data, **kwargs)

        if not only_scene:
            self.text_list.set_text(self._gen_text())

        self.canvas.draw_x(self.init_coordinate)

    def _handle_del_with_id_button(self, event=None):
        new_window = MyDelWithIdForm(self)
        id = new_window.handle_open()

        if id is None:
            return

        if 0 <= id < len(self.position.data):
            self._make_record()
            tag = self.position.data[id].tag
            del self.position.data[id]
            self.set_position(tag=tag)

    def _gen_text(self):
        text = ''

        for ind, figure in enumerate(self.position.data):
            state = 'finished' if figure.finished else 'not finished'
            text += f'id: {ind}, state: {state}\n'
            text += f'last time: {figure.last_time * 1000 :.3f}\n'

            for dot in figure.dots:
                text += f'  {dot}\n'

        text += '\n'

        return text

    def _handle_new_figure_button(self, event=None):
        if self.hand_mod:
            return

        if self.position.data:
            if not self.position.data[-1].finished:
                del self.position.data[-1]

        new_figure = {
            'finished': False,
            'tag': 'tag' + str(self.inner_index),
            'erase': self.fill_mod.get() == 1,
            'fill': self.canvas.fill_color,
            'type': 'polygon',
            'dots': [],
            'init_coordinate': self.init_coordinate,
        }

        self._make_record()
        self.position.data.append(Figure(self.canvas, **new_figure))
        self.set_position(only_text=True)

    def _handle_finish_figure_button(self, event=None):
        if self.hand_mod:
            return

        if self.position.data:
            if self.position.data[-1].finished:
                return

            tag = self.position.data[-1].tag

            if len(self.position.data[-1].dots) < 3:
                del self.position.data[-1]

                self.set_position(tag=tag)
                return

            self.position.data[-1].finished = True
            self.set_position(tag=tag)

    def _get_vector_from_entries(self):
        str_x = self.text_x.get()
        str_y = self.text_y.get()
        self.text_x.set('')
        self.text_y.set('')

        x, y = None, None

        try:
            x = float(str_x)
        except Exception:
            if len(str_x) > 0:
                showerror('x error', 'x not a float number')

            return None

        try:
            y = float(str_y)
        except Exception:
            if len(str_y) > 0:
                showerror('y error', 'y not a float number')

            return None

        return Vector(x, y)

    def _handle_add_dot_button(self, event=None):
        if self.hand_mod:
            return

        if self.position.data:
            if self.position.data[-1].finished:
                return

        dot = self._get_vector_from_entries()

        if self.position.data:
            tag = self.position.data[-1].tag
            self.position.data[-1].dots.append(dot)

            self.set_position(tag=tag)

    def _handle_set_center_button(self, event=None):
        if self.hand_mod:
            return

        if self.position.data:
            if not self.position.data[-1].finished:
                return

        dot = self._get_vector_from_entries()

        self.init_coordinate = dot

        self.set_position()

    def _start_make_figure_process(self, event=None):
        if self.position.data:
            if not self.position.data[-1].finished:
                del self.position.data[-1]

        self.hand_mod = True

        binds = []
        line_width = 2

        def add_dot(self, event=None):
            on_canvas = Vector(event.x, event.y)
            on_real = self.canvas.canvasCoordinates2vector(on_canvas)
            self.position.data[-1].dots.append(on_real)
            tag = self.position.data[-1].tag
            # print(self.position._data)
            self.set_position(tag=tag)

        def add_perpendicular_dot(self,  event=None):
            on_canvas = Vector(event.x, event.y)
            on_real = self.canvas.canvasCoordinates2vector(on_canvas)

            if len(self.position.data[-1].dots) > 0:
                last_dot = self.position.data[-1].dots[-1]
                delta = on_real - last_dot
                if abs(delta.x) >= abs(delta.y):
                    on_real = last_dot + Vector(delta.x, 0)
                else:
                    on_real = last_dot + Vector(0, delta.y)

            self.position._data[-1].dots.append(on_real)
            # print(self.position._data)
            tag = self.position.data[-1].tag
            self.set_position(tag=tag)

        def create_prompt_line(self, event):
            if len(self.position.data[-1].dots) > 0:
                tag = self.position.data[-1].tag
                self.set_position(tag=tag)
                # self.canvas.delete('to_del')

                on_canvas = Vector(event.x, event.y)
                on_real = self.canvas.canvasCoordinates2vector(on_canvas)
                last_dot = self.position.data[-1].dots[-1]
                self.canvas.draw_line(last_dot, on_real, fill='red', width=line_width, tag=tag)

        def create_perpendicular_prompt_line(self, event):
            if len(self.position.data[-1].dots) > 0:
                tag = self.position.data[-1].tag
                self.set_position(tag=tag)

                on_canvas = Vector(event.x, event.y)
                on_real = self.canvas.canvasCoordinates2vector(on_canvas)
                last_dot = self.position.data[-1].dots[-1]

                delta = on_real - last_dot
                if abs(delta.x) >= abs(delta.y):
                    on_real = last_dot + Vector(delta.x, 0)
                else:
                    on_real = last_dot + Vector(0, delta.y)

                self.canvas.draw_line(last_dot, on_real, fill='red', width=line_width, tag=tag)

        def finish_make_figure_process(self, event=None):
            if len(self.position.data[-1].dots) < 3:
                del self.position.data[-1]
            else:
                self.position.data[-1].finished = True

            self.unbind("<Return>", binds[0])
            self.canvas.unbind("<Button-1>", binds[1])
            self.canvas.unbind("<Motion>", binds[2])
            self.canvas.unbind("<Shift-Button-1>", binds[3])
            self.canvas.unbind("<Shift-Motion>", binds[4])

            self.hand_mod = False

            tag = self.position.data[-1].tag
            self.set_position(tag=tag)

        new_figure = {
            'finished': False,
            'tag': 'tag' + str(self.inner_index),
            'erase': self.fill_mod.get() == 1,
            'fill': self.canvas.fill_color,
            'type': 'polygon',
            'dots': [],
            'init_coordinate': self.init_coordinate,
        }

        self._make_record()
        self.position.data.append(Figure(self.canvas, **new_figure))
        self.set_position(only_text=True)

        binds.append(self.bind("<Return>", lambda event: finish_make_figure_process(self, event)))
        binds.append(self.canvas.bind("<Button-1>", lambda event: add_dot(self, event)))
        binds.append(self.canvas.bind("<Motion>", lambda event: create_prompt_line(self, event)))
        binds.append(self.canvas.bind("<Shift-Button-1>", lambda event: add_perpendicular_dot(self, event)))
        binds.append(self.canvas.bind("<Shift-Motion>", lambda event: create_perpendicular_prompt_line(self, event)))

