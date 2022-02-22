from src.calculations import analitic_geometry
from src.vector import Vector
from src.settings.settings import Settings

import itertools
import math

class Circle:
    def __init__(self, pack, vectors):
        self.settings = Settings()
        self.pack = list(pack)
        self.center = analitic_geometry.circumscribedCircleCenter(self.pack[0], self.pack[1], self.pack[2])
        self.r = analitic_geometry.distance(self.center, self.pack[0])
        self.count = self.countEntries(vectors)

    def __str__(self):
        return f"-> {self.center} r={self.r} count={self.count} <-"

    def __gt__(self, other):
        if isinstance(other, Circle):
            return self.count > other.count
        else:
            return NotImplemented

    def countEntries(self, vectors):
        count = 0
        eps = self.settings.math.eps
        for vector in vectors:
            if self.r > analitic_geometry.distance(self.center, vector) or \
            math.fabs(self.r - analitic_geometry.distance(self.center, vector)) < eps:
                count += 1
        return count

def solution(vectors):
    packs = list(itertools.combinations(vectors, 4))
    circles = list()
    for pack in packs:
        tmp = list(pack)
        if analitic_geometry.isFourPointsCircle(tmp[0], tmp[1], tmp[2], tmp[3]):
            circles.append(Circle(pack, vectors))
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
    maxArea = analitic_geometry.circlesIntersectionArea(maxCouple[0].center, \
    maxCouple[0].r, maxCouple[1].center, maxCouple[1].r)

    for couple in couples:
        area = analitic_geometry.circlesIntersectionArea(couple[0].center, \
        couple[0].r, couple[1].center, couple[1].r)
        if area > maxArea:
            maxArea = area
            maxCouple = couple

    return (maxCouple[0].center, maxCouple[0].r, maxCouple[1].center, maxCouple[1].r)
