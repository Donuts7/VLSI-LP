from mip import *


# questi sono dati hardcodati, poi quando facciamo funzionare metteremo la possibilità di leggere da file

width = 8
n_circuits = 4
circuit_x = [3, 3, 5, 5]
circuit_y = [3, 5, 3, 5]
max_y = 5

m = Model(solver_name=mip.CBC) # use GRB for Gurobi

height = sum(circuit_y)
h_to_min = m.add_var("Height",var_type=INTEGER,lb=max_y)

x_coord = [m.add_var(name="x{}".format(i + 1),lb=0,ub=width,var_type=INTEGER) for i in range(n_circuits)]
y_coord = [m.add_var(name="y{}".format(i + 1),lb=0,ub=height,var_type=INTEGER) for i in range(n_circuits)]


x_pair = [[m.add_var("x{}{}".format(i + 1,j+1),var_type=BINARY) for j in range(n_circuits)] for i in range(n_circuits)]
y_pair = [[m.add_var("y{}{}".format(i + 1,j+1),var_type=BINARY) for j in range(n_circuits)] for i in range(n_circuits)]

m.objective += minimize(h_to_min)

# print(len(m.vars) )

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
print("\n")
print(width, int(h_to_min.x) )

"""
for i in range(n_circuits):
    for j in range(n_circuits):
        if x_pair[i][j].x is not None:
            print(x_pair[i][j].name, '=', x_pair[i][j].x, ' ', y_pair[i][j].name, '=', y_pair[i][j].x)
"""
for i in range(n_circuits):
      print(circuit_x[i],circuit_y[i], int(x_coord[i].x), int(y_coord[i].x))




"""
for v in m.vars:
    print('{} : {}'.format(v.name, v.x))
"""