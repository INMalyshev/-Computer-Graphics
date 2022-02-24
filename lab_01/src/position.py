class Position:
    def __init__(self, parent, son, dots, solution, circles):
        self.previous = parent
        self.next = son
        self.dots = dots
        self.solution = solution
        self.circles = circles # [c1, r1, c2, r2]

    def add(self, data, solution, circles):
        self.next = Position(self, None, data, solution, circles)

        return self.next

    def backward(self):
        if self.previous is None:
            return self

        return self.previous

    def forward(self):
        if self.next is None:
            return self

        return self.next
