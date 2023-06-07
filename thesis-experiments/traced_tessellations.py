import sys
from matplotlib import pyplot as plt

sys.path.append("../thesis")
sys.path.append("./thesis")

from thesis.discrepancy import calculate_discrepancy, plot_discrepancy
from thesis.geometry import Tessellation
from thesis.voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from thesis.voronoi_approximation import VoronoiApproximation

if __name__ == "__main__":
    ...
