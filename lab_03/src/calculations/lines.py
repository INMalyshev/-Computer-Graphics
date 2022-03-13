from math import modf, floor
from colorsys import rgb_to_hsv, hsv_to_rgb

from src.vector import Vector

def dda_line(start, finish, outline="darkred", tag="None"):
    if isinstance(start, Vector) and isinstance(finish, Vector):
        x = start.x
        y = start.y

        x_arr = [floor(x)]
        y_arr = [floor(y)]
        color_arr = [outline]
        tag_arr = [tag]

        l = max(abs(finish.x - start.x), abs(finish.y - start.y)) + 1

        for i in range(int(l)):
            x += (finish.x - start.x) / l
            y += (finish.y - start.y) / l

            x_arr.append(floor(x))
            y_arr.append(floor(y))
            color_arr.append(outline)
            tag_arr.append(tag)

        return x_arr, y_arr, color_arr, tag_arr

    else:
        print('---> something wrong with __dda_line method')
        return None

def bresenham_line(start, finish, outline="darkred", tag="None"):
    if isinstance(start, Vector) and isinstance(finish, Vector):
        x0, x1 = start.x, finish.x
        y0, y1 = start.y, finish.y

        delta_x = abs(x1 - x0)
        delta_y = abs(y1 - y0)

        error = 0.0

        dir_y = 1 if y1 - y0 > 0 else -1
        dir_x = 1 if x1 - x0 > 0 else -1

        x_arr = []
        y_arr = []
        color_arr = []
        tag_arr = []

        if abs(x1 - x0) > abs(y1 - y0):
            delta_err = (delta_y + 1) / (delta_x + 1)
            y = y0

            for x in range(int(x0), int(x1) + 1, dir_x):
                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(outline)
                tag_arr.append(tag)

                error = error + delta_err
                if error >= 1.0:
                    y += dir_y
                    error = error - 1.0

        else:
            delta_err = (delta_x + 1) / (delta_y + 1)
            x = x0

            for y in range(int(y0), int(y1) + 1, dir_y):
                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(outline)
                tag_arr.append(tag)

                error = error + delta_err
                if error >= 1.0:
                    x += dir_x
                    error = error - 1.0

        return x_arr, y_arr, color_arr, tag_arr

    else:
        print('---> something wrong with __bresenham_line method')
        return None

def int_bresenham_line(start, finish, outline="darkred", tag="None"):
    if isinstance(start, Vector) and isinstance(finish, Vector):
        x0, x1 = start.x, finish.x
        y0, y1 = start.y, finish.y

        delta_x = abs(x1 - x0)
        delta_y = abs(y1 - y0)

        error = 0.0

        dir_y = 1 if y1 - y0 > 0 else -1
        dir_x = 1 if x1 - x0 > 0 else -1

        x_arr = []
        y_arr = []
        color_arr = []
        tag_arr = []

        if abs(x1 - x0) > abs(y1 - y0):
            delta_err = (delta_y + 1)
            y = y0

            for x in range(int(x0), int(x1) + 1, dir_x):
                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(outline)
                tag_arr.append(tag)

                error = error + delta_err
                if error >= (delta_x + 1):
                    y += dir_y
                    error = error - (delta_x + 1)

        else:
            delta_err = (delta_x + 1)
            x = x0

            for y in range(int(y0), int(y1) + 1, dir_y):
                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(outline)
                tag_arr.append(tag)

                error = error + delta_err
                if error >= (delta_y + 1):
                    x += dir_x
                    error = error - (delta_y + 1)

        return x_arr, y_arr, color_arr, tag_arr

    else:
        print('---> something wrong with __int_bresenham_line method')
        return None

def no_angle_bresenham_line(start, finish, outline="darkred", tag="None"):
    if isinstance(start, Vector) and isinstance(finish, Vector):
        de = 0.3

        x0, x1 = start.x, finish.x
        y0, y1 = start.y, finish.y
        i = 2
        x = x0
        y = y0
        delta_x = x1 - x0
        delta_y = y1 - y0
        e = 1 / 2
        dir_y = 1 if y1 - y0 > 0 else -1
        dir_x = 1 if x1 - x0 > 0 else -1

        x_arr = []
        y_arr = []
        color_arr = []
        tag_arr = []

        if abs(x1 - x0) > abs(y1 - y0):
            m = abs((i * delta_y) / delta_x)
            w = i - m

            x_arr.append(floor(x))
            y_arr.append(floor(y))
            color_arr.append(___change_color(outline, modf(m / 2)[0]))
            tag_arr.append(tag)

            for x in range(int(x0), int(x1) + 1, dir_x):
                if e < w:
                    x = x + dir_x
                    e = e + m
                else:
                    x = x + dir_x
                    y = y + dir_y
                    e = e - w

                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(___change_color(outline, modf(e)[0]))
                tag_arr.append(tag)
        else:
            m = abs((i * delta_x) / delta_y)
            w = i - m

            x_arr.append(floor(x))
            y_arr.append(floor(y))
            color_arr.append(___change_color(outline, modf(m / 2)[0]))
            tag_arr.append(tag)

            for y in range(int(y0), int(y1) + 1, dir_y):
                if e < w:
                    y += dir_y
                    e += m
                else:
                    y += dir_y
                    x += dir_x
                    e -= w

                x_arr.append(floor(x))
                y_arr.append(floor(y))
                color_arr.append(___change_color(outline, modf(e)[0]))
                tag_arr.append(tag)

        return x_arr, y_arr, color_arr, tag_arr

    else:
        print('---> something wrong with __no_angle_bresenham_line method')
        return None

def wu_line(start, finish, outline="darkred", tag="None"):
    if isinstance(start, Vector) and isinstance(finish, Vector):
        x0, x1 = start.x, finish.x
        y0, y1 = start.y, finish.y

        x_up_arr = []
        y_up_arr = []
        color_up_arr = []
        tag_up_arr = []

        x_down_arr = []
        y_down_arr = []
        color_down_arr = []
        tag_down_arr = []

        if abs(x1 - x0) > abs(y1 - y0):
            if x1 < x0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            delta_x = x1 - x0
            delta_y = y1 - y0
            gradient = delta_y / delta_x

            # обработать начальную точку

            x_end = round(x0)
            y_end = y0 + gradient * (x_end - x0)

            x_gap = 1 - modf((x0 + 0.5))[0]
            x_pxl1 = x_end

            y_pxl1 = modf(y_end)[1]

            x_up_arr.append(floor(x_pxl1))
            y_up_arr.append(floor(y_pxl1))
            color_up_arr.append(___change_color(outline, (1 - modf(y_end)[0]) * x_gap))
            tag_up_arr.append(tag)

            x_down_arr.append(floor(x_pxl1))
            y_down_arr.append(floor(y_pxl1 + 1))
            color_down_arr.append(___change_color(outline, modf(y_end)[0] * x_gap))
            tag_down_arr.append(tag)

            inter_y = y_end + gradient # первое y - пересечение дл цикла

            # обработать конечную точку

            x_end = round(x1)
            y_end = y1 + gradient * (x_end - x1)
            x_gap = modf(x1 + 0.5)[0]
            x_pxl2 = x_end
            y_pxl2 = modf(y_end)[1]

            x_up_arr.append(floor(x_pxl2))
            y_up_arr.append(floor(y_pxl2))
            color_up_arr.append(___change_color(outline, (1 - modf(y_end)[0]) * x_gap))
            tag_up_arr.append(tag)

            x_down_arr.append(floor(x_pxl2))
            y_down_arr.append(floor(y_pxl2 + 1))
            color_down_arr.append(___change_color(outline, modf(y_end)[0] * x_gap))
            tag_down_arr.append(tag)

            # основной цикл
            for x in range(x_pxl1, x_pxl2 + 1):
                x_up_arr.append(floor(x))
                y_up_arr.append(floor(modf(inter_y)[1]))
                color_up_arr.append(___change_color(outline, 1 - modf(inter_y)[0]))
                tag_up_arr.append(tag)

                x_down_arr.append(floor(x))
                y_down_arr.append(floor(modf(inter_y)[1] + 1))
                color_down_arr.append(___change_color(outline, modf(inter_y)[0]))
                tag_down_arr.append(tag)

                inter_y = inter_y + gradient

        else:
            if y1 < y0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            delta_x = x1 - x0
            delta_y = y1 - y0
            gradient = delta_x / delta_y

            # обработать начальную точку

            y_end = round(y0)
            x_end = x0 + gradient * (y_end - y0)

            y_gap = 1 - modf((y0 + 0.5))[0]
            y_pxl1 = y_end

            x_pxl1 = modf(x_end)[1]

            x_up_arr.append(floor(x_pxl1))
            y_up_arr.append(floor(y_pxl1))
            color_up_arr.append(___change_color(outline, (1 - modf(x_end)[0]) * y_gap))
            tag_up_arr.append(tag)

            x_down_arr.append(floor(x_pxl1 + 1))
            y_down_arr.append(floor(y_pxl1))
            color_down_arr.append(___change_color(outline, modf(x_end)[0] * y_gap))
            tag_down_arr.append(tag)

            inter_x = x_end + gradient # первое y - пересечение дл цикла

            # обработать конечную точку

            y_end = round(y1)
            x_end = x1 + gradient * (y_end - y1)
            y_gap = modf(y1 + 0.5)[0]
            y_pxl2 = y_end
            x_pxl2 = modf(x_end)[1]

            x_up_arr.append(floor(x_pxl2))
            y_up_arr.append(floor(y_pxl2))
            color_up_arr.append(___change_color(outline, (1 - modf(x_end)[0]) * y_gap))
            tag_up_arr.append(tag)

            x_down_arr.append(floor(x_pxl2 + 1))
            y_down_arr.append(floor(y_pxl2))
            color_down_arr.append(___change_color(outline, modf(x_end)[0] * y_gap))
            tag_down_arr.append(tag)

            # основной цикл
            for y in range(y_pxl1, y_pxl2 + 1):
                x_up_arr.append(floor(modf(inter_x)[1]))
                y_up_arr.append(floor(y))
                color_up_arr.append(___change_color(outline, 1 - modf(inter_x)[0]))
                tag_up_arr.append(tag)

                x_down_arr.append(floor(modf(inter_x)[1] + 1))
                y_down_arr.append(floor(y))
                color_down_arr.append(___change_color(outline, modf(inter_x)[0]))
                tag_down_arr.append(tag)

                inter_x = inter_x + gradient

        return x_up_arr, y_up_arr, color_up_arr, tag_up_arr, x_down_arr, y_down_arr, color_down_arr, tag_down_arr

    else:
        print('---> something wrong with __no_angle_bresenham_line method')
        return None

def ___change_color(rgb, k):
    _rgb = rgb.strip("#")
    _r = _rgb[0:2]
    _g = _rgb[2:4]
    _b = _rgb[4:6]
    r = int(_r, 16)
    g = int(_g, 16)
    b = int(_b, 16)

    hsv = rgb_to_hsv(r, g, b)

    new_rgb = hsv_to_rgb(hsv[0], hsv[1] * k, hsv[2])

    rh = ('0' + str(hex(int(new_rgb[0]))[2:].upper()))[-2:]
    gh = ('0' + str(hex(int(new_rgb[1]))[2:].upper()))[-2:]
    bh = ('0' + str(hex(int(new_rgb[2]))[2:].upper()))[-2:]

    result = f"#{rh}{gh}{bh}"

    return result

def calculate_steps(data):
    if data is None:
        return None

    eps = 1e-3

    x_arr = data[0].copy()
    y_arr = data[1].copy()

    if abs(x_arr[-1] - x_arr[0]) < abs(y_arr[-1] - y_arr[0]):
        x_arr, y_arr = y_arr, x_arr

    def my_tan(x0, y0, x1, y1):
        k = 1000000000
        return ((y1 - y0) * k + 1) / ((x1 - x0) * k + 1)

    odds = [my_tan(x_arr[i-1], y_arr[i-1], x_arr[i], y_arr[i]) for i in range(1, len(x_arr))]

    step_amount = 0

    for i in range(1, len(odds)):
        if abs(odds[i-1] - odds[i]) > eps:
            step_amount += 1

    return step_amount // 2
