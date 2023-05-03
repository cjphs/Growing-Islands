from point import Point

class Diagram:
    def __init__(self, vertices:list[Point] = [], edges:list[list[int]] = [], regions:list = []):
        self.vertices = vertices
        # Edges: list of lists of integers where the integers are vertex indices of the vertices list
        self.edges = edges 
        # Regions: List of lists of edges
        self.regions = regions


def scipy_voronoi_to_diagram(vor):
    ...