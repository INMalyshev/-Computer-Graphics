""" Rotate Scale Push """

from math import cos, sin

from src.vector import Vector

def rotate(dot, phi, axis):
    if not (isinstance(dot, Vector) and isinstance(axis, Vector)):
        return NotImplemented

    normal = dot - axis
    rotated = Vector(normal.x * cos(phi) - normal.y * sin(phi), normal.x * sin(phi) + normal.y * cos(phi))
    result = rotated + axis

    return result

def push(dot, vec):
    if not (isinstance(dot, Vector) and isinstance(vec, Vector)):
        return NotImplemented

    return dot + vec

def scale(dot, kx, ky, rel):
    if not isinstance(dot, Vector) or not isinstance(dot, Vector):
        return NotImplemented

    tmp = dot - rel
    tmpp = Vector(tmp.x * kx, tmp.y * ky)
    res = tmpp + rel

    return res

