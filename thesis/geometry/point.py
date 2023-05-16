from matplotlib import pyplot as plt
from math import sqrt

class Point:
    def __init__(self, x, y, label=-1, origin_point_x=0, origin_point_y=0, plot_element=None):
        self.x, self.y, self.label = x, y, label
        self.origin_point_x = origin_point_x
        self.origin_point_y = origin_point_y
        self.plot_element = plot_element

        self.satisfied = False

    def distance(self, other):
        if type(other) == Point:
            return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        else:
            return None

    def direction_to(self, other):
        dist = self.distance(other)

        dx = (other.x - self.x) / dist
        dy = (other.y - self.y) / dist

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

        return closest_point
        
    def plot(self, style='co'):
        plt.plot(self.x, self.y, style)

    def update_plot(self):
        self.plot_element[0].set_data([self.x], [self.y])
    
    def __str__(self):
        return f"({self.x}, {self.y}, L = {self.label})"