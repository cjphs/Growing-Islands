from sympy.geometry import Polygon


class Tessellation:
    def __init__(self, polygons:list=[], neighborhood_dict={}):
        self.polygons = polygons
        self.neighborhood_dict = neighborhood_dict


    def add_polygon(self, poly:Polygon):
        self.polygons.append(poly)
        self.neighborhood_dict[len(self.polygons)] = []
