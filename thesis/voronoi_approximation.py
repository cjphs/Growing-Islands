from matplotlib import pyplot as plt
from nudging import nudge_estimators
from preprocessing import generate_estimator_points, generate_label_points

import sys
import os
from datetime import datetime
from math import floor

from geometry.diagram import Diagram
from geometry.point import Point

from helper_funcs import clamp


class VoronoiApproximation:

    def __init__(self, diagram:Diagram, gui:bool=False, clamp_to_diagram:bool=True):
        self.diagram = diagram

        self.gui = gui
        self.print_progress = True
        
        self.omega = 1
        self.done = False
        
        self.estimator_points = generate_estimator_points(diagram, gui=gui)

        if clamp_to_diagram:
            for p in self.estimator_points:
                p.x = clamp(p.x, self.diagram.xmin, self.diagram.xmax)
                p.y = clamp(p.y, self.diagram.ymin, self.diagram.ymax)


    def on_press(self, event) -> None:
        print(event.key)
        sys.stdout.flush()
        if event.key == 'x':
            self.done = True


    def do_thingy(
            self, 
            phi:float=.005, 
            iterations_before_reduction:int=100, 
            omega_reduction:float=.05, 
            margin:float=1
        ) -> list[Point]:

        begin = datetime.now()
        self.points_satisfied = []

        if self.gui:
            plt.gcf().canvas.mpl_connect('key_press_event', self.on_press)
        
        highest_satisfied_count = 0
        iterations_since_highest = 0

        original_phi = phi

        self.done = False
        all_labels_satisfied = False

        iterations = 0

        while not all_labels_satisfied:

            label_points = generate_label_points(self.diagram, self.omega, gui=self.gui)

            while(not self.done):
                nudged, satisfied_count = nudge_estimators(
                    self.estimator_points, 
                    label_points, 
                    phi, 
                    pull=True, 
                    push=True, 
                    diagram=self.diagram,
                    gui=self.gui
                )
                iterations += 1

                if not nudged:
                    self.done = True

                if satisfied_count > highest_satisfied_count:
                    highest_satisfied_count = satisfied_count
                    iterations_since_highest = 0
                else:
                    iterations_since_highest += 1
                    if iterations_since_highest >= iterations_before_reduction:
                        self.done = True

                satisfied_percentage = satisfied_count/len(label_points)

                # Dampen phi
                phi = original_phi * (1-satisfied_percentage)

                if satisfied_percentage >= margin:
                    all_labels_satisfied = True
                    self.done = True

                self.points_satisfied.append(satisfied_percentage)

                # Print progress
                if self.print_progress:
                    percent_bar_length = os.get_terminal_size().columns
                    m = floor(satisfied_percentage * percent_bar_length)
                    percent_bar = m * "█" + (percent_bar_length - m) * "░"
                    progress = f"{percent_bar}"
                    sys.stdout.write("\r" + progress)
                    sys.stdout.flush()

                if self.gui:
                    for p in self.estimator_points:
                        p.update_plot()

                        if self.diagram.point_inside_region(p, p.label):
                            p.plot_element[0].set_markerfacecolor('b')
                        else:
                            p.plot_element[0].set_markerfacecolor('aqua')

                    plt.pause(1e-10)

            if not all_labels_satisfied:
                if self.gui:
                    for l in label_points:
                            l.plot_element[0].remove()

                self.omega -= omega_reduction
                self.label_points = generate_label_points(self.diagram, self.omega)
                self.done = False

        end = datetime.now()

        sys.stdout.write("\r" + f"Finished in {end - begin} ({iterations} iterations)")
        sys.stdout.flush()
        print()

        return self.estimator_points