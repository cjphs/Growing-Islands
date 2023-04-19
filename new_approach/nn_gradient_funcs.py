from point import Point
from scipy.spatial import Voronoi
from math import sqrt


def get_region_estimator_point(estimator_points, region_label):
    for p in estimator_points:
        if p.label == region_label:
            return p
    return None


def generate_label_points(vor:Voronoi, omega:float) -> list:
    
    label_points = []
    estimator_points = []

    region_point_count = []

    region_index = -1
    for r in vor.regions:
        region_index += 1
        region_point_count.append(0)

        l = r.copy()

        # exclude -1 index vertices & use length 3 to form bisectors
        if len(l) < 2 or -1 in l:
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
            point = Point(p3[0], p3[1], label=region_index, origin_point_x=p1[0], origin_point_y=p1[1])

            region_point_count[region_index] += 1

            label_points.append(point)

            point_index += 1

        center_x /= len(l)
        center_y /= len(l)

        estimator_points.append(Point(center_x, center_y, region_index))
    
    return [label_points, estimator_points, region_point_count]
