import AnaliticGeometry
import DotObject
import Settings

import itertools
import math

class Circle:
    def __init__(self, pack, dots):
        self.settings = Settings.Settings()
        self.pack = list(pack)
        self.center = AnaliticGeometry.circumscribedCircleCenter(self.pack[0], self.pack[1], self.pack[2])
        self.r = AnaliticGeometry.distance(self.center, self.pack[0])
        self.count = self.countEntries(dots)

    def __str__(self):
        return f"-> {self.center} r={self.r} count={self.count} <-"

    def __gt__(self, other):
        if isinstance(other, Circle):
            return self.count > other.count
        else:
            return NotImplemented

    def countEntries(self, dots):
        count = 0
        for dot in dots:
            if self.r > AnaliticGeometry.distance(self.center, dot) or \
            math.fabs(self.r - AnaliticGeometry.distance(self.center, dot)) < self.settings.eps:
                count += 1
        return count

def solution(dots):
    packs = list(itertools.combinations(dots, 4))
    circles = list()
    for pack in packs:
        tmp = list(pack)
        if AnaliticGeometry.isFourPointsCircle(tmp[0], tmp[1], tmp[2], tmp[3]):
            circles.append(Circle(pack, dots))
    circles.sort(reverse=True) # Получил упорядоченный список окружностей
    if len(circles) < 2:
        return None
    canditionalCircles = list()
    for circle in circles:
        if circle == circles[0] or circle == circles[1]:
            if circle not in canditionalCircles:
                canditionalCircles.append(circle)
    couples = list(itertools.combinations(canditionalCircles, 2))
    for i in range(len(couples)):
        couples[i] = list(couples[i])
    maxCouple = couples[0]
    maxArea = AnaliticGeometry.circlesIntersectionArea(maxCouple[0].center, \
    maxCouple[0].r, maxCouple[1].center, maxCouple[1].r)

    for couple in couples:
        area = AnaliticGeometry.circlesIntersectionArea(couple[0].center, \
        couple[0].r, couple[1].center, couple[1].r)
        if area > maxArea:
            maxArea = area
            maxCouple = couple

    return (maxCouple[0].center, maxCouple[0].r, maxCouple[1].center, maxCouple[1].r)


# a = DotObject.DotObject(-1, 1, None)
# b = DotObject.DotObject(-1, -1, None)
# c = DotObject.DotObject(1, 1, None)
# d = DotObject.DotObject(1, -1, None)
# e = DotObject.DotObject(0, 0, None)
# f = DotObject.DotObject(0, 2, None)
# g = DotObject.DotObject(2, 2, None)
# h = DotObject.DotObject(2, 0, None)
# 
#
# dots = [a, b, c, d, e, f, g, h]
#
# res = solution(dots)
# print(res[0])
# print(res[1])
# print(res[2])
# print(res[3])
