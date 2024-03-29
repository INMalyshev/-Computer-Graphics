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
        # self.lines_with_cutter(**kwargs)
        self.lab_09(**kwargs)

    def lab_09(self, **kwargs):
        kwgs = {
            'fill': self.canvas.circuit_color if not self.finished else self.fill,
            'tag': self.tag,
            'width': self.canvas.line_width,
        }

        if self.canvas.cutter is None or not self.finished:
            for i in range(len(self.dots) - 1):
                self.canvas.draw_line(self.dots[i], self.dots[i+1], **kwgs)
            if self.finished:
                self.canvas.draw_line(self.dots[-1], self.dots[0], **kwgs)
            print('skip')
            return

        for i in range(-1, len(self.dots) - 1, 1):
            self.canvas.draw_line(self.dots[i], self.dots[i + 1], **kwgs, dash=(2, 10))

        ################################################################################################################

        def get_vect(dot_start, dot_end):
            return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]

        def get_vect_mul(fvector, svector):
            return fvector[0] * svector[1] - fvector[1] * svector[0]

        def get_scalar_mul(fvector, svector):
            return fvector[0] * svector[0] + fvector[1] * svector[1]

        def isCutterConvex(cutter):
            PosAngle = False
            NegAngle = False
            for i in range(len(cutter)):
                x1 = cutter[i][0]
                y1 = cutter[i][1]
                x2 = cutter[(i + 1) % len(cutter)][0]
                y2 = cutter[(i + 1) % len(cutter)][1]
                x3 = cutter[(i + 2) % len(cutter)][0]
                y3 = cutter[(i + 2) % len(cutter)][1]
                d = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
                if d > 0:
                    PosAngle = True
                elif d < 0:
                    NegAngle = True

            if PosAngle and NegAngle:
                return False
            else:
                return True

        def get_normal(dot_start, dot_end, dot_check):
            vect = get_vect(dot_start, dot_end)
            normal = None

            if vect[0] == 0:
                normal = [1, 0]
            else:
                normal = [-vect[1] / vect[0], 1]

            if get_scalar_mul(get_vect(dot_end, dot_check), normal) < 0:
                for i in range(len(normal)):
                    normal[i] = -normal[i]

            return normal

        def is_visible(dot, f_dot, s_dot, other):
            vec1 = get_vect(f_dot, dot)
            normal = get_normal(f_dot, s_dot, other)
            scal_pr = get_scalar_mul(normal, vec1)

            if scal_pr > 0:
                return True
            else:
                return False

        X_DOT = 0
        Y_DOT = 1

        def get_lines_parametric_intersec(line1, line2, normal):
            d = get_vect(line1[0], line1[1])
            w = get_vect(line2[0], line1[0])

            d_scalar = get_scalar_mul(d, normal)
            w_scalar = get_scalar_mul(w, normal)

            t = -w_scalar / d_scalar

            dot_intersec = [line1[0][X_DOT] + d[0] * t, line1[0][Y_DOT] + d[1] * t]

            return dot_intersec

        def sutherland_hodgman_algorythm(cutter_line, dot3, position, prev_result):
            cur_result = []

            dot1 = cutter_line[0]
            dot2 = cutter_line[1]

            normal = get_normal(dot1, dot2, position)

            prev_vision = is_visible(prev_result[-2], dot1, dot2, dot3)

            for cur_dot_index in range(-1, len(prev_result)):
                cur_vision = is_visible(prev_result[cur_dot_index], dot1, dot2, dot3)

                if (prev_vision):
                    if (cur_vision):
                        cur_result.append(prev_result[cur_dot_index])
                    else:
                        figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                        cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))
                else:
                    if (cur_vision):
                        figure_line = [prev_result[cur_dot_index - 1], prev_result[cur_dot_index]]

                        cur_result.append(get_lines_parametric_intersec(figure_line, cutter_line, normal))

                        cur_result.append(prev_result[cur_dot_index])

                prev_vision = cur_vision

            return cur_result

        def cut_area(cutter, figure):
            if (len(cutter) < 3):
                # messagebox.showinfo("Ошибка", "Не задан отсекатель")
                return

            if (not isCutterConvex(cutter)):
                # messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
                print('cutter error')
                return

            result = figure.copy()

            for cur_dot_ind in range(-1, len(cutter) - 1):
                line = [cutter[cur_dot_ind], cutter[cur_dot_ind + 1]]

                position_dot = cutter[cur_dot_ind + 1]

                result = sutherland_hodgman_algorythm(line, cutter[(cur_dot_ind + 2) % len(cutter)], position_dot,
                                                      result)

                if (len(result) <= 2):
                    return

            return result

        ################################################################################################################

        c = []
        for v in self.canvas.cutter:
            vv = self.canvas.vector2canvasCoordinates(v)
            c.append((vv.x, vv.y))

        f = []
        for v in self.dots:
            vv = self.canvas.vector2canvasCoordinates(v)
            f.append((vv.x, vv.y))


        c = [(v.x, v.y) for v in self.canvas.cutter]
        f = [(v.x, v.y) for v in self.dots]

        r = cut_area(c, f)
        area = [Vector(v[0], v[1]) for v in r]

        for i in range(-1, len(area) - 1, 1):
            self.canvas.draw_line(area[i], area[i + 1], **kwgs)

