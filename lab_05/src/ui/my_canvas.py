from tkinter import Canvas
from math import fabs

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector

from src.cadre import Cadre

from src.calculations.circles import *
from src.calculations.ellipses import *

from src.utils.decorators import calculate_time

from src.calculations.lines import line

class MyCanvas(Canvas):
    def __init__(self, parent):
        self.settings = Settings()

        self.bg_color = self.settings.ui.canvas.bg
        self.fill_color = 'pink'

        super(MyCanvas, self).__init__(
            parent,
            width=self.settings.ui.canvas.width,
            height=self.settings.ui.canvas.height,
            bg=self.bg_color,
        )

        self.field = Field(
            Vector(self.settings.ui.canvas.field_start_x, self.settings.ui.canvas.field_start_y),
            Vector(self.settings.ui.canvas.field_finish_x, self.settings.ui.canvas.field_finish_y)
            )

        self.bind("<Configure>", lambda event: self.correct_field())

    def zoom(self, k):
        if k > 0:
            v1 = self.field.start
            v2 = self.field.finish
            dv = v2 - v1
            new_dv = dv * k
            d = new_dv - dv
            new_v1 = v1 - (d * 0.5)
            new_v2 = v2 + (d * 0.5)

            self.field.start = new_v1
            self.field.finish = new_v2

    def pull(self, vector):
        if isinstance(vector, Vector):
            self.field.start += vector
            self.field.finish += vector

    def vector2canvasCoordinates(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented

        width = self.winfo_width()
        height = self.winfo_height()

        diagonal = self.field.finish - self.field.start

        kx = width / diagonal.x
        ky = height / diagonal.y

        zero = Vector(-self.field.start.x, -self.field.finish.y)
        zero_dot = zero + vector

        return Vector(zero_dot.x * kx, -zero_dot.y * ky)

    def canvasCoordinates2vector(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented

        width = self.winfo_width()
        height = self.winfo_height()

        diagonal = self.field.finish - self.field.start

        kx = width / diagonal.x
        ky = height / diagonal.y
        zero = Vector(-self.field.start.x, -self.field.finish.y)

        pos_3 = Vector(vector.x / kx, -vector.y / ky)
        pos_2 = pos_3 - zero

        return pos_2

    def distance2canvasDistance(self, alpha):
        a = Vector(0, 0)
        b = Vector(alpha, 0)
        aa = self.vector2canvasCoordinates(a)
        bb = self.vector2canvasCoordinates(b)
        return abs(aa - bb)

    def canvasDistance2distance(self, alpha):
        a = Vector(0, 0)
        b = Vector(alpha, 0)
        aa = self.canvasCoordinates2vector(a)
        bb = self.canvasCoordinates2vector(b)
        return abs(aa - bb)

    def draw_cross(self):
        n = 10
        d = min(self.field.finish.x - self.field.start.x, self.field.finish.y - self.field.start.y) / n
        dash_param = (1, 10)
        font_param = ('Helvetica 7 bold')

        if self.field.start.x < 0 < self.field.finish.x:
            l2_start = Vector(0, self.field.start.y)
            l2_finish = Vector(0, self.field.finish.y)
            self.draw_line(l2_start, l2_finish, fill="black", tag="cross", width=2)

        if self.field.start.y < 0 < self.field.finish.y:
            l1_start = Vector(self.field.start.x, 0)
            l1_finish = Vector(self.field.finish.x, 0)
            self.draw_line(l1_start, l1_finish, fill="black", tag="cross", width=2)

        for i in range(-10 * n, 10 * n + 1, 1):
            cur_x = d * i

            if i != 0:
                l2_start = Vector(cur_x, self.field.start.y)
                l2_finish = Vector(cur_x, self.field.finish.y)
                self.draw_line(l2_start, l2_finish, fill="grey", tag="cross", width=1, dash=dash_param)

            text_point = Vector(cur_x, 0)
            shift = Vector(5, 3) * ((self.field.finish.x - self.field.start.x) / self.winfo_height())
            text = f"{text_point.x:.2f}"
            self.draw_text(text_point + shift, text=text, font=font_param)

        for i in range(-10 * n, 10 * n + 1, 1):
            if i == 0:
                continue

            cur_y = d * i

            l2_start = Vector(self.field.start.x, cur_y)
            l2_finish = Vector(self.field.finish.x, cur_y)
            self.draw_line(l2_start, l2_finish, fill="grey", tag="cross", width=1, dash=dash_param)

            text_point = Vector(0, cur_y)
            shift = Vector(15, 3) * ((self.field.finish.x - self.field.start.x) / self.winfo_width())
            text = f"{text_point.y:.2f}"
            self.draw_text(text_point + shift, text=text, font=font_param)

    def correct_field(self):
        width = self.winfo_width()
        height = self.winfo_height()

        fwidth = self.field.finish.x - self.field.start.x
        fheight = self.field.finish.y - self.field.start.y

        if fabs(fwidth * height - fheight * width) > self.settings.math.eps:
            fxmid = 0.5 * (self.field.finish.x + self.field.start.x)
            new_fwidth = fheight * width / height
            self.field.start.x = fxmid - new_fwidth * 0.5
            self.field.finish.x = fxmid + new_fwidth * 0.5

    def pri_pix(self, x, y, **kwargs):
        bl = [x, y]
        br = [x + 1, y]
        ul = [x, y + 1]
        ur = [x + 1, y + 1]
        self.create_polygon(bl, br, ur, ul, **kwargs)

    def draw_line(self, a, b, **kwargs):
        a_converted = self.vector2canvasCoordinates(a)
        b_converted = self.vector2canvasCoordinates(b)

        x0, y0 = a_converted.x, a_converted.y
        x1, y1 = b_converted.x, b_converted.y

        self.create_line(x0, y0, x1, y1, **kwargs)

    def draw_text(self, point, **kwargs):
        point_converted = self.vector2canvasCoordinates(point)

        x, y = point_converted.x, point_converted.y

        self.create_text(x, y, **kwargs)

    def change_bg_color(self, color):
        self.configure(bg=color)
        self.bg_color = color

    def change_fill_color(self, color):
        self.fill_color = color

    def _set_position(self, position, animated=False):
        self.delete("all")
        self.draw_cross()

        if not isinstance(position, Cadre):
            return NotImplemented

        line_width = 2

        self.draw_figures(position._data, animated)

        if len(position._data) > 0:
            if not position._data[-1]['finished']:
                for j in range(len(position._data[-1]['dots']) - 1):
                    self.draw_line(position._data[-1]['dots'][j], position._data[-1]['dots'][j+1], fill='red', width=line_width)

    def draw_figures(self, figures_original, animated=False):
        line_width = 2
        figures = figures_original.copy()
        figures.sort(key=lambda x: x['erase'])
        canvas_matrix = [[None for _ in range(self.winfo_height())] for _ in range(self.winfo_width())]

        for figure in figures:
            if figure['finished']:
                self.draw_figure(figure, canvas_matrix)

                if figure['erase'] == 1:
                    for i in range(-1, len(figure['dots']) - 1):
                        self.draw_line(figure['dots'][i], figure['dots'][i + 1], fill='red', width=line_width)

        for y in range(self.winfo_height()):
            if animated:
                self.update()
            for x in range(self.winfo_width()):
                if canvas_matrix[x][y]:
                    self.pri_pix(x, y, fill=canvas_matrix[x][y])

    def draw_figure(self, figure, matrix):
        # canvas_matrix = [[False for _ in range(len(matrix))] for _ in range(len(matrix[0]))]
        canvas_matrix = [[None for _ in range(self.winfo_height())] for _ in range(self.winfo_width())]

        figure_dots = figure['dots']

        right = figure_dots[0].x

        field = Field(Vector(0, 0), Vector(self.winfo_width(), self.winfo_height()))

        for fd in figure_dots:
            right = max(right, fd.x)

        cr = self.distance2canvasDistance(right - self.field.start.x)

        figure_sides = [(figure_dots[i], figure_dots[i + 1]) for i in range(-1, len(figure_dots) - 1, 1)]
        for fs in figure_sides:
            start = self.vector2canvasCoordinates(fs[0])
            finish = self.vector2canvasCoordinates(fs[1])

            x_arr, y_arr = line(start, finish)

            if y_arr[-1] > y_arr[0]:
                y_arr.reverse()
                x_arr.reverse()

            for i in range(1, len(x_arr), 1):
                x, y = int(x_arr[i]), int(y_arr[i])

                if field.start.y <= y <= field.finish.y:
                    if x < 0:
                        x = 0

                    for dx in range(0, min(int(cr) - x, self.winfo_width() - x)):
                        if 0 < x + dx >= len(canvas_matrix) or 0 < y >= len(canvas_matrix[0]):
                            break
                        # canvas_matrix[x + dx][y] = not canvas_matrix[x + dx][y]
                        canvas_matrix[x + dx][y] = figure['color'] if canvas_matrix[x + dx][y] is None else None

        for xi in range(len(matrix)):
            for yi in range(len(matrix[0])):
                if figure['erase']:
                    matrix[xi][yi] = False if canvas_matrix[xi][yi] is not None else matrix[xi][yi]
                else:
                    # matrix[xi][yi] = max(canvas_matrix[xi][yi], matrix[xi][yi])
                    matrix[xi][yi] = canvas_matrix[xi][yi] if canvas_matrix[xi][yi] is not None else matrix[xi][yi]
