import microsim
import cell_data
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

def main():
    plt.hold(True)
    f, ax1 = plt.subplots(1, 1, sharey=True)
    f, ax2 = plt.subplots(1, 1, sharey=True)
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=1.)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    c = np.squeeze(np.asarray(sio.loadmat('results/c_7.38905609893_0.1.mat')['c_hat']))
    y = np.squeeze(np.asarray(sio.loadmat('data/y_vector_full.mat')['y']))
    top = np.max(c)
    bottom = np.min(c)
    links = microsim.models.Link.objects.all().order_by("id")
    for ind, link in enumerate(links):
        xs = [x[0] for x in link.geom]
        ys = [x[1] for x in link.geom]
        col = (1.-(c[ind]-bottom)/(top-bottom),0.0,(c[ind]-bottom)/(top-bottom))
        col = scalarMap.to_rgba((c[ind]-bottom)/(top-bottom))
        ax1.plot(xs, ys, linewidth=3, color=col)
    cells = cell_data.models.Tower.objects.all().order_by('id')
    xs = [x.location[0] for x in cells]
    ys = [x.location[1] for x in cells]
    ax1.scatter(xs, ys, marker='o', c=[y[ind] for ind, x in enumerate(cells)])
    ax2.scatter(xs, ys, marker='o', c=[y[ind] for ind, x in enumerate(cells)])
    c = np.squeeze(np.asarray(sio.loadmat('results/c_7.38905609893_0.1.mat')['c_true']))
    top = np.max(c)
    bottom = np.min(c)
    links = microsim.models.Link.objects.all().order_by("id")
    for ind, link in enumerate(links):
        xs = [x[0] for x in link.geom]
        ys = [x[1] for x in link.geom]
        col = (1.-(c[ind]-bottom)/(top-bottom),0.0,(c[ind]-bottom)/(top-bottom))
        col = scalarMap.to_rgba((c[ind]-bottom)/(top-bottom))
        ax2.plot(xs, ys, linewidth=3, color=col)
    plt.show()
