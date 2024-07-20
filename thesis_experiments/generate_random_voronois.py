import sys
import os
from pathlib import Path
from matplotlib import pyplot as plt

# Get the absolute path of the parent directory
parent_dir = Path(os.getcwd()).parent.absolute()

# Add the parent directory to sys.path
sys.path.append(str(parent_dir))

from growing_islands.geometry import Tessellation
from growing_islands.voronoi import random_voronoi_tessellation

n = 100

for i in range(n):
    tess = random_voronoi_tessellation(num_points=32)
    tess.save_to_txt(f"in/diagrams/voronoi_{i}.txt")
