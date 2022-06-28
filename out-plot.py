import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import csv
import numpy as np
import matplotlib.patches as mpatches


for ins in range(1, 41):
    a = []
    with open('my-out\ins-{}-solved.txt'.format(ins), 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            if row == ['----------']:
                break
            for i in row:
                a.append(i.replace(" ", ","))
    ints = []
    for e in a:
        ints.append([int(i) for i in e.split(',')])


    def create(a):
        width = int(a[0][0])
        height = int(a[0][1])
        length = int(a[1][0])

        s = (width, height)
        cell = np.ones(s)

        for i in range(length):
            x_s = a[i + 2][0]
            y_s = a[i + 2][1]
            x_c = a[i + 2][2]
            y_c = a[i + 2][3]

            for y_el in range(y_s):
                for x_el in range(x_s):
                    cell[x_c + x_el, y_c + y_el] = int(i + 1)
        cell = np.rot90(cell)
        cell = np.flipud(cell)
        return cell


    legnd = []
    for el in range(2, len(ints)):
        legnd.append("size: " + str(ints[el][0]) + ", " + str(ints[el][1]) +
                     "\ncoordinate: " + str(ints[el][2]) + ", " + str(ints[el][3]))

    try:
        n_colors = int(ints[1][0])
        data = create(ints)
        print(ins)

        cmap = plt.cm.get_cmap('tab20c', n_colors)

        if n_colors >= 19:
            plt.figure(figsize=(14, 11), dpi=100)
        else:
            plt.figure(figsize=(12, 8), dpi=100)

        plt.pcolormesh(data, edgecolors='white', linewidth=0.6, cmap=cmap)
        plt.title('Instance number {} ({} circuits), {}x{}'.format(ins, n_colors, ints[0][0], ints[0][1]))
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_aspect('equal')
        ax.set_xlabel('Width')
        ax.set_ylabel('Height')




        bound = np.linspace(0, 1, n_colors + 1)
        bound_prep = np.round(bound * (n_colors - 1), 2)

        plt.legend([mpatches.Patch(color=cmap(b)) for b in bound[:-1]],
                   ['{}'.format(legnd[i], bound_prep[i + 1] - 0.01) for i in range(n_colors)], bbox_to_anchor=(1.04, 1),
                   loc="upper left")

        plt.rcParams.update({'figure.max_open_warning': 0})
    except IndexError:
        print("Empty output")
    else:
        plt.savefig('plotted-out\ins-{}-plotted'.format(ins))

