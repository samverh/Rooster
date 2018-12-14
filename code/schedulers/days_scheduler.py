"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program makes random schedule based on information from information.py
and writes it to a csv file.
"""

import random as rd
import information as inf
import csv
import schedule_basics as bas


def assign_roomdate(poss_days, rooms):
    """
    Assigns room and date for a course by scheduling it randomly in a free slot.
    """

    # choose random room and day, considering preferred sequence of activities
    room = rooms[rd.randint(0, 6)]
    randd = rd.choice(poss_days)
    day = room.days[randd]

    # largest lecture room has an additional timeslot, other rooms have four
    if room.cap == 117:
        randh = rd.randint(0, 4)

    else:
        randh = rd.randint(0, 3)

    # choose randomly timeslot in the selected day and room and remember the slot
    hour = day.hours[randh]
    date = int("{}{}".format(randd, randh))

    return room, randd, day, randh, hour, date


def scheduler(course, lect_type, group_id, poss_days, rooms, courses, course_names, matrix):
    """
    Schedules on given days.
    """

    # choose day and hour and make sure timeslot is free
    room, randd, day, randh, hour, date = assign_roomdate(poss_days, rooms)
    j = 0

    while hour.scheduled or bas.matrix_checker(course.name, date, courses, course_names, matrix):
        j += 1
        if j > 10000:
            poss_days = [x for x in range(5)]

        room, randd, day, randh, hour, date = assign_roomdate(poss_days, rooms)


    # add class activity (lecture type) to hour and course and add group ID
    if group_id == 'x':
        hour.course = course.name + ' | ' + lect_type
        hour.scheduled = True
        course.activities.append(inf.Activity(lect_type, date, [" "], group_id, room.name, course.e_students))

    else:
        hour.course = course.name + ' | ' + lect_type + ' | ' + group_id
        hour.scheduled = True
        course.activities.append(inf.Activity(lect_type, date, [" "], group_id, room.name, max(course.max_werkcolleges, course.max_practica)))


def days_returner(course):
    """
    Return possible days for all lecture types considering the preferred sequence
    of hearing lectures before other activities.
    """

    # make a list with a number for every possible working days in a week
    all = [x for x in range(5)]

    # no hoorcolleges
    if course.hoorcolleges == 0:
        return [], all, all

    # only hoorcolleges
    elif course.practica == 0 and course.werkcolleges == 0:
        return all, [], []

    # more hoorcolleges
    elif course.hoorcolleges > course.practica + course.werkcolleges:
        return all[:2], all[2:], all[2:]

    # less hoorcolleges
    else:
        return all[:2], all[2:], all[2:]


def course_scheduler(course, rooms, courses, course_names, matrix):
    """
    Schedules course.
    """

    # determine amount of lecture types for the specified course
    hc_days, wc_days, pr_days = days_returner(course)
    i = 0

    # schedule all lecture types
    for f in range(course.hoorcolleges):
        scheduler(course, "Hoorcollege", 'x', hc_days, rooms, courses, course_names, matrix)
        i += 1

    for j in range(course.werkcolleges):
        m, r = 0, course.e_students

        while r > 0:
            m += 1
            r -= course.max_werkcolleges

        for j_2 in range(m):
            scheduler(course, "Werkcollege", chr(97+j_2), wc_days, rooms,\
                      courses, course_names, matrix)
            i += 1

    for k in range(course.practica):
        m, r = 0, course.e_students

        while r > 0:
            m += 1
            r -= course.max_practica

        for k_2 in range(m):
            scheduler(course, "Practica", chr(97+k_2), pr_days, rooms, courses,\
                      course_names, matrix)
            i += 1

    return i


def total_schedule(rooms, courses, course_names, matrix):
    """
    Makes the total schedule.
    """

    # keep track of amount of scheduled classes
    schedulings = 0

    # schedule all required classes
    for course in courses:
        # schedule all hoorcolleges
        schedulings += course_scheduler(course, rooms, courses, course_names, matrix)
    print("Schedulings:", schedulings)
