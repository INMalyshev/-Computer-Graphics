from src.ui.my_canvas import MyCanvas
from src.field import Field
from src.vector import Vector


class MyLabCanvas(MyCanvas):
    def __init__(self, parent):
        super(MyLabCanvas, self).__init__(parent)

        self.line_width = parent.line_width
        self.line_color = parent.line_color
        self.circuit_color = parent.circuit_color

        self.cutter = Field(Vector(-20, -20), Vector(20, 20))

    def change_cutter(self, cutter):
        self.cutter = cutter

    def change_line_color(self, color):
        if color is not None:
            self.line_color = color

    def draw_cutter(self):
        if self.cutter is not None:
            d1 = self.cutter.start
            d3 = self.cutter.finish
            d2 = Vector(d1.x, d3.y)
            d4 = Vector(d3.x, d1.y)

            kwgs = {
                'fill': self.circuit_color,
                'tag': 'cutter',
                'width': self.line_width,
            }

            self.draw_line(d1, d2, **kwgs)
            self.draw_line(d2, d3, **kwgs)
            self.draw_line(d3, d4, **kwgs)
            self.draw_line(d4, d1, **kwgs)

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
