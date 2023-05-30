from thesis.geometry.point import Point
from thesis.geometry.tessellation import Tessellation
from thesis.input_generation.voronoi_funcs import voronoi_from_points
from thesis.voronoi_approximation import VoronoiApproximation

points = []
for i in range(1, 10):
    for j in range(1, 10):
        x = i/10
        y = j/10 + (i%2)*(1/20)
        points.append(Point(x, y))

v = voronoi_from_points(points)
d = Tessellation(voronoi=v)

approx = VoronoiApproximation(d, gui=False)

print(approx.compute_omega(d.centers))