from matplotlib import pyplot as plt
from math import sqrt

from scipy.spatial import Voronoi


class Point:
    def __init__(
        self, x, y, label=-1, origin_point_x=0, origin_point_y=0, plot_element=None
    ):
        self.x, self.y, self.label = x, y, label
        self.origin_point_x = origin_point_x
        self.origin_point_y = origin_point_y
        self.plot_element = plot_element

        self.satisfied = False

    def distance(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def direction_to(self, other, normalize=True):
        dist = self.distance(other)

        dx = other.x - self.x
        dy = other.y - self.y

        if normalize:
            dx /= dist
            dy /= dist

        return Point(dx, dy)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.label)

    def __mul__(self, value):
        return Point(self.x * value, self.y * value, self.label)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def closest_point_in_list(self, points_list):
        closest_point = None
        closest_point_distance = 999999999999

        for _ in points_list:
            d = self.distance(_)

            if d < closest_point_distance:
                closest_point = _
                closest_point_distance = d

            if d == closest_point_distance and self.label == _.label:
                closest_point = _
                closest_point_distance = d

        return closest_point

    def plot(self, style="co"):
        plt.plot(self.x, self.y, style)

    def update_plot(self):
        self.plot_element[0].set_data([self.x], [self.y])

    def __str__(self):
        return f"({self.x}, {self.y}, L = {self.label})"


class Tessellation:
    def __init__(
        self,
        vertices: list[Point] = [],
        regions: list = [],
        voronoi: Voronoi = None,
        txt_file: str = None,
        xmin: float = 0,
        xmax: float = 1,
        ymin: float = 0,
        ymax: float = 1,
    ):
        self.regions = regions
        self.vertices = vertices

        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax

        if voronoi is not None and txt_file is not None:
            raise ("Diagram can only be voronoi or txt_file, but not both!")

        if voronoi is not None:
            self.load_from_scipy_voronoi(voronoi)
        elif txt_file is not None:
            self.load_from_txt(txt_file)

        # self.centers = self.region_centers()

    def region_centers(self) -> list[Point]:
        centers = []
        for i, region in enumerate(self.regions):
            n = len(region)

            center_x = 0
            center_y = 0

            for point in region:
                center_x += self.vertices[point].x
                center_y += self.vertices[point].y

            center = Point(center_x / n, center_y / n, label=i)
            centers.append(center)
        return centers

    def point_inside_region(self, point: Point, region_index: int) -> bool:
        region = self.regions[region_index]

        pos = 0
        neg = 0

        for i in range(len(region)):
            j = (i + 1) % len(region)
            e1 = self.vertices[region[i]]
            e2 = self.vertices[region[j]]

            x1, y1 = e1.x, e1.y
            x2, y2 = e2.x, e2.y

            if point.x == x1 and point.y == y1:
                return True

            # Compute the cross product
            d = (point.x - x1) * (y2 - y1) - (point.y - y1) * (x2 - x1)

            if d > 0:
                pos += 1
            if d < 0:
                neg += 1

            # If the sign changes, then point is outside
            if pos > 0 and neg > 0:
                return False

        return True

    def save_to_txt(self, txt_file: str):
        with open(txt_file, "w") as f:
            for v in self.vertices:
                f.write(f"{v.x} {v.y}\n")
            for r in self.regions:
                for i in r:
                    f.write(f"{i} ")
                f.write("\n")

    def load_from_txt(self, txt_file: str):
        self.vertices = []
        self.regions = []
        i = -1
        with open(txt_file, "r") as f:
            for l in f.readlines():
                i += 1

                l = l.replace("\n", "").strip()
                l = l.split(" ")
                if len(l) == 2:
                    x, y = l
                    self.vertices.append(Point(float(x), float(y)))
                elif len(l) > 2:
                    self.regions.append([int(i) for i in l if i != ""])

        print(
            f"Loaded {len(self.vertices)} vertices and {len(self.regions)} regions from {txt_file}."
        )

    def load_from_scipy_voronoi(self, vor):
        self.vertices = [Point(v[0], v[1]) for v in vor.vertices]
        self.regions = []
        for r in vor.regions:
            if len(r) < 2 or -1 in r:
                continue
            self.regions.append(r)

    def plot(
        self,
        color: str = "black",
        linewidth: float = 0.5,
        name="",
        show_axes=False,
        show_region_indices=False,
    ):
        for i, r in enumerate(self.regions):
            cx, cy = 0, 0
            for j in range(len(r)):
                v1 = self.vertices[r[j]]
                v2 = self.vertices[r[(j + 1) % len(r)]]
                plt.plot(
                    [v1.x, v2.x], [v1.y, v2.y], "-", linewidth=linewidth, color=color
                )

                cx += v1.x
                cy += v1.y

            cx /= len(r)
            cy /= len(r)

        if not show_axes:
            plt.xticks([])
            plt.yticks([])

        if show_region_indices:
            plt.text(cx, cy, str(i), fontsize=8, color=color)


def copy_points_list(points_list: list):
    return [Point(p.x, p.y, p.label) for p in points_list]
