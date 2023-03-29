from sympy.geometry import Polygon, Line
from polygon_functions import polygon_intersection
from helpers import log

class Tessellation:
    def __init__(self, regions:list=[], neighborhood_dict={}):
        self.regions= regions
        self.neighborhood_dict = neighborhood_dict
        self.cores = regions.copy()

        # [line object, index i, index j]
        self.edges = []


    def add_region(self, region:Polygon):

        self.regions.append(region)
        self.neighborhood_dict[len(self.polygons)] = []
        self.cores.append(region.copy())

    
    # def compute_cores(self):
    #     new_cores = []

    #     for i in range(0, len(self.regions)):
    #         core = self.cores[i].copy()

    #         for other in self.neighborhood_dict[i]:
                
    #             l = Line(other['edge'].p1, other['edge'].p2)
    #             reflection = self.cores[other['index']].reflect(l)

    #             core = polygon_intersection(core, reflection)

    #         new_cores.append(core)

    #     self.cores = new_cores
        
    #     return self.cores.copy()
    
    def compute_cores(self):
        new_cores = [None for i in range(0, len(self.cores))]

        for e in self.edges:
            region1_core = self.cores[e[1]]
            region2_core = self.cores[e[2]]

            region1_reflect = region1_core.reflect(e[0])
            region2_reflect = region2_core.reflect(e[0])

            new_cores[e[1]] = polygon_intersection(region1_core, region2_reflect)
            new_cores[e[2]] = polygon_intersection(region2_core, region1_reflect)

        self.cores = new_cores

        return self.cores.copy()


    def process_neighbors(self):
        N = len(self.regions)

        for i in range(0, N):

            self.neighborhood_dict[i] = []

            region = self.regions[i]

            for j in range(0, N):
                if i == j:
                    continue
            
                else:
                    other = self.regions[j]

                    log(f"Testing polygon {i} on polygon {j}")

                    intersect = polygon_intersection(region, other)

                    if intersect != []:
                        log("Segment found: ", intersect)
                        self.neighborhood_dict[i].append({'index': j, 'region':other, 'edge':intersect[0]})
                        line = Line(intersect[0].p1, intersect[0].p2)
                        
                        self.edges.append([line, i, j])
                    else:
                        log("No intersection.")
