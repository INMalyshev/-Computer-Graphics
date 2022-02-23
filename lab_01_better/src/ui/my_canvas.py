from tkinter import Canvas

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector
from src.position import Position

class MyCanvas(Canvas):
    def __init__(self, parent):
        self.settings = Settings()

        super(MyCanvas, self).__init__(
        parent,
        width=self.settings.ui.canvas.width,
        height=self.settings.ui.canvas.height,
        bg=self.settings.ui.canvas.bg,
        )

        self.field = Field(\
            Vector(self.settings.ui.canvas.field_start_x, self.settings.ui.canvas.field_start_y),\
            Vector(self.settings.ui.canvas.field_finish_x, self.settings.ui.canvas.field_finish_y)\
        )

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

    def draw_line(self, a, b):
        a_converted = self.vector2canvasCoordinates(a)
        b_converted = self.vector2canvasCoordinates(b)

        self.create_line(a_converted.x, a_converted.y, b_converted.x, b_converted.y)

    def draw_cross(self):
        if self.field.start.x < 0 and self.field.finish.x > 0:
            l2_start = Vector(0, self.field.start.y)
            l2_finish = Vector(0, self.field.finish.y)
            self.draw_line(l2_start, l2_finish)

        if self.field.start.y < 0 and self.field.finish.y > 0:
            l1_start = Vector(self.field.start.x, 0)
            l1_finish = Vector(self.field.finish.x, 0)
            self.draw_line(l1_start, l1_finish)

        # if self.field.include(Vector(0.0, 0.0)):
        #
        #     l1_start = Vector(self.field.start.x, 0)
        #     l1_finish = Vector(self.field.finish.x, 0)
        #
        #     l2_start = Vector(0, self.field.start.y)
        #     l2_finish = Vector(0, self.field.finish.y)
        #
        #     self.draw_line(l1_start, l1_finish)
        #     self.draw_line(l2_start, l2_finish)

    def draw_dot(self, vector):
        if not isinstance(vector, Vector):
            return NotImplemented

        if self.field.include(vector):
            converted = self.vector2canvasCoordinates(vector)
            self.create_oval(
                converted.x - self.settings.ui.dot.radius,
                converted.y - self.settings.ui.dot.radius,
                converted.x + self.settings.ui.dot.radius,
                converted.y + self.settings.ui.dot.radius,
                fill=self.settings.ui.dot.fill_color,
                tag=self.settings.ui.dot.tag,
            )

    def set_position(self, position):
        self.delete("all")

        self.draw_cross()

        if position is None:
            return

        if not isinstance(position, Position):
            return NotImplemented

        for dot in position.dots:
            if not isinstance(dot, Vector):
                return NotImplemented

            if self.field.include(dot):
                self.draw_dot(dot)

        if position.solution is True:
            self._draw_oval(position.circles[0], position.circles[1])
            self._draw_oval(position.circles[2], position.circles[3])

    def _draw_oval(self, center, radius):
        if not isinstance(center, Vector):
            return NotImplemented

        width = self.winfo_width()
        height = self.winfo_height()

        diagonal = self.field.finish - self.field.start

        kx = width / diagonal.x
        ky = height / diagonal.y

        converted = self.vector2canvasCoordinates(center)

        self.create_oval(
        converted.x - kx * radius,
        converted.y - ky * radius,
        converted.x + kx * radius,
        converted.y + ky * radius,
        )
