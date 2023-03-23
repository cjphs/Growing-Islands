from voronoi_functions import *
from polygon_functions import *
from tessellation import Tessellation
from matplotlib import pyplot as plt
from file_reader import *

from datetime import datetime

start_time = datetime.now()

def log(*msg):
    global start_time

    current_time = datetime.now()
    s = ''
    for _ in msg:
        s += f'{_}  '
    ts = '%s' % str(current_time - start_time).split('.')[0]
    print(f"{ts} - {s}")
    last_time = current_time


def format_time(t:datetime):
    return t.strftime("%H:%M:%S")


if __name__ == "__main__":
    start = datetime.now()

    log("Generating points...")
    points = generate_random_points(20)

    log("Generating Voronoi diagram from points...")
    vor = generate_random_voronoi(points)

    log("Converting Voronoi diagram to regions...")
    regions = voronoi_to_polygons(vor)

    tessellation = Tessellation(regions[0])

    neighborhood_dict = regions[1]

    log("Checking for neighbors...")

    N = len(tessellation.polygons)

    for i in range(0, N):

        log(f"Progress... {i}/{N}")
        neighborhood_dict[i] = []
        

        for j in range(0, N):
            if i == j:
                continue
        
            else:
                log(f"Testing polygon {i} on polygon {j}")

                intersect = polygon_intersection(tessellation.polygons[i], tessellation.polygons[j])

                if intersect != []:
                    log("Segment found: ", intersect)
                    neighborhood_dict[i].append([tessellation.polygons[j], intersect[0]])
                else:
                    log("No intersection.")

    save_tessellation('test.txt', tessellation=tessellation)

    cores = []
    for i in range(0, N):

        core = tessellation.polygons[i].copy()

        for other in neighborhood_dict[i]:
            
            l = Line(other[1].p1, other[1].p2)
            reflection = other[0].reflect(l)

            log(type(core))
            log('gaga', core, reflection)
            core = polygon_intersection(core, reflection)

        cores.append(core)

    log("Finished core iteration 1.")

    cores2 = []
    for i in range(0, N):
        core = cores[i].copy()
        for other in neighborhood_dict[i]:
            
            l = Line(other[1].p1, other[1].p2)
            reflection = cores[tessellation.polygons.index(other[0])].reflect(l)

            core = polygon_intersection(core, reflection)

        cores2.append(core)

    finish = datetime.now()

    duration = finish - start

    log("Total runtime: ", str(duration))


    plt.figure()
    plot_polygons(tessellation.polygons,style='r-')
    plot_polygons(cores,style="c--")
    plot_polygons(cores2,style='b--')
    for p in points:
        plt.plot(p[0], p[1], 'ro')
    plt.show()
