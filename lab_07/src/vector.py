import math

from src.settings.settings import Settings

class Vector:
    def __init__(self, x, y):
        self.settings = Settings()

        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x:.1f}, {self.y:.1f})"

    def __eq__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector):
            # Если other имеет тип Vector
            eps = self.settings.math.eps
            return math.fabs(self.x - other.x) < eps \
             and math.fabs(self.y - other.y) < eps
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __gt__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector):
            # Если other имеет тип Vector
            return self.x > other.x and self.y > other.y
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __lt__(self, other):
        # Сравнение двух точек
        if isinstance(other, Vector):
            # Если other имеет тип Vector
            return self.x < other.x and self.y < other.y
        # Иначе возвращаю NotImplemented
        return NotImplemented

    def __le__(self, other):
        return self < other or self == other

    def __be__(self, other):
        return self > other or self == other

    def __mul__(self, other):
        if isinstance(other, int):
            return Vector(self.x * other, self.y * other)

        elif isinstance(other, float):
            return Vector(self.x * other, self.y * other)

        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return NotImplemented

    def __repr__(self):
        return f"Vector{str(self)}"

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
