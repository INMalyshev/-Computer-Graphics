import math
from src.vector import Vector


def canonical_equation_ellipse(center, x_radius, y_radius, outline='darkred', tag='non'):   # gets canvas coordinates
    dots = []

    a = x_radius
    b = y_radius

    x = 0
    y = b

    el_tan = -(2 * b * b * x) / (2 * a * a * y)

    while el_tan > -1:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        x += 1
        y = math.sqrt(-(b * b * x * x - a * a * b * b) / (a * a))

        el_tan = -(2 * b * b * x) / (2 * a * a * y)

    while y >= 0:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        y -= 1
        x = math.sqrt(-(a * a * y * y - a * a * b * b) / (b * b))

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


def parametric_equation_ellipse(center, x_radius, y_radius, outline='darkred', tag='non'):
    phi = 0.0
    dphi = 1 / abs(max(x_radius, y_radius))

    dots = []

    while phi < 2 * math.pi:
        x = x_radius * math.cos(phi)
        y = y_radius * math.sin(phi)
        dots.append(center + Vector(x, y))
        phi += dphi

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


def bresenham_ellipse(center, x_radius, y_radius, outline='darkred', tag='non'):
    eps = 2

    a = x_radius
    b = y_radius

    x = 0
    y = b

    dots = []

    while y >= 0:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        k = b * b * (x + 1) * (x + 1) + a * a * (y - 1) * (y - 1) - a * a * b * b

        if abs(k) < eps:
            x += 1
            y -= 1
        elif k < 0:
            x += 1
        else:
            y -= 1

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


def middle_dot_ellipse(center, x_radius, y_radius, outline='darkred', tag='non'):
    dots = []

    a = x_radius
    b = y_radius

    x = 0
    y = b

    el_tan = -(2 * b * b * x) / (2 * a * a * y)

    while el_tan > -1:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        k = b * b * (x + 1) * (x + 1) + a * a * (y - 0.5) * (y - 0.5) - a * a * b * b

        x += 1

        if k >= 0:
            y -= 1

        el_tan = -(2 * b * b * x) / (2 * a * a * y)

    while y >= 0:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        k = b * b * (x + 1) * (x + 1) + a * a * (y - 0.5) * (y - 0.5) - a * a * b * b

        y -= 1

        if k <= 0:
            x += 1

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags
