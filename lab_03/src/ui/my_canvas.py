from tkinter import Canvas
from math import fabs

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector

from src.cadre import Cadre


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

        print("not finished yet")

    # lab_03

    def draw_line(self, a, b, mod, color, tag):  # todo
        a_converted = self.vector2canvasCoordinates(a)
        b_converted = self.vector2canvasCoordinates(b)

        print(color)

        if mod == 0:
            # default
            self.create_line(a_converted.x, a_converted.y, b_converted.x, b_converted.y, fill=color, tag=tag)

        elif mod == 1:
            # dda mode
            self.__dda_line(a_converted, b_converted, outline=color, tag=tag)

        elif mod == 2:
            # bresenham
            self.__bresenham_line(a_converted, b_converted, outline=color, tag=tag)

        elif mod == 3:
            # int bresenham
            self.__int_bresenham_line(a_converted, b_converted, outline=color, tag=tag)

        elif mod == 4:
            # no angle bresenham
            self.__no_angle_bresenham_line(a_converted, b_converted, outline=color, tag=tag)

        else:
            print("mod error")
            return NotImplemented

    def __dda_line(self, start, finish, outline="darkred", tag="None"):
        if isinstance(start, Vector) and isinstance(finish, Vector):
            x = start.x
            y = start.y

            self.create_oval(x - self.settings.pixel_radius,
                             y - self.settings.pixel_radius,
                             x + self.settings.pixel_radius,
                             y + self.settings.pixel_radius,
                             outline=outline,
                             tag=tag)

            l = max(abs(finish.x - start.x), abs(finish.y - start.y)) + 1

            for i in range(int(l)):
                x += (finish.x - start.x) / l
                y += (finish.y - start.y) / l

                self.create_oval(x - self.settings.pixel_radius,
                                 y - self.settings.pixel_radius,
                                 x + self.settings.pixel_radius,
                                 y + self.settings.pixel_radius,
                                 outline=outline,
                                 tag=tag)

        else:
            return NotImplemented

    def __bresenham_line(self, start, finish, outline="darkred", tag="None"):
        if isinstance(start, Vector) and isinstance(finish, Vector):
            x0, x1 = start.x, finish.x
            y0, y1 = start.y, finish.y

            delta_x = abs(x1 - x0)
            delta_y = abs(y1 - y0)

            error = 0.0

            dir_y = 1 if y1 - y0 > 0 else -1
            dir_x = 1 if x1 - x0 > 0 else -1

            if abs(x1 - x0) > abs(y1 - y0):
                delta_err = (delta_y + 1) / (delta_x + 1)
                y = y0

                for x in range(int(x0), int(x1) + 1, dir_x):
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)

                    error = error + delta_err
                    if error >= 1.0:
                        y += dir_y
                        error = error - 1.0

            else:
                delta_err = (delta_x + 1) / (delta_y + 1)
                x = x0

                for y in range(int(y0), int(y1) + 1, dir_y):
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)

                    error = error + delta_err
                    if error >= 1.0:
                        x += dir_x
                        error = error - 1.0

        else:
            return NotImplemented

    def __int_bresenham_line(self, start, finish, outline="darkred", tag="None"):
        if isinstance(start, Vector) and isinstance(finish, Vector):
            x0, x1 = start.x, finish.x
            y0, y1 = start.y, finish.y

            delta_x = abs(x1 - x0)
            delta_y = abs(y1 - y0)

            error = 0.0

            dir_y = 1 if y1 - y0 > 0 else -1
            dir_x = 1 if x1 - x0 > 0 else -1

            if abs(x1 - x0) > abs(y1 - y0):
                delta_err = (delta_y + 1)
                y = y0

                for x in range(int(x0), int(x1) + 1, dir_x):
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)

                    error = error + delta_err
                    if error >= (delta_x + 1):
                        y += dir_y
                        error = error - (delta_x + 1)

            else:
                delta_err = (delta_x + 1)
                x = x0

                for y in range(int(y0), int(y1) + 1, dir_y):
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)

                    error = error + delta_err
                    if error >= (delta_y + 1):
                        x += dir_x
                        error = error - (delta_y + 1)

        else:
            return NotImplemented

    def __no_angle_bresenham_line(self, start, finish, outline="darkred", tag="None"):
        if isinstance(start, Vector) and isinstance(finish, Vector):
            x0, x1 = start.x, finish.x
            y0, y1 = start.y, finish.y
            i = 2
            x = x0
            y = y0
            delta_x = x1 - x0
            delta_y = y1 - y0
            e = 1 / 2
            dir_y = 1 if y1 - y0 > 0 else -1
            dir_x = 1 if x1 - x0 > 0 else -1

            if abs(x1 - x0) > abs(y1 - y0):
                m = abs((i * delta_y) / delta_x)
                w = i - m
                self.create_oval(x - self.settings.pixel_radius,
                                 y - self.settings.pixel_radius,
                                 x + self.settings.pixel_radius,
                                 y + self.settings.pixel_radius,
                                 outline=outline,
                                 tag=tag)
                for x in range(int(x0), int(x1) + 1, dir_x):
                    if e < w:
                        x = x + dir_x
                        e = e + m
                    else:
                        x = x + dir_x
                        y = y + dir_y
                        e = e - w
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)
            else:
                print("second")
                m = abs((i * delta_x) / delta_y)
                w = i - m
                self.create_oval(x - self.settings.pixel_radius,
                                 y - self.settings.pixel_radius,
                                 x + self.settings.pixel_radius,
                                 y + self.settings.pixel_radius,
                                 outline=outline,
                                 tag=tag)
                for y in range(int(y0), int(y1) + 1, dir_y):
                    if e < w:
                        y += dir_y
                        e += m
                    else:
                        y += dir_y
                        x += dir_x
                        e -= w
                    self.create_oval(x - self.settings.pixel_radius,
                                     y - self.settings.pixel_radius,
                                     x + self.settings.pixel_radius,
                                     y + self.settings.pixel_radius,
                                     outline=outline,
                                     tag=tag)

        else:
            return NotImplemented

    def __wu_line(self, start, finish, outline="darkred", tag="None"):
        if isinstance(start, Vector) and isinstance(finish, Vector):
            pass
        else:
            return NotImplemented
