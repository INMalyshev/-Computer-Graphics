class Position:
    def __init__(self, parent, son, dots, solution):
        self.previous = parent
        self.next = son
        self.dots = dots
        self.solution = solution
