from mip import *
from utils import *

for ins_number in range(5, 20):

    d = get_data(ins_number)

    width = d['width']
    n_circuits = d['n_circuits']
    circuit_x = d["circuit_x"]
    circuit_y = d["circuit_y"]
    max_y = d['max_y']

    m = Model(solver_name=mip.CBC)  # use GRB for Gurobi

    height = sum(circuit_y)
    h_to_min = m.add_var("Height", var_type=INTEGER, lb=max_y)

    x_coord = [m.add_var(name="x{}".format(i + 1), lb=0, ub=width, var_type=INTEGER) for i in range(n_circuits)]
    y_coord = [m.add_var(name="y{}".format(i + 1), lb=0, ub=height, var_type=INTEGER) for i in range(n_circuits)]

    x_pair = [[m.add_var("x{}{}".format(i + 1, j + 1), var_type=BINARY) for j in range(n_circuits)] for i in
              range(n_circuits)]
    y_pair = [[m.add_var("y{}{}".format(i + 1, j + 1), var_type=BINARY) for j in range(n_circuits)] for i in
              range(n_circuits)]

    m.objective += minimize(h_to_min)

    for i in range(n_circuits):
        for j in range(n_circuits):
            m += x_coord[i] + circuit_x[i] <= width
            m += y_coord[i] + circuit_y[i] <= h_to_min

            if i < j:
                m += x_coord[i] + circuit_x[i] <= x_coord[j] + width * (x_pair[i][j] + y_pair[i][j])
                m += x_coord[i] - circuit_x[j] >= x_coord[j] - width * (1 - x_pair[i][j] + y_pair[i][j])
                m += y_coord[i] + circuit_y[i] <= y_coord[j] + height * (1 + x_pair[i][j] - y_pair[i][j])
                m += y_coord[i] - circuit_y[j] >= y_coord[j] - height * (2 - x_pair[i][j] - y_pair[i][j])

    m.optimize()
    out = ""
    out += "{} {}\n".format(width, int(h_to_min.x))

    for i in range(n_circuits):
        # print(circuit_x[i],circuit_y[i], int(x_coord[i].x), int(y_coord[i].x))
        out += "{} {} {} {}\n".format(circuit_x[i], circuit_y[i], int(x_coord[i].x), int(y_coord[i].x))

    out += "----------"

    save_data(out, ins_number)
