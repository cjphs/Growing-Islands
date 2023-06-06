from geometry.tessellation import Tessellation
import shapely
from shapely import ops, geometry
import matplotlib.pyplot as plt
import geopandas as gpd


def tess2polys(tess:Tessellation) -> list[shapely.geometry.Polygon]:
    polys = []
    for r in tess.regions:
        points = []
        for v in r:
            p = tess.vertices[v]
            points.append([p.x, p.y])
        poly = geometry.Polygon(points)
        polys.append(poly)
    return polys

def calculate_discrepancy(T1:Tessellation, T2:Tessellation) -> float:
    p1 = tess2polys(T1)
    p2 = tess2polys(T2)

    discrep = geometry.Polygon()

    for i in range(len(p1)):
        for j in range(len(p2)):
            if i == j:
                continue
            discrep = discrep.union(p1[i].intersection(p2[j]))

    boundary_box = geometry.Polygon([(0,0), (1,0), (1,1), (0,1)])
    #discrep = discrep.intersection(boundary_box)

    myPoly = gpd.GeoSeries([discrep])
    myPoly.plot()

    return discrep.area