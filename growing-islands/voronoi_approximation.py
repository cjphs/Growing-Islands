from matplotlib import pyplot as plt
from nudging import nudge_generator_points
from label_points import generate_label_points_from_generators

import sys
import os
from datetime import datetime
from math import floor

from geometry import Point, Tessellation

from helper_funcs import clamp
from voronoi import voronoi_tessellation_from_points


class VoronoiApproximation:
    def __init__(
        self,
        tessellation: Tessellation,
        clamp_to_diagram: bool = True,
        print_progress: bool = True,
    ):
        self.tessellation = tessellation

        self.print_progress = print_progress

        self.done = False

        print(self.tessellation.regions)
        self.generator_points = self.tessellation.region_centers()
        self.bestimator_points = self.generator_points

        self.time_taken = None

        self.vertex_label_points = generate_label_points_from_generators(
            tessellation, self.generator_points, 1
        )

        if clamp_to_diagram:
            for p in self.generator_points:
                p.x = clamp(p.x, self.tessellation.xmin, self.tessellation.xmax)
                p.y = clamp(p.y, self.tessellation.ymin, self.tessellation.ymax)

    # Compute using the spokes from the generator points instead
    def compute_omega(self, points: list[Point]) -> float:
        omega_min, omega_max = 0, 1

        for i, p in enumerate(points):
            region = self.tessellation.regions[p.label]

            for corner_vertex_index in region:
                v = Point(
                    self.tessellation.vertices[corner_vertex_index].x,
                    self.tessellation.vertices[corner_vertex_index].y,
                )

                for j, q in enumerate(points):
                    if j == i:
                        continue

                    if v.distance(q) > v.distance(p):
                        continue

                    top = (
                        (q.x**2 + q.y**2)
                        - (p.x**2 + p.y**2)
                        - 2 * p.x * (q.x - p.x)
                        - 2 * p.y * (q.y - p.y)
                    )
                    bottom = 2 * (v.x - p.x) * (q.x - p.x) + 2 * (v.y - p.y) * (
                        q.y - p.y
                    )

                    if bottom == 0:
                        omega_max = 1
                        continue

                    om = top / bottom

                    if 0 <= om <= 1:
                        if bottom > 0:
                            omega_max = min(om, omega_max)
                        elif bottom < 0:
                            omega_min = max(-om, omega_min)

        if omega_max >= omega_min:
            return omega_max
        else:
            return None

    def start(
        self, phi: float = 0.005, iterations_before_reduction: int = 50
    ) -> list[Point]:
        begin = datetime.now()

        self.points_satisfied = []

        highest_satisfied_count = 0
        iterations_since_highest = 0

        original_phi = phi

        self.done = False
        all_labels_satisfied = False

        iterations = 0

        done = False
        while not done:
            omega = self.compute_omega(self.generator_points)
            omega_target = omega + (1 - omega) / 2
            phi = original_phi * (1 - omega)

            print(f"[{iterations} previous: {omega}, new: {omega_target}")

            all_labels_satisfied = False

            self.omega = omega

            while not all_labels_satisfied:
                label_points = generate_label_points_from_generators(
                    self.tessellation, self.generator_points, omega_target
                )

                nudged, satisfied_count = nudge_generator_points(
                    self.generator_points,
                    label_points,
                    phi,
                    pull=True,
                    push=True,
                )

                satisfied_percentage = satisfied_count / len(label_points)
                self.points_satisfied.append(satisfied_percentage)

                if not nudged:
                    print(f"All labels satisfied!")
                    all_labels_satisfied = True
                    break

                iterations += 1
                if satisfied_count > highest_satisfied_count:
                    highest_satisfied_count = satisfied_count
                    iterations_since_highest = 0
                else:
                    iterations_since_highest += 1
                    if iterations_since_highest >= iterations_before_reduction:
                        omega_target = (omega_target + omega) / 2
                        print("Omega reduction", omega_target, "->", omega)
                        iterations_since_highest = 0

                if omega_target - omega < 0.001:
                    done = True
                    break

                # Print progress
                if self.print_progress:
                    percent_bar_length = os.get_terminal_size().columns
                    m = floor(satisfied_percentage * percent_bar_length)
                    percent_bar = m * "█" + (percent_bar_length - m) * "░"
                    progress = f"{percent_bar}"
                    sys.stdout.write("\r" + progress)
                    sys.stdout.flush()

                    plt.pause(1e-10)

        end = datetime.now()

        self.time_taken = end - begin
        self.iterations = iterations

        sys.stdout.write("\r" + f"Finished in {end - begin} ({iterations} iterations)")
        sys.stdout.flush()
        print()

        return self.generator_points
