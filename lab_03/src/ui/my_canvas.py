from tkinter import Canvas
from math import fabs

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector

from src.cadre import Cadre

from src.calculations.lines import *
from math import degrees, radians, pi
from src.calculations.rsp import rotate


class MyCanvas(Canvas):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyCanvas, self).__init__(
            parent,
            width=self.settings.ui.canvas.width,
            height=self.settings.ui.canvas.height,
            bg=self.settings.ui.canvas.bg,
        )

        self.field = Field( \
            Vector(self.settings.ui.canvas.field_start_x, self.settings.ui.canvas.field_start_y), \
            Vector(self.settings.ui.canvas.field_finish_x, self.settings.ui.canvas.field_finish_y) \
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

    def draw_cross(self):
        if self.field.start.x < 0 and self.field.finish.x > 0:
            l2_start = Vector(0, self.field.start.y)
            l2_finish = Vector(0, self.field.finish.y)
            self.draw_line(l2_start, l2_finish, 0, "black", "cross")

        if self.field.start.y < 0 and self.field.finish.y > 0:
            l1_start = Vector(self.field.start.x, 0)
            l1_finish = Vector(self.field.finish.x, 0)
            self.draw_line(l1_start, l1_finish, 0, "black", "cross")

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

    def _set_position(self, position):
        self.delete("all")
        self.draw_cross()

        if not isinstance(position, Cadre):
            return NotImplemented

        for i in range(len(position._data)):
            if position._data[i]["type"] == "line":
                self.draw_line(position._data[i]["start"], position._data[i]["finish"], position._data[i]["mod"], \
                               position._data[i]["color"], f"line_{i}")
            elif position._data[i]["type"] == "bunch":
                self.draw_bunch(position._data[i]["center"], position._data[i]["line_len"], position._data[i]["angle_step"], \
                                position._data[i]["mod"], position._data[i]["color"], f"line_{i}")


    # lab_03

    def pri_pix(self, x, y, color, tag):
        self.create_oval(x - self.settings.pixel_radius,
                         y - self.settings.pixel_radius,
                         x + self.settings.pixel_radius,
                         y + self.settings.pixel_radius,
                         outline=color,
                         tag=tag)

    def draw_line(self, a, b, mod, color, tag):
        # Возвращает количество ступенек или None, если defaul или исключение

        a_converted = self.vector2canvasCoordinates(a)
        b_converted = self.vector2canvasCoordinates(b)

        if a_converted == b_converted:
            self.pri_pix(a_converted.x, a_converted.y, color, tag)
            return None

        functions = [
            dda_line,
            bresenham_line,
            int_bresenham_line,
            no_angle_bresenham_line,
            wu_line,
        ]

        answer = None

        if mod == 0:
            # default
            self.create_line(a_converted.x, a_converted.y, b_converted.x, b_converted.y, fill=color, tag=tag)

            return answer

        elif mod in range(1, 6):
            data = functions[mod-1](a_converted, b_converted, color, tag)

            answer = calculate_steps(data)

            if data is not None:
                for i in range(0, len(data), 4):
                    for j in range(len(data[0])):
                        self.pri_pix(data[i][j], data[i+1][j], data[i+2][j], data[i+3][j])

            return answer

        else:
            return answer

    def draw_bunch(self, center, line_len, degree_angle_step, mod, color, tag):
        default_dot = Vector(center.x + line_len, center.y)
        angle = 0

        while abs(angle) < degrees(2 * pi):
            second_dot = rotate(default_dot, radians(angle), center)
            self.draw_line(center, second_dot, mod, color, tag)
            angle += degree_angle_step
