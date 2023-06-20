import sys
from matplotlib import pyplot as plt

sys.path.append("../thesis")
sys.path.append("./thesis")

from src.discrepancy import calculate_discrepancy, plot_discrepancy
from src.geometry import Tessellation
from src.voronoi import random_voronoi_tessellation, voronoi_tessellation_from_points
from src.voronoi_approximation import VoronoiApproximation

if __name__ == "__main__":
    ...
