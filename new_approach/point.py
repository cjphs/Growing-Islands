from matplotlib import pyplot as plt
from math import sqrt

class Point:
    def __init__(self, x, y, label=-1):
        self.x, self.y, self.label = x, y, label

    def distance(self, other):
        if type(other) == Point:
            return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        else:
            return None
        
    def closest_point_in_list(self, points_list):
        closest_point = None
        closest_point_distance = 999999999999

        for _ in points_list:
            if len(_) == 0:
                continue
            
            d = self.distance(_)

            if d < closest_point_distance:
                closest_point = _
                closest_point_distance = d

        return closest_point
        
    def plot(self, style='co'):
        plt.plot(self.x, self.y, style)