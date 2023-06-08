import sys
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

from discrepancy import calculate_discrepancy, plot_discrepancy
from geometry import Tessellation, Point
from voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from voronoi_approximation import VoronoiApproximation

import random

if __name__ == "__main__":
    points = [
        Point(i / 10, j / 10 + (i % 2) * 0.05)
        for i in range(1, 10)
        for j in range(1, 10)
    ]

    tess = voronoi_tessellation_from_points(points)

    wiggle = 0.0025
    f = open("results/wiggle_0025.txt", "w")

    for i in range(50):
        for v in tess.vertices:
            v.x += random.uniform(-wiggle, wiggle)
            v.y += random.uniform(-wiggle, wiggle)

        approx = VoronoiApproximation(tess, print_progress=False)
        approx.do_thingy(phi=0.025, iterations_before_reduction=100)

        final_tess = voronoi_tessellation_from_points(approx.generator_points)

        discrepancy = calculate_discrepancy(tess, final_tess)

        f.write(f"{approx.omega},{discrepancy.area},{approx.time_taken}\n")

    f.close()

    black_patch = mpatches.Patch(color="black", label="Input tessellation")
    blu_patch = mpatches.Patch(color="blue", label="Voronoi approximation")

    plt.legend(handles=[black_patch, blu_patch])

    final_tess.plot(color="blue")
    plt.show()
