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
        self.lines_with_cutter(**kwargs)

    def lines_with_cutter(self, **kwargs):
        if self.finished:
            eps = 1e-6

            a = self.dots[0]
            b = self.dots[1]

            print('a: ', a)
            print('b: ', b)

            r0, r1 = None, None
            q = None
            i = None

            kwgs = {
                'fill': self.fill,
                'tag': self.tag,
                'width': self.canvas.line_width,
            }

            if self.canvas.cutter is None:
                print('no cutter - skip')
                self.canvas.draw_line(a, b, **kwgs)

                return

            x_left, y_bottom = self.canvas.cutter.start.x, self.canvas.cutter.start.y
            x_right, y_top = self.canvas.cutter.finish.x, self.canvas.cutter.finish.y

            print('x_left', x_left)
            print('x_right', x_right)
            print('y_bottom', y_bottom)
            print('y_top', y_top)


            x0, y0 = a.x, a.y
            x1, y1 = b.x, b.y

            t0 = [x0 < x_left, x0 > x_right, y0 < y_bottom, y0 > y_top]
            print(t0)
            t1 = [x1 < x_left, x1 > x_right, y1 < y_bottom, y1 > y_top]
            print(t1)

            s0 = bool(sum(t0))
            s1 = bool(sum(t1))

            print('s0: ', s0, '\ns1: ', s1)

            pr = True
            m = 1e30

            if not (s0 or s1):
                print('both sides in cutter')

                r0 = Vector(x0, y0)
                r1 = Vector(x1, y1)

                self.canvas.draw_line(r0, r1, **kwgs)

                return

            # p = bool(sum([t0[i] * t1[i] for i in range(4)]))
            # if not p:
            #     print('p - 0 => pr = False')
            #     pr = False
            #
            #     return

            if not s0:
                print('s0 visible')

                r0 = a
                q = b
                i = 2

            if not s1:
                print('s1 visible')

                r0 = b
                q = a
                # a, b = b, a
                i = 2

            if i is None:
                print('both sides not visible')

                i = 0

            while i <= 2:
                print('------------------------------------------')
                i += 1

                if q is None:
                    if i == 1:
                        print('q = a')
                        q = a
                    else:
                        print('q = b')
                        q = b

                # i += 1

                if a.x == b.x:
                    if abs(m) < eps:
                        print('ort1')

                        continue

                if a.x != b.x:
                    m = (y1 - y0) / (x1 - x0)

                if q.x > x_left:
                    if q.x < x_right:
                        if abs(m) < eps:
                            print('idk')
                            continue

                y_p = m * (x_left - q.x) + q.y

                if y_bottom <= y_p <= y_top and q.x <= x_left:
                    print('приклеиваю к левой стороне')
                    if r0 is None:
                        r0 = Vector(x_left, y_p)
                    elif r1 is None:
                        r1 = Vector(x_left, y_p)
                    q = None

                    continue

                if q.x < x_right:
                    if abs(m) < eps:
                        continue

                y_p = m * (x_right - q.x) + q.y

                if y_bottom <= y_p <= y_top and q.x >= x_right:
                    print('приклеиваю к правой стороне')

                    if r0 is None:
                        r0 = Vector(x_right, y_p)
                    elif r1 is None:
                        r1 = Vector(x_right, y_p)
                    q = None

                    continue

                if abs(m) < eps:
                    continue

                if q.y < y_top:
                    if q.y > y_bottom:
                        print('pr - False')

                        pr = False

                x_p = (y_top - q.y) / m + q.x

                if x_left <= x_p <= x_right and q.y >= y_top:
                    print('приклеиваю к верхней стороне')

                    if r0 is None:
                        r0 = Vector(x_p, y_top)
                    elif r1 is None:
                        r1 = Vector(x_p, y_top)
                    q = None

                    continue

                if q.y > y_bottom:
                    print('pr - False')
                    pr = False

                x_p = (y_bottom - q.y) / m + q.x

                print('???', x_left, x_p, x_right)

                if x_left <= x_p <= x_right and q.y <= y_bottom:
                    print('приклеиваю к нижней стороне')

                    if r0 is None:
                        r0 = Vector(x_p, y_bottom)
                    elif r1 is None:
                        r1 = Vector(x_p, y_bottom)
                    q = None

                    continue

                pr = False

            self.canvas.draw_line(a, b, **kwgs, dash=(1, 10))

            if pr and r0 is not None and r1 is not None:
                print('Отрисовка')
                self.canvas.draw_line(r0, r1, **kwgs)
