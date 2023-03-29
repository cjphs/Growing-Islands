from sympy import Polygon, Line, Point2D, Segment2D, intersection, Triangle
from math import atan2, pi, cos, sin, sqrt, acos
import matplotlib.pyplot as plt



def plot_polygons(polys:list, style:str="-"):
    i = 0
    for p in polys:
        plot_polygon(p,l=style,txt=i)
        i += 1
    


def plot_polygon(poly, l='-', txt:str=""):    

    coords = [[v.x, v.y] for v in poly.vertices]
        
    cntr = poly.centroid
    plt.text(cntr.x, cntr.y, txt)
        
    coords = [[v.x, v.y] for v in poly.vertices]
    xs, ys = zip(*coords)
    plt.plot(xs, ys, l)
    
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')


def in_polygon_bounds(x, y, poly:Polygon):
    b = poly.bounds
    return (x < b[2] and y < b[3] and x > b[0] and y > b[1])

def point_in_poly(point:Point2D, poly:Polygon):
    if type(poly) == Segment2D or type(poly) == Point2D or type(poly) == Triangle:
        return poly.encloses_point(point)

    vertices = poly.vertices

    old_v = None
    theta = 0

    for v in vertices:
        if old_v != None:
            vec1 = (old_v.x - point.x, old_v.y - point.y)
            vec2 = (v.x - point.x, v.y - point.y)

            prod = vec1[0]*vec2[0] + vec1[1]*vec2[1]
            denom = sqrt(vec1[0]**2 + vec1[1]**2) * sqrt(vec2[0]**2 + vec2[1]**2)

            p = float(prod/denom)

            print(p)
            print(type(p))

            if p <= -1:
                theta += pi
            elif p >= 1:
                theta += 0
            else:
                theta += acos(prod/denom)

            if theta >= pi:
                return True

        old_v = v

    return False


def polygon_intersection(poly1, poly2):

    # hack fix in case types fuck up for whatever reason
    if type(poly1) == list:
        print("POOO!!!!", poly1)
        print(3*"\n")
    elif type(poly2) == list:
        poly2 = Polygon(*poly2)

    b1 = poly1.bounds
    b2 = poly2.bounds

    # Don't bother with the slow intersection algorithm if the polygons' bounds don't overlap
    if not (b1[0] < b2[2] and b1[1] < b2[3] and b1[2] > b2[0] and b1[3] > b2[1]):
        return []
    
    p = intersection(poly1, poly2)
    
    for _ in poly1.vertices:
        if not in_polygon_bounds(_.x, _.y, poly2):
            continue

        if point_in_poly(_, poly2) and not _ in p:
            p.append(_)
            
    for _ in poly2.vertices:
        if not in_polygon_bounds(_.x, _.y, poly1):
            continue

        if point_in_poly(_, poly1) and not _ in p:
            p.append(_)

    # UGLY!
    if len(p) >= 2:
        pp = []
        for ppp in p:
            if type(ppp) == Segment2D:
                pp.append(ppp.p1)
                pp.append(ppp.p2)
            else:
                pp.append(ppp)
        # print('to be sorted: ', pp)
        poly3 = sort_polygon_vertices(Polygon(*pp))
    else:
        poly3 = p

    if type(poly3) != Polygon:
        print(poly3)
    else:
        print(type(poly3), len(poly3.vertices))

    return poly3


def sort_polygon_vertices(poly):
    cx, cy = 0, 0
    n = len(poly.vertices)
    
    for _ in poly.vertices:
        cx += _.x
        cy += _.y
    
    centroid = Point2D(cx/n, cy/n)
    
    segs = []
    
    for _ in poly.vertices:
        segs.append((_, atan2(_.x-centroid.x, _.y-centroid.y)))
        
    sort = sorted(segs, key=lambda x: x[1])
    
    points = [p[0] for p in sort]

    points.append(points[0])
        
    return Polygon(*points)
