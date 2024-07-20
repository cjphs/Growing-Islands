import shapely
import shapely.ops
import random
import matplotlib.pyplot as plt

from geometry import Point, Tessellation


def random_voronoi_tessellation(num_points: float = 30) -> Tessellation:
    points = [Point(random.random(), random.random()) for i in range(num_points)]
    return voronoi_tessellation_from_points(points)


def voronoi_tessellation_from_points(points_list: list[Point]) -> Tessellation:
    bound_box = shapely.geometry.Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])

    points = [(p.x, p.y) for p in points_list]

    clip = shapely.Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    voronoi = shapely.ops.voronoi_diagram(
        shapely.geometry.MultiPoint(points), envelope=clip
    )

    def xy_hash_index(x, y):
        return str(x) + "," + str(y)

    vertices_indices = {}

    vertices = []
    regions = []

    vor_regions = list(voronoi.geoms)
    vertex_index = 0

    for r in vor_regions:
        r = r.intersection(bound_box)

        points = list(r.exterior.coords[:-1])

        region = []

        for p in points:
            xy_hash = xy_hash_index(p[0], p[1])

            if xy_hash not in vertices_indices:
                vertices_indices[xy_hash] = vertex_index
                vertex_index += 1

                x, y = float(p[0]), float(p[1])

                vertices.append(Point(x, y))
            region.append(vertices_indices[xy_hash])
        regions.append(region)

    # Sort regions by generator points
    regions_sorted = [[] for i in range(len(regions))]
    for i, p in enumerate(points_list):
        for j, r in enumerate(vor_regions):
            if r.contains(shapely.geometry.Point(p.x, p.y)):
                regions_sorted[i] = regions[j]
                break

    return Tessellation(vertices, regions_sorted)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python voronoi.py <output_txt_file> [--num_points <points=30>] [--show] [--seed <seed>]"
        )
        sys.exit(1)

    output_txt_file = sys.argv[1]

    num_points = 32
    if "--num_points" in sys.argv:
        num_points_index = sys.argv.index("--num_points")
        num_points = int(sys.argv[num_points_index + 1])

    if "--seed" in sys.argv:
        seed_index = sys.argv.index("--seed")
        seed = int(sys.argv[seed_index + 1])
        random.seed(seed)

    tess = random_voronoi_tessellation(num_points=num_points)
    tess.plot()

    tess.save_to_txt(output_txt_file)

    if "--show" in sys.argv:
        plt.show()
