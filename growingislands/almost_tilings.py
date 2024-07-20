import sys
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

from discrepancy import calculate_discrepancy, plot_discrepancy
from geometry import Tessellation, Point
from voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from voronoi_approximation import VoronoiApproximation

import random

if __name__ == "__main__":
    n = 8
    points = [
        Point(i / n, j / n + (i % 2) * (1 / (n * 2)))
        for i in range(1, n)
        for j in range(1, n)
    ]

    tess = voronoi_tessellation_from_points(points)

    plt.show()

    wiggle = 0.01

    t = None

    for i in range(2):
        tess = voronoi_tessellation_from_points(points)

        for v in tess.vertices:
            v.x += random.uniform(-wiggle, wiggle)
            v.y += random.uniform(-wiggle, wiggle)

        tess.save_to_txt("in/wiggle.txt")

        t = tess
