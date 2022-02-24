import math

from src.vector import Vector
from src.settings.settings import Settings

def equal(alpha, betta):
    settings = Settings()
    eps = settings.math.eps
    return math.fabs(alpha.x - betta.x) < eps and math.fabs(alpha.y - betta.y) < eps

def distance(alpha, betta):
    if isinstance(alpha, Vector) and isinstance(betta, Vector):
        return math.sqrt((alpha.x - betta.x) * (alpha.x - betta.x) + (alpha.y - betta.y) * (alpha.y - betta.y))
    return NotImplemented

def angle(alpha, betta, gamma):
    if isinstance(alpha, Vector) and isinstance(betta, Vector) and isinstance(gamma, Vector):
        ab = distance(alpha, betta)
        bg = distance(betta, gamma)
        scalar = (alpha.x - betta.x) * (gamma.x - betta.x) + (alpha.y - betta.y) * (gamma.y - betta.y)
        cosinus = scalar / (ab * bg)
        return math.acos(cosinus)
    return NotImplemented

def onOneExis(alpha, betta, gamma):
    if isinstance(alpha, Vector) and isinstance(betta, Vector) and isinstance(gamma, Vector):
        settings = Settings()
        eps = settings.math.eps
        if math.fabs(angle(alpha, betta, gamma) - math.pi) < eps:
            return True
        elif math.fabs(angle(betta, alpha, gamma) - math.pi) < eps:
            return True
        elif math.fabs(angle(alpha, gamma, betta) - math.pi) < eps:
            return True
        else:
            return False
    return NotImplemented

def circumscribedCircleCenter(alpha, betta, gamma):
    if isinstance(alpha, Vector) and isinstance(betta, Vector) and isinstance(gamma, Vector):
        if onOneExis(alpha, betta, gamma):
            return None
        x_12 = alpha.x - betta.x
        x_23 = betta.x - gamma.x
        x_31 = gamma.x - alpha.x
        y_12 = alpha.y - betta.y
        y_23 = betta.y - gamma.y
        y_31 = gamma.y - alpha.y
        z_1 = alpha.x * alpha.x + alpha.y * alpha.y
        z_2 = betta.x * betta.x + betta.y * betta.y
        z_3 = gamma.x * gamma.x + gamma.y * gamma.y
        z_x = y_12 * z_3 + y_23 * z_1 + y_31 * z_2
        z_y = x_12 * z_3 + x_23 * z_1 + x_31 * z_2
        z = x_12 * y_31 - y_12 * x_31
        a = -z_x / (2 * z)
        b = z_y / (2 * z)
        result = Vector(a, b)
        return result
    return NotImplemented

def isFourPointsCircle(alpha, betta, gamma, delta):
    if isinstance(alpha, Vector) and isinstance(betta, Vector) and isinstance(gamma, Vector) and isinstance(delta, Vector):
        abc = circumscribedCircleCenter(alpha, betta, gamma)
        if abc is None:
            return False
        abd = circumscribedCircleCenter(alpha, betta, delta)
        if abd is None:
            return False
        if not equal(abc, abd):
            return False
        acd = circumscribedCircleCenter(alpha, gamma, delta)
        if acd is None:
            return False
        if not equal(abd, acd):
            return False
        bcd = circumscribedCircleCenter(betta, gamma, delta)
        if bcd is None:
            return False
        if not equal(acd, bcd):
            return False
        return True
    return NotImplemented

def circleArea(radius):
    return math.pi * radius * radius

def circlesIntersectionArea(centerA, radiusA, centerB, radiusB):  # wrong solution
    settings = Settings()
    eps = settings.math.eps
    if isinstance(centerA, Vector) and isinstance(centerB, Vector):
        dist = distance(centerA, centerB)
        if radiusA + radiusB < dist or \
        math.fabs(radiusA + radiusB - dist) < eps:
            return 0.0
        if dist < math.fabs(radiusA - radiusB):
            return 0.0
        r1 = radiusA
        r2 = radiusB
        f1 = 2 * math.acos((r1*r1 - r2*r2 + dist*dist) / (2 * r1 * dist))
        f2 = 2 * math.acos((r2*r2 - r1*r1 + dist*dist) / (2 * r2 * dist))
        f1 %= math.pi
        f1 %= math.pi
        s1 = (r1*r1 * (f1 - math.sin(f1))) / 2
        s2 = (r2*r2 * (f2 - math.sin(f2))) / 2
        return s1 + s2;
    else:
        return NotImplemented
