# Code
## Schedulers
* ```schedule_basics.py``` contains basic function for scheduling.
* ```random_scheduler.py``` generates a random schedule.
* ```days_scheduler.py``` generates a schedule respecting the distribution of courses over the weekdays.

## Classes
* ```information.py``` contains the python data structure with classes.

## Algorithms
* ```hillclimber.py``` runs a hillclimber on the random schedule and contains simulated annealing functions.
* ```student_hillclimber.py``` runs a hillclimber for schedule with students.
* ```population_based.py``` is a plant propagation algorithm.

## Score and other calculations
* ```score.py``` gives a score to the generates schedule.
* ```calculations.py``` calculates the state space using N/K.
* ```painpoints.py``` determines the painpoints in the case. Running the script generates an excel file, found under "data".

## Visualizer
* ```rooster.css``` visual.html makes a webpage of the generated schedule csv file, using rooster.css as stylesheet.
* ```plot_results.py``` visualizes data gathered by running the scheduler consequently (randomly, with hillclimber and with simulated annealing types). Data is included of scheduling only courses, as well as with students included. The program will prompt for input, please follow the descriptions to generate the desired plots. Additionally, a picture of the plots (png format) is included in the folder "results".
* ```input_prompt.py``` is a script which is used by main.py to get input from the user on how to run the scheduler.
