class Position:
    def __init__(self, parent, son, dots, solution):
        self.previous = parent
        self.next = son
        self.dots = dots
        self.solution = solution

    def add(self, data, solution):
        # print(len(self.dots))

        self.next = Position(self, None, data, solution)

        # print(len(self.dots))
        # print(len(self.next.dots))
        # print(len(self.dots), len(self.next.dots))

        return self.next

    def backward(self):
        if self.previous is None:
            # print("initial position")
            return self

        # print("prev dots: " + str(self.previous.dots))
        return self.previous

    def forward(self):
        if self.next is None:
            return self

        return self.next
