from src.ui.my_canvas import MyCanvas
from src.vector import Vector


class MyLabCanvas(MyCanvas):
    def __init__(self, parent):
        super(MyLabCanvas, self).__init__(parent)

        self.matrix = [[None for _ in range(self.winfo_height())] for _ in range(self.winfo_width())]
        self.bind('<Configure>', self.update_matrix, '+')

        self.line_width = parent.line_width
        self.line_color = parent.line_color
        self.fill_color = parent.fill_color

    def update_matrix(self, event=None):
        self.matrix = [[None for _ in range(self.winfo_height())] for _ in range(self.winfo_width())]

    def change_fill_color(self, color):
        if color is not None:
            self.fill_color = color

    def draw_x(self, a):
        x, y = a.x, a.y
        kwgs = {
            'fill': 'red',
            'tag': 'x',
            'width': 5,
        }

        d = 5
        dx = self.canvasDistance2distance(d)

        self.draw_line(Vector(x-dx, y-dx), Vector(x+dx, x+dx), **kwgs)
        self.draw_line(Vector(x-dx, y+dx), Vector(x+dx, x-dx), **kwgs)

    def set_position(self, data,  **kwargs):
        tag = None if 'tag' not in kwargs else kwargs['tag']

        if tag is not None:
            print('with tag')

            self.delete(tag)

            for fig in data:
                if fig.tag == tag:
                    fig.merge_and_draw(**kwargs)

            return

        self.delete("all")
        self.draw_cross()
        self.update_matrix()

        for fig in data:
            fig.merge_and_draw(**kwargs)
