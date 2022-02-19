import math

from src.settings.settings import Settings

class Dot:
    def __init__(self, x, y):
        self.settings = Settings()

        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        # Сравнение двух точек
        if isinstance(other, Dot):
            # Если other имеет тип Dot
            eps = self.settings.math.eps
            return math.fabs(self.x - other.x) < eps \
             and math.fabs(self.y - other.y) < eps
        # Иначе возвращаю NotImplemented
        return NotImplemented
