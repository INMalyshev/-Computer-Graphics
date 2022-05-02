from src.app import App
from src.ui.my_lab_canvas import MyLabCanvas
from src.figure import Figure
from src.vector import Vector
from src.field import Field

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
        self.line_width = 3
        self.line_color = 'blue'
        self.circuit_color = 'red'
        self.inner_index = 0
        self.hand_mod = False

        # Настройки канвы

        self.canvas = MyLabCanvas(self)
        self.canvas.place(relx=0, rely=0, relheight=1.0, relwidth=0.8)

        # Кнопки
        self.process_button = MyButton(self, 'Задать отрезок руками', self._start_make_figure_process)
        self.process_button.place(relx=0.8, rely=0, relheight=0.05, relwidth=0.2)

        self.slowly_button = MyButton(self, 'Сбросить отсечение', self._handle_rewind_cutter_button)
        self.slowly_button.place(relx=0.8, rely=0.05, relheight=0.05, relwidth=0.2)

        self.fill_mod = IntVar()
        self.fill_mod.set(0)
        self.filling_mod = Radiobutton(self, text="duplicated", variable=self.fill_mod, value=0)
        self.erasing_mod = Radiobutton(self, text="duplicated", variable=self.fill_mod, value=1)
        self.filling_mod.place(relx=0.8, rely=0.1, relheight=0.05, relwidth=0.1)
        self.erasing_mod.place(relx=0.9, rely=0.1, relheight=0.05, relwidth=0.1)

        self.del_with_id_button = MyButton(self, 'Удалить по индексу', self._handle_del_with_id_button)
        self.del_with_id_button.place(relx=0.8, rely=0.15, relheight=0.05, relwidth=0.2)

        self.change_color_button = MyButton(self, 'Изменить цвет линии', self._handle_choose_line_color_button)
        self.change_color_button.place(relx=0.8, rely=0.2, relheight=0.05, relwidth=0.2)

        self.new_figure_button = MyButton(self, 'duplicated', None)
        self.new_figure_button.place(relx=0.8, rely=0.45, relheight=0.05, relwidth=0.2)

        self.finish_figure_button = MyButton(self, 'duplicated', None)
        self.finish_figure_button.place(relx=0.8, rely=0.5, relheight=0.05, relwidth=0.2)

        self.text_x0 = StringVar()
        self.text_y0 = StringVar()
        self.text_x1 = StringVar()
        self.text_y1 = StringVar()

        Label(self, text='x0:').place(relx=0.8, rely=0.55, relheight=0.05, relwidth=0.05)
        self.x0_entry = Entry(self, textvariable=self.text_x0)
        self.x0_entry.place(relx=0.85, rely=0.55, relheight=0.05, relwidth=0.15)

        Label(self, text='y0:').place(relx=0.8, rely=0.6, relheight=0.05, relwidth=0.05)
        self.y0_entry = Entry(self, textvariable=self.text_y0)
        self.y0_entry.place(relx=0.85, rely=0.6, relheight=0.05, relwidth=0.15)

        Label(self, text='x1:').place(relx=0.8, rely=0.65, relheight=0.05, relwidth=0.05)
        self.x1_entry = Entry(self, textvariable=self.text_x1)
        self.x1_entry.place(relx=0.85, rely=0.65, relheight=0.05, relwidth=0.15)

        Label(self, text='y1:').place(relx=0.8, rely=0.7, relheight=0.05, relwidth=0.05)
        self.y1_entry = Entry(self, textvariable=self.text_y1)
        self.y1_entry.place(relx=0.85, rely=0.7, relheight=0.05, relwidth=0.15)

        self.add_dot_button = MyButton(self, 'Установить отсечение', self._handle_set_cutter_button)
        self.add_dot_button.place(relx=0.8, rely=0.75, relheight=0.05, relwidth=0.2)

        self.change_center_button = MyButton(self, 'Добавить отрезок', self._handle_add_line_button)
        self.change_center_button.place(relx=0.8, rely=0.8, relheight=0.05, relwidth=0.2)

        # Text

        self.text_list = MyText(self)
        self.text_list.place(relx=0.8, rely=0.25, relheight=0.2, relwidth=0.2)

    def set_position(self, event=None, **kwargs):
        self.inner_index += 1

        only_text = False if 'only_text' not in kwargs else kwargs['only_text']
        only_scene = False if 'only_scene' not in kwargs else kwargs['only_scene']

        # print(self.inner_index)

        if not only_text:
            self.canvas.set_position(self.position.data, **kwargs)

        if not only_scene:
            self.text_list.set_text(self._gen_text())

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

        for ind, fig in enumerate(self.position.data):
            text += f'{ind}: state - {"finished" if fig.finished else "not finished"}\n' \
                    f'{fig.dots[-1] if fig.dots else "..."} - {fig.dots[-1] if fig.finished else "..."}\n\n'

        return text

    def _get_two_vectors_from_entries(self):
        str_x0 = self.text_x0.get()
        str_y0 = self.text_y0.get()
        str_x1 = self.text_x1.get()
        str_y1 = self.text_y1.get()

        self.text_x0.set('')
        self.text_y0.set('')
        self.text_x1.set('')
        self.text_y1.set('')

        x0, y0, x1, y1 = None, None, None, None

        try:
            x0 = float(str_x0)

        except Exception:
            if len(str_x0) > 0:
                showerror('x0 error', 'x0 not a float number')

            return None

        try:
            y0 = float(str_y0)
        except Exception:
            if len(str_y0) > 0:
                showerror('y0 error', 'y0 not a float number')

            return None

        a = Vector(x0, y0)

        try:
            x1 = float(str_x1)
        except Exception:
            if len(str_x1) > 0:
                showerror('x1 error', 'x1 not a float number')

            return None

        try:
            y1 = float(str_y1)
        except Exception:
            if len(str_y1) > 0:
                showerror('y1 error', 'y1 not a float number')

            return None

        b = Vector(x1, y1)

        return a, b

    def _rewind(self, event=None):
        self._make_record()

        self.position.data = list()
        self.canvas.cutter = None

        self.set_position()

    def _handle_rewind_cutter_button(self, event=None):
        self.canvas.change_cutter(None)
        self.set_position()

    def _handle_set_cutter_button(self, event=None):
        answer = self._get_two_vectors_from_entries()

        if answer is not None:
            a, b = answer

            if not self.canvas.field.include(a):
                showerror('cutter error', f'{a} not in {self.canvas.field.start} : {self.canvas.field.finish}')

                return None

            if not self.canvas.field.include(b):
                showerror('cutter error', f'{b} not in {self.canvas.field.start} : {self.canvas.field.finish}')

                return None

            cutter = Field(a, b)

            self.canvas.change_cutter(cutter)

            self.set_position()

    def _handle_add_line_button(self, event=None):
        answer = self._get_two_vectors_from_entries()

        if answer is not None:
            a, b = answer

            new_figure = {
                    'finished': True,
                    'tag': 'tag' + str(self.inner_index),
                    'fill': self.canvas.line_color,
                    'type': 'line',
                    'dots': [a, b],
                }

            self._make_record()
            self.position.data.append(Figure(self.canvas, **new_figure))
            self.set_position()

    def _handle_choose_line_color_button(self, event=None):
        color = colorchooser.askcolor()
        if color is not None:
            self.canvas.change_line_color(color[1])


    def _start_make_figure_process(self, event=None):
        if self.position.data:
            if not self.position.data[-1].finished:
                del self.position.data[-1]

        self.hand_mod = True

        binds = []
        line_width = self.canvas.line_width

        def finish_make_figure_process(self, event=None):
            # self.unbind("<Return>", binds[0])
            self.canvas.unbind("<Button-1>", binds[1])
            self.canvas.unbind("<Motion>", binds[2])
            self.canvas.unbind("<Shift-Button-1>", binds[3])
            self.canvas.unbind("<Shift-Motion>", binds[4])

            self.hand_mod = False

            tag = self.position.data[-1].tag
            self.set_position(tag=tag)

        def add_dot(self, event=None):
            on_canvas = Vector(event.x, event.y)
            on_real = self.canvas.canvasCoordinates2vector(on_canvas)
            self.position.data[-1].dots.append(on_real)
            tag = self.position.data[-1].tag
            self.set_position(tag=tag)
            if len(self.position.data[-1].dots) >= 2:
                self.position.data[-1].finished = True
                finish_make_figure_process(self)

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

            self.position.data[-1].dots.append(on_real)
            tag = self.position.data[-1].tag
            self.set_position(tag=tag)

            if len(self.position.data[-1].dots) >= 2:
                self.position.data[-1].finished = True
                finish_make_figure_process(self)

        def create_prompt_line(self, event):
            if len(self.position.data[-1].dots) > 0:
                tag = self.position.data[-1].tag
                self.set_position(tag=tag)

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

        # def finish_make_figure_process(self, event=None):
        #     # self.unbind("<Return>", binds[0])
        #     self.canvas.unbind("<Button-1>", binds[1])
        #     self.canvas.unbind("<Motion>", binds[2])
        #     self.canvas.unbind("<Shift-Button-1>", binds[3])
        #     self.canvas.unbind("<Shift-Motion>", binds[4])
        #
        #     self.hand_mod = False
        #
        #     # tag = self.position.data[-1].tag
        #     # self.set_position(tag=tag)

        new_figure = {
            'finished': False,
            'tag': 'tag' + str(self.inner_index),
            'fill': self.canvas.line_color,
            'type': 'line',
            'dots': [],
        }

        self._make_record()
        self.position.data.append(Figure(self.canvas, **new_figure))
        self.set_position(only_text=True)

        binds.append(self.bind("<Return>", None))
        binds.append(self.canvas.bind("<Button-1>", lambda event: add_dot(self, event)))
        binds.append(self.canvas.bind("<Motion>", lambda event: create_prompt_line(self, event)))
        binds.append(self.canvas.bind("<Shift-Button-1>", lambda event: add_perpendicular_dot(self, event)))
        binds.append(self.canvas.bind("<Shift-Motion>", lambda event: create_perpendicular_prompt_line(self, event)))

