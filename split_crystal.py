#!/Users/jdiaz/miniconda3/bin/python

import time
from matplotlib.pyplot import show
import matplotlib.pyplot as plt
from matplotlib import collections as mc
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


def units_distance(p, q):
    a = 1600
    b = 1600
    rad_0 = 50
    rad_1 = 200
    rad_2 = 600
    rad_3 = 1000
    rad_4 = 1400
    rad_5 = 1800
    point_1 = ((p[0] - a) * (p[1] - b))
    point_2 = ((q[0] - a) * (q[1] - b))
    if (point_1 < rad_0 * rad_0) and (point_2 < rad_0 * rad_0):
        return 0.5
    elif((point_1 > rad_0 * rad_0) and (point_2 > rad_0 * rad_0) and
         (point_1 < rad_1 * rad_1) and (point_2 < rad_1 * rad_1)):
        return 0.6
    elif((point_1 > rad_1 * rad_1) and (point_2 > rad_1 * rad_1) and
         (point_1 < rad_2 * rad_2) and (point_2 > rad_2 * rad_2)):
        return 0.7
    elif((point_1 > rad_2 * rad_2) and (point_2 > rad_2 * rad_2) and
         (point_1 < rad_3 * rad_3) and (point_2 < rad_3 * rad_3)):
        return 0.8
    elif((point_1 > rad_3 * rad_3) and (point_2 > rad_3 * rad_3) and
         (point_1 < rad_4 * rad_4) and (point_2 < rad_4 * rad_4)):
        return 0.9
    elif((point_1 > rad_4 * rad_4) and (point_2 > rad_4 * rad_4) and
         (point_1 < rad_5 * rad_5) and (point_2 < rad_5 * rad_5)):
        return 1.0
    elif((point_1 > rad_5 * rad_5) and (point_2 > rad_5 * rad_5)):
        return 1.1
    else:
        return 0.5


def euclidean_distance(ordered_pairs, distance=0.5):
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
                            dist = find_distance(p, q)
                            distance = units_distance(p, q)
                            if dist <= distance:
                                pair = [p, q]
                                print("{}\t<-- {:.2f} -->\t{}\tWITHIN {}".format(p, dist, q, distance))
                                close_pairs.append(pair)
                                closest_pairs[q[0]] = [q[1]]
                                # save the midpoints of the close pairs
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
    pair = []
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
        if pair:
            final_closest_points.append(pair)
        min_distance = 217468273
    return final_closest_points


def plot_euclid_pairs(close_pairs, midpoints, pairs, closest_pairs,
                      final_closest_points, f):
    # these are line segments between close pairs
    lc = mc.LineCollection(close_pairs,
                           colors=[(0, 0, 0, 1)],
                           linewidths=0.30)
    fig, ax = plt.subplots(figsize=(6,6))
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
    ax.scatter(x_vals, y_vals, color='blue', s=0.1, alpha=1)

    # circles for different levels of distance
    circle_6 = plt.Circle((1600, 1600), 1800, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_6)

    circle_5 = plt.Circle((1600, 1600), 1600, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_5)

    circle_4 = plt.Circle((1600, 1600), 1400, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_4)

    circle_3 = plt.Circle((1600, 1600), 1000, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_3)

    circle_2 = plt.Circle((1600, 1600), 600, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_2)

    circle_1 = plt.Circle((1600, 1600), 200, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_1)

    circle_0 = plt.Circle((1600, 1600), 50, lw=0.3, color='black', fill=False)
    ax.add_artist(circle_0)

    ax.set_title(f)
    show()


def write_closest_pairs(f, closest_pairs):
    directory_to_write = '/CLOSE_SPOTS'
    filename = f.split('/')[5] + '_SPOT.XDS'
    current_dir = os.getcwd()
    if os.path.isdir(current_dir + directory_to_write):
        os.chdir(current_dir + directory_to_write)
        with open(filename, 'w+') as f:
            for x in closest_pairs:
                for y in closest_pairs[x]:
                    f.write("{} {}\n".format(x, y))
    else:
        os.mkdir(current_dir + directory_to_write)
        os.chdir(current_dir + directory_to_write)
        with open(filename, 'w+') as f:
            for x in closest_pairs:
                for y in closest_pairs[x]:
                    f.write("{} {}\n".format(x, y))
    os.chdir(current_dir)


def main():
    s_time = time.time()
    files = []
    xds_spot = '/xds_spot_files'
    dials_spot = '/dials_spot_files'
    while True:
        print("Which program do you want?\n1. {}\n2.{}".format(xds_spot,
                                                               dials_spot))
        choice = int(input())
        if choice == 1:
            program = xds_spot
            index = 4
            break
        elif choice == 2:
            program = dials_spot
            index = 4
            break

    with open(os.getcwd() + program, 'r') as f:
        for line in f:
            files.append(line.replace('\n', ''))
    files.sort()
    for f in files:
        message = '''
        *-----------------------*
        *\tPROCESSING\t*
        *\t{}\t\t*
        *-----------------------*
        '''
        print(message.format(f.split('/')[index].upper()))
        start_time = time.time()
        pairs = read_spot_file(f)
        ordered_pairs = collections.OrderedDict(sorted(pairs.items()))
        ordered_pairs = add_index_to_dict(ordered_pairs)
        close_pairs, midpoints, closest_pairs = euclidean_distance(ordered_pairs)
        final_closest_points = find_closest_point_to_ea_point(midpoints)
        end_time = time.time()
        print("TIME TAKEN: {:.3}s".format(end_time - start_time))
        plot_euclid_pairs(close_pairs, midpoints, pairs,
                          closest_pairs, final_closest_points,
                          f.split('/')[index].upper())
        write_closest_pairs(f, closest_pairs)
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - s_time))
    print("TOTAL TIME: {}".format(elapsed_time))


if __name__ == '__main__':
    main()
