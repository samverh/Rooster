# Rooster
Class: Heuristieken - Universiteit van Amsterdam
Subject: Lesroosters

Scheduling classes at the university is a difficult task that this program facilitates using heuristics. The classes are scheduled taking into account the expected student count, undesired timeslots, preferred sequence of activities and overlapping courses. It provides an optimal schedule using a genetic algorithm.


((Roostermaker.py creates a schedule for the courses in vakken.txt in the rooms from lokalen.txt. The program uses the structures defined in information.py. A score is assigned to the created schedule in score.py))

## Getting Started
### Prerequisites
The program requires the pandas library to run successfully, download pandas the following:

```
pip install pandas
```

### Structure
All python codes are in the main folder "Rooster", together with the input values and the output schedule file.

### Testing
To run the program, run the main function:

```
python main.py
```

## Authors
* Sam Verhezen, Ya'gel Schoonderbeek & Johan Diepstraten

## Acknowledgements
* Special thanks to our techassistant Bart van Baal
