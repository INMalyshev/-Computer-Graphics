from tkinter import Canvas
from math import fabs

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector

from src.cadre import Cadre

from src.calculations.circles import *
from src.calculations.ellipses import *


class MyCanvas(Canvas):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyCanvas, self).__init__(
            parent,
            width=self.settings.ui.canvas.width,
            height=self.settings.ui.canvas.height,
            bg=self.settings.ui.canvas.bg,
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
            if position._data[i]["type"] == "circle":
                self.draw_circle(position._data[i]["center"], position._data[i]["radius"], position._data[i]["mod"], \
                               position._data[i]["color"], f"circle_{i}")

            elif position._data[i]["type"] == "circle_bunch":
                self.draw_circle_bunch(position._data[i]["center"], position._data[i]["min_radius"], position._data[i]["max_radius"], \
                                position._data[i]["circle_amount"], position._data[i]["mod"], position._data[i]["color"], f"circle_bunch_{i}")

            elif position._data[i]["type"] == "ellipse":
                self.draw_ellipse(position._data[i]["center"], position._data[i]["x_radius"], position._data[i]["y_radius"], \
                                 position._data[i]["mod"], position._data[i]["color"], f"ellipse_{i}")

            elif position._data[i]["type"] == "ellipse_bunch":
                self.draw_ellipse_bunch(position._data[i]["center"], position._data[i]["min_radius_x"], position._data[i]["max_radius_x"], \
                                        position._data[i]["min_radius_y"], position._data[i]["max_radius_y"], \
                                        position._data[i]["ellipse_amount"], position._data[i]["mod"], position._data[i]["color"], f"ellipse_bunch_{i}")

    # lab_03
    def pri_pix(self, x, y, color, tag):
        self.create_polygon([x, y], [x + 1, y], [x + 1, y + 1], [x, y + 1], fill=color, tag=tag)


    def draw_line(self, a, b, mod, color, tag):
        a_converted = self.vector2canvasCoordinates(a)
        b_converted = self.vector2canvasCoordinates(b)

        if a_converted == b_converted:
            self.pri_pix(a_converted.x, a_converted.y, color, tag)
            return

        # default
        self.create_line(a_converted.x, a_converted.y, b_converted.x, b_converted.y, fill=color, tag=tag)

    def draw_circle(self, center, radius, mod, color, tag):
        center_converted = self.vector2canvasCoordinates(center)
        temp = self.vector2canvasCoordinates(Vector(center.x + radius, center.y))
        r = abs(center_converted - temp)

        if radius == 0:
            self.pri_pix(center.x, center.y, color, tag)
            return None

        functions = [
            canonical_equation_circle,
            parametric_equation_circle,
            bresenham_circle,
            middle_dot_circle,
        ]

        x = center_converted.x
        y = center_converted.y

        answer = None

        if mod == 0:
            # default
            self.create_oval(x - r, y - r, x + r, y + r, outline=color, tag=tag)

            return answer

        elif mod in range(1, 5):
            data = functions[mod - 1](center_converted, r, color, tag)

            if data is not None:
                for i in range(0, len(data), 3):
                    for j in range(len(data[0])):
                        self.pri_pix(data[i][j].x, data[i][j].y, data[i + 1][j], data[i + 2][j])

            return answer

        else:
            return answer


    def draw_ellipse(self, center, x_radius, y_radius, mod, color, tag):
        center_converted = self.vector2canvasCoordinates(center)
        temp = self.vector2canvasCoordinates(Vector(center.x + x_radius, center.y))
        r_x = abs(center_converted - temp)
        temp = self.vector2canvasCoordinates(Vector(center.x, center.y + y_radius))
        r_y = abs(center_converted - temp)

        functions = [
            canonical_equation_ellipse,
            parametric_equation_ellipse,
            bresenham_ellipse,
            middle_dot_ellipse,
        ]

        x = center_converted.x
        y = center_converted.y

        answer = None

        if mod == 0:
            # default
            self.create_oval(x - r_x, y - r_y, x + r_x, y + r_y, outline=color, tag=tag)

            return answer

        elif mod in range(1, 5):
            data = functions[mod - 1](center_converted, r_x, r_y, color, tag)

            if data is not None:
                for i in range(0, len(data), 3):
                    for j in range(len(data[0])):
                        self.pri_pix(data[i][j].x, data[i][j].y, data[i + 1][j], data[i + 2][j])

            return answer

        else:
            return answer

    def draw_circle_bunch(self, center, min_radius, max_radius, circle_amount, mod, color, tag):
        r = min_radius
        dr = (max_radius - min_radius) / (circle_amount - 1)

        for i in range(circle_amount):
            self.draw_circle(center, r, mod, color, tag)

            r += dr

    def draw_ellipse_bunch(self, center, min_radius_x, max_radius_x, min_radius_y, max_radius_y, ellipse_amount, mod, color, tag):
        rx = min_radius_x
        drx = (max_radius_x - min_radius_x) / (ellipse_amount - 1)
        ry = min_radius_y
        dry = (max_radius_y - min_radius_y) / (ellipse_amount - 1)

        for i in range(ellipse_amount):
            self.draw_ellipse(center, rx, ry, mod, color, tag)

            rx += drx
            ry += dry
