from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from input_generation.random_voronoi import generate_random_voronoi
from nn_gradient_funcs import generate_label_points

from nn_gradient import nudge_estimators

if __name__ == "__main__":

    omega = 0.01
    phi = 0.00015

    vor = generate_random_voronoi(60)
    voronoi_plot_2d(vor)

    points = generate_label_points(vor, omega)
    
    label_points = points[0]
    estimator_points = points[1]

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