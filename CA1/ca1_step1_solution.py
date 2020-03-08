""" Oliver Johansson and Anton Sandberg """
""" Group 7, Assignment 1 Step 1 """

""" 1.1 Opens the file and read the first two lines """
with open("ca1_step1_input_data.txt", "r") as file:

    line = file.readline()
    print(line)

    line = file.readline()
    print(line)

    """ Formating the data """
    line = line.replace(";", ",")
    line = line.split(",")

    """ Create variables with correct names """
    time_steps = int(line[0])
    time_step = float(line[1])
    radius = float(line[2])
    v_variance = float(line[3])
    N_particles = int(line[4])
    lista = [time_steps, time_step, radius, v_variance, N_particles]
    print(lista)


    """ Creating a function to swap ; for , to parse main header """
    def convert(x):
        x = x.strip()
        x = x.replace(";", ",")
        x = x.split(",")
        for i in range(4):
            x[i] = float(x[i])
        return x

    print(file.readline())

    """ Create arrays of the data """
    numb_val = []
    part_ind = []
    data = []
    steps = 0
    while steps < 1000:
        line = file.readline()
        if "# time_step" in line:           # Corrected from first delivery
            if "# time_step 0" in line:
                continue
            else:
                data.append(part_ind)
                part_ind = []
                steps += 1
                continue
        if line.find("# x") == 0:   #
            continue
        if line.isspace():
            continue
        if len(part_ind) == 400:    # Realising the last space is the end
            data.append(part_ind)
            print(numb_val)
            break
        numb_val = convert(line)
        part_ind.append(numb_val)


    print(len(data), len(data[0]), len(data[0][0]), type(data[0][0][0]))

import numpy as np
data = np.array(data)

""" Splitting data """
R = data[:, :, 0:2]     # Extracting the positions into one array
V = data[:, :, 2:4]     # Velocity into another

""" Swapping data according to the assignment """
R = np.swapaxes(R, 1, 2)
V = np.swapaxes(V, 1, 2)

print(R.shape)          # Making sure it's right
print(V.shape)

""" plotting all the elements in the first time step """
import matplotlib.pyplot as plt
plt.figure()
plt.scatter(R[1, 0, :], R[1, 1, :])
plt.axis("square")
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.show()



""" Storing the data """
import h5py
with h5py.File("ca1_step1_output_data.h5", "w") as f:
    f.create_dataset("R", data=R)
    f.create_dataset("V", data=V)
    f.attrs.create("time_steps", data=time_steps)
    f.attrs.create("time_step", data=time_step)
    f.attrs.create("radius", data=radius)
    f.attrs.create("v_variance", data=v_variance)
    f.attrs.create("N_particles", data=N_particles)














