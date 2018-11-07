"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program makes random schedule based on information from classes.py.
"""

from information import *
import random as rd

# print total numbers just for info
def totaal_printer():
    aantal_uren = 5*5*7

    aantal_nodig = 0

    for vak in vakken:
        aantal_nodig += vak.practica + vak.werkcolleges + vak.hoorcolleges

    print("GENERAL INFO:\nTotaal aantal uren beschikbaar: {}\nTotaalaantal in-te-roosteren colleges: {}\n".format(aantal_uren,aantal_nodig))

# print how the hours are scheduled
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

# function adds class to room
def class_adder(vak,type):
    #indelen
    randl = rd.randint(0,6)
    randd = rd.randint(0,4)
    randh = rd.randint(0,4)
    lokaal = lokalen[randl]
    day = lokaal.days[randd]
    hour = day.hours[randh]
    appendal = vak.name + type
    hour.courses.append(appendal)

# keep track of amount of scheduled classes
ingedeeld = 0

# general info & stats before scheduling
totaal_printer()
print("BEFORE SCHEDULING")
foutenprinter()

# schedule all required classes
for vak in vakken:
    # schedule all hoorcolleges
    for i in range(vak.hoorcolleges):
        class_adder(vak," - Hoorcollege")
        ingedeeld += 1

    for j in range(vak.werkcolleges):
        class_adder(vak," - Werkcollege ")
        ingedeeld += 1

    for k in range(vak.practica):
        class_adder(vak," - Practica ")
        ingedeeld += 1

# print amount of schedulings & stats after scheduling
print("\nAFTER SCHEDULING\nIngedeeld: {}".format(ingedeeld))
foutenprinter()

# clear the schedule
for lokaal in lokalen:
    for i in range(5):
        for j in range(5):
            lokaal.days[i].hours[j].courses = []
