from geometry import Point, Tessellation
from matplotlib import pyplot as plt


def get_region_generator_point(estimator_points, region_label):
    for p in estimator_points:
        if p.label == region_label:
            return p
    return None


def generate_label_points_from_generators(
    tessellation: Tessellation, generators: list, omega: float
) -> list:
    label_points = []

    region_index = -1
    for region in tessellation.regions:
        region_index += 1

        n = len(region)

        if n < 2 or -1 in region:
            continue

        generator = get_region_generator_point(generators, region_index)

        region_label_points = []

        for point in region:
            corner_x = tessellation.vertices[point].x
            corner_y = tessellation.vertices[point].y

            corner_point = Point(corner_x, corner_y, label=region_index)
            corner_point.origin_point_x = corner_x
            corner_point.origin_point_y = corner_y

            region_label_points.append(corner_point)

        for l in region_label_points:
            delta = (
                generator + generator.direction_to(l) * generator.distance(l) * omega
            )

            l.set_position(delta.x, delta.y)

        label_points.extend(region_label_points)

    return label_points
