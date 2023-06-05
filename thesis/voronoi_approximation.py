from matplotlib import pyplot as plt
from nudging import nudge_estimators
from preprocessing import generate_label_points, generate_label_points_from_generators, get_region_estimator_point
from input_generation.voronoi_funcs import voronoi_from_points

import sys
import os
from datetime import datetime
from math import floor

from geometry.tessellation import Tessellation
from geometry.point import Point, copy_points_list

from helper_funcs import clamp

from scipy.spatial import voronoi_plot_2d


class VoronoiApproximation:

    def __init__(self, tessellation:Tessellation, gui:bool=False, clamp_to_diagram:bool=True, print_progress:bool=True):
        self.tessellation = tessellation

        self.gui = gui
        self.print_progress = print_progress
        
        self.omega = 1
        self.done = False
        
        self.generator_points = self.tessellation.region_centers()
        self.bestimator_points= self.generator_points

        self.vertex_label_points = generate_label_points(tessellation, 1, gui=False)

        if clamp_to_diagram:
            for p in self.generator_points:
                p.x = clamp(p.x, self.tessellation.xmin, self.tessellation.xmax)
                p.y = clamp(p.y, self.tessellation.ymin, self.tessellation.ymax)

        initial_omega = self.compute_omega_2(self.generator_points)
        print(f"Initial omega: {initial_omega}")


    def on_press(self, event) -> None:
        print(event.key)
        sys.stdout.flush()
        if event.key == 'x':
            self.done = True

    
    def compute_omega(self, points: list[Point]) -> float:
        omega_min, omega_max = 0, 1

        # first, get all points that are within the circle VC

        for i, p in enumerate(points):
            
            region = self.tessellation.regions[p.label]
            c = self.tessellation.centers[p.label]

            for r in region:
                
                v = Point(self.tessellation.vertices[r].x, self.tessellation.vertices[r].y)

                for j, q in enumerate(points):
                    if j == i:
                        continue

                    if v.distance(q) > max(v.distance(p), v.distance(c)):
                        continue

                    top = (q.x**2 + q.y**2) - (p.x**2 + p.y**2) - 2*c.x*(q.x - p.x) - 2*c.y*(q.y - p.y)
                    bottom = (v.x - c.x) * (2*q.x - 2*p.x) + (v.y - c.y)*(2*q.y - 2*p.y)

                    om = top/bottom


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
            c = self.tessellation.centers[p.label]

            for corner_vertex_index in region:
                
                v = Point(
                    self.tessellation.vertices[corner_vertex_index].x,
                    self.tessellation.vertices[corner_vertex_index].y
                )

                for j, q in enumerate(points):
                    if j == i:
                        continue

                    if v.distance(q) > v.distance(p):
                        continue

                    top = (q.x**2 + q.y**2) - (p.x**2 + p.y**2) - 2*p.x*(q.x - p.x) - 2*p.y*(q.y - p.y)
                    bottom = (v.x - p.x) * (2*q.x - 2*p.x) + (v.y - p.y)*(2*q.y - 2*p.y)

                    om = top/bottom

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
            phi:float=.005, 
            iterations_before_reduction:int=100, 
            omega_reduction:float=.05, 
            margin:float=1
        ) -> list[Point]:

        begin = datetime.now()

        if self.gui:
            plt.gcf().canvas.mpl_connect('key_press_event', self.on_press)
        
        self.points_satisfied = []

        highest_satisfied_count = 0
        iterations_since_highest = 0

        original_phi = phi

        self.done = False
        all_labels_satisfied = False

        iterations = 0

        omega = self.compute_omega_2(self.generator_points)
        previous_omega = omega

        force_quit = False

        while not all_labels_satisfied:

            iteration_phi = phi

            while(not self.done):
                # print("NEW ITERATION: ", omega)
                label_points = generate_label_points_from_generators(self.tessellation, self.generator_points, omega, gui=self.gui)

                nudged, satisfied_count = nudge_estimators(
                    self.generator_points, 
                    label_points, 
                    phi, 
                    pull=True, 
                    push=True, 
                    diagram=self.tessellation,
                    gui=self.gui
                )
                iterations += 1

                if not nudged:
                    print('all good man!')
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
                #phi = iteration_phi * (1 - satisfied_percentage)
                # Dampen phi with iterations
                #phi = original_phi * (1-satisfied_percentage) * (1 - iterations_since_highest/iterations_before_reduction)

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
                    for p in self.generator_points:
                        p.update_plot()

                        if self.diagram.point_inside_region(p, p.label):
                            p.plot_element[0].set_markerfacecolor('b')
                        else:
                            p.plot_element[0].set_markerfacecolor('aqua')

                    plt.pause(1e-10)

            # Push omega up if all labels are satisfied
            if all_labels_satisfied and not force_quit:
                previous_omega = omega
                om = self.compute_omega_2(self.generator_points)
                print("up you go!", iterations, omega, om, omega_reduction)

                # omega = om + omega_reduction
                omega = om + (1-om) / 2

                print("new omega: ", omega, om + omega_reduction)
                
                if omega < .98:
                    phi = original_phi * (1 - om)
                    iterations_since_highest = 0
                    highest_satisfied_count = 0
                    all_labels_satisfied = False
                    self.bestimator_points = copy_points_list(self.generator_points)
                    self.done = False

                    print("The show's not over yet. \n")

            # Push omega down if not all labels are satisfied
            elif not all_labels_satisfied:
                if omega - previous_omega > .002:
                    om = (previous_omega + omega)/2
                    print("Down you go!", om)

                    omega = om

                    iterations_since_highest = 0
                    highest_satisfied_count = 0

                    self.done = False

            #if not all_labels_satisfied:
            #    if self.gui:
            #        for l in label_points:
            #                l.plot_element[0].remove()

            #    self.omega -= omega_reduction
            #    self.label_points = generate_label_points(self.tessellation, self.omega)
            #    self.done = False

        end = datetime.now()

        sys.stdout.write("\r" + f"Finished in {end - begin} ({iterations} iterations)")
        sys.stdout.flush()
        print()

        print(self.compute_omega_2(self.bestimator_points))

        return self.bestimator_points