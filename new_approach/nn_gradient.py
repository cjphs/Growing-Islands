from point import Point
from nn_gradient_funcs import get_region_estimator_point

# Returns true if any estimator was nudged. False -> All labels are okay
def nudge_estimators(estimator_points:list[Point], label_points:list[Point], phi:float):
    N = len(estimator_points)*2
    nudge = [Point(0, 0) for i in range(N)]
    print(N)

    points_nudged = False

    for label_point in label_points:
        closest_estimator = label_point.closest_point_in_list(estimator_points)
        vertex_point = Point(label_point.origin_point_x, label_point.origin_point_y, label=label_point.label)
        
        # Want to push closest_estimator away from label_point
        # Pull label_point's regione estimator closer to label point...
        if closest_estimator.label != label_point.label:
            push_vector = vertex_point.direction_to(closest_estimator) * phi

            label_point_region_estimator_point = get_region_estimator_point(estimator_points, label_point.label)

            pull_vector = label_point_region_estimator_point.direction_to(vertex_point) * phi

            nudge[label_point.label] += pull_vector
            nudge[closest_estimator.label] += push_vector

            points_nudged = True

    # s = ''
    # for n in nudge:
    #     s += str(n)
    # print(s)

    for estimator_point in estimator_points:
        estimator_point.x += nudge[estimator_point.label].x
        estimator_point.y += nudge[estimator_point.label].y

    return points_nudged
    # return estimator_points


            


# Old...
# def nudge_estimators_old(estimator_points, label_points, attract_factor, repulse_factor):
#     N = len(estimator_points)

#     wrong_label_right_region = [[0, 0] for i in range(N)]
#     right_label_wrong_region = [[0, 0] for i in range(N)]

#     incorrect_count = [[0, 0] for i in range(N)]

#     for label_point in label_points:
#         regio = label_point[2]

#         closest_point = closest_point_in_set(label_point[0], label_point[1], estimator_points)

#         closest_point_region = closest_point[2]

#         label_point[3] = (closest_point_region == region)

#         label_point[5].set_text(f'{region}, {closest_point_region}')

#         if not p[3]:
#             wrong_label_right_region[region][0] += label_point[0]
#             wrong_label_right_region[region][1] += label_point[1]
#             incorrect_count[region][0] += 1

#             right_label_wrong_region[closest_point_region][0] += label_point[0]
#             right_label_wrong_region[closest_point_region][1] += label_point[1]
#             incorrect_count[closest_point_region][1] += 1

#     # Normalize
#     # for i in range(N):
#     #     if incorrect_count[i][0] > 0:
#     #         wrong_label_right_region[i][0] /= incorrect_count[i][0]
#     #         wrong_label_right_region[i][1] /= incorrect_count[i][0]
            
#     #     if incorrect_count[i][1] > 0:
#     #         right_label_wrong_region[i][0] /= incorrect_count[i][1]
#     #         right_label_wrong_region[i][1] /= incorrect_count[i][1]

#     # shift
#     for i in range(N):
#         if len(estimator_points[i]) == 0:
#             continue

#         dx_attract = wrong_label_right_region[i][0] - estimator_points[i][0]
#         dy_attract = wrong_label_right_region[i][1] - estimator_points[i][1]
#         dl_attract = distance(0, 0, dx_attract , dy_attract )

#         dx_repulse = right_label_wrong_region[i][0] - estimator_points[i][0]
#         dy_repulse = right_label_wrong_region[i][1] - estimator_points[i][1]
#         dl_repulse = distance(0, 0, dx_repulse , dy_repulse )

#         if dl_attract != 0:
#             dx_attract /= dl_attract
#             dy_attract /= dl_attract

#         if dl_repulse != 0:
#             dx_repulse /= dl_repulse
#             dy_repulse /= dl_repulse

#         estimator_points[i][0] += attract_factor * dx_attract
#         estimator_points[i][1] += attract_factor * dy_attract

#         estimator_points[i][0] -= repulse_factor * dx_repulse
#         estimator_points[i][1] -= repulse_factor * dy_repulse