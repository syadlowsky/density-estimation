#!/usr/bin/env python
import os, sys
import numpy as np
import microsim
import matplotlib.pyplot as plt
import scipy.io as sio

from django.contrib.gis.geos import Point, LineString, GEOSGeometry

def gaussian_on_line_segment(line_segment, scale=0.01):
    """ Sample in lat-lon

    variance is equivalent to (roughly) 0.5km std-dev
    """
    theta = np.random.uniform()
    starts = [Point(p) for p in line_segment[:-1]]
    ends = [Point(p) for p in line_segment[1:]]
    dists = np.array([p.distance(q) for p, q in zip(starts, ends)])
    probs = dists/dists.sum()
    idx = np.random.multinomial(1, probs)[0]
    starting_point = np.array(line_segment[idx])
    ending_point = np.array(line_segment[idx+1])
    gaussian_center = theta*starting_point + (1.-theta)*ending_point
    perturbation = np.random.normal(0., scale, 2)
    return gaussian_center + perturbation

def lnks(links):
    pts = []
    for link in links:
        for p in link.geom:
            pts.append(p)
    return np.array(pts)

def choose_line_segments(n):
    links = microsim.models.Link.objects.all()
    plt.hold(True)
    see_links = lnks(links)
    plt.scatter(see_links[:,0], see_links[:,1], color='r')
    p = np.zeros(len(links))
    for idx, link in enumerate(links):
        p[idx] = (link.lane_count or 2)*link.length
    p.astype(float)
    p /= p.sum()
    np.set_printoptions(threshold=np.nan)
    line_segment_indices = np.random.multinomial(n, p)
    geoms = []
    for idx, link in enumerate(links):
        for _ in xrange(line_segment_indices[idx]):
            geoms.append(link.geom)
    return np.array(geoms)

def uniform_dist(count):
    l = microsim.models.Link.objects.raw("SELECT * FROM microsim_link ORDER BY ST_XMin(geom) LIMIT 1;")[0]
    m = microsim.models.Link.objects.raw("SELECT * FROM microsim_link ORDER BY ST_XMax(geom) DESC LIMIT 1;")[0]
    n = microsim.models.Link.objects.raw("SELECT * FROM microsim_link ORDER BY ST_YMin(geom) LIMIT 1;")[0]
    o = microsim.models.Link.objects.raw("SELECT * FROM microsim_link ORDER BY ST_YMax(geom) DESC LIMIT 1;")[0]
    min_pts = (l.geom.extent[0], n.geom.extent[1])
    max_pts = (m.geom.extent[2], o.geom.extent[3])
    x_diff = max_pts[0] - min_pts[0]
    y_diff = max_pts[1] - min_pts[1]
    rand_x = x_diff * np.random.rand(1, count)
    rand_y = y_diff * np.random.rand(1, count)
    uniform_points = np.vstack((rand_x, rand_y))
    uniform_points += np.array(min_pts)[:,np.newaxis]
    return uniform_points.T

def gaussian_near_roads(n):
    line_segments = choose_line_segments(n)
    return map(gaussian_on_line_segment, line_segments)

def main():
    uniform_points = uniform_dist(150)
    points_near_roads = gaussian_near_roads(250)
    all_points = np.vstack((points_near_roads, uniform_points))
    sio.savemat('data/tower_locations.mat', {'towers':all_points})
    plt.scatter(all_points[:,0], all_points[:,1])
    plt.scatter(uniform_points[:,0], uniform_points[:,1])
    plt.show()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    main()
