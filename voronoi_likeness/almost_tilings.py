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

    wiggle = 0.03
    f = open("results/wiggle_03.txt", "w")

    t = None

    for i in range(2):
        tess = voronoi_tessellation_from_points(points)

        for v in tess.vertices:
            v.x += random.uniform(-wiggle, wiggle)
            v.y += random.uniform(-wiggle, wiggle)

        approx = VoronoiApproximation(tess, print_progress=False)
        approx.do_thingy(phi=0.02, iterations_before_reduction=100)

        final_tess = voronoi_tessellation_from_points(approx.generator_points)

        try:
            discrepancy = calculate_discrepancy(tess, final_tess)
            f.write(f"{approx.omega},{discrepancy.area},{approx.time_taken}\n")
        except:
            print("uh")

        t = tess

    f.close()

    print(calculate_discrepancy(t, final_tess).area)

    black_patch = mpatches.Patch(color="black", label="Input tessellation")
    blu_patch = mpatches.Patch(color="blue", label="Voronoi approximation")

    plt.legend(handles=[black_patch, blu_patch])

    t.plot(color="black")
    final_tess.plot(color="blue")
    plt.show()
