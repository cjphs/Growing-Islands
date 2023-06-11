from matplotlib import pyplot as plt
from nudging import nudge_estimators
from preprocessing import (
    generate_label_points,
    generate_label_points_from_generators,
    get_region_estimator_point,
)

import sys
import os
from datetime import datetime
from math import floor

from geometry import Point, Tessellation, copy_points_list

from helper_funcs import clamp


class VoronoiApproximation:
    def __init__(
        self,
        tessellation: Tessellation,
        gui: bool = False,
        clamp_to_diagram: bool = True,
        print_progress: bool = True,
    ):
        self.tessellation = tessellation

        self.gui = gui
        self.print_progress = print_progress

        self.omega = 1
        self.done = False

        print(self.tessellation.regions)
        self.generator_points = self.tessellation.region_centers()
        self.bestimator_points = self.generator_points

        self.time_taken = None

        self.vertex_label_points = generate_label_points(tessellation, 1, gui=False)

        if clamp_to_diagram:
            for p in self.generator_points:
                p.x = clamp(p.x, self.tessellation.xmin, self.tessellation.xmax)
                p.y = clamp(p.y, self.tessellation.ymin, self.tessellation.ymax)

        initial_omega = self.compute_omega_2(self.generator_points)

    def on_press(self, event) -> None:
        print(event.key)
        sys.stdout.flush()
        if event.key == "x":
            self.done = True

    def compute_omega(self, points: list[Point]) -> float:
        omega_min, omega_max = 0, 1

        # first, get all points that are within the circle VC

        for i, p in enumerate(points):
            region = self.tessellation.regions[p.label]
            c = Point(p.x, p.y)

            for r in region:
                v = Point(
                    self.tessellation.vertices[r].x, self.tessellation.vertices[r].y
                )

                for j, q in enumerate(points):
                    if j == i:
                        continue

                    if v.distance(q) > max(v.distance(p), v.distance(c)):
                        continue

                    top = (
                        (q.x**2 + q.y**2)
                        - (p.x**2 + p.y**2)
                        - 2 * c.x * (q.x - p.x)
                        - 2 * c.y * (q.y - p.y)
                    )
                    bottom = (v.x - c.x) * (2 * q.x - 2 * p.x) + (v.y - c.y) * (
                        2 * q.y - 2 * p.y
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
                        else:
                            print("we got a 0!")

        if omega_max >= omega_min:
            return omega_max
        else:
            return None

    # Compute using the spokes from the generator points instead
    def compute_omega_2(self, points: list[Point]) -> float:
        omega_min, omega_max = 0, 1

        # first, get all points that are within the circle VC

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
                    bottom = (v.x - p.x) * (2 * q.x - 2 * p.x) + (v.y - p.y) * (
                        2 * q.y - 2 * p.y
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
                        else:
                            print("we got a 0!")

        if omega_max >= omega_min:
            return omega_max
        else:
            return None

    def do_thingy(
        self,
        phi: float = 0.005,
        iterations_before_reduction: int = 200,
        omega_reduction: float = 0.05,
        margin: float = 1,
    ) -> list[Point]:
        begin = datetime.now()

        if self.gui:
            plt.gcf().canvas.mpl_connect("key_press_event", self.on_press)

        self.points_satisfied = []

        highest_satisfied_count = 0
        iterations_since_highest = 0

        original_phi = phi

        self.done = False
        all_labels_satisfied = False

        iterations = 0

        force_quit = False

        done = False
        while not done:
            iteration_phi = phi

            omega = self.compute_omega_2(self.generator_points)
            omega_target = omega + (1 - omega) / 2
            phi = original_phi * (1 - omega)

            print(f"[{iterations} previous: {omega}, new: {omega_target}")

            all_labels_satisfied = False

            self.omega = omega

            while not all_labels_satisfied:
                label_points = generate_label_points_from_generators(
                    self.tessellation, self.generator_points, omega_target, gui=self.gui
                )

                nudged, satisfied_count = nudge_estimators(
                    self.generator_points,
                    label_points,
                    phi,
                    pull=True,
                    push=True,
                    diagram=self.tessellation,
                    gui=self.gui,
                )

                satisfied_percentage = satisfied_count / len(label_points)
                self.points_satisfied.append(satisfied_percentage)

                if not nudged:
                    print(f"all good man! satisfied % = {satisfied_percentage}")
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
                        print("omega down! ", omega_target, omega)
                        iterations_since_highest = 0  #

                if omega_target - omega < 0.001:
                    done = True
                    break

                # Dampen phi
                # phi = iteration_phi * (1 - satisfied_percentage)
                # Dampen phi with iterations
                # phi = original_phi * (1-satisfied_percentage) * (1 - iterations_since_highest/iterations_before_reduction)

                # Print progress
                if self.print_progress:
                    percent_bar_length = os.get_terminal_size().columns
                    m = floor(satisfied_percentage * percent_bar_length)
                    percent_bar = m * "█" + (percent_bar_length - m) * "░"
                    progress = f"{percent_bar}"
                    sys.stdout.write("\r" + progress)
                    sys.stdout.flush()

                if self.gui:
                    for p in self.generator_points:
                        p.update_plot()

                        if self.diagram.point_inside_region(p, p.label):
                            p.plot_element[0].set_markerfacecolor("b")
                        else:
                            p.plot_element[0].set_markerfacecolor("aqua")

                    plt.pause(1e-10)

        end = datetime.now()

        self.time_taken = end - begin
        self.iterations = iterations

        sys.stdout.write("\r" + f"Finished in {end - begin} ({iterations} iterations)")
        sys.stdout.flush()
        print()

        return self.bestimator_points
