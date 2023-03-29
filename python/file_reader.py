from sympy.geometry import Polygon, Point2D
from polygon_functions import sort_polygon_vertices
from tessellation import Tessellation

def save_tessellation(filename:str, tessellation:Tessellation):
    file = open(filename, 'a')

    file.write('regions\n')

    for r in tessellation.polygons:
        s = ''
        for v in r.vertices:
            s += f'{float(v.x)} {float(v.y)} '
        file.write(f'{s}\n')


def read_tessellation_file(filename:str):
    regions = []
    neighborhood_dict = {}

    mode = ''
    mode1 = 'regions'
    mode2 = 'adjacencies'

    file = open(filename, 'r')
    lines = file.readlines()

    for l in lines:
        if l in [mode1, mode2]:
            mode = l

        # read region polygons
        elif mode == mode1:
            l = l.split(" ")

            points = []

            for i in range(0, len(l)/2):
                x = l[2*i]
                y = l[2*i+1]

                x, y = float(x), float(y)

                points.append(Point2D(x, y))

            regions.append(*tuple(points))

        # read neighborhoods
        elif mode == mode2:
            l = l.split(" ")
            i, j = int(l[0]), int(l[1])

            if not i in neighborhood_dict:
                neighborhood_dict[i] = []
            else:
                neighborhood_dict[i].append(j)

    return Tessellation(polygons=regions, neighborhood_dict=neighborhood_dict)