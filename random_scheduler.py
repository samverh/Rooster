"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program makes random schedule based on information from information.py.
"""

import random as rd


def roomsinfo(rooms, courses):
    """
    Prints how the hours are scheduled.
    """
    double = 0
    free = 0
    good = 0

    # iterate over hourslots in rooms and determine amount of scheduled courses
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


def info_print(courses):
    """
    Prints stats of schedule.
    """

    # general info
    nec_schedules # --------------------------------------- shouldnt be here?
    for course in courses:
        nec_schedules += course.practica + course.werkcolleges + course.hoorcolleges

    print("GENERAL INFO:\nAvailable hours: {}\nLectures to be scheduled: {}\n".format(4*5*7, nec_schedules))

    # print amount of schedulings and stats after scheduling
    print("\nAFTER SCHEDULING\nScheduled hours: {}".format(schedulings))
    roomsinfo(rooms, courses)


def scheduler(course, rooms, lect_type):
    """
    Adds class to randomly chosen room, day and hour.
    """
    randr = rd.randint(0, 6)
    randd = rd.randint(0, 4)
    randh = rd.randint(0, 3)
    room = rooms[randr]
    day = room.days[randd]
    hour = day.hours[randh]
    hour.courses.append(course.name + ' - ' + lect_type)
    course.dates.append(int("{}{}".format(randd, randh)))
    course.types.append(lect_type)


def total_schedule(rooms, courses):
    """
    Makes total schedule.
    """

    # keep track of amount of scheduled classes
    schedulings = 0

    # schedule all required classes
    for course in courses:

        # schedule all hoorcolleges
        for i in range(course.hoorcolleges):
            scheduler(course, rooms, "Hoorcollege")
            schedulings += 1

        for j in range(course.werkcolleges):
            scheduler(course, rooms, "Werkcollege")
            schedulings += 1

        for k in range(course.practica):
            scheduler(course, rooms, "Practica")
            schedulings += 1

    return rooms, courses
