import DotObject
import math
import AnaliticGeometry

a = DotObject.DotObject(-1, -1, None)
b = DotObject.DotObject(1, 0, None)
c = DotObject.DotObject(1, 1, None)
d = DotObject.DotObject(0, 1, None)

print(AnaliticGeometry.isFourPointsCircle(a, b, c, d))
