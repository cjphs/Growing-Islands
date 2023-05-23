from geometry.point import Point
from geometry.diagram import Diagram
from math import sqrt
from matplotlib import pyplot as plt


def get_region_estimator_point(estimator_points, region_label):
    for p in estimator_points:
        if p.label == region_label:
            return p
    return None


def generate_estimator_points(diagram:Diagram) -> list[Point]:
    estimator_points = []

    region_index = -1
    for region in diagram.regions:
        region_index += 1

        n = len(region)

        if n < 2 or -1 in region:
            continue

        center_x = 0
        center_y = 0

        for point in region:
            center_x += diagram.vertices[point].x
            center_y += diagram.vertices[point].y

        center = Point(center_x/n, center_y/n, label=region_index)
        center.plot_element = plt.plot(center.x, center.y, 'bo')
        estimator_points.append(center)
    
    return estimator_points


def generate_label_points(diagram:Diagram, omega:float) -> list:

    label_points = []

    region_index = -1
    for region in diagram.regions:
        region_index += 1

        n = len(region)

        if n < 2 or -1 in region:
            continue

        center_x = 0
        center_y = 0

        region_label_points = []

        for point in region:

            corner_x = diagram.vertices[point].x
            corner_y = diagram.vertices[point].y

            center_x += corner_x
            center_y += corner_y

            corner_point = Point(corner_x, corner_y, label=region_index)
            corner_point.origin_point_x = corner_x
            corner_point.origin_point_y = corner_y
            
            region_label_points.append(corner_point)

        center = Point(center_x/n, center_y/n, label=region_index)

        for l in region_label_points:
            delta = center + center.direction_to(l) * center.distance(l) * omega

            l.set_position(delta.x, delta.y)
            l.plot_element = plt.plot(delta.x, delta.y, 'ro')
        
        label_points.extend(region_label_points)
    
    return label_points
