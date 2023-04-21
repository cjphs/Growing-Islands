from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from input_generation.random_voronoi import generate_random_voronoi
from nn_gradient_funcs import generate_label_points

from geometry.point import Point

from nn_gradient import nudge_estimators

def voronoi_from_points(points:list[Point]) -> Voronoi:
    return Voronoi([[p.x, p.y] for p in points])

if __name__ == "__main__":

    omega = 1
    phi = .025

    vor = generate_random_voronoi(20,xmin=0,xmax=100,ymin=0,ymax=100)
    voronoi_plot_2d(vor)

    points = generate_label_points(vor, omega)

    label_points = points[0]
    estimator_points = points[1]

    original_approximation = voronoi_from_points(estimator_points)
    voronoi_plot_2d(original_approximation, line_colors='orange', line_alpha=0.4, ax=plt.gca(), show_vertices=False, show_points=False)

    done = False
    while(not done):
        nudged = nudge_estimators(estimator_points, label_points, phi, pull=True, push=True)

        if not nudged:
            print('all labels satisfied')
            done = True

        for p in estimator_points:
            p.update_plot()

        #plt.waitforbuttonpress()
        plt.pause(0.001)

    plt.waitforbuttonpress()

    # generate new voronoi diagram from final estimator point positions
    new_vor = Voronoi([[p.x, p.y] for p in estimator_points])
    voronoi_plot_2d(new_vor, ax=plt.gca(), line_alpha=.25)

    plt.show()