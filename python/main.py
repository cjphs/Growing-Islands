from voronoi_functions import *
from polygon_functions import *
from tessellation import Tessellation
from matplotlib import pyplot as plt
from file_reader import *

from datetime import datetime

from helpers import log

from sympy.geometry import Point2D, Segment2D


if __name__ == "__main__":
    start = datetime.now()



    log("Generating points...")
    points = generate_random_points(20)

    log("Generating Voronoi diagram from points...")
    vor = generate_random_voronoi(points)

    log("Converting Voronoi diagram to regions...")
    regions = voronoi_to_polygons(vor)

    tess = Tessellation(regions)

    log("Checking for neighbors...")
    tess.process_neighbors()

    N = len(tess.regions)

    # Process neighbors
    # save_tessellation('test.txt', tessellation=tessellation)
    log('calculating new cores...')
    cores1 = tess.compute_cores()
    log('calculating new cores...')
    cores2 = tess.compute_cores()
    log('calculating new cores...')
    cores3 = tess.compute_cores()
        
    log("Finished core iteration 4.")

    finish = datetime.now()

    duration = finish - start

    log("Total runtime: ", str(duration))


    plt.figure()
    plot_polygons(tess.regions,style='r-')
    plot_polygons(cores1,style="c--")
    plot_polygons(cores2,style='b--')
    plot_polygons(cores3,style='g--')
    
    for p in points:
        plt.plot(p[0], p[1], 'ro')
    plt.show()
