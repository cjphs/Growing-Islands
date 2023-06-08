import sys
from matplotlib import pyplot as plt

sys.path.append("../thesis")
sys.path.append("./thesis")

from thesis.geometry import Tessellation
from thesis.voronoi import random_voronoi_tessellation

n = 100

for i in range(n):
    tess = random_voronoi_tessellation(num_points=32)
    tess.save_to_txt(f"in/diagrams/voronoi_{i}.txt")
