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

    A = geometry.Polygon()
    for p in p2:
        A = A.union(p)
    
    B = geometry.Polygon()
    for j in range(len(p2)):
        B = B.union(p1[j].intersection(p2[j]))

    discrep = A.difference(B)

    boundary_box = geometry.Polygon([(0,0), (1,0), (1,1), (0,1)])
    discrep = discrep.intersection(boundary_box)

    myPoly = gpd.GeoSeries([discrep])
    myPoly.plot()

    return discrep.area