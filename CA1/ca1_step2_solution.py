""" Oliver Johansson and Anton Sandberg """
""" Group 7, Assignment 1 Step 2 """

import numpy as np
import h5py
import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import uniform
from scipy.stats import norm
from scipy.stats import rayleigh
import os
import matplotlib.animation as animation



""" Function to plot the window with the 8 graphs assigned """
def plot_statistical_analysis(R, V, time_step, filename):
    # Total kinetic energy and total velocity
    V_calc1 = np.linalg.norm(V, axis=1)         # Calculating sumations and norms accordingly
    V_calc2 = (V_calc1 ** 2)                    # by the given exercise
    E_k = np.sum(V_calc2, axis=1) / 2
    V_tot = np.sum(V, axis=2)
    V_tot = np.linalg.norm(V_tot, axis=1)
    print(R.shape)

    dists = R[:, :, np.newaxis, :] - R[:, :, :, np.newaxis]    # Creating another axis to be able to compare the values
                                                               # And calculate the distances between particles

    dists = np.linalg.norm(dists, axis=1)                      # Calculating norm
    dists = np.reshape(dists, (400*400*1000, 1))            # Putting every value in a row

    R = np.reshape(R, [400*1000, 2])    # reshape the matrixes so they can be plotted
    R_x = R[:, 0]   # Creating x and y vectors
    R_y = R[:, 1]
    V = np.reshape(V, [400*1000, 2])

    V_x = V[:, 0]   # Creating x and y vectors
    V_y = V[:, 1]
    V = np.linalg.norm(V, axis=1)           # Creating the norm vector needed for plotting

    time = "time"
    t = np.arange(0, 20, time_step)     # Predefinitions

    plt.figure(tight_layout=True, figsize=[9., 6.])
    # Average time
    plt.subplot(421)
    plt.plot(t, V_tot)                  # Everything here is pretty self explanatory
    plt.xlabel(time)                    # plot time with wanted vector, V, dists and E_k
    plt.ylabel("Average speed")

    # Kinetic energy
    plt.subplot(422)
    plt.plot(t, E_k)
    plt.ylabel("Kinetic energy")
    plt.ylim([min(E_k)-0.2, max(E_k)+0.2])
    plt.xlabel(time)

    # Distance
    plt.subplot(423)
    plt.xlabel("distance")                          # Create the histograms with hist
    plt.ylabel("Pair distribution\n probability")   # and then input the wanted vectors
    plt.xlim([-0.5, max(dists)+1])
    plt.hist(dists, bins=50, density="True")

    # Speed
    plt.subplot(424)
    plt.xlabel("speed")
    plt.ylabel("Velocity norm\n probability")
    plt.hist(V, bins="auto", density="True")
    x = np.linspace(min(V), max(V), 100)            # The vector needed to plot the pdf and reg. plot needs together with
    loc_V, scale_V = rayleigh.fit(V)                # Creating the values pdf needs
    plt.plot(x, rayleigh.pdf(x, loc_V, scale_V))
                                                    # All the other pdfs are done
    # x position                                    # the same way
    plt.subplot(425)                                # also am creating x.lims and y.lims
    plt.xlabel("x position")                        # where they are needed
    plt.ylabel("Probability")
    plt.hist(R_x, bins="auto", density="True")
    x = np.linspace(min(R_x)-0.5, max(R_x)+0.5, 100)
    loc_R_x, scale_R_x = uniform.fit(R_x)
    plt.plot(x, uniform.pdf(x, loc_R_x, scale_R_x))

    # y position
    plt.subplot(426)
    plt.xlabel("y position")
    plt.ylabel("Probability")
    plt.hist(R_y, bins="auto", density="True")
    x = np.linspace(min(R_y)-0.5, max(R_y)+0.5, 100)
    loc_R_y, scale_R_y = uniform.fit(R_y)
    plt.plot(x, uniform.pdf(x, loc_R_y, scale_R_y))

    # x velocity
    plt.subplot(427)
    plt.xlabel("x velocity")
    plt.ylabel("Probability")
    plt.hist(V_x, bins="auto", density="True")
    x = np.linspace(min(V_x)-0.2, max(V_x)+0.2, 100)
    loc_v_x, scale_v_x = norm.fit(V_x)
    plt.plot(x, norm.pdf(x, loc_v_x, scale_v_x))

    # y velocity
    plt.subplot(428)
    plt.xlabel("y velocity")
    plt.ylabel("Probability")
    plt.hist(V_y, bins="auto", density="True")
    x = np.linspace(min(V_y)-0.2, max(V_y)+0.2, 100)
    loc_v_y, scale_v_y = norm.fit(V_y)
    plt.plot(x, norm.pdf(x, loc_v_y, scale_v_y))
    plt.savefig(filename)
    plt.show()

# Function to be able to make the clip
def animate_particles(R, time_step, filename='movie.mp4'):
    """Generates an mp4 movie with the particle trajectories
    using MatPlotLib. """

    if os.path.isfile(filename):
        print('WARNING (animate_particles): The output file', filename, 'exists. Skipping animation.')
        return

    frames = R.shape[0]
    frames_per_second = 1. / time_step

    fig = plt.figure(figsize=(6, 6))
    ax = plt.subplot()

    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('image')
    plt.xlim([-1.0, 1.0])
    plt.ylim([-1.0, 1.0])

    markers = ax.scatter([], [], s=200, alpha=0.5)
    text = plt.text(-0.9, 0.9, 'frame =', ha='left')

    def update(frame, markers, text):
        print('frame =', frame)
        r = R[frame]
        markers.set_offsets(r.T)
        text.set_text('frame = {}'.format(frame))

    anim = animation.FuncAnimation(
        fig, update,
        frames=frames, interval=50,
        fargs=(markers, text),
        blit=False, repeat=False,
    )

    writer = animation.writers['ffmpeg'](fps=frames_per_second)
    anim.save(filename, writer=writer, dpi=100)
    plt.close()

if __name__ == "__main__":
    """ Read data from file """
    with h5py.File("ca1_step1_output_data.h5", "r") as f:
        R1 = f.get("R")     # Extracting the arrays with get
        R  = np.array(R1)   # and then create arrays out of them
        V1 = f.get("V")
        V  = np.array(V1)
        time_step = f.attrs["time_step"]    # Grabbing the wanted values
        radius = f.attrs["radius"]
        v_variance = f.attrs["v_variance"]
        print(type(V), type(R))

    """ Code to plot the first graph, for particle 123 """
    y_pos = R[:, 1, 123]
    time = "time"

    """ Creating the first plot, of particle 123 """
    t = np.arange(0, 20, time_step)
    plt.figure()
    plt.plot(t, y_pos)
    plt.ylabel("y-position of particle nr. 123")
    plt.xlabel(time)
    plt.show()

    plot_statistical_analysis(R, V, time_step, filename='ca1_step2_figure_summary.svg')

    animate_particles(R, time_step, filename='ca1_step1_movie.mp4')







































