from tkinter import Canvas

from src.settings.settings import Settings
from src.field import Field
from src.vector import Vector

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
            new_v1 = v2 + (d * 0.5)

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

    def draw_cross(self):
        if self.field.include(Vector(0.0, 0.0)):

            l1_start = Vector(self.field.start.x, 0)
            l1_finish = Vector(self.field.finish.x, 0)

            l2_start = Vector(0, self.field.start.y)
            l2_finish = Vector(0, self.field.finish.y)

            l1s_converted = self.vector2canvasCoordinates(l1_start)
            l1f_converted = self.vector2canvasCoordinates(l1_finish)

            l2s_converted = self.vector2canvasCoordinates(l2_start)
            l2f_converted = self.vector2canvasCoordinates(l2_finish)

            self.create_line(l1s_converted.x, l1s_converted.y, l1f_converted.x, l1f_converted.y)
            self.create_line(l2s_converted.x, l2s_converted.y, l2f_converted.x, l2f_converted.y)
