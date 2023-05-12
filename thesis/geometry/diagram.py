from geometry.point import Point
from matplotlib import pyplot as plt

class Diagram:
    def __init__(self, vertices:list[Point] = [], edges:list[list[int]] = [], regions:list = [], voronoi=None, txt_file:str = None):
        self.vertices = vertices
        self.regions = regions

        if voronoi is not None:
            self.load_from_scipy_voronoi(voronoi)
        elif txt_file is not None:
            self.load_from_txt(txt_file)
    
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
