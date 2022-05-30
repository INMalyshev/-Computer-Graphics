from src.app import App
from src.ui.my_lab_canvas import MyLabCanvas

from tkinter import colorchooser

from src.ui.my_text import MyText
from src.vector import Vector
from src.ui.my_button import MyButton
from src.ui.del_with_id_form import MyDelWithIdForm

from tkinter.messagebox import showerror

from tkinter import StringVar, IntVar
from tkinter import Label, Entry, Radiobutton
from math import sin, radians, cos
import numpy as np
from src.vector import Vector
from math import pi, sin, cos
from numpy import arange

# from fhorizon import funcs


class LabApp(App):
    def __init__(self):
        super(LabApp, self).__init__()

        self.title('lab_10')

        # Параметры
        self.inner_index = 0

        self.default_x0 = '-5'
        self.default_xn = '5'
        self.default_dx = '0.2'

        self.default_z0 = '-5'
        self.default_zn = '5'
        self.default_dz = '0.2'

        self.default_dr = '0'
        self.default_ds = '1'

        self.functions = [
            lambda x, z: x + z,
            lambda x, z: sin(x) * sin(z),
            lambda x, z: sin(cos(x)) * sin(z),
            lambda x, z: sin(z) * x / 2,
        ]

        self.color = "#FF0000"
        self.scale = 10

        self.mat = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

        self.bind("<MouseWheel>", self._handle_zoom, "+")



        # Настройки канвы

        self.canvas = MyLabCanvas(self)
        self.canvas.place(relx=0, rely=0, relheight=1.0, relwidth=0.8)

        # Разметка
        self.process_button = MyButton(self, 'Рассчитать поверхность', self.handle_main_btn)
        self.process_button.place(relx=0.8, rely=0, relheight=0.05, relwidth=0.2)

        self.text_x0 = StringVar()
        self.text_x0.set(self.default_x0)
        self.text_xn = StringVar()
        self.text_xn.set(self.default_xn)
        self.text_dx = StringVar()
        self.text_dx.set(self.default_dx)

        Label(self, text='x0:').place(relx=0.8, rely=0.1, relheight=0.025, relwidth=0.05)
        self.x0_entry = Entry(self, textvariable=self.text_x0)
        self.x0_entry.place(relx=0.85, rely=0.1, relheight=0.025, relwidth=0.125)

        Label(self, text='xn:').place(relx=0.8, rely=0.125, relheight=0.025, relwidth=0.05)
        self.xn_entry = Entry(self, textvariable=self.text_xn)
        self.xn_entry.place(relx=0.85, rely=0.125, relheight=0.025, relwidth=0.125)

        Label(self, text='dx:').place(relx=0.8, rely=0.15, relheight=0.025, relwidth=0.05)
        self.dx_entry = Entry(self, textvariable=self.text_dx)
        self.dx_entry.place(relx=0.85, rely=0.15, relheight=0.025, relwidth=0.125)

        self.text_z0 = StringVar()
        self.text_z0.set(self.default_z0)
        self.text_zn = StringVar()
        self.text_zn.set(self.default_zn)
        self.text_dz = StringVar()
        self.text_dz.set(self.default_dz)

        Label(self, text='z0:').place(relx=0.8, rely=0.2, relheight=0.025, relwidth=0.05)
        self.z0_entry = Entry(self, textvariable=self.text_z0)
        self.z0_entry.place(relx=0.85, rely=0.2, relheight=0.025, relwidth=0.125)

        Label(self, text='zn:').place(relx=0.8, rely=0.225, relheight=0.025, relwidth=0.05)
        self.zn_entry = Entry(self, textvariable=self.text_zn)
        self.zn_entry.place(relx=0.85, rely=0.225, relheight=0.025, relwidth=0.125)

        Label(self, text='dz:').place(relx=0.8, rely=0.25, relheight=0.025, relwidth=0.05)
        self.dz_entry = Entry(self, textvariable=self.text_dz)
        self.dz_entry.place(relx=0.85, rely=0.25, relheight=0.025, relwidth=0.125)

        self.function_number = IntVar()
        self.function_number.set(0)

        self.f0 = Radiobutton(self, text="y = x + z", variable=self.function_number, value=0)
        self.f1 = Radiobutton(self, text="y = sin(x) * sin(z)", variable=self.function_number, value=1)
        self.f2 = Radiobutton(self, text="sin(cos(x)) * sin(z)", variable=self.function_number, value=2)
        self.f3 = Radiobutton(self, text="sin(z) * x / 2", variable=self.function_number, value=3)
        # self.f4 = Radiobutton(self, text="function number five", variable=self.function_number, value=4)
        # self.f5 = Radiobutton(self, text="function number six", variable=self.function_number, value=5)

        self.f0.place(relx=0.8, rely=0.3, relheight=0.025, relwidth=0.2)
        self.f1.place(relx=0.8, rely=0.325, relheight=0.025, relwidth=0.2)
        self.f2.place(relx=0.8, rely=0.35, relheight=0.025, relwidth=0.2)
        self.f3.place(relx=0.8, rely=0.375, relheight=0.025, relwidth=0.2)
        # self.f4.place(relx=0.8, rely=0.4, relheight=0.025, relwidth=0.2)
        # self.f5.place(relx=0.8, rely=0.425, relheight=0.025, relwidth=0.2)

        self.text_drx = StringVar()
        self.text_drx.set(self.default_dr)
        Label(self, text='Поворот вокруг x (градусы):').place(relx=0.8, rely=0.475, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_drx).place(relx=0.91, rely=0.475, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Повернуть', self.handle_xrot).place(relx=0.945, rely=0.475, relheight=0.025, relwidth=0.05)

        self.text_dry = StringVar()
        self.text_dry.set(self.default_dr)
        Label(self, text='Поворот вокруг y (градусы):').place(relx=0.8, rely=0.5, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_dry).place(relx=0.91, rely=0.5, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Повернуть', self.handle_yrot).place(relx=0.945, rely=0.5, relheight=0.025, relwidth=0.05)

        self.text_drz = StringVar()
        self.text_drz.set(self.default_dr)
        Label(self, text='Поворот вокруг z (градусы):').place(relx=0.8, rely=0.525, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_drz).place(relx=0.91, rely=0.525, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Повернуть', self.handle_zrot).place(relx=0.945, rely=0.525, relheight=0.025, relwidth=0.05)

        self.text_dsx = StringVar()
        self.text_dsx.set(self.default_ds)
        Label(self, text='Масштабирование по x:').place(relx=0.8, rely=0.575, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_dsx).place(relx=0.91, rely=0.575, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Масштабировать', self.handle_xscal).place(relx=0.945, rely=0.575, relheight=0.025, relwidth=0.05)

        self.text_dsy = StringVar()
        self.text_dsy.set(self.default_ds)
        Label(self, text='Масштабирование по y:').place(relx=0.8, rely=0.6, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_dsy).place(relx=0.91, rely=0.6, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Масштабировать', self.handle_yscal).place(relx=0.945, rely=0.6, relheight=0.025, relwidth=0.05)

        self.text_dsz = StringVar()
        self.text_dsz.set(self.default_ds)
        Label(self, text='Масштабирование по z:').place(relx=0.8, rely=0.625, relheight=0.025, relwidth=0.105)
        Entry(self, textvariable=self.text_dsz).place(relx=0.91, rely=0.625, relheight=0.025, relwidth=0.03)
        MyButton(self, 'Масштабировать', self.handle_zscal).place(relx=0.945, rely=0.625, relheight=0.025, relwidth=0.05)

        MyButton(self, 'Сбросить', self._rewind).place(relx=0.8, rely=0.675, relheight=0.05, relwidth=0.2)

        self.menu.filemenu.add_separator()
        self.menu.filemenu.add_command(label="Изменить цвет фигуры", command=self.change_color)

    def change_color(self, event=None):
        color = colorchooser.askcolor()
        if color is not None:
            self.color = color[1]

    def set_position(self, event=None, **kwargs):
        self.inner_index += 1
        # self.calculate()

        self.canvas.set_position(self.position.data, **kwargs)

    def _handle_zoom(self, event=None):
        if (event.delta > 0):
                self.scale *= 1.1
        elif (event.delta < 0):
            self.scale *= 0.9
        self.set_position()

        self.calculate()

    def _rewind(self, event=None):
        self.set_default()
        self.default_properties()
        self.canvas.delete('all')
        self.set_position()

    def set_default(self):
        self.text_x0.set(self.default_x0)
        self.text_xn.set(self.default_xn)
        self.text_dx.set(self.default_dx)

        self.text_z0.set(self.default_z0)
        self.text_zn.set(self.default_zn)
        self.text_dz.set(self.default_dz)

        self.text_drx.set(self.default_dr)
        self.text_dry.set(self.default_dr)
        self.text_drz.set(self.default_dr)

    @staticmethod
    def get_float(s):
        res = None

        try:
            res = float(s)
        except:
            showerror('Ошибка приведения', f'"{s}" не приводится к float.')

            return None

        return res

    @staticmethod
    def get_int(s):
        res = None

        try:
            res = int(s)
        except:
            showerror('Ошибка приведения', f'"{s}" не приводится к int.')

            return None

        return res

    def get_meta(self):
        x0 = self.get_float(self.text_x0.get())
        xn = self.get_float(self.text_xn.get())
        dx = self.get_float(self.text_dx.get())

        z0 = self.get_float(self.text_z0.get())
        zn = self.get_float(self.text_zn.get())
        dz = self.get_float(self.text_dz.get())

        drx = radians(self.get_int(self.text_drx.get()))
        dry = radians(self.get_int(self.text_dry.get()))
        drz = radians(self.get_int(self.text_drz.get()))

        dsx = self.get_float(self.text_dsx.get())
        dsy = self.get_float(self.text_dsy.get())
        dsz = self.get_float(self.text_dsz.get())

        answer = {
            'x0': x0, 'xn': xn, 'dx': dx,
            'z0': z0, 'zn': zn, 'dz': dz,
            'drx': drx, 'dry': dry, 'drz': drz,
            'dsx': dsx, 'dsy': dsy, 'dsz': dsz,
            'function': self.functions[self.function_number.get()],
        }

        if None in answer.values():
            self.set_default()

            return None

        if xn < x0 or dx < 0:
            showerror('Ошибка значений', 'Значения для оси X неудовлетворительны.')

            return None

        if zn < z0 or dz < 0:
            showerror('Ошибка значений', 'Значения для оси Z неудовлетворительны.')

            return None

        return answer






    def draw_pixel(self, x, y, color):
        self.canvas.create_line(x, y, x + 1, y + 1, fill=color)

    def is_visible(self, dot):
        return 0 <= dot[0] < self.canvas.winfo_width() and 0 <= dot[1] < self.canvas.winfo_height()

    def draw_dot(self, x, y, uphor, lowhor):
        if not self.is_visible([x, y]):
            return False

        if y > uphor[x]:
            uphor[x] = y
            self.draw_pixel(x, y, self.color)

        elif y < lowhor[x]:
            lowhor[x] = y
            self.draw_pixel(x, y, self.color)

        return True

    def draw_line(self, dot_start, dot_end, color):
        self.canvas.create_line(dot_start[0], dot_start[1], dot_end[0], dot_end[1], fill=color)

    def rotate_mat(self, mat):
        res_mat = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        for i in range(4):
            for j in range(4):
                for k in range(4):
                    res_mat[i][j] += self.mat[i][k] * mat[k][j]

        self.mat = res_mat

    def trans_dot(self, dot):
        dot.append(1)
        res_dot = [0, 0, 0, 0]
        for i in range(4):
            for j in range(4):
                res_dot[i] += dot[j] * self.mat[j][i]

        for i in range(3):
            res_dot[i] *= self.scale

        res_dot[0] += self.canvas.winfo_width() // 2
        res_dot[1] += self.canvas.winfo_height() // 2

        return res_dot[:3]

    def xrotate(self, val):
        mat = [
            [1, 0, 0, 0],
            [0, cos(val), sin(val), 0],
            [0, -sin(val), cos(val), 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def yrotate(self, val):
        mat = [
            [cos(val), 0, -sin(val), 0],
            [0, 1, 0, 0],
            [sin(val), 0, cos(val), 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def zrotate(self, val):
        mat = [
            [cos(val), sin(val), 0, 0],
            [-sin(val), cos(val), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def xscale(self, val):
        mat = [
            [val, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def yscale(self, val):
        mat = [
            [1, 0, 0, 0],
            [0, val, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def zscale(self, val):
        mat = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, val, 0],
            [0, 0, 0, 1]
        ]
        self.rotate_mat(mat)

    def predraw_horizon(self, fdot, sdot, uphor, lowhor):
        if fdot[0] > sdot[0]:
            fdot, sdot = sdot, fdot

        dx = sdot[0] - fdot[0]
        dy = sdot[1] - fdot[1]

        l = None
        if dx > dy:
            l = dx
        else:
            l = dy

        dx /= l
        dy /= l

        x = fdot[0]
        y = fdot[1]

        for _ in range(int(l) + 1):
            x = int(round(x))
            if not self.draw_dot(x, y, uphor, lowhor):
                return

            x += dx
            y += dy

    def draw_horizon(self, func, uphor, lowhor, start, end, step, z):
        def f(x):
            return func(x, z)

        prev = None

        for x in arange(start, end + step, step):
            cur = self.trans_dot([x, f(x), z])
            if prev:
                self.predraw_horizon(prev, cur, uphor, lowhor)
            prev = cur

    def fhorizon(self, meta):
        # self.reset()

        func = meta['function']

        uphor = [0 for _ in range(self.canvas.winfo_width())]
        lowhor = [self.canvas.winfo_height() for _ in range(self.canvas.winfo_width())]

        for z in arange(meta['z0'], meta['zn'] + meta['dz'], meta['dz']):
            self.draw_horizon(func, uphor, lowhor, meta['x0'], meta['xn'], meta['dx'], z)

        for z in arange(meta['z0'], meta['zn'], meta['dz']):
            fdot = self.trans_dot([meta['x0'], func(meta['x0'], z), z])
            sdot = self.trans_dot([meta['x0'], func(meta['x0'], z + meta['dz']), z + meta['dz']])
            self.draw_line(fdot, sdot, self.color)
            fdot = self.trans_dot([meta['xn'], func(meta['xn'], z), z])
            sdot = self.trans_dot([meta['xn'], func(meta['xn'], z + meta['dz']), z + meta['dz']])
            self.draw_line(fdot, sdot, self.color)







    def default_properties(self):
        self.scale = 10

        self.mat = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]

    def calculate(self, event=None):
        self.set_position()
        meta = self.get_meta()
        if meta is None:
            return
        self.fhorizon(meta)

    def handle_main_btn(self, event=None):
        self.default_properties()
        self.calculate(event)

    def handle_xrot(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.xrotate(meta['drx'])
        self.calculate()

    def handle_yrot(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.yrotate(meta['dry'])
        self.calculate()

    def handle_zrot(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.zrotate(meta['drz'])
        self.calculate()

    def handle_xscal(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.xscale(meta['dsx'])
        self.calculate()

    def handle_yscal(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.yscale(meta['dsy'])
        self.calculate()

    def handle_zscal(self):
        meta = self.get_meta()
        if meta is None:
            return
        self.zscale(meta['dsz'])
        self.calculate()







