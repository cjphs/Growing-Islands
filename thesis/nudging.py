from geometry.point import Point
from preprocessing import get_region_estimator_point

# Returns true if any estimator was nudged. False -> All labels are okay
def nudge_estimators(
        estimator_points:list[Point],
        label_points:list[Point],
        phi:float,
        pull:bool=True,
        push:bool=False,
        diagram=None,
        gui:bool=False
    ):
    
    N = len(estimator_points)*2
    nudge = [Point(0, 0) for i in range(N)]

    points_nudged = False

    satisfied_count = 0

    for label_point in label_points:
        closest_estimator = label_point.closest_point_in_list(estimator_points)
        vertex_point = Point(label_point.origin_point_x, label_point.origin_point_y, label=label_point.label)
        vertex_point = label_point

        if closest_estimator.label != label_point.label:

            label_point_region_estimator_point = get_region_estimator_point(estimator_points, label_point.label)

            if pull:
                pull_vector = label_point_region_estimator_point.direction_to(vertex_point, normalize=False) * phi
                nudge[label_point.label] += pull_vector
            if push:
                push_vector = vertex_point.direction_to(closest_estimator, normalize=False) * phi
                nudge[closest_estimator.label] += push_vector

            points_nudged = True

            label_point.satisfied = False
            if gui:
                label_point.plot_element[0].set_markerfacecolor('r')
        else:
            label_point.satisfied = True
            satisfied_count += 1
            if gui:
                label_point.plot_element[0].set_markerfacecolor('lime')


    for estimator_point in estimator_points:
        test_point = Point(
            estimator_point.x + nudge[estimator_point.label].x,
            estimator_point.y + nudge[estimator_point.label].y
        )

        #if diagram.point_inside_region(test_point, estimator_point.label):
        estimator_point.x = test_point.x
        estimator_point.y = test_point.y

    return points_nudged, satisfied_count