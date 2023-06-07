import sys

from datetime import datetime

from geometry import Tessellation
from matplotlib import pyplot as plt
from voronoi_approximation import VoronoiApproximation
from discrepancy import calculate_discrepancy

from shapely_voronoi import (
    random_voronoi_tessellation,
    voronoi_tessellation_from_points,
)


def enforce_plot_scale(xmin, xmax, ymin, ymax):
    ax = plt.gca()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])


def get_arg(args, arg_name):
    if arg_name in args:
        return args[args.index(arg_name) + 1]
    return None


def parse_args(phi, num_points, gui):
    num = get_arg(sys.argv, "--num_points")
    if num != None:
        num_points = int(num)
    om = get_arg(sys.argv, "--omega")
    if om != None:
        omega = float(om)
    ph = get_arg(sys.argv, "--phi")
    if ph != None:
        phi = float(ph)
    gu = get_arg(sys.argv, "--gui")
    if gu != None:
        if gu == "False":
            gui = False
    ma = get_arg(sys.argv, "--margin")
    if ma != None:
        margin = float(ma)
    return phi, num_points, gui


def main():
    gui = False

    phi = 0.0005

    # margin < 1 yields better results in shorter time
    margin = 1

    num_points = 40

    xmin, xmax = 0, 1
    ymin, ymax = 0, 1

    phi, num_points, gui = parse_args(phi, num_points, gui)

    load_from_file = ""
    # load_from_file = "in/diagram_luxembourg.txt"
    # load_from_file = "in/23-53-05_30_0.005.txt"
    # load_from_file = "in/diagram_field2.txt"
    # load_from_file = "in/fields3.txt"
    # load_from_file = "in/14-04-12_40_0.0005.txt"

    original_points = []

    if load_from_file == "":
        # vor = generate_random_voronoi(num_points,
        #                              xmin=xmin,
        #                              xmax=xmax,
        #                              ymin=ymin,
        #                              ymax=ymax
        #                              )

        # tessellation = Tessellation(voronoi=vor)

        tessellation = random_voronoi_tessellation(num_points)

        filename = f"in/{datetime.now().strftime(f'%H-%M-%S_{num_points}_{phi}')}.txt"
        tessellation.save_to_txt(f"{filename}")

        # original_points = [Point(p[0], p[1]) for p in vor.points]
    else:
        tessellation = Tessellation(txt_file=load_from_file)

    # Plot the original input diagram
    if gui:
        plt.figure()

        tessellation.plot()
        enforce_plot_scale(xmin, xmax, ymin, ymax)
        plt.title(label="Input diagram")
        plt.waitforbuttonpress(0)

    ####################
    # The main part... #
    ####################

    approximation = VoronoiApproximation(tessellation, gui=gui, print_progress=False)

    # Create Voronoi diagram from centroids to compare later on.
    original_approximation = voronoi_tessellation_from_points(
        approximation.generator_points
    )

    # Run the approximation algorithm.
    approximation.do_thingy(
        phi=0.02, iterations_before_reduction=200, omega_reduction=0.02, margin=1
    )

    #########
    # Done. #
    #########

    print(f"Lower bound for omega: {approximation.omega}")

    print(f"om... {approximation.compute_omega_2(approximation.bestimator_points)}")

    if not gui:
        tessellation.plot()
        original_approximation.plot(color="orange")

    # generate new voronoi diagram from final estimator point positions
    final_tess = voronoi_tessellation_from_points(approximation.bestimator_points)
    # final_tess.plot(color='blue')
    enforce_plot_scale(xmin, xmax, ymin, ymax)
    plt.pause(1e-10)

    print(f"Area discrepancy: {calculate_discrepancy(tessellation, final_tess)} %")
    tessellation.plot(color="black")
    final_tess.plot(color="red")
    # enforce_plot_scale(xmin,xmax,ymin,ymax)
    plt.show()

    for p in approximation.generator_points:
        plt.scatter(p.x, p.y, color="red", marker="o")
    # for p in original_points:
    #    plt.scatter(p.x, p.y, color='black', marker='x')

    plt.figure()
    plt.plot(approximation.points_satisfied, color="black")
    plt.title(label="Percentage of label points satisfied over time")
    plt.ylim([0, 1])
    plt.ylabel("% Satisfied label points")
    plt.xlabel("Time step")

    plt.pause(1e-10)
    plt.show()


if __name__ == "__main__":
    main()
