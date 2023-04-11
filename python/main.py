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
    points = generate_random_points(33)

    log("Generating Voronoi diagram from points...")
    vor = generate_random_voronoi(points)

    log("Converting Voronoi diagram to regions...")
    regions:list[Polygon] = voronoi_to_polygons(vor)

    cleaned_regions = []

    for region in regions:
        xmin = region.bounds[0]
        ymin = region.bounds[1]
        xmax = region.bounds[2]
        ymax = region.bounds[3]

        if xmin >= 0 and xmax <= 1 and ymin >= 0 and ymax <= 1:
            cleaned_regions.append(region)
    regions = cleaned_regions

    tess = Tessellation(regions)

    plt.ion()
    plt.show()

    #voronoi_plot_2d(vor)
    #plt.pause(1e-10)

    log("Checking for neighbors...")
    tess.process_neighbors()

    for p in points:
        plt.plot(p[0], p[1], 'ro')
    plot_polygons(tess.regions,style='r-')
    plt.pause(1e-10)

    N = len(tess.regions)

    num_core_iterations = 3
    core_iterations = []

    c_cols = ['b', 'c', 'c', 'c', 'c']
    i = 0
    while(num_core_iterations > 0):
        print('begin iteration ' + str(num_core_iterations) + ' ...')
        core_iterations.append(tess.compute_cores())
        print('finished iteration')
        num_core_iterations -= 1

        plot_polygons(core_iterations[i],style=f"{c_cols[i]}--")
        i += 1

    log("Finished core iteration 4.")

    finish = datetime.now()

    duration = finish - start

    log("Total runtime: ", str(duration))
        
    

    plt.ioff()
    plt.show()
