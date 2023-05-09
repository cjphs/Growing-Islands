from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from input_generation.voronoi_funcs import generate_random_voronoi, voronoi_from_points

from preprocessing import generate_label_points
from nudging import nudge_estimators

from geometry.point import Point

from math import ceil, floor
import sys

import os

from datetime import datetime

def enforce_plot_scale(xmin,xmax,ymin,ymax):
    ax = plt.gca()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

def on_press(event):
    global done
    sys.stdout.flush()
    if event.key == 'x':
        done = True

def get_arg(args, arg_name):
    if arg_name in args:
        return args[args.index(arg_name) + 1]
    return None

def main():
    gui = True

    omega, phi= .002, .0002

    num_points = 20

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

    xmin,xmax = 0,1
    ymin,ymax = 0,1

    show_input_generators = True

    vor = generate_random_voronoi(num_points,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)

    # Plot the original input diagram
    if gui:
        plt.figure()
        voronoi_plot_2d(vor, ax=plt.gca(), line_width=.5,  show_points=show_input_generators, show_vertices=False)
        enforce_plot_scale(xmin,xmax,ymin,ymax)
        plt.title(label="Input diagram")
        plt.waitforbuttonpress(0)

    points = generate_label_points(vor, omega)

    label_points = points[0]
    estimator_points = points[1]

    original_approximation = voronoi_from_points(estimator_points)

    if gui:
        for p in estimator_points:
            plt.plot(p.x, p.y, "b+", alpha=.2)
            p.x = min(max(p.x, xmin), xmax)
            p.y = min(max(p.y, ymin), ymax)

        voronoi_plot_2d(original_approximation, line_colors='orange', line_alpha=0.2, ax=plt.gca(), show_points=False, show_vertices=False)
        enforce_plot_scale(xmin,xmax,ymin,ymax)
        plt.title(label="Centroid approximation")
        plt.waitforbuttonpress(0)

        plt.gcf().canvas.mpl_connect('key_press_event', on_press)
        plt.title(label="Nudging generator approximations...")

    iterations = 0
    points_satisfied = []
    begin = datetime.now()

    done = False
    while(not done):
        nudged = nudge_estimators(estimator_points, label_points, phi, pull=True, push=True)
        iterations += 1

        if not nudged:
            plt.title(label="All label points satisfied!")
            done = True

        if gui:
            for p in estimator_points:
                p.update_plot()

        satisfied_count = 0
        for l in label_points:
            if l.satisfied:
                satisfied_count += 1

        satisfied_percentage = satisfied_count/len(label_points)

        points_satisfied.append(satisfied_percentage)

        percent_bar_length = os.get_terminal_size().columns

        m = floor(satisfied_percentage * percent_bar_length)

        percent_bar = m * "█" + (percent_bar_length - m) * "░"

        progress = f"{percent_bar}"

        sys.stdout.write("\r" + progress)
        sys.stdout.flush()

        if gui:
            plt.pause(1e-10)

    end = datetime.now()

    sys.stdout.write("\r" + f"Finished in {end - begin} ({iterations} iterations)")
    sys.stdout.flush()
    print()

    # generate new voronoi diagram from final estimator point positions
    new_vor = voronoi_from_points(estimator_points)
    voronoi_plot_2d(new_vor, ax=plt.gca(), line_alpha=.5, line_colors='blue')
    enforce_plot_scale(xmin,xmax,ymin,ymax)

    plt.pause(1e-10)

    plt.figure()
    plt.plot(points_satisfied, color='black')
    plt.title(label="Percentage of label points satisfied over time")

    plt.show()


if __name__ == "__main__":
    main()