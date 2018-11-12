"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program makes random schedule based on information from information.py.
"""

from information import *
import random as rd


# Print how the hours are scheduled
def roomsinfo(rooms, courses):
    double = 0
    free = 0
    good = 0
    for room in rooms:
        for i in range(5):
            for j in range(4):
                amount = len(room.days[i].hours[j].courses)
                if amount == 0:
                    free += 1
                elif amount == 1:
                    good += 1
                else:
                    double += 1
    print("Free hours: {}\nSingle course scheduled hours: {}\nHours with multiple courses: {}".format(free, good, double))


# Prints stats of schedule
def info_print(courses):

    # General info
    nec_schedules
    for course in courses:
        nec_schedules += course.practica + course.werkcolleges + course.hoorcolleges
    print("GENERAL INFO:\nAvailable hours: {}\nLectures to be scheduled: {}\n".format(4*5*7, nec_schedules))

    # Print amount of schedulings & stats after scheduling
    print("\nAFTER SCHEDULING\nScheduled hours: {}".format(schedulings))
    roomsinfo(rooms, courses)


# function adds class to room
def scheduler(course, rooms, lect_type):

    #Indelen
    randr = rd.randint(0, 6)
    randd = rd.randint(0, 4)
    randh = rd.randint(0, 3)
    room = rooms[randr]
    day = room.days[randd]
    hour = day.hours[randh]
    hour.courses.append(course.name + lect_type)


# Makes total_schedule
def total_schedule(rooms, courses):

    # Keep track of amount of scheduled classes
    schedulings = 0
    read_info(courses, rooms)

    # Schedule all required classes
    for course in courses:

        # Schedule all hoorcolleges
        for i in range(course.hoorcolleges):
            scheduler(course, rooms, " - Hoorcollege")
            schedulings += 1

        for j in range(course.werkcolleges):
            scheduler(course, rooms, " - Werkcollege ")
            schedulings += 1

        for k in range(course.practica):
            scheduler(course, rooms, " - Practica ")
            schedulings += 1

    return rooms, courses
