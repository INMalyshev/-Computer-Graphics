from src.ui.my_canvas import MyCanvas


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
