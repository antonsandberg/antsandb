""" Oliver Johansson and Anton Sandberg """
""" Group 7, Assignment 1 Step 3 """

import numpy as np
import scipy.spatial
import h5py
import matplotlib.pyplot as plt
from ca1_step2_solution import animate_particles, plot_statistical_analysis

def time_propagation(r, v, time_step):
   r = r + time_step*v
   return r, v

def boundary_collisions(r, v):


    """ Creating boolean arrays and four different where function to check all 4 sides of the square """

    change_v = -v   #Preparing the negative value
    v[0, :] = np.ma.where((r[0, :] < -1)*(v[0, :] < 0), change_v[0, :], v[0, :])   # Depending on where they are about to exit the square
    v[0, :] = np.ma.where((r[0, :] > 1)*(v[0, :] > 0), change_v[0, :], v[0, :])   # Check different x and why values
    v[1, :] = np.ma.where((r[1, :] < -1)*(v[1, :] < 0), change_v[1, :], v[1, :])
    v[1, :] = np.ma.where((r[1, :] > 1)*(v[1, :] > 0), change_v[1, :], v[1, :])
    return r, v

def particle_collisions(r, v, radius):
    for i in range(r.shape[1]):
        for j in range(i+1, r.shape[1]):
            if np.linalg.norm(r[:, i] - r[:, j]) < radius*2 and np.dot(v[:, i] - v[:, j], r[:, i] - r[:, j]) < 0:
                v[:, [i, j]] = v[:, [j, i]] # Swapping velocity values to bounce
    return r, v

def particle_collisions_fast(r, v, radius):
    r_swapaxes = np.swapaxes(r, 1, 0)    #Making r usablue for KDTree
    tree_r = scipy.spatial.cKDTree(r_swapaxes)
    pair = scipy.spatial.cKDTree.query_pairs(tree_r, p=2, r=radius*2)
    pair = np.array(list(pair))   # Modify it to be able to calculate with
    for k in range(len(pair)):
        i, j = pair[k]
        if np.dot(v[:, i] - v[:, j], r[:, i] - r[:, j]) < 0:    # Checking if they are also moving towards each other
            v[:, [i, j]] = v[:, [j, i]]                         # Swapping velocities to bounce
    return r, v

def update_with_interactions_fast(r, v, time_step, radius):
    r, v = time_propagation(r, v, time_step)
    r, v = boundary_collisions(r, v)
    r, v = particle_collisions_fast(r, v, radius)
    return r, v

""" Simulation for the 1st video """
def simulate(r0, v0, time_step, radius, time_steps, update_function, **kwargs):
    R = []  # Create another layer of list
    V = []
    R.append(r0)
    V.append(v0)
    for i in range(time_steps):
        r, v = update_function(R[i], V[i], time_step, radius)
        R.append(r)
        V.append(v)
    R = np.array(R)
    V = np.array(V)
    return R, V

""" Read data from file """
with h5py.File("ca1_step1_output_data.h5", "r") as f:
    time_step = f.attrs["time_step"]
    radius = f.attrs["radius"]
    v_variance = f.attrs["v_variance"]
    N_particles = f.attrs["N_particles"]
    time_steps = f.attrs["time_steps"]

r0 = np.random.uniform(low=-1.0, high=1.0, size=[2, N_particles])
v0 = np.random.normal(loc=0.0, scale=v_variance, size=[2, N_particles])

print(r0.shape, v0.shape)   #Confirming correct shape

x0, y0 = r0[0, :], r0[1, :]
plt.scatter(x0, y0, alpha=0.5)
plt.axis('square')
plt.tight_layout()
plt.show()

simulation4 = simulate(r0, v0, time_step, radius, time_steps=time_steps-1, update_function=update_with_interactions_fast)

R = simulation4[0]
V = simulation4[1]      # Saving away the variables from the simulation

animate_particles(simulation4[0], time_step, 'ca1_step3_movie4.mp4')


plot_statistical_analysis(R, V, time_step, filename='ca1_step3_figure_summary.svg')


