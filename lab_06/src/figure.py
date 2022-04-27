from src.calculations.lines import line


class Figure:
    def __init__(self, canvas, **kwargs):
        self.canvas = canvas

        self.finished = False if 'finished' not in kwargs else kwargs['finished']
        self.tag = 'default' if 'tag' not in kwargs else kwargs['tag']
        self.erase = False if 'erase' not in kwargs else kwargs['erase']
        self.fill = 'pink' if 'fill' not in kwargs else kwargs['fill']
        self.dots = [] if 'dots' not in kwargs else kwargs['dots']
        self.type = 'polygon' if 'type' not in kwargs else kwargs['type']

    def merge_and_draw(self, **kwargs):
        step_by_step = False if 'step_by_step' not in kwargs else kwargs['step_by_step']
        # step_by_step = True

        if not self.finished:
            figure_sides = [[self.dots[i], self.dots[i+1]] for i in range(len(self.dots) - 1)]
            for side in figure_sides:
                self.canvas.draw_line(side[0], side[1], fill=self.canvas.line_color, tag=self.tag, width=self.canvas.line_width)

            return

        matrix = [[None for _ in range(self.canvas.winfo_height())] for _ in range(self.canvas.winfo_width())]

        right = self.dots[0].x

        for fd in self.dots:
            right = max(right, fd.x)

        cr = self.canvas.distance2canvasDistance(right - self.canvas.field.start.x)

        figure_sides = [(self.dots[i], self.dots[i + 1]) for i in range(-1, len(self.dots) - 1, 1)]

        for fs in figure_sides:
            start = self.canvas.vector2canvasCoordinates(fs[0])
            finish = self.canvas.vector2canvasCoordinates(fs[1])

            x_arr, y_arr = line(start, finish)

            if y_arr[-1] > y_arr[0]:
                y_arr.reverse()
                x_arr.reverse()

            for i in range(1, len(x_arr), 1):
                x, y = int(x_arr[i]), int(y_arr[i])

                if 0 <= y < self.canvas.winfo_height():
                    if x < 0:
                        x = 0

                    for dx in range(0, min(int(cr) - x, self.canvas.winfo_width() - x)):
                        if 0 < x + dx >= len(matrix) or 0 < y >= len(matrix[0]):
                            break

                        color = self.fill if matrix[x + dx][y] is None else None
                        matrix[x + dx][y] = color

                        if step_by_step:
                            color = self.canvas.bg_color if color is not None and self.erase else color if color is not None else self.canvas.bg_color
                            if color is not None:
                                self.canvas.pri_pix(x + dx, y, fill=color, tag=self.tag)

                    if step_by_step:
                        self.canvas.update()

        for xi in range(len(matrix)):
            for yi in range(len(matrix[0])):
                if self.erase:
                    color = self.canvas.bg_color if matrix[xi][yi] is not None else self.canvas.matrix[xi][yi]
                    self.canvas.matrix[xi][yi] = color
                else:
                    color = matrix[xi][yi] if matrix[xi][yi] is not None else self.canvas.matrix[xi][yi]
                    self.canvas.matrix[xi][yi] = color

                if color is not None and not step_by_step:
                    self.canvas.pri_pix(xi, yi, fill=color, tag=self.tag)

        # if not step_by_step:
            # self.canvas.update()
