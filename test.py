def get_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)

    return x, y

if __name__ == '__main__':
    print(get_intersection(0,0, 0,2, -1,1, 1,1))