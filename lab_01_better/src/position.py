class Position:
    def __init__(self, parent, son, dots, solution):
        self.previous = parent
        self.next = son
        self.dots = dots
        self.solution = solution

    def add(self, data, solution):
        self.next = Position(self, None, data, solution)

        return self.next

    def backward(self):
        if self.previous is None:
            return self

        return self.previous

    def forward(self):
        if self.next is None:
            return self

        return self.next
