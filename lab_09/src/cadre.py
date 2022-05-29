import copy


class Cadre:
    def __init__(self, parent, son, data):
        self.prev = parent
        self.next = son

        # self.data = copy.deepcopy(data)
        self.data = data.copy()


    def add(self, data):
        self.next = Cadre(self, None, data)

        return self.next

    def backward(self):
        if self.prev is None:
            return self

        return self.prev

    def forward(self):
        if self.next is None:
            return self

        return self.next
