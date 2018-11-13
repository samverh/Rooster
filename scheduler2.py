"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen
Program makes random schedule based on information from information.py.
"""

from information import *
import random as rd

# print how the hours are scheduled
def roomsinfo(rooms,courses):
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
    print("Free hours: {}\nSingle course scheduled hours: {}\nHours with multiple courses: {}".format(free,good,double))

# prints stats of schedule
def info_print(courses):
    # general info
    nec_schedules
    for course in courses:
        nec_schedules += course.practica + course.werkcolleges + course.hoorcolleges
    print("GENERAL INFO:\nAvailable hours: {}\nLectures to be scheduled: {}\n".format(4*5*7,nec_schedules))

    # print amount of schedulings & stats after scheduling
    print("\nAFTER SCHEDULING\nScheduled hours: {}".format(schedulings))
    roomsinfo(rooms,courses)

# schedules on given days
def scheduler(course,rooms,lect_type,days):
    # choose day and hour
    room = rooms[rd.randint(0,6)]
    day = rd.choice(room.days)
    hour = days.hours[rd.randint(0,3)]

    # make sure hour is free
    while hour.scheduled:
        room = rooms[rd.randint(0,6)]
        day = rd.choice(room.days)
        hour = days.hours[rd.randint(0,3)]

    hour.courses.append(course.name + ' - ' + lect_type)
    hour.scheduled = True
    course.dates.append(int("{}{}".format(randd,randh)))
    course.types.append(lect_type)

# return possible days for all types
def days_returner(course):
    all = [x for x in range(5)]

    # no hoorcolleges
    if course.hoorcolleges == 0:
        return [], all, all
    # only hoorcolleges
    elif course.practica == 0 and course.werkcolleges == 0:
        return all, [], []
    # more hoorcolleges
    elif course.hoorcolleges > course.practica + course.werkcolleges:
        return all[:3], all[3:], all[3:]
    # less hoorcolleges
    else
        return all[:2], all[2:], all[2:]

# course scheduler
def course_scheduler(course):
    hc_days, wc_days, pr_days = days_returner(course)

    # schedule all types
    for i in range(course.hoorcolleges):
        scheduler(course,rooms,"Hoorcollege",hc_days)
    for j in range(course.werkcolleges):
        scheduler(course,rooms,"Werkcollege",wc_days)
    for k in range(course.practica):
        scheduler(course,rooms,"Practica",pr_days)

# makes total_schedule
def total_schedule(rooms,courses):
    # keep track of amount of scheduled classes
    schedulings = 0

    # schedule all required classes
    for course in courses:
        # schedule all hoorcolleges
        course_scheduler(course)

    return rooms, courses
