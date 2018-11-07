"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program makes random schedule based on information from classes.py.
"""

from information import *
import random as rd

# keep track of amount of scheduled classes
ingedeeld = 0

# schedule all required classes
for vak in vakken:
    for i in range(vak.hoorcolleges):
        ingedeeld = ingedeeld + 1
        #indelen
        lokaal = lokalen[rd.randint(0,6)]
        day = lokaal.days[rd.randint(0,4)]
        hour = day.hours[rd.randint(0,4)]
        hour.scheduled = True
        hour.courses.append(vak.name + " - Hoorcollege ")

    for j in range(vak.werkcolleges):
        ingedeeld = ingedeeld + 1
        # indelen
        lokaal = lokalen[rd.randint(0,6)]
        day = lokaal.days[rd.randint(0,4)]
        hour = day.hours[rd.randint(0,4)]
        hour.scheduled = True
        hour.courses.append(vak.name + " - Werkcollege")

    for k in range(vak.practica):
        ingedeeld = ingedeeld + 1
        # indelen
        lokaal = lokalen[rd.randint(0,6)]
        lokaal = lokalen[rd.randint(0,6)]
        day = lokaal.days[rd.randint(0,4)]
        hour = day.hours[rd.randint(0,4)]
        hour.scheduled = True
        hour.courses.append(vak.name + " - Practicum ")

# print amount of schedulings
print("Ingedeeld: {}\n".format(ingedeeld))

# print for each room how it is scheduled
def foutenprinter():
    dubbeluren = 0
    vrijlokalen = 0
    goedgepland = 0
    for lokaal in lokalen:
        for i in range(5):
            for j in range(5):
                aantal = len(lokaal.days[i].hours[j].courses)
                if aantal == 0:
                    vrijlokalen += 1
                elif aantal == 1:
                    goedgepland += 1
                else:
                    dubbeluren += 1
    print("Vrije uren: {}\nGoed geroosterde uren: {}\nDubbel geroosterde uren: {}".format(vrijlokalen,goedgepland,dubbeluren))

# print total numbers
def totaal_printer():
    aantal_uren = 5*5*7

    aantal_nodig = 0

    for vak in vakken:
        aantal_nodig += vak.practica + vak.werkcolleges + vak.hoorcolleges

    print("\nTotaal aantal uren beschikbaar: {}\nTotaalaantal benodigde colleges: {}".format(aantal_uren,aantal_nodig))

foutenprinter()
totaal_printer()

for lokaal in lokalen:
    for i in range(5):
        for j in range(5):
            lokaal.days[i].hours[j].courses = []
