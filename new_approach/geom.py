from math import pi, acos,sqrt,cos,sin, inf
from matplotlib import pyplot as plt


'''
Point class
'''
class Point:
    def __init__(self, x:float, y:float):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    def plot(self):
        plt.plot(self.x, self.y, 'o')

    def in_boundary(self, xmin, xmax, ymin, ymax):
        return self.x >= xmin and self.x <= xmax and self.y >= ymin and self.y <= ymax
    
    def __eq__(self, other):
        if type(other) == Point:
            return (self.x == other.x and self.y == other.y)
        else:
            return False

'''
Line class
'''
class Line:
    def __init__(self, p1:Point, p2:Point):
        self.p1, self.p2 = p1, p2

    def __str__(self):
        return f"Line({str(self.p1)}, {str(self.p2)})"
    
    def __eq__(self, other):
        if type(other) == Line:
            return (other.p1 == self.p1 and other.p2 == self.p2) or (other.p1 == self.p2 and other.p2 == self.p1)
        else:
            return False

    def in_boundary(self, xmin, xmax, ymin, ymax):
        return self.p1.in_boundary(xmin, xmax, ymin, ymax) and self.p2.in_boundary(xmin, xmax, ymin, ymax)

    def line_intersect(self, other):
        xdiff = (self.p1.x - self.p2.x, other.p1.x - other.p2.x)
        ydiff = (self.p1.y - self.p2.y, other.p1.y - other.p2.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)

        if div == 0:
            return None
        
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

'''
Polygon class
'''
class Polygon:

    def __init__(self, edges:list[Line], vertices:list[Point]):
        self.edges = edges
        self.vertices = vertices

        self.ymin, self.ymax, self.xmin, self.xmax = inf,-inf,inf,-inf

        for v in vertices:
            if v.x < self.xmin:
                self.xmin = v.x
            if v.x > self.xmax:
                self.xmax = v.x
            if v.y < self.ymin:
                self.ymin = v.y
            if v.y > self.ymax:
                self.ymax = v.y


    def intersection(self, other):
        ymin = max(self.ymin, other.ymin)
        ymax = min(self.ymax, other.ymax)
        xmin = max(self.xmin, other.xmin)
        xmax = min(self.xmax, other.xmax)

        for e in self.edges:
            for e2 in other.edges:
                if not (e.in_boundary(xmin,xmax,ymin,ymax) and e2.in_boundary(xmin,xmax,ymin,ymax)):
                    continue
                    

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div


    def contains_point(self, point:Point):
        old_v = None
        theta = 0

        for e in self.edges:
            vec1 = (e.p1.x - point.x, e.p1.y - point.y)
            vec2 = (e.p2.x - point.x, e.p2.y - point.y)

            prod = vec1[0]*vec2[0] + vec1[1]*vec2[1]
            denom = sqrt(vec1[0]**2 + vec1[1]**2) * sqrt(vec2[0]**2 + vec2[1]**2)

            # distance = 0 -> point in poly
            if denom == 0:
                return True

            p = float(prod/denom)
            

            if p <= -1:
                theta += pi
            elif p >= 1:
                theta += 0
            else:
                theta += acos(p)

            if abs(2*pi-theta) <= 1e-10:
                return True

        return False
    
    def plot(self, l='-'):
        coords = [[v.x, v.y] for v in self.vertices]
        coords.append([self.vertices[0].x, self.vertices[0].y])
        xs, ys = zip(*coords)
        plt.plot(xs, ys, l)


if __name__ == "__main__":
    n = 6

    points = []
    lines = []

    old_p = None
    for i in range(0, n):
        x = cos(i/n * 2 * pi)
        y = sin(i/n * 2 * pi)

        p = Point(x, y)

        points.append(p)

        if old_p != None:
            lines.append(Line(old_p, p))

        old_p = p

    poly = Polygon(lines, points)

    p1 = Point(.2, .5)

    p2 = Point(2,3)

    plt.figure()

    poly.plot()
    p1.plot()
    p2.plot()
    p3 = Point(1, 0)

    print('?', poly.contains_point(p1))
    print('?', poly.contains_point(p2))
    print('?', poly.contains_point(p3))

    print(p1 == p2)
    print(Point(3,2) == Point(3,2))

    print(poly.xmax)

    plt.show()

