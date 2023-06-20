import sys
from matplotlib import pyplot as plt

sys.path.append("../thesis")
sys.path.append("./thesis")

from voronoi_likeness.discrepancy import calculate_discrepancy, plot_discrepancy
from voronoi_likeness.geometry import Tessellation
from voronoi_likeness.voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from voronoi_likeness.voronoi_approximation import VoronoiApproximation

if __name__ == "__main__":
    ...
