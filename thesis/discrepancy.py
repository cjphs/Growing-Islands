import shapely
from shapely import ops, geometry
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib import patches as mpatches

from geometry import Tessellation


def tess2polys(tess: Tessellation) -> list[shapely.geometry.Polygon]:
    polys = []
    for r in tess.regions:
        points = []
        for v in r:
            p = tess.vertices[v]
            points.append([p.x, p.y])
        poly = geometry.Polygon(points)
        polys.append(poly)
    return polys


def calculate_discrepancy(T1: Tessellation, T2: Tessellation) -> float:
    p1 = tess2polys(T1)
    p2 = tess2polys(T2)

    discrep = geometry.Polygon()

    for i in range(len(p1)):
        for j in range(len(p2)):
            if i == j:
                continue
            discrep = discrep.union(p1[i].intersection(p2[j]))

    return discrep


def plot_discrepancy(discrepancy_polygon):
    myPoly = gpd.GeoSeries([discrepancy_polygon])
    myPoly.plot(color="gray")


if __name__ == "__main__":
    from voronoi_approximation import VoronoiApproximation
    from voronoi import (
        random_voronoi_tessellation,
        voronoi_tessellation_from_points,
    )

    tessellation = random_voronoi_tessellation(30)

    approximation = VoronoiApproximation(tessellation)

    # Create Voronoi diagram from centroids to compare later on.
    original_approximation = voronoi_tessellation_from_points(
        approximation.generator_points
    )
    discrepancy = calculate_discrepancy(tessellation, original_approximation)

    print("Area discrepancy:", discrepancy.area)

    tessellation.plot(color="black")
    original_approximation.plot(color="red", linewidth=1.25)

    black_patch = mpatches.Patch(color="black", label="Input tessellation")
    red_patch = mpatches.Patch(color="red", label="Voronoi of centroids of input")
    blu_patch = mpatches.Patch(color="gray", label="Area discrepancy")

    plt.legend(handles=[black_patch, red_patch, blu_patch], bbox_to_anchor=(1, 1))
    # enforce_plot_scale(xmin,xmax,ymin,ymax)
    plt.show()
