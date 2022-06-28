import pulp as pl
from pulp import *
from utils import *

for ins_number in range(1, 41):

    d = get_data(ins_number)

    width = d['width']
    n_circuits = d['n_circuits']
    circuit_x = d["circuit_x"]
    circuit_y = d["circuit_y"]
    max_y = d['max_y']

    prob = LpProblem("VLSI", LpMinimize)

    solver_list = pl.listSolvers()
    path_to_cplex = r"C:\Program Files\IBM\ILOG\CPLEX_Studio221\cplex\bin\x64_win64\cplex.exe"
    solver = pl.CPLEX_CMD(path=path_to_cplex, timelimit=180)

    height = sum(circuit_y)
    h_to_min = LpVariable("Height", max_y, height, LpInteger)

    x_coord = [LpVariable("x{}".format(i + 1), 0, width, LpInteger) for i in range(n_circuits)]
    y_coord = [LpVariable("y{}".format(i + 1), 0, height, LpInteger) for i in range(n_circuits)]

    x_pair = [[LpVariable("x{}-{}".format(i + 1, j + 1), 0, 1, cat="Integer") for j in range(n_circuits)] for i in
              range(n_circuits)]
    y_pair = [[LpVariable("y{}-{}".format(i + 1, j + 1), 0, 1, cat="Integer") for j in range(n_circuits)] for i in
              range(n_circuits)]

    prob += h_to_min, "Height of the plate"

    for i in range(n_circuits):
        for j in range(n_circuits):
            prob += x_coord[i] + circuit_x[i] <= width
            prob += y_coord[i] + circuit_y[i] <= h_to_min

            if i < j:
                prob += x_coord[i] + circuit_x[i] <= x_coord[j] + width * (x_pair[i][j] + y_pair[i][j])
                prob += x_coord[i] - circuit_x[j] >= x_coord[j] - width * (1 - x_pair[i][j] + y_pair[i][j])
                prob += y_coord[i] + circuit_y[i] <= y_coord[j] + height * (1 + x_pair[i][j] - y_pair[i][j])
                prob += y_coord[i] - circuit_y[j] >= y_coord[j] - height * (2 - x_pair[i][j] - y_pair[i][j])

    prob.solve(solver)

    out = ""
    out += "{} {}\n{}\n".format(width, int(h_to_min.varValue), n_circuits)

    for i in range(n_circuits):
        out += "{} {} {} {}\n".format(circuit_x[i], circuit_y[i], int(x_coord[i].varValue), int(y_coord[i].varValue))

    out += "----------"


    save_data(out, ins_number)
