from math import modf, floor, ceil
from colorsys import rgb_to_hsv, hsv_to_rgb

from src.vector import Vector


def line1(start, finish):
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

        if abs(x1 - x0) > abs(y1 - y0):
            delta_err = (delta_y + 1) / (delta_x + 1)
            y = y0

            for x in range(int(x0), int(x1) + 1, dir_x):
                x_arr.append(int(x))
                y_arr.append(int(y))

                error = error + delta_err
                if error >= 1.0:
                    y += dir_y
                    error = error - 1.0

        else:
            delta_err = (delta_x + 1) / (delta_y + 1)
            x = x0

            for y in range(int(y0), int(y1) + 1, dir_y):
                x_arr.append(int(x))
                y_arr.append(int(y))

                error = error + delta_err
                if error >= 1.0:
                    x += dir_x
                    error = error - 1.0

        rx = []
        ry = []
        ly = None
        for x, y in zip(x_arr, y_arr):
            if y != ly:
                ly = y
                rx.append(x)
                ry.append(y)

        # return x_arr, y_arr
        return rx, ry


def line(start, finish):
    x0, y0 = start.x, start.y
    x1, y1 = finish.x, finish.y

    n = int(abs(y1 - y0))

    if n == 0:
        return [min(x0, x1)], [y0]

    dx = (x1 - x0) / n
    dy = 1
    if y1 < y0:
        dy = -1

    x, y = x0, y0
    x_arr, y_arr = [x], [y]

    for _ in range(n):
        x += dx
        y += dy

        x_arr.append(x)
        y_arr.append(y)

    return x_arr, y_arr


