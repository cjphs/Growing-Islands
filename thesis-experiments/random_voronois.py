import sys
from matplotlib import pyplot as plt

sys.path.append("../thesis")
sys.path.append("./thesis")

from thesis.discrepancy import calculate_discrepancy, plot_discrepancy
from thesis.geometry import Tessellation
from thesis.voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from thesis.voronoi_approximation import VoronoiApproximation

if __name__ == "__main__":

    def approximate_random_voronoi(
        vor_tess: Tessellation,
        phi: float,
        iterations_before_reduction: int,
    ):
        vor_approx = VoronoiApproximation(vor_tess)

        vor_approx.do_thingy(phi=0.01, iterations_before_reduction=300)

        final_tess = voronoi_tessellation_from_points(vor_approx.generator_points)

        discrepancy = calculate_discrepancy(vor_tess, final_tess)

        omega = vor_approx.omega

        return final_tess, omega, discrepancy

    num_points = 50
    vor_tess = random_voronoi_tessellation(num_points)
    final_tess, omega, discrepancy = approximate_random_voronoi(vor_tess, 0.005, 300)

    print(f"omega: {omega}, discrepancy: {discrepancy.area}")

    # plot outcome
    plot_discrepancy(discrepancy)
    vor_tess.plot(color="black")
    final_tess.plot(color="blue")

    vor_tess.plot()
    plt.show()
