import os
import csv


def get_data(instance_num):
    with open('instances\ins-{}.txt'.format(instance_num), 'r') as fd:
        reader = csv.reader(fd)
        a = []
        for row in reader:
            for i in row:
                a.append(i.replace(" ", ","))

    ints = []

    for e in a:
        ints.append([int(i) for i in e.split(',')])

    d = {}
    keys = ["width", "n_circuits", "circuit_x", "circuit_y", "max_height", "max_y"]
    values = [ints[0][0], ints[1][0], [], []]
    ints.pop(0)
    ints.pop(0)

    tot_area = 0

    for i in ints:
        x_size = int(i[0])
        y_size = int(i[1])
        values[2].append(x_size)
        values[3].append(y_size)
        tot_area += x_size * y_size

    max_y = max(values[3])

    for key, value in zip(keys, values):
        d[key] = value

    z = int((tot_area - (max_y * d['width'])) / d['width'])

    d['max_height'] = max_y + z
    d['max_y'] = max_y
    return d


def save_data1(out, ins_number):
    save_path = "my-out"
    file_name = "ins-{}-solved.txt".format(ins_number)
    completeName = os.path.join(save_path, file_name)
    file1 = open(completeName, "w")
    file1.write(out)


def save_data(save_path,out, ins_number):
    file_name = "ins-{}-solved.txt".format(ins_number)
    completeName = os.path.join(save_path, file_name)
    file1 = open(completeName, "w")
    file1.write(out)