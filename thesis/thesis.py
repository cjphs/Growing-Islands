import sys

from datetime import datetime

from geometry.diagram import Diagram
from input_generation.voronoi_funcs import generate_random_voronoi, voronoi_from_points
from matplotlib import pyplot as plt
from scipy.spatial import voronoi_plot_2d
from voronoi_approximation import VoronoiApproximation

def enforce_plot_scale(xmin,xmax,ymin,ymax):
    ax = plt.gca()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])

def get_arg(args, arg_name):
    if arg_name in args:
        return args[args.index(arg_name) + 1]
    return None

def parse_args(phi, num_points, gui):
    num = get_arg(sys.argv, "--num_points")
    if num != None:
        num_points = int(num)
    om = get_arg(sys.argv, "--omega")
    if om != None:
        omega = float(om)
    ph = get_arg(sys.argv, "--phi")
    if ph != None:
        phi = float(ph)
    gu = get_arg(sys.argv, "--gui")
    if gu != None:
        if gu == "False":
            gui = False
    ma = get_arg(sys.argv, "--margin")
    if ma != None:
        margin = float(ma)
    return phi, num_points, gui

def main():
    gui = False

    phi     = .001

    margin = .975

    num_points = 50

    xmin,xmax = 0,1
    ymin,ymax = 0,1

    phi, num_points, gui = parse_args(phi, num_points, gui)

    load_from_file = ""
    #load_from_file = "in/diagram_luxembourg.txt"
    #load_from_file = "in/23-53-05_30_0.005.txt"

    if load_from_file == "":
        vor = generate_random_voronoi(num_points,
                                      xmin=xmin,
                                      xmax=xmax,
                                      ymin=ymin,
                                      ymax=ymax
                                      )

        diagram = Diagram(voronoi=vor)

        filename = f"in/{datetime.now().strftime(f'%H-%M-%S_{num_points}_{phi}')}.txt"
        diagram.save_to_txt(f"{filename}")
    else:
        diagram = Diagram(txt_file=load_from_file)

    # Plot the original input diagram
    if gui:
        plt.figure()    
        
        #for p in vor.points:
            #plt.plot(p[0], p[1], "o", alpha=1, color="black")
            
        diagram.plot()
        enforce_plot_scale(xmin,xmax,ymin,ymax)
        plt.title(label="Input diagram")
        plt.waitforbuttonpress(0)


    approximation = VoronoiApproximation(diagram, phi, gui=gui)
    original_approximation = voronoi_from_points(approximation.estimator_points)

    if gui:
        enforce_plot_scale(xmin,xmax,ymin,ymax)

        #voronoi_plot_2d(
        #    original_approximation,
        #    line_colors='orange',
        #    line_alpha=0.2,
        #    ax=plt.gca(),
        #    show_points=False,
        #    show_vertices=False
        #)
        enforce_plot_scale(xmin,xmax,ymin,ymax)
        plt.title(label="Centroid approximation")
        plt.waitforbuttonpress(0)

        plt.title(label="Nudging generator approximations...")

    approximation.do_thingy(margin=margin)

    print(approximation.omega)

    if not gui:
        diagram.plot()
        voronoi_plot_2d(
           original_approximation,
           line_colors='orange',
           line_alpha=0.2,
           ax=plt.gca(),
           show_points=False,
           show_vertices=False
        )

    # generate new voronoi diagram from final estimator point positions
    new_vor = voronoi_from_points(approximation.estimator_points)
    voronoi_plot_2d(new_vor, ax=plt.gca(), line_alpha=.5, line_colors='blue')
    enforce_plot_scale(xmin,xmax,ymin,ymax)
    plt.pause(1e-10)

    plt.figure()
    plt.plot(approximation.points_satisfied, color='black')
    plt.title(label="Percentage of label points satisfied over time")
    plt.ylim([0, 1])
    plt.ylabel("% Satisfied label points")
    plt.xlabel("Time step")

    plt.pause(1e-10)
    plt.show()

if __name__ == "__main__":
    main()