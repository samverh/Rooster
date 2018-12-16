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

# prompt user for input
type = input("Which data do you want to visualize? (students inc, courses only): ")
while not type in ["students inc", "courses only"]:
    type = input("Incorrect input. Try again (students inc, courses only): ")

# load data
if type == "students inc":
    plotdata = pd.read_csv("../../results/scores_students_inc.csv")
elif type == "courses only":
    plotdata = pd.read_csv("../../results/scores_courses_only.csv")

# set graph attributes
plt.xlabel("Score")
plt.ylabel("Frequency")

# plot random and hillclimber first
p1 = plt.hist(plotdata["Random Scheduling"], bins=50, fc=(1, 0, 0, 0.5), label = "Random")
p2 = plt.hist(plotdata["Random Hillclimber"], bins=50, fc=(0, 0, 1, 0.5), label = "Hillclimber")

# create legend
red_patch = mpatches.Patch(color=(1, 0, 0, 0.5), label="Random")
blue_patch = mpatches.Patch(color=(0, 0, 1, 0.5), label="Hillclimber (1000 iteraties)")
plt.legend(handles=[red_patch, blue_patch])

# add graph title
plt.title("Course scheduling: score distribution of random scheduling and hillclimber (N=1000)")

# visualize plot
plt.show()

# plot histograms per simulated annealing type second
p1 = plt.hist(plotdata["Sigmoidal"], bins=50, fc=(1, 0, 0, 0.5), label = "Sigmoidal")
p2 = plt.hist(plotdata["Exponential"], bins=50, fc=(0, 0, 1, 0.5), label = "Exponential")
p3 = plt.hist(plotdata["Linear"], bins=50, fc=(0.8, 0.3, 0.5, 0.5), label = "Linear")
p4 = plt.hist(plotdata["Geman"], bins=50, fc=(0.2, 1, 0.4, 0.5), label = "Geman")

# create legend
red_patch = mpatches.Patch(color=(1, 0, 0, 0.5), label="Sigmoidal (5000 iteraties)")
blue_patch = mpatches.Patch(color=(0, 0, 1, 0.5), label="Exponential (20000 iteraties)")
wine_patch = mpatches.Patch(color=(0.8, 0.3, 0.5, 0.5), label="Linear (20000 iteraties)")
new_patch = mpatches.Patch(color=(0.2, 1, 0.4, 0.5), label = "Geman (20000 iteraties)")
plt.legend(handles=[red_patch, blue_patch, wine_patch, new_patch])

# add graph title
plt.title("Course scheduling: score distribution of simulated annealing types (N=1000)")

# visualize plot
plt.show()
