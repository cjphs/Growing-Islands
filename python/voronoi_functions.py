from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, delaunay_plot_2d
from random import uniform as U
from sympy import Polygon, Point2D
from polygon_functions import sort_polygon_vertices, polygon_intersection


def generate_random_points(num_points:int=20):
    points = []
    while(num_points > 0):
        points.append([U(0,1), U(0,1)])
        num_points -= 1
    return points


def generate_random_voronoi(points):
    vor = Voronoi(points)
    return vor


def voronoi_to_polygons(vor:Voronoi):
    polygons = []

    bounding_poly = Polygon((0,0), (1,0), (1,1), (0,1))

    index = 0

    for region in vor.regions:
        if not -1 in region and len(region) > 0:

            points = []

            for p in region:
                v = vor.vertices[p]
                point_obj = Point2D(v[0], v[1])
                points.append(point_obj)

            points.append(points[0])

            index += 1
            region_polygon = Polygon(*tuple(points))

            # p = polygon_intersection(region_polygon, bounding_poly)

            polygons.append(region_polygon)
            

    return polygons