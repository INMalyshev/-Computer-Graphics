from Dot import Dot

class DotObject(Dot):
    def __init__(self, x, y, id):
        super(DotObject, self).__init__(x, y)
        self.id = id
    def __str__(self):
        return super(DotObject, self).__str__()
    def __eq__(self, other):
        return super(DotObject, self).__eq__(other)
    def distance(self, other):
        return super(DotObject, self).distance(other)
