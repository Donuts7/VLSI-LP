from mip import *


# questi sono dati hardcodati, poi quando facciamo funzionare metteremo la possibilità di leggere da file

width = 8
n_circuits = 4
circuit_x1 = [3, 3, 5, 5]
circuit_y1 = [3, 5, 3, 5]

circuit_x = [4, 3, 6, 7]
circuit_y = [5, 7, 4, 7]


max_y = 12

m = Model(sense=minimize, solver_name=CBC) # use GRB for Gurobi

height = sum(circuit_y)
h_to_min = m.add_var("Height",max_y,height,var_type=INTEGER)

x_coord = [m.add_var("x{}".format(i + 1),lb=1,ub=max(circuit_x),var_type=INTEGER) for i in range(n_circuits)]
y_coord = [m.add_var("y{}".format(i + 1),lb=1,ub=max_y,var_type=INTEGER) for i in range(n_circuits)]


x_pair = [[m.add_var("x{}{}".format(i + 1,j+1),lb=0,ub=1,var_type=BINARY) for j in range(n_circuits)] for i in range(n_circuits)]
y_pair = [[m.add_var("y{}{}".format(i + 1,j+1), lb=0,ub=1,var_type=BINARY) for j in range(n_circuits)] for i in range(n_circuits)]

m.objective += minimize(h_to_min)

# print(len(m.vars) )

for i in range(n_circuits):
    for j in range(n_circuits):
        m += x_coord[i] + circuit_x[i] <= width
        m += y_coord[i] + circuit_y[i] <= h_to_min

        if i < j:
            
            m += x_coord[i] + circuit_x[i] <= x_coord[j] + width * (x_pair[i][j] + y_pair[i][j])
            m += x_coord[i] + circuit_x[i] <= x_coord[j] + width * (x_pair[i][j] + y_pair[i][j])
            m += x_coord[i] - circuit_x[j] >= x_coord[j] - width * (1 - x_pair[i][j] + y_pair[i][j])
            m += y_coord[i] + circuit_y[i] <= y_coord[j] + height * (1 + x_pair[i][j] - y_pair[i][j])
            
            m += y_coord[i] - circuit_y[j] >= y_coord[j] - height * (2 - x_pair[i][j] - y_pair[i][j])
m.optimize()

for v in m.vars:
    print('{} : {}'.format(v.name, v.x))