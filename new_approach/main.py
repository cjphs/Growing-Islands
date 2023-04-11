from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, delaunay_plot_2d
from random import uniform as U
from matplotlib import pyplot as plt

from math import sin, cos, atan2, sqrt


class Point:
    def __init__(self, x, y, region=-1):
        self.x, self.y, self.region = x, y, region


def generate_random_points(num_points:int=20) -> list[list[int, int]]:
    points = []
    while(num_points > 0):
        points.append([U(0,1), U(0,1)])
        num_points -= 1
    return points


def generate_voronoi(points) -> Voronoi:
    vor = Voronoi(points)
    return vor


def distance(x1:float, y1:float, x2:float, y2:float) -> float:
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)


def plot_points(points:list, style:str='bo', alpha=1):
    ex = []
    ey = []

    for e in points:
        if len(e) > 0:
            ex.append(e[0])
            ey.append(e[1])
            e[3].set_position((e[0], e[1]))

    plt.plot(ex, ey, style, alpha=alpha)


def generate_label_points(vor:Voronoi, omega:float) -> list:
    
    
    label_points = []
    estimator_points = []

    region_point_count = []

    # pre-processing
    region_index = -1
    for r in vor.regions:
        region_index += 1
        region_point_count.append(0)

        estimator_points.append([])

        l = r.copy()

        print('new region!', r)

        # exclude -1 index vertices & use length 3 to form bisectors
        if len(l) < 3 or -1 in l:
            continue

        center_x = 0
        center_y = 0

        point_index = 0
        for point in l:
            # find points
            p0 = l[(point_index-1) % len(l)]
            p1 = l[point_index]
            p2 = l[(point_index+1) % len(l)]

            print(f'{l}: handling points {p0}, {p1}, {p2}')

            p0 = vor.vertices[p0].copy()
            p1 = vor.vertices[p1].copy()
            p2 = vor.vertices[p2].copy()

            # centroid
            center_x += p1[0]
            center_y += p1[1]

            # p1 is the middle point of the angle, set p1 as origin
            p0[0] -= p1[0]
            p0[1] -= p1[1]

            p2[0] -= p1[0]
            p2[1] -= p1[1]

            # set new point to the middle of p0, p2
            len_p0 = sqrt(p0[0]**2 + p0[1]**2)
            len_p2 = sqrt(p2[0]**2 + p2[1]**2)

            p0 = [p0[0]/len_p0, p0[1]/len_p0]
            p2 = [p2[0]/len_p2, p2[1]/len_p2]

            p3 = [(p0[0] + p2[0])/2, (p0[1] + p2[1])/2]
            len_p3 = sqrt(p3[0]**2 + p3[1]**2)

            p3[0] = p1[0] + omega * p3[0]/len_p3
            p3[1] = p1[1] + omega * p3[1]/len_p3

            # Add correct region as label
            p3.append(region_index)
            p3.append(False)
            p3.append(plt.plot(p3[0], p3[1], 'ro'))
            p3.append(plt.text(p3[0], p3[1], str(region_index)))

            region_point_count[region_index] += 1

            label_points.append(p3)

            point_index += 1

        center_x /= len(l)
        center_y /= len(l)

        estimator_points[region_index] = [center_x, center_y, region_index, plt.text(center_x, center_y, f'{region_index}')]
    
    return [label_points, estimator_points, region_point_count]


def closest_point_in_set(point_x, point_y, points_set):
    closest_point = None
    closest_point_distance = 999999999999

    for _ in points_set:
        if len(_) == 0:
            continue
        
        d = distance(point_x, point_y, _[0], _[1])

        if d < closest_point_distance:
            closest_point = _
            closest_point_distance = d

    return closest_point


def nudge_estimators(estimator_points, label_points, attract_factor, repulse_factor):
    N = len(estimator_points)

    wrong_label_right_region = [[0, 0] for i in range(N)]
    right_label_wrong_region = [[0, 0] for i in range(N)]

    incorrect_count = [[0, 0] for i in range(N)]

    for label_point in label_points:
        region = label_point[2]

        closest_point = closest_point_in_set(label_point[0], label_point[1], estimator_points)

        closest_point_region = closest_point[2]

        label_point[3] = (closest_point_region == region)

        label_point[5].set_text(f'{region}, {closest_point_region}')

        if not p[3]:
            wrong_label_right_region[region][0] += label_point[0]
            wrong_label_right_region[region][1] += label_point[1]
            incorrect_count[region][0] += 1

            right_label_wrong_region[closest_point_region][0] += label_point[0]
            right_label_wrong_region[closest_point_region][1] += label_point[1]
            incorrect_count[closest_point_region][1] += 1

    # Normalize
    # for i in range(N):
    #     if incorrect_count[i][0] > 0:
    #         wrong_label_right_region[i][0] /= incorrect_count[i][0]
    #         wrong_label_right_region[i][1] /= incorrect_count[i][0]
            
    #     if incorrect_count[i][1] > 0:
    #         right_label_wrong_region[i][0] /= incorrect_count[i][1]
    #         right_label_wrong_region[i][1] /= incorrect_count[i][1]

    # shift
    for i in range(N):
        if len(estimator_points[i]) == 0:
            continue

        dx_attract = wrong_label_right_region[i][0] - estimator_points[i][0]
        dy_attract = wrong_label_right_region[i][1] - estimator_points[i][1]
        dl_attract = distance(0, 0, dx_attract , dy_attract )

        dx_repulse = right_label_wrong_region[i][0] - estimator_points[i][0]
        dy_repulse = right_label_wrong_region[i][1] - estimator_points[i][1]
        dl_repulse = distance(0, 0, dx_repulse , dy_repulse )

        if dl_attract != 0:
            dx_attract /= dl_attract
            dy_attract /= dl_attract

        if dl_repulse != 0:
            dx_repulse /= dl_repulse
            dy_repulse /= dl_repulse

        estimator_points[i][0] += attract_factor * dx_attract
        estimator_points[i][1] += attract_factor * dy_attract

        estimator_points[i][0] -= repulse_factor * dx_repulse
        estimator_points[i][1] -= repulse_factor * dy_repulse


if __name__ == "__main__":
    p:list[list] = generate_random_points(num_points=30)
    vor:Voronoi = generate_voronoi(p)

    omega = 0.05
    
    voronoi_plot_2d(vor)

    points = generate_label_points(vor, omega)
    
    label_points = points[0]
    estimator_points = points[1]

    # new_vor = generate_voronoi(estimator_points)
    # voronoi_plot_2d(new_vor)

    num_correct_labels = 0

    plt.ion()

    phi = 0.05

    while(True):
        nudge_estimators(estimator_points, label_points, attract_factor=0.001, repulse_factor=0.0000)
        plot_points(estimator_points, 'co', alpha=.2)
        plt.pause(1e-10)

    for lbl in label_points:
        if lbl[3]:
            plt.plot(lbl[0], lbl[1], 'go')
        else:
            plt.plot(lbl[0], lbl[1], 'ro')


    print(region_point_count)
    print(f'correct labels: {num_correct_labels} out of {len(label_points)} ({len(estimator_points)} estimator points)')

    plt.show()