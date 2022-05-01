from src.calculations.lines import line, line1, line2
from src.vector import Vector
from math import floor, ceil
from src.utils.decorators import calculate_time


class Figure:
    def __init__(self, canvas, **kwargs):
        self.canvas = canvas

        self.finished = False if 'finished' not in kwargs else kwargs['finished']
        self.tag = 'default' if 'tag' not in kwargs else kwargs['tag']
        self.erase = False if 'erase' not in kwargs else kwargs['erase']
        self.fill = 'pink' if 'fill' not in kwargs else kwargs['fill']
        self.dots = [] if 'dots' not in kwargs else kwargs['dots']
        self.type = 'None' if 'type' not in kwargs else kwargs['type']
        self.init_coordinate = Vector(0, 0) if 'init_coordinate' not in kwargs else kwargs['init_coordinate']
        self.circuit_color = self.canvas.line_color if 'circuit_color' not in kwargs else kwargs['circuit_color']
        self.last_time = 0

    def merge_and_draw(self, **kwargs):
        # self.along_ribs(**kwargs)
        answer = self.line_seeding(**kwargs)
        self.last_time = answer[-1]
        print(answer[-1])

    @calculate_time
    def line_seeding(self, **kwargs):
        step_by_step = False if 'step_by_step' not in kwargs else kwargs['step_by_step']
        # step_by_step = True

        if not self.finished:
            figure_sides = [[self.dots[i], self.dots[i+1]] for i in range(len(self.dots) - 1)]
            for side in figure_sides:
                self.canvas.draw_line(side[0], side[1], fill=self.canvas.line_color, tag=self.tag, width=self.canvas.line_width)

            return

        canvas_pixel = self.canvas.vector2canvasCoordinates(self.init_coordinate)

        stack = [canvas_pixel]
        matrix = [[None for _ in range(self.canvas.winfo_height())] for _ in range(self.canvas.winfo_width())]
        figure_sides = [(self.dots[i], self.dots[i + 1]) for i in range(-1, len(self.dots) - 1, 1)]

        for fs in figure_sides:
            start = self.canvas.vector2canvasCoordinates(fs[0])
            finish = self.canvas.vector2canvasCoordinates(fs[1])

            x_arr, y_arr = line2(start, finish)
            for x, y in zip(map(int, x_arr), map(int, y_arr)):
                # matrix[x][y] = self.circuit_color
                for i in range(3):
                    for j in range(3):
                        matrix[x+i][y+j] = self.circuit_color

                        if step_by_step or self.erase:
                            self.canvas.pri_pix(x + i, y + j, fill=self.circuit_color, tag=self.tag)

        if step_by_step:
            self.canvas.update()

        x_max = len(matrix)
        x_min = 0
        y_max = len(matrix[0])
        y_min = 0

        while stack:
            # print('stack len', len(stack))
            canvas_pixel = stack.pop()

            x, y = int(canvas_pixel.x), int(canvas_pixel.y)
            if matrix[x][y] == self.fill:
                continue

            while x < x_max and matrix[x][y] != self.circuit_color:
                matrix[x][y] = self.fill

                if step_by_step:
                    if self.erase:
                        color = self.canvas.bg_color if matrix[x][y] == self.fill else self.canvas.matrix[x][y]
                    else:
                        color = matrix[x][y] if matrix[x][y] is not None else self.canvas.matrix[x][y]

                    self.canvas.pri_pix(x, y, fill=color, tag=self.tag)

                if x == x_max - 1 or matrix[x + 1][y] == self.circuit_color:
                    if y < y_max - 1:
                        if matrix[x][y + 1] not in [self.fill, self.circuit_color]:
                            stack.append(Vector(x, y + 1))
                    if y > y_min:
                        if matrix[x][y - 1] not in [self.fill, self.circuit_color]:
                            stack.append(Vector(x, y - 1))

                else:
                    if y < y_max - 1:
                        if matrix[x + 1][y + 1] == self.circuit_color:
                            stack.append(Vector(x, y + 1))
                    if y > y_min:
                        if matrix[x + 1][y - 1] == self.circuit_color:
                            stack.append(Vector(x, y - 1))

                x += 1

            x, y = int(canvas_pixel.x) - 1, int(canvas_pixel.y)
            while x >= x_min and matrix[x][y] != self.circuit_color:
                matrix[x][y] = self.fill

                if step_by_step:
                    if self.erase:
                        color = self.canvas.bg_color if matrix[x][y] == self.fill else self.canvas.matrix[x][y]
                    else:
                        color = matrix[x][y] if matrix[x][y] is not None else self.canvas.matrix[x][y]

                    self.canvas.pri_pix(x, y, fill=color, tag=self.tag)

                if y < y_max - 1:
                    if matrix[x + 1][y + 1] == self.circuit_color and matrix[x][y + 1] not in [self.fill, self.circuit_color]:
                        stack.append(Vector(x, y + 1))
                if y > y_min:
                    if matrix[x + 1][y - 1] == self.circuit_color and matrix[x][y - 1] not in [self.fill, self.circuit_color]:
                        stack.append(Vector(x, y - 1))

                x -= 1

            if step_by_step:
                self.canvas.update()

        for xi in range(len(matrix)):
            for yi in range(len(matrix[0])):
                if self.erase:
                    color = self.canvas.bg_color if matrix[xi][yi] is not None and matrix[xi][yi] != self.circuit_color else self.canvas.matrix[xi][yi]
                    self.canvas.matrix[xi][yi] = color
                else:
                    color = matrix[xi][yi] if matrix[xi][yi] is not None else self.canvas.matrix[xi][yi]
                    self.canvas.matrix[xi][yi] = color

                if color is not None and not step_by_step:
                    self.canvas.pri_pix(xi, yi, fill=color, tag=self.tag)

    def along_ribs(self, **kwargs):
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
