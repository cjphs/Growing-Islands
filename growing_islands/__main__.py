from datetime import datetime

from geometry import Tessellation
from matplotlib import pyplot as plt
from voronoi_approximation import VoronoiApproximation
from discrepancy import calculate_discrepancy
from voronoi import (
    random_voronoi_tessellation,
    voronoi_tessellation_from_points,
)
import sys


def enforce_plot_scale(xmin, xmax, ymin, ymax):
    ax = plt.gca()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])


def main():
    ##################
    # Input handling #
    ##################

    xmin, xmax = 0, 1
    ymin, ymax = 0, 1

    load_from_file = ""
    if len(sys.argv) > 1:
        load_from_file = sys.argv[1]

    if load_from_file == "":
        num_points = 32
        tessellation = random_voronoi_tessellation(num_points)
        filename = f"in/{datetime.now().strftime(f'%H-%M-%S_{num_points}')}.txt"
        tessellation.save_to_txt(f"{filename}")
    else:
        tessellation = Tessellation(txt_file=load_from_file)

    ####################
    # The main part... #
    ####################

    approximation = VoronoiApproximation(tessellation, print_progress=False)

    # Create Voronoi diagram from centroids to compare later on.
    original_approximation = voronoi_tessellation_from_points(
        approximation.generator_points
    )

    # Run the approximation algorithm.
    approximation.start(phi=0.02, iterations_before_reduction=50)

    #########
    # Done. #
    #########

    print(f"Lower bound for omega: {approximation.omega}")
    print(f"om... {approximation.compute_omega(approximation.bestimator_points)}")

    # generate new voronoi diagram from final estimator point positions
    final_tess = voronoi_tessellation_from_points(approximation.bestimator_points)
    print(f"Area discrepancy: {calculate_discrepancy(tessellation, final_tess).area} %")

    tessellation.plot(color="black")
    final_tess.plot(color="red")

    for p in approximation.generator_points:
        plt.scatter(p.x, p.y, color="red", marker="o")

    plt.show()


if __name__ == "__main__":
    main()
