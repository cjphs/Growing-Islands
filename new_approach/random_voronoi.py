from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, delaunay_plot_2d
from random import uniform as U


def generate_random_points(num_points:int=20) -> list[list[int, int]]:
    points = []
    while(num_points > 0):
        points.append([U(0,1), U(0,1)])
        num_points -= 1
    return points


def generate_random_voronoi(num_points:int=20) -> Voronoi:
    points = generate_random_points(num_points)
    vor = Voronoi(points)
    return vor

