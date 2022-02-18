import math

import settings

class Dot:
    def __init__(self, x, y):
        self.settings = settings.Settings()
        
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        # Сравнение двух точек
        if isinstance(other, Dot):
            # Если other имеет тип Dot
            return math.fabs(self.x - other.x) < self.settings.math.eps \
             and math.fabs(self.y - other.y) < self.settings.math.eps
        # Иначе возвращаю NotImplemented
        return NotImplemented
