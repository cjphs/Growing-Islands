from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

from random_voronoi import generate_random_voronoi
from nn_gradient_funcs import generate_label_points

if __name__ == "__main__":
    vor = generate_random_voronoi(20)

    omega = 0.01
    
    voronoi_plot_2d(vor)

    points = generate_label_points(vor, omega)
    
    label_points = points[0]
    estimator_points = points[1]

    print('label points: ', label_points)
    print('estimator points: ', estimator_points)

    for l in label_points:
        l.plot('ro')

    for e in estimator_points:
        e.plot('co')

    plt.ion()

    phi = 0.05

    while(True):
        #nudge_estimators(estimator_points, label_points, attract_factor=0.001, repulse_factor=0.0000)
        #plot_points(estimator_points, 'co', alpha=.2)
        plt.pause(1e-10)

    for lbl in label_points:
        if lbl[3]:
            plt.plot(lbl[0], lbl[1], 'go')
        else:
            plt.plot(lbl[0], lbl[1], 'ro')


    print(region_point_count)
    print(f'correct labels: {num_correct_labels} out of {len(label_points)} ({len(estimator_points)} estimator points)')

    plt.show()