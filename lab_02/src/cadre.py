import copy

class Cadre:
    def __init__(self, parent, son, couples):
        self.prev = parent
        self.next = son

        self._couples = copy.deepcopy(couples)

    def add(self, couples):
        self.next = Cadre(self, None, couples)

        return self.next

    def backward(self):
        if self.prev is None:
            return self

        return self.prev

    def forward(self):
        if self.next is None:
            return self

        return self.next
