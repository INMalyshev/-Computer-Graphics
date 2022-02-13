import math

from Dot import Dot
from Settings import Settings

def equal(alpha, betta):
    settings = Settings()
    eps = settings.eps
    return math.fabs(alpha.x - betta.x) < eps and math.fabs(alpha.y - betta.y) < eps

def distance(alpha, betta):
    if isinstance(alpha, Dot) and isinstance(betta, Dot):
        return math.sqrt((alpha.x - betta.x) * (alpha.x - betta.x) + (alpha.y - betta.y) * (alpha.y - betta.y))
    return NotImplemented

def angle(alpha, betta, gamma):
    if isinstance(alpha, Dot) and isinstance(betta, Dot) and isinstance(gamma, Dot):
        ab = distance(alpha, betta)
        bg = distance(betta, gamma)
        scalar = (alpha.x - betta.x) * (gamma.x - betta.x) + (alpha.y - betta.y) * (gamma.y - betta.y)
        cosinus = scalar / (ab * bg)
        return math.acos(cosinus)
    return NotImplemented

def onOneExis(alpha, betta, gamma):
    if isinstance(alpha, Dot) and isinstance(betta, Dot) and isinstance(gamma, Dot):
        settings = Settings()
        if math.fabs(angle(alpha, betta, gamma) - math.pi) < settings.eps:
            return True
        elif math.fabs(angle(betta, alpha, gamma) - math.pi) < settings.eps:
            return True
        elif math.fabs(angle(alpha, gamma, betta) - math.pi) < settings.eps:
            return True
        else:
            return False
    return NotImplemented

def circumscribedCircleCenter(alpha, betta, gamma):
    if isinstance(alpha, Dot) and isinstance(betta, Dot) and isinstance(gamma, Dot):
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
        result = Dot(a, b)
        return result
    return NotImplemented

def isFourPointsCircle(alpha, betta, gamma, delta):
    if isinstance(alpha, Dot) and isinstance(betta, Dot) and isinstance(gamma, Dot) and isinstance(delta, Dot):
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
