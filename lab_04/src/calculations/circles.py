import math
from src.vector import Vector


def canonical_equation_circle(center, radius, outline='darkred', tag='non'):   # gets canvas coordinates
    # (X-Xo) + (Y-Yo) = R
    dots = []
    for x in range(center.x - radius, center.x + radius + 1, 1):
        y = math.sqrt(radius * radius - (x - center.x) * (x - center.x)) + center.y
        dots.append(Vector(x, y))
        dots.append(Vector(x, -y))

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags


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

def bresenham_circle(center, radius, outline='darkred', tag='non'):
    eps = 1e-5

    x = center.x
    y = center.y + radius

    dot = Vector(x, y)

    dots = [dot]

    for _ in range(int(radius)):
        ddot = Vector(dot.x + 1, dot.y + 1)
        k = radius * radius - abs(ddot - center) * abs(ddot - center)

        if math.fabs(k) < eps:
            dot = Vector(dot.x + 1, dot.y - 1)
        elif k > 0:
            dot = Vector(dot.x + 1, dot.y)
        else:
            dot = Vector(dot.x, dot.y - 1)

        dots.append(dot)
        dots.append(Vector(dot.x, dot.y - 2 * (dot.y - center.y)))
        dots.append(Vector(dot.x - 2 * (dot.x - center.x), dot.y))
        dots.append(Vector(dot.x - 2 * (dot.x - center.x), dot.y - 2 * (dot.y - center.y)))

    cols = [outline for _ in range(len(dots))]
    tags = [tag for _ in range(len(dots))]

    return dots, cols, tags
