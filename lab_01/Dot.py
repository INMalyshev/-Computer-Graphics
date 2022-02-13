import math

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        # Сравнение двух точек
        if isinstance(other, Dot):
            # Если other имеет тип Dot
            return self.x == other.x and self.y == other.y
        # Иначе возвращаю NotImplemented
        return NotImplemented
