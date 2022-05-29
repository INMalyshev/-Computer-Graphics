from src.ui.my_canvas import MyCanvas
from src.field import Field
from src.vector import Vector


class MyLabCanvas(MyCanvas):
    def __init__(self, parent):
        super(MyLabCanvas, self).__init__(parent)

        self.line_width = parent.line_width
        self.line_color = parent.line_color
        self.circuit_color = parent.circuit_color

        self.cutter = None
        self.cutter_buffer = None
        # self.cutter = [
        #     Vector(40, 40),
        #     Vector(40, -40),
        #     # Vector(-40, -40),
        #     Vector(-40, 40),
        # ]

    def change_cutter(self, cutter):
        self.cutter = cutter

    def change_line_color(self, color):
        if color is not None:
            self.line_color = color

    def draw_cutter(self):
        kwgs = {
            'fill': self.circuit_color,
            'tag': 'cutter',
            'width': self.line_width,
        }

        if self.cutter is not None:
            for i in range(-1, len(self.cutter) - 1, 1):
                self.draw_line(self.cutter[i], self.cutter[i + 1], **kwgs)

        elif self.cutter_buffer is not None:
            for i in range(0, len(self.cutter_buffer) - 1, 1):
                self.draw_line(self.cutter_buffer[i], self.cutter_buffer[i + 1], **kwgs)

    def set_position(self, data,  **kwargs):
        tag = None if 'tag' not in kwargs else kwargs['tag']

        if tag is not None:
            # print('with tag')

            self.delete(tag)
            for fig in data:
                if fig.tag == tag:
                    fig.merge_and_draw(**kwargs)

        else:
            self.delete("all")
            self.draw_cross()
            self.draw_cutter()

            for fig in data:
                fig.merge_and_draw(**kwargs)
