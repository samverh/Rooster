# Rooster
Class: Heuristieken - Universiteit van Amsterdam

Subject: Lesroosters

Scheduling classes at the university is a difficult task that this program facilitates using heuristics. The classes are scheduled taking into account the expected student count, undesired timeslots, preferred sequence of activities and overlapping courses. It provides an optimal schedule using a genetic algorithm.

**Upper bound:**	 

Goed verdeeld vak: 22 * 20 = 440

Studenten zonder vakconflicten = 609 * 1 = 609

Totaal: 1049 Bonuspunten

**Lower bound:** 

Zaal<#studenten = 1177

Avondslot: 5 * 20 = 100

Vakactiviteiten(n) op n-1 dagen = 430

Vakconflict = 11417

Totaal: 13124 Maluspunten

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
* Johan Diepstraten
* Ya'gel Schoonderbeek
* Sam Verhezen

## Acknowledgements
* Special thanks to our techassistant Bart van Baal
