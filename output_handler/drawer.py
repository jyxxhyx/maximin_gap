import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def draw_result(interval_list, result, file_name):
    polygons = []
    scatter_x = []
    scatter_y = []
    for idx, (interval, x_i) in enumerate(zip(interval_list, result)):
        scatter_x.append(x_i)
        scatter_y.append(idx)

        lb_x = interval[0]
        ub_x = interval[1]
        lb_y = idx - 0.3
        ub_y = idx + 0.3
        polygon = [[lb_x, lb_y], [lb_x, ub_y], [ub_x, ub_y], [ub_x, lb_y], [lb_x, lb_y]]
        polygons.append(polygon)

    fig, ax = plt.subplots()
    patches = [Polygon(polygon, True) for polygon in polygons]
    p = PatchCollection(patches,
                        facecolors='gray',
                        edgecolors='gray',
                        alpha=0.3)
    plt.scatter(scatter_x, scatter_y, s=25, c='red')
    ax.add_collection(p)

    plt.savefig('{}.jpg'.format(file_name), bbox_inches='tight', pad_inches=0)
    plt.savefig('{}.pdf'.format(file_name), bbox_inches='tight', pad_inches=0)
    return
