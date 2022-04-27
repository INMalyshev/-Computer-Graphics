import math
from src.vector import Vector
from src.utils.decorators import calculate_time


@calculate_time
def canonical_equation_circle(center, radius, outline='darkred', tag='non'):   # gets canvas coordinates
    # (X-Xo) + (Y-Yo) = R
    dots = []

    y = radius
    x = 0

    while x <= y:
        dots.append(center + Vector(x, y))
        dots.append(center + Vector(x, -y))
        dots.append(center + Vector(-x, y))
        dots.append(center + Vector(-x, -y))

        dots.append(center + Vector(y, x))
        dots.append(center + Vector(y, -x))
        dots.append(center + Vector(-y, x))
        dots.append(center + Vector(-y, -x))

        y = math.sqrt(radius * radius - x * x)
        x += 1

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


@calculate_time
def parametric_equation_circle(center, radius, outline='darkred', tag='non'):
    phi = 0.0
    dphi = 1 / abs(radius)

    dots = []

    while phi < 2 * math.pi:
        x = center.x + radius * math.cos(phi)
        y = center.y + radius * math.sin(phi)
        dots.append(Vector(x, y))
        phi += dphi

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


@calculate_time
def bresenham_circle(center, radius, outline='darkred', tag='non'):
    eps = 2

    x = 0
    y = radius

    dot = Vector(x, y)

    dots = []

    dots.append(dot + center)
    dots.append(Vector(x, -y) + center)
    dots.append(Vector(-x, y) + center)
    dots.append(Vector(-x, -y) + center)

    while dot.y > 0:
        ddot = Vector(dot.x + 1, dot.y - 1)
        k = radius * radius - abs(ddot) * abs(ddot)

        if math.fabs(k) < eps:
            dot = Vector(dot.x + 1, dot.y - 1)
        elif k > 0:
            dot = Vector(dot.x + 1, dot.y)
        else:
            dot = Vector(dot.x, dot.y - 1)

        dots.append(dot + center)
        dots.append(Vector(dot.x, -dot.y) + center)
        dots.append(Vector(-dot.x, dot.y) + center)
        dots.append(Vector(-dot.x, -dot.y) + center)

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


@calculate_time
def middle_dot_circle(center, radius, outline='darkred', tag='non'):
    x = 0
    y = radius

    dots = []

    dot = Vector(x, y)

    dots.append(center + dot)
    dots.append(center - dot)
    dots.append(center + Vector(dot.x, -dot.y))
    dots.append(center + Vector(-dot.x, dot.y))

    dots.append(center + Vector(dot.y, dot.x))
    dots.append(center - Vector(dot.y, dot.x))
    dots.append(center + Vector(dot.y, -dot.x))
    dots.append(center + Vector(-dot.y, dot.x))

    while dot.x <= dot.y:
        k = radius * radius - abs(Vector(dot.x + 1, dot.y - 0.5)) * abs(Vector(dot.x + 1, dot.y - 0.5))

        if k > 0:
            dot = Vector(dot.x + 1, dot.y)
        else:
            dot = Vector(dot.x + 1, dot.y - 1)

        dots.append(center + dot)
        dots.append(center - dot)
        dots.append(center + Vector(dot.x, -dot.y))
        dots.append(center + Vector(-dot.x, dot.y))

        dots.append(center + Vector(dot.y, dot.x))
        dots.append(center - Vector(dot.y, dot.x))
        dots.append(center + Vector(dot.y, -dot.x))
        dots.append(center + Vector(-dot.y, dot.x))

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags
