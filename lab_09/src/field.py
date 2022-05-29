from src.vector import Vector

class Field:
    def __init__(self, a, b):
        if isinstance(a, Vector) and isinstance(b, Vector):
            if b > a:
                self.start = a # bottom left
                self.finish = b # top right

    def include(self, vector):
        if isinstance(vector, Vector):
            return vector >= self.start and vector <= self.finish
        else:
            return NotImplemented
