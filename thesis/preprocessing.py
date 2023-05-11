from geometry.point import Point
from scipy.spatial import Voronoi
from math import sqrt
from matplotlib import pyplot as plt


def get_region_estimator_point(estimator_points, region_label):
    for p in estimator_points:
        if p.label == region_label:
            return p
    return None


def generate_label_points323(vor:Voronoi, omega:float) -> list:

    label_points = []
    estimator_points = []

    region_index = -1
    for r in vor.regions:
        region_index += 1

        l = r.copy()

        # exclude -1 index vertices & use length 3 to form bisectors
        if len(l) < 2 or -1 in l:
            continue

        center_x = 0
        center_y = 0

        points_temp = []

        # first find center
        for point in l:

            corner_x = vor.vertices[point][0]
            corner_y = vor.vertices[point][1]
            
            center_x += vor.vertices[point][0]
            center_y += vor.vertices[point][1]
            
            points_temp.append(Point(corner_x, corner_y, label=region_index))
        
        center = Point(center_x/len(l), center_y/len(l), label=region_index)
        center.plot_element = plt.plot(center.x, center.y, 'bo')
        estimator_points.append(center)

        for lbl in points_temp:
            delta = center + center.direction_to(lbl) * center.distance(lbl) * omega

            delta.origin_point_x = lbl.x
            delta.origin_point_y = lbl.y
            delta.plot_element = plt.plot(delta.x, delta.y, 'ro')
            delta.label = region_index

            label_points.append(delta)

    print(len(label_points), len(estimator_points))

    return label_points, estimator_points



def generate_label_points(vor:Voronoi, omega:float) -> list:

    label_points = []
    estimator_points = []

    region_index = -1
    for region in vor.regions:
        region_index += 1

        n = len(region)

        if n < 2 or -1 in region:
            continue

        center_x = 0
        center_y = 0

        region_label_points = []

        for point in region:

            corner_x = vor.vertices[point][0]
            corner_y = vor.vertices[point][1]

            center_x += corner_x
            center_y += corner_y

            corner_point = Point(corner_x, corner_y, label=region_index)
            corner_point.origin_point_x = corner_x
            corner_point.origin_point_y = corner_y
            
            region_label_points.append(corner_point)
        
        center = Point(center_x/n, center_y/n, label=region_index)
        center.plot_element = plt.plot(center.x, center.y, 'bo')
        estimator_points.append(center)

        for l in region_label_points:
            delta = center + center.direction_to(l) * center.distance(l) * omega

            l.set_position(delta.x, delta.y)
            l.plot_element = plt.plot(delta.x, delta.y, 'ro')
        
        label_points.extend(region_label_points)
    
    return label_points, estimator_points


# Keep for legacy reasons
def generate_label_points_old(vor:Voronoi, omega:float) -> list:
    
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
            point.plot_element = plt.plot(p3[0], p3[1], 'ro')

            region_point_count[region_index] += 1

            label_points.append(point)

            point_index += 1

        center_x /= len(l)
        center_y /= len(l)

        point = Point(center_x, center_y, region_index)
        point.plot_element = plt.plot(center_x, center_y, 'co')
        estimator_points.append(point)
    
    return label_points, estimator_points
