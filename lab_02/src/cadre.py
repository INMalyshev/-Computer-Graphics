class Cadre:
    def __init__(self, parent, son):
        self.prev = parent
        self.next = son

    def add(self):
        self.next = Cadre(self, None)

        return self.next

    def backward(self):
        if self.prev is None:
            return self

        return self.prev

    def forward(self):
        if self.next is None:
            return self

        return self.next
