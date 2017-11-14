import sys
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

##plot confic variables
fig, ax = plt.subplots()
fig.set_size_inches(7, 7)
xmax, ymax, xmin, ymin = 5, 5, -5, -5

############################
x = np.linspace(xmin, xmax, 500)
slope = float(Fraction(sys.argv[1]))

if len(sys.argv) > 2:
    b = float(Fraction(sys.argv[2]))
else:
    b = 0.0
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

# ax.xaxis.set_ticks([-9, -8, -7, -6,
#                     -5, -4, -3, -2, -1,
#                     1, 2, 3, 4, 5,
#                     6, 7, 8, 9])
# ax.yaxis.set_ticks([-9, -8, -7, -6,
#                     -5, -4, -3, -2, -1,
#                     1, 2, 3, 4, 5,
#                     6, 7, 8, 9])

ax.xaxis.set_ticks([-5, -4, -3, -2, -1,
                    1, 2, 3, 4, 5])
ax.yaxis.set_ticks([-5, -4, -3, -2, -1,
                    1, 2, 3, 4, 5])

adjust_spines(ax, ["left", "bottom"])
ax.xaxis.grid(color='k', lw=1.2, zorder=10)
ax.yaxis.grid(color='k', lw=1.2, zorder=10)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
adjust_labels(ax.get_xticklabels())
adjust_labels(ax.get_yticklabels())
#fig.savefig("./graphs_linear_equalities/{0:1.2f}x_{1:1.2f}.png".format(slope, b))
plt.show()
