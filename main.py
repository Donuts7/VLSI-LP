from pulp import *
from utils import *
# così il problema non trova una soluzione, se togli il constraint linea 40 invece si (trova 0 ma non va bene ovviamente)
ins_number=2

d = get_data(ins_number)

width = d['width']
n_circuits = d['n_circuits']
circuit_x = d["circuit_x"]
circuit_y = d["circuit_y"]
max_y = d['max_y']

prob = LpProblem("VLSI", LpMinimize)

# mantengo sia Y che H (come nel video), dove Y è h_to_min e H è height
height = sum(circuit_y)
h_to_min = LpVariable("Height",max_y,height,LpInteger)

x_coord = [LpVariable("x{}".format(i + 1), 0, width, LpInteger) for i in range(n_circuits)]
y_coord = [LpVariable("y{}".format(i + 1), 0, height, LpInteger) for i in range(n_circuits)]

# non so come fare in modo che queste due siano variabili booleane
x_pair = [[LpVariable("x{}{}".format(i + 1, j + 1), 0, 1, cat="Integer") for j in range(n_circuits)]for i in range(n_circuits)]
y_pair = [[LpVariable("y{}{}".format(i + 1, j + 1), 0, 1, cat="Integer") for j in range(n_circuits)]for i in range(n_circuits)]


# questa è da minimizzare
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

prob.solve()

'''
for i in range(n_circuits):
    for j in range(n_circuits):
        if x_pair[i][j].varValue != None:
            print(x_pair[i][j], '=', x_pair[i][j].varValue, ' ', y_pair[i][j], '=', y_pair[i][j].varValue)

for i in range(n_circuits):
      print(x_coord[i], '=', x_coord[i].varValue, ' ', y_coord[i], '=', y_coord[i].varValue)
'''
out = ""
out += "{} {}\n".format(width, int(h_to_min.varValue))

for i in range(n_circuits):
    out += "{} {} {} {}\n".format(circuit_x[i], circuit_y[i], int(x_coord[i].varValue), int(y_coord[i].varValue))

out += "----------"

print(out)
"""    
for v in prob.variables():
    if len(v.name) == 2:
        print(v.name, "=", v.varValue)
"""