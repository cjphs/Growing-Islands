from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from input_generation.random_voronoi import generate_random_voronoi

from preprocessing import generate_label_points
from nudging import nudge_estimators

from geometry.point import Point

import sys

def voronoi_from_points(points:list[Point]) -> Voronoi:
    return Voronoi([[p.x, p.y] for p in points])

#TODO: #1 force voronoi plot to be in xmin xmax ymin ymax boundary

def enforce_plot_scale(xmin,xmax,ymin,ymax):
    ax = plt.gca()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

done = False

def on_press(event):
    global done
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'x':
        done = True


if __name__ == "__main__":

    omega = .002
    phi = .0002

    num_points = 20

    xmin,xmax = 0,1
    ymin,ymax = 0,1

    show_input_generators = True

    plt.figure()
    
    vor = generate_random_voronoi(num_points,xmin=xmin,xmax=xmax,ymin=ymin,ymax=ymax)

    # Plot the original input diagram
    voronoi_plot_2d(vor, ax=plt.gca(), line_width=.5,  show_points=show_input_generators, show_vertices=False)
    enforce_plot_scale(xmin,xmax,ymin,ymax)
    plt.title(label="Input diagram")
    plt.waitforbuttonpress(0)
    
    points = generate_label_points(vor, omega)

    label_points = points[0]
    estimator_points = points[1]

    original_approximation = voronoi_from_points(estimator_points)

    for p in estimator_points:
        plt.plot(p.x, p.y, "b+", alpha=.2)

    voronoi_plot_2d(original_approximation, line_colors='orange', line_alpha=0.2, ax=plt.gca(), show_points=False, show_vertices=False)
    enforce_plot_scale(xmin,xmax,ymin,ymax)
    plt.title(label="Centroid approximation")
    plt.waitforbuttonpress(0)

    plt.gcf().canvas.mpl_connect('key_press_event', on_press)

    iterations = 0

    plt.title(label="Nudging generator approximations...")

    trajectory_interval = 0

    while(not done):
        nudged = nudge_estimators(estimator_points, label_points, phi, pull=True, push=True)
        iterations += 1

        if not nudged:
            plt.title(label="All label points satisfied!")
            done = True

        for p in estimator_points:
            p.update_plot()

        trajectory_interval -= 1
        if trajectory_interval < 0:
            trajectory_interval = 50

        print(trajectory_interval)

        plt.pause(1e-10)

    # generate new voronoi diagram from final estimator point positions
    new_vor = voronoi_from_points(estimator_points)
    voronoi_plot_2d(new_vor, ax=plt.gca(), line_alpha=.5, line_colors='blue')
    enforce_plot_scale(xmin,xmax,ymin,ymax)

    plt.show()