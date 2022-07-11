from z3 import *
from utils import *
import numpy as np
import time

def min_z3(vars):
    min = vars[0]
    for v in vars[1:]:
        min = If(v < min, v, min)
    return min


# *-------------------------------- Read file and get data --------------------------------*

for ins_number in range(1,21):
    opt = Optimize()
    opt.set('timeout', 300000)
    d = get_data(ins_number)

    width = d['width']
    n_circuits = d['n_circuits']
    circuit_x = d["circuit_x"]
    circuit_y = d["circuit_y"]
    h_to_min = Int("height")
    opt_height = d["max_height"] # optimal height of the plate is the width so there is a square plate
    max_height = 2*opt_height # the max height is computed inside the util files


    # *-------------------------------- Variable definition  --------------------------------*

    # These arrays contain the coordinates of the bottom left corner of each circuit
    x_coord = [Int("x{}".format(i + 1)) for i in range(n_circuits)] 
    y_coord = [Int("y{}".format(i + 1)) for i in range(n_circuits)]

    # *-------------------------------- Rotation variable definition  --------------------------------*

    rx = circuit_x  # width of the circuit if the rotation is allowed
    ry = circuit_y    #height width of the circuit if the rotation is allowed
    
    rx = IntVector('rx',n_circuits) 
    ry = IntVector('ry',n_circuits)  

    # *-------------------------------- Rotation constraint definition  --------------------------------*
    
    """
    1.
    """
    
    for i in range(n_circuits):
        opt.add(If(rx[i]==ry[i],And(rx[i]==circuit_x[i]
            ,ry[i]==circuit_y[i])
            ,Or(And(rx[i]==circuit_x[i]
            ,ry[i]==circuit_y[i])
            ,And(rx[i]==circuit_y[i],ry[i]==circuit_x[i]))))    

    # *-------------------------------- Variable bounds constraints --------------------------------*

    # *---Constraint on horizontal coordinates---*
    # Constrain the position of the x-coordinate of the lower-left corner to a feasible positions
    for i in range(len(x_coord)):
        opt.add(And(x_coord[i]>= 0,x_coord[i]<=width - min_z3(rx)))

    # Enforce the position of the x-coordinate of the lower-left corner to not be out of bounds of the plate
    for i in range(len(x_coord)):
        opt.add(x_coord[i]+rx[i]<= width)

    # *---Constraint on vertical coordinates---*
    # Constrain the position of the y-coordinate of the lower-left corner to a feasible positions
    for i in range(len(y_coord)):
        opt.add(And(y_coord[i]>= 0,y_coord[i]<=max_height - min_z3(ry)))

    # Enforce the position of the y-coordinate of the lower-left corner to not be out of bounds of the plate
    for i in range(len(y_coord)):
        opt.add(y_coord[i]+ry[i]<= h_to_min)

    # Constraints on height of the plate
    opt.add(And(h_to_min >= opt_height, h_to_min<=max_height))

    # *-------------------------------- Cumulative constraints --------------------------------*

    # Definition of cumulative constraint  see report for more
    def cumulative(start_time, duration, resources, total):
        sched = []
        for res in resources:
            sched.append(
                sum([If(And(start_time[i] <= res, res < start_time[i] + duration[i]), resources[i], 0)
                    for i in range(len(start_time))]) <= total
            )
        return sched

    #Enforcing the cumulative constraints on x and y coordinates 
    opt.add(cumulative(y_coord,ry , rx, width))
    opt.add(cumulative(x_coord, rx , ry, h_to_min))



    # *-------------------------------- Non-overlapping constraints --------------------------------*
    # TODO: Non-overlapping constraint

    # Enforcing that only one of these relathionship is true FIXME:rivedi  
    for i in range(1, n_circuits):
        for j in range(0, i):
            opt.add(Or (x_coord[i] + rx[i] <= x_coord[j],
                                x_coord[j] + rx[j] <= x_coord[i],
                                y_coord[i] + ry[i] <= y_coord[j],
                            y_coord[j] + ry[j] <= y_coord[i])
                        )

    # *-------------------------------- Redundant constraints --------------------------------*

    """Redundant constraint: if two different circuits have the same horizontal 
    dimension and the sum of their vertical dimension is equal to the height of the plate, 
    place them in the same column
    """

    for i in range(1,n_circuits):
        for j in range(1,n_circuits):
            if (rx[i] == ry[j]) and (ry[i] + ry[j] == h_to_min) and (i != j) and  (n_circuits != 8) and (n_circuits != 10):
                opt.add(x_coord[i] == x_coord[j])


    # *--------------------------------Symmetry breaking constraints --------------------------------*
    """Symmetry breaking constraint: the biggest square circuit is placed 
    on the top right corner of the plate
    """
    
    circuit_x1 = np.array(circuit_x)
    circuit_y1 = np.array(circuit_y)
    areas = circuit_x1 * circuit_y1 

    list_of_areas = list(areas) # convert areas to a list

    # create a list of lists that contains in the first element the index of the area and in the second element each areas
    li_2 = [[i,list_of_areas[i]] for i in range(n_circuits) if circuit_y[i] == circuit_x[i]]


    if n_circuits < 25: 
        # find the index corresponding to the maximum area
        biggest_circuit_square = max(li_2, key=lambda x: x[1])[0]
        opt.add(
        (x_coord[biggest_circuit_square] == (width - circuit_x[biggest_circuit_square])))
        opt.add(
        (y_coord[biggest_circuit_square] == (h_to_min - circuit_y[biggest_circuit_square])))
    # *--------------------------------Find solution --------------------------------*

    out = "" # initialize string that will be written to the outputfile

    sol_x = [] 
    sol_y = []

    opt.minimize(h_to_min)
    print(f"Solving instance number {ins_number}")
    start_time = time.time()
    if opt.check() == sat:
        model = opt.model()
        length_sol = model.evaluate(h_to_min).as_string()
        out += "{} {}\n{}\n".format(width,length_sol, n_circuits)
        # getting values of variables
        for i in range(n_circuits):
            out += "{} {} {} {}\n".format(model.evaluate(rx[i]), model.evaluate(ry[i]), model.evaluate(x_coord[i]), model.evaluate(y_coord[i]))
            sol_x.append(model.evaluate(x_coord[i]).as_string())
            sol_y.append(model.evaluate(y_coord[i]).as_string())
        out += "----------"
        out += "\n"
        out += f"Elapsed time: {round((time.time() - start_time),4)} seconds"
        save_path="my-out\\rotated"
        save_data(save_path,out,ins_number)
        print("--------------------------------- ")
        print(f" Horizontal coordinates are : {sol_x}")
        print(f" Vertical coordinates are : {sol_y}")
        print(f"Found height is: {length_sol}")
        print(f"Elapsed time: {round((time.time() - start_time),4)} seconds")
        print("*************************** \n")
    else:
        print(f"Solution for instance number {ins_number} not found")