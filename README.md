# Rooster
Class: Heuristieken - Universiteit van Amsterdam

Subject: Lesroosters

Scheduling classes at the university is a difficult task that this program facilitates using heuristics. The classes are scheduled taking into account the expected student count, undesired timeslots, preferred sequence of activities and overlapping courses. It provides an optimal schedule using algorithms. The case consists of 7 classrooms with 20 hours in the week. Additionally, 1 classroom contains an extra evening time slot, which adds 5 extra possible hours to the week. There are 129 course activities, exisiting of normal lectures, working sections and practica. The total amount of student is 609, all of which have individual course subscriptions.

### Constraints & Points
* Normal lectures should be scheduled before other activities of a course
* Some courses should not overlap (see matrix.csv)
* Use of the evening time slot takes -20 points
* Maximal distribution of a course's activities earns +20 points, but points are taken if the distribution is not optimal
* Every student that does not fit in the room takes -1 point
* Per student, +1 point is earned per individual non-conflicting course
* Each course conflict per student results in -1 point

### Bounds of the problem
**Upper bound:**	 

* Maximal distribution per course (considering different groups within course): 880 (outcome of calculations.py)
* Students without course conflicts = 609 * 1 = 609

Total: +1489 points

**Lower bound:** 

* Room < #students = 1177
* Use evening time slot: 5 * 20 = 100
* Course activities (n) divided over n-1 days = 430
* Course conflicts = 11417

Total: -13124 points

### State Space
+ No double scheduling: 145 x 144 x … 18 x 17 x 16 = 10^238 possibilities 

+ Courses overlap: > 10^232 (estimated)

+ 609 students with 1372 individual course subscriptions: 4 x 10^973 (outcome of calculations.py)


Total: 4 x 10^1211

### Algorithms
The algorithms used to improve the schedule are hillclimber and simulated annealing. Four types of simulated annealing were tested, including Sigmoidal, Exponential, Linear and Geman. Due to limited time the different types were ran 25 times each (for now). The distributions of the scores are shown in the graph below.
 ![alt text](https://github.com/samverh/Rooster/blob/master/results/sim_annealing_types.png "Simulated Annealing Types")
 
 The data, image and python script to visualize the plot can be found in the folder "algorithms_visualisations".

## Getting Started
### Prerequisites
The program requires the pandas and termcolor library to run successfully, download the pandas and termcolor libraries using the following codes:

```
pip install pandas
pip install termcolor
```

### Structure
All python codes are in the main folder "Rooster", together with the input values and the output schedule file.

### Testing
To run the program, run the main function:

```
python main.py
```

By opening rooster.html, you can investigate the schedule on a visual level.

## Authors
* Johan Diepstraten
* Ya'gel Schoonderbeek
* Sam Verhezen

## Acknowledgements
* Special thanks to our techassistant Bart van Baal, tutorial assistant Wouter Vrielink and professor Daan van den Berg!
