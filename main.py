from pulp import *

width = 8
n_circuits = 4
circuit_x = [3, 3, 5, 5]
circuit_y = [3, 5, 3, 5]

max_y = 5

prob = LpProblem("VLSI", LpMinimize)

height = sum(circuit_y)
x_coord = [LpVariable("x{}".format(i + 1), 1, max(circuit_x), LpInteger) for i in range(n_circuits)]
y_coord = [LpVariable("y{}".format(i + 1), 1, max_y, LpInteger) for i in range(n_circuits)]

x_pair = [[LpVariable("x{}{}".format(i + 1, j + 1), 0, 1, LpBinary) for j in range(n_circuits)]for i in range(n_circuits)]
y_pair = [[LpVariable("y{}{}".format(i + 1, j + 1), 0, 1, LpBinary) for j in range(n_circuits)]for i in range(n_circuits)]

git config --global user.email "alessandro.calo98@outlook.com"

prob += height, "Height of the plate"

#prob += [x_coord[i]+circuit_x[i] <= width for i in range(n_circuits)],"Respect width"
#prob += [y_coord[i]+circuit_y[i] <= height for i in range(n_circuits)],"Respect height"

for i in range(n_circuits):
    for j in range(n_circuits):
        prob += x_coord[i] + circuit_x[i] <= width
        prob += y_coord[i] + circuit_y[i] <= height

        if i < j:

            prob += x_coord[i] + circuit_x[i] <= x_coord[j] + width * (x_pair[i][j] + y_pair[i][j])
            prob += x_coord[i] - circuit_x[j] >= x_coord[j] - width * (1 - x_pair[i][j] + y_pair[i][j])
            prob += y_coord[i] + circuit_y[i] <= y_coord[j] + height * (1 + x_pair[i][j] - y_pair[i][j])
            prob += y_coord[i] - circuit_y[j] >= y_coord[j] - height * (2 - x_pair[i][j] - y_pair[i][j])

prob.solve()

for i in range(n_circuits):
    for j in range(n_circuits):
        if x_pair[i][j].varValue != None:
            print(x_pair[i][j], '=', x_pair[i][j].varValue, ' ', y_pair[i][j], '=', y_pair[i][j].varValue)

for i in range(n_circuits):
      print(x_coord[i], '=', x_coord[i].varValue, ' ', y_coord[i], '=', y_coord[i].varValue)


"""    
for v in prob.variables():
    if len(v.name) == 2:
        print(v.name, "=", v.varValue)
"""