from geometry.point import Point
from matplotlib import pyplot as plt

from scipy.spatial import Voronoi

class Diagram:
    def __init__(
            self, 
            vertices:list[Point] = [],
            regions:list = [], 
            voronoi:Voronoi=None, 
            txt_file:str=None,
            xmin:float=0,
            xmax:float=1,
            ymin:float=0,
            ymax:float=1
        ):

        self.vertices = vertices
        self.regions = regions

        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax

        if voronoi is not None and txt_file is not None:
            raise("Diagram can only be voronoi or txt_file, but not both!")

        if voronoi is not None:
            self.load_from_scipy_voronoi(voronoi)
        elif txt_file is not None:
            self.load_from_txt(txt_file)

    def point_inside_region(self, point:Point, region_index:int) -> bool:
        region = self.regions[region_index]
        
        pos = 0
        neg = 0

        for i in range(len(region)):
            j = (i+1)%len(region)
            e1 = self.vertices[region[i]]
            e2 = self.vertices[region[j]]

            x1, y1 = e1.x, e1.y
            x2, y2 = e2.x, e2.y

            if point.x == x1 and point.y == y1:
                return True

            #Compute the cross product
            d = (point.x - x1)*(y2 - y1) - (point.y - y1)*(x2 - x1)

            if (d > 0):
                pos += 1
            if (d < 0):
                neg += 1

            # If the sign changes, then point is outside
            if (pos > 0 and neg > 0):
                return False
            
        return True

    def save_to_txt(self, txt_file:str):
        with open(txt_file, "w") as f:
            for v in self.vertices:
                f.write(f"{v.x} {v.y}\n")
            for r in self.regions:
                for i in r:
                    f.write(f"{i} ")
                f.write("\n")

    def load_from_txt(self, txt_file:str):
        with open(txt_file, "r") as f:
            for l in f.readlines():
                print(l)
                if l == "\n" or l == "" or l == " ":
                    continue
                if l[0] == "#":
                    continue
                
                l = l.replace("\n", "").strip()
                l = l.split(" ")
                if len(l) == 2:
                    x, y = l
                    self.vertices.append(Point(float(x), float(y)))
                elif len(l) > 2:
                    print(l)
                    self.regions.append([int(i) for i in l if i != ""])

        print(f"Loaded {len(self.vertices)} vertices and {len(self.regions)} regions from {txt_file}.")

    def load_from_scipy_voronoi(self, vor):
        self.vertices = [Point(v[0], v[1]) for v in vor.vertices]
        self.regions = vor.regions

    def plot(self):
        for r in self.regions:
            for i in range(len(r)):
                if r[i] == -1 or r[(i+1)%len(r)] == -1:
                    continue
                v1 = self.vertices[r[i]]
                v2 = self.vertices[r[(i+1)%len(r)]]
                plt.plot([v1.x, v2.x], [v1.y, v2.y], '-', linewidth=.5, color='black')
