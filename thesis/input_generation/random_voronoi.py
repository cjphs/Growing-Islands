from scipy.spatial import Voronoi
from random import uniform as U

def generate_random_points(num_points:int=20, xmin=0, xmax=1, ymin=0, ymax=1) -> list[list[int, int]]:
    points = []
    while(num_points > 0):
        points.append([U(xmin,xmax), U(ymin,ymax)])
        num_points -= 1
    return points

def generate_random_voronoi(num_points:int=20, xmin=0, xmax=1, ymin=0, ymax=1) -> Voronoi:
    points = generate_random_points(num_points, xmin, xmax, ymin, ymax)
    vor = Voronoi(points)
    return vor

