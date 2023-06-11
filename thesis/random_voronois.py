import sys
from matplotlib import pyplot as plt

from discrepancy import calculate_discrepancy, plot_discrepancy
from geometry import Tessellation
from voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from voronoi_approximation import VoronoiApproximation


def approximate_random_voronoi(
    vor_tess: Tessellation,
    phi: float,
    iterations_before_reduction: int,
):
    vor_approx = VoronoiApproximation(vor_tess, print_progress=False)

    vor_approx.do_thingy(
        phi=phi, iterations_before_reduction=iterations_before_reduction
    )

    final_tess = voronoi_tessellation_from_points(vor_approx.generator_points)

    discrepancy = calculate_discrepancy(vor_tess, final_tess)

    time = vor_approx.time_taken
    iterations = vor_approx.iterations
    omega = vor_approx.omega

    return final_tess, omega, discrepancy, iterations, time


if __name__ == "__main__":
    phi = 0.0175
    its = 50

    f = open("results/results_0175_50.txt", "w")

    num_points = 32
    for j in range(100):
        fname = f"in/diagrams/voronoi_{j}.txt"
        print(f"moving onto {fname}")

        vor_tess = Tessellation()
        vor_tess.load_from_txt(fname)

        # vor_tess = random_voronoi_tessellation(num_points)
        final_tess, omega, discrepancy, iterations, time = approximate_random_voronoi(
            vor_tess, phi, its
        )
        f.write(f"{omega},{discrepancy.area},{time}\n")

        print(f"{j} / {100}")

    f.close()

    print(f"omega: {omega}, discrepancy: {discrepancy.area}")

    # plot outcome
    plot_discrepancy(discrepancy)
    vor_tess.plot(color="black")
    final_tess.plot(color="blue")

    vor_tess.plot()
    plt.show()
