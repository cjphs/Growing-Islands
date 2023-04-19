from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from random_voronoi import generate_random_voronoi
from nn_gradient_funcs import generate_label_points

from nn_gradient import nudge_estimators

def plot_all(diagram, estimator_points, label_points):
    plt.clf()
    voronoi_plot_2d(diagram, ax=plt.gca())
    for l in label_points:
        l.plot('ro')
    for p in estimator_points:
        p.plot('co')

if __name__ == "__main__":
    vor = generate_random_voronoi(20)

    omega = 0.02
    phi = 0.00025

    points = generate_label_points(vor, omega)
    
    label_points = points[0]
    estimator_points = points[1]

    print('label points: ', label_points)
    print('estimator points: ', estimator_points)

    plot_all(vor, estimator_points, label_points)

    done = False
    while(not done):
        #nudge_estimators(estimator_points, label_points, attract_factor=0.001, repulse_factor=0.0000)
        #plot_points(estimator_points, 'co', alpha=.2)
        #estimator_points = nudge_estimators(estimator_points, label_points, phi)
        nudged = nudge_estimators(estimator_points, label_points, phi)
        plot_all(vor, estimator_points, label_points)

        if not nudged:
            print('all labels satisfied')
            done = True

        #plt.waitforbuttonpress()
        plt.pause(0.001)

    plt.waitforbuttonpress()

    new_vor = Voronoi([[p.x, p.y] for p in estimator_points])
    voronoi_plot_2d(new_vor)

    plt.show()