from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from input_generation.random_voronoi import generate_random_voronoi

from preprocessing import generate_label_points
from nudging import nudge_estimators

from geometry.point import Point

def voronoi_from_points(points:list[Point]) -> Voronoi:
    return Voronoi([[p.x, p.y] for p in points])

#TODO: #1 force voronoi plot to be in xmin xmax ymin ymax boundary

if __name__ == "__main__":

    omega = .001
    phi = .00025

    vor = generate_random_voronoi(20,xmin=0,xmax=1,ymin=0,ymax=1)
    voronoi_plot_2d(vor)

    points = generate_label_points(vor, omega)

    label_points = points[0]
    estimator_points = points[1]

    original_approximation = voronoi_from_points(estimator_points)
    voronoi_plot_2d(original_approximation, line_colors='orange', line_alpha=0.4, ax=plt.gca(), show_vertices=False, show_points=False)

    iterations = 0

    done = False
    while(not done):
        nudged = nudge_estimators(estimator_points, label_points, phi, pull=True, push=True)
        iterations += 1

        if not nudged:
            print(f'all labels satisfied after {iterations} iterations')
            done = True

        for p in estimator_points:
            p.update_plot()

        plt.pause(0.001)

    print('uh?')
    # generate new voronoi diagram from final estimator point positions
    new_vor = voronoi_from_points(estimator_points)
    voronoi_plot_2d(new_vor, ax=plt.gca(), line_alpha=.5, line_colors='blue')

    plt.show()