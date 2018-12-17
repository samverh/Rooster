"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This script visualizes the data gathered by running the different simulated
annealing types.
"""

import matplotlib.pyplot as plt
import pandas as pd
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
plt.hist(plotdata["Random Scheduling"], bins=50, fc=(1, 0, 0, 0.5), label = "Random")

# create legend
red_patch = mpatches.Patch(color=(1, 0, 0, 0.5), label="Random")
plt.legend(handles=[red_patch])

# add graph title
plt.title("Course scheduling: score distribution of random scheduling (N=1000)")

# visualize random plot
plt.show()

# plot histograms for optimizations
p1 = plt.hist(plotdata["Exponential"], bins=50, fc=(0, 0, 1, 0.5), label = "Exponential")
p2 = plt.hist(plotdata["Linear"], bins=50, fc=(0.8, 0.3, 0.5, 0.5), label = "Linear")
p3 = plt.hist(plotdata["Hillclimber"], bins=50, fc=(0.2, 0.2, 0.3, 0.5), label = "Hillclimber")

if type == "courses only":
    p4 = plt.hist(plotdata["Sigmoidal"], bins=50, fc=(1, 0, 0, 0.5), label = "Sigmoidal")
    p5 = plt.hist(plotdata["Geman"], bins=50, fc=(0.2, 1, 0.4, 0.5), label = "Geman")

# create legend
p1_patch = mpatches.Patch(color=(0, 0, 1, 0.5), label="Exponential (20000 iterations)")
p2_patch = mpatches.Patch(color=(0.8, 0.3, 0.5, 0.5), label="Linear (20000 iterations)")
p3_patch = mpatches.Patch(color=(0.2, 0.2, 0.3, 0.5), label = "Hillclimber (1000 iterations)")

if type == "courses only":
    p4_patch = mpatches.Patch(color=(1, 0, 0, 0.5), label="Sigmoidal (5000 iterations)")
    p5_patch = mpatches.Patch(color=(0.2, 1, 0.4, 0.5), label = "Geman (20000 iterations)")

# add legend and graph title
if type == "courses only":
    plt.legend(handles=[p1_patch, p2_patch, p3_patch, p4_patch, p5_patch])
    plt.title("Course scheduling: score distribution of schedules after optimization (N=1000)")
else:
    plt.legend(handles=[p1_patch, p2_patch, p3_patch])
    plt.title("Students scheduling: score distribution of schedules after optimization (N=500)")

# visualize optimization plot
plt.show()
