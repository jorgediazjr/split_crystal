#!/Users/jdiaz/miniconda3/bin/python

from matplotlib.pyplot import show
from matplotlib import collections as mc
import pylab as pl
import os
import collections
import math


def read_spot_file(file_name):
    xy_pairs = {}
    with open(file_name, 'r') as f:
        for line in f:
            x = float(line.split()[0])
            y = float(line.split()[1])
            if x in xy_pairs:
                xy_pairs[round(x, 4)].append(y)
            else:
                xy_pairs[round(x, 4)] = [y]
    return xy_pairs


def add_index_to_dict(ordered_pairs):
    new_dict = {}
    for i, key in enumerate(ordered_pairs):
        new_dict[i] = {key: ordered_pairs[key]}
    return new_dict


def find_distance(p, q):
    dist = math.sqrt(((p[0] - q[0])*(p[0] - q[0])) +
                     ((p[1] - q[1])*(p[1] - q[1])))
    return dist


def euclidean_distance(ordered_pairs, distance=0.7):
    close_pairs = []        # these are pairs of points that are close together
    closest_pairs = dict()  # this has x,y values that are closest
    midpoints = dict()      # the midpoints between the close pairs
    for index in ordered_pairs:
        for x_coord in ordered_pairs[index]:
            for y_coord in ordered_pairs[index][x_coord]:
                x1 = x_coord
                y1 = y_coord
                p = [x1, y1]
                current = 0
                while current < len(ordered_pairs):
                    if current != index:
                        x2 = list(ordered_pairs[current].keys())[0]
                        for _y in ordered_pairs[current][x2]:
                            y2 = _y
                            q = [x2, y2]
                            if find_distance(p, q) <= distance:
                                pair = [p, q]
                                print("{} <---> {}".format(p, q))
                                close_pairs.append(pair)
                                #if p[0] in closest_pairs:
                                #    closest_pairs[p[0]].append(p[1])
                                #else:
                                #    closest_pairs[p[0]] = [p[1]]
                                #if q[0] in closest_pairs:
                                #    closest_pairs[q[0]].append(q[1])
                                #else:
                                closest_pairs[q[0]] = [q[1]]
                                midpoint_x = (p[0] + q[0]) / 2
                                midpoint_y = (p[1] + q[1]) / 2
                                midpoints[midpoint_x] = midpoint_y
                        current += 1
                    else:
                        current += 1
    return close_pairs, midpoints, closest_pairs


def find_closest_point_to_ea_point(midpoints):
    # these are for pairs of points that are closest
    final_closest_points = []
    min_distance = 217468273
    for x1 in midpoints:
        y1 = midpoints[x1]
        for x2 in midpoints:
            if x2 != x1:
                y2 = midpoints[x2]
                p = [x1, y1]
                q = [x2, y2]
                if find_distance(p, q) <= min_distance:
                    min_distance = find_distance(p, q)
                    pair = [p, q]
        final_closest_points.append(pair)
        min_distance = 217468273
    return final_closest_points


def plot_euclid_pairs(close_pairs, midpoints, pairs, closest_pairs,
                      final_closest_points):
    # these are line segments between close pairs
    lc = mc.LineCollection(close_pairs,
                           colors=[(0, 0, 0, 1)],
                           linewidths=0.30)
    fig, ax = pl.subplots()
    ax.add_collection(lc)

    # these are the midpoints between close pairs
    x_vals = list(midpoints.keys())
    y_vals = list(midpoints.values())
    ax.scatter(x_vals, y_vals, s=5, color='red')
    ax.autoscale()
    ax.margins(0.1)

    # these are lines between midpoints and their nearest midpoint
    ls = mc.LineCollection(final_closest_points,
                           colors=[(0, 1, 0, 1)],
                           linewidths=0.70)
    ax.add_collection(ls)

    # these are the points that are included in the close_pairs dictionary
    x_vals = []
    y_vals = []
    for x in closest_pairs:
        for y in closest_pairs[x]:
            x_vals.append(x)
            y_vals.append(y)
    ax.scatter(x_vals, y_vals, color='black', s=0.1)

    x_vals = []
    y_vals = []
    for x in pairs:
        for y in pairs[x]:
            x_vals.append(x)
            y_vals.append(y)
    ax.scatter(x_vals, y_vals, color='blue', s=0.1, alpha=.5)
    #ax.set_xlim([1150, 2050])
    #ax.set_ylim([1150, 2050])
    show()


def write_closest_pairs(f, closest_pairs):
    filename = f.split('/')[4] + '_SPOT.XDS'
    with open(filename, 'w+') as f:
        for x in closest_pairs:
            for y in closest_pairs[x]:
                f.write("{} {}\n".format(x, y))


def main():
    files = []
    with open(os.getcwd() + '/spot_files', 'r') as f:
        for line in f:
            files.append(line.replace('\n', ''))

    for f in files:
        pairs = read_spot_file(f)
        ordered_pairs = collections.OrderedDict(sorted(pairs.items()))
        ordered_pairs = add_index_to_dict(ordered_pairs)
        close_pairs, midpoints, closest_pairs = euclidean_distance(ordered_pairs)
        final_closest_points = find_closest_point_to_ea_point(midpoints)
        plot_euclid_pairs(close_pairs, midpoints, pairs,
                          closest_pairs, final_closest_points)
        write_closest_pairs(f, closest_pairs)


if __name__ == '__main__':
    main()
