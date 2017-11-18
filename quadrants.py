from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('center'))  # outward by 10 points
            # spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine


def adjust_labels(labels):
    for label in labels:
        label.set_backgroundcolor('white')
        label.set_size('x-small')
        label.set_weight('demi')
        label.zorder = 20

def make_quandrants(m, b, fp):
    ##plot confic variables
    fig, ax = plt.subplots()
    fig.set_size_inches(7, 7)
    xmax, ymax, xmin, ymin = 5, 5, -5, -5

    ############################
    x = np.linspace(xmin, xmax, 500)
    slope = m
    gt = ymax
    lt = ymin
    space = lt
    y = slope * x + b

    # ax.set_title('Title')

    ax.plot(x, y, 'k-', zorder=31, linewidth=3)
    ##ax.fill_between(x, y, space, color='gray', alpha=.5, zorder = 30)


    # Arrow Section
    ##########################################
    scale = .7
    verts = np.array([
        (-1., 0.25),  # left, bottom
        (0., 0.),  # left, top
        (-1, -0.25),  # right, top
        (0., 0.),  # ignored
    ])

    verts = verts * scale
    if slope > 0:
        theta = np.arctan(slope)
        pos = min(xmax, (xmax - b) / slope)
    else:
        theta = -np.arctan(-slope)
        pos = min(xmax, (xmin - b) / slope)
    for index, row in enumerate(verts):
        verts[index] = np.array([row[0] * np.cos(theta) - row[1] *
                                np.sin(theta), row[0] * np.sin(theta) + row[1] * np.cos(theta)])


    verts[:, 0] = verts[:, 0] + pos  # x translation
    verts[:, 1] = verts[:, 1] + slope * pos + b  # y translation
    codes = [Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
            ]

    path = Path(verts, codes)

    patch = patches.PathPatch(path, facecolor='black', lw=0, zorder=30)
    ax.add_patch(patch)


    verts = np.array([
        (-1., 0.25),  # left, bottom
        (0., 0.),  # left, top
        (-1, -0.25),  # right, top
        (0., 0.),  # ignored
    ])

    verts = verts * scale
    if slope > 0:
        theta = np.arctan(slope) + np.pi
        neg = max(xmin, (xmin - b) / slope)
    else:
        theta = np.pi - np.arctan(-slope)
        neg = max(xmin, (xmax - b) / slope)
    for index, row in enumerate(verts):
        verts[index] = np.array([row[0] * np.cos(theta) - row[1] *
                                np.sin(theta), row[0] * np.sin(theta) + row[1] * np.cos(theta)])


    verts[:, 0] = verts[:, 0] + neg  # x translation
    verts[:, 1] = verts[:, 1] + slope * neg + b  # y translation
    codes = [Path.MOVETO,
            Path.LINETO,
            Path.LINETO,
            Path.CLOSEPOLY,
            ]

    path = Path(verts, codes)

    patch = patches.PathPatch(path, facecolor='black', lw=0, zorder=30)
    ax.add_patch(patch)
    ##########################################


    ##Creating the border of the image
    ax.plot([xmin, ymin], [xmin, ymax], color='k')
    ax.plot([xmin, ymax], [xmax, ymax], color='k')
    ax.plot([xmax, ymax], [xmin, ymax], color='k')
    ax.plot([xmin, ymax], [xmin, ymin], color='k')
    ax.grid(True)

    ##creating the size of the image
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.xaxis.set_ticks([x for x in range(xmin +1, xmax) if x != 0])
    ax.yaxis.set_ticks([y for y in range(ymin +1, ymax) if y != 0])

    adjust_spines(ax, ["left", "bottom"])
    ax.xaxis.grid(color='k', lw=1.2, zorder=10)
    ax.yaxis.grid(color='k', lw=1.2, zorder=10)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    adjust_labels(ax.get_xticklabels())
    adjust_labels(ax.get_yticklabels())
    plt.tight_layout()
    fig.savefig(fp, format="png")
    #plt.show()

if __name__ == "__main__":
    import sys

    try:
        m = float(Fraction(sys.argv[1]))
    except(ValueError):
        m = 1.0
    try:
        b = float(Fraction(sys.argv[2]))
    except(ValueError):
        b = 0.0

    make_quandrants(m, b, "img/img.png")