from matplotlib import pyplot as plt
from nudging import nudge_estimators
from preprocessing import generate_estimator_points, generate_label_points
from input_generation.voronoi_funcs import voronoi_from_points

import sys
import os
from datetime import datetime
from math import floor

from geometry.diagram import Diagram
from geometry.point import Point

from helper_funcs import clamp

from scipy.spatial import voronoi_plot_2d


class VoronoiApproximation:

    def __init__(self, diagram:Diagram, gui:bool=False, clamp_to_diagram:bool=True):
        self.diagram = diagram

        self.gui = gui
        self.print_progress = True
        
        self.omega = 1
        self.done = False
        
        self.estimator_points = self.diagram.region_centers()

        self.vertex_label_points = generate_label_points(diagram, 1, gui=False)

        if clamp_to_diagram:
            for p in self.estimator_points:
                p.x = clamp(p.x, self.diagram.xmin, self.diagram.xmax)
                p.y = clamp(p.y, self.diagram.ymin, self.diagram.ymax)

        initial_omega = self.compute_omega(self.estimator_points)
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

            print(p.label)
            print(len(self.diagram.regions))
            print(len(self.diagram.centers))
            
            region = self.diagram.regions[p.label]
            c = self.diagram.centers[p.label]

            print('lets check this shit')
            print(self.diagram.point_inside_region(p, p.label))
            print(self.diagram.point_inside_region(c, p.label))

            for r in region:
                
                v = Point(self.diagram.vertices[r].x, self.diagram.vertices[r].y)

                for j, q in enumerate(points):
                    if j == i:
                        continue

                    if v.distance(q) > max(v.distance(p), v.distance(c)):
                        continue
                    
                    top = p.x * (p.x/2 - c.x) + p.y * (p.y/2 - c.y) + q.x * (c.x - q.x/2) + q.y * (c.y - q.y/2)
                    
                    top = (p.x**2 + p.y**2 - q.x**2 - q.y**2)/2 + c.x * (q.x - p.x) + c.y * (q.y - p.y)
                    bottom = (v.x - c.x) * (p.x - q.x) + (v.y - c.y) * (p.y - q.y)

                    top = (q.x**2 + q.y**2) - (p.x**2 + p.y**2) - 2*c.x*(q.x - p.x) - 2*c.y*(q.y - p.y)
                    bottom = (v.x - c.x) * (2*q.x - 2*p.x) + (v.y - c.y)*(2*q.y - 2*p.y)

                    om = top/bottom

                    print(f"{top}/{bottom} = {om}")

                    if 0 <= om <= 1:
                        if bottom > 0:
                            omega_max = min(om, omega_max)
                        elif bottom < 0:
                            omega_min = max(-om, omega_min)
                        else:
                            print("we got a 0!")

        print(omega_min, omega_max)
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

                # vor = voronoi_from_points(self.estimator_points)
                # ax = plt.gca()
                # ax.set_xlim([0, 1])
                # ax.set_ylim([0, 1])
                # f = voronoi_plot_2d(vor, ax=ax, show_points=False, show_vertices=False)
                # f.savefig(f"vor_gif/voronoi_{iterations}.png")
                # plt.close(f)

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