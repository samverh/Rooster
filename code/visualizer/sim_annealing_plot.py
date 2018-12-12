"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This script visualizes the data gathered by running the different simulated
annealing types.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches

# load data
plotdata = pd.read_csv("sim_annealing_data.csv")

# plot histograms per simulated annealing type
p1 = plt.hist(plotdata["sigmoidal(5000 iteraties)"], bins=50, fc=(1, 0, 0, 0.5), label = "Sigmoidal")
p2 = plt.hist(plotdata["exponential(20000 iteraties)"], bins=50, fc=(0, 0, 1, 0.5), label = "Exponential")
p3 = plt.hist(plotdata["linear(20000 iteraties)"], bins=50, fc=(0.8, 0.3, 0.5, 0.9), label = "Linear")
p4 = plt.hist(plotdata["geman(20000 iteraties)"], bins=50, fc=(0.2, 1, 0.4, 0.9), label = "Geman")

# create legend
red_patch = mpatches.Patch(color=(1, 0, 0, 0.5), label="Sigmoidal")
blue_patch = mpatches.Patch(color=(0, 0, 1, 0.5), label="Exponential")
wine_patch = mpatches.Patch(color=(0.8, 0.3, 0.5, 0.9), label="Linear")
new_patch = mpatches.Patch(color=(0.2, 1, 0.4, 0.9), label = "Geman")
plt.legend(handles=[red_patch, blue_patch, wine_patch, new_patch])

# add graph attributes
plt.xlabel("Score")
plt.ylabel("Frequency")
plt.title("Random scheduling: score distribution of simulated annealing types (N=25)")

# visualize plot
plt.show()
