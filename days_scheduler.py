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


def roomsinfo():
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
    print("Free hours:", free)
    print("Single course scheduled hours:", good)
    print("Hours with multiple courses:", double)


def info_print():
    """
    Prints stats schedules.
    """

    # general info
    nec_schedules = 0

    # iterate over courses and determine amount of course activities
    for course in courses:
        nec_schedules += course.practica + \
            course.werkcolleges + course.hoorcolleges
    print("GENERAL INFO:\nAvailable hours:", 4*5*7)
    print("Lectures to be scheduled:", nec_schedules, "\n")

    # print amount of schedulings & stats after scheduling
    print("\nAFTER SCHEDULING")
    roomsinfo(rooms, courses)


def matrix_checker(coursename, date, courses, course_names, matrix):
    """
    Checks matrix for overlapping courses.
    Returns true if not-overlapping courses overlap and returns false otherwise.
    """

    # get position of course in matrix
    x = course_names.index(coursename) + 1

    # go through matrix and determine courses with which no overlap may occur
    for i in range(1, len(matrix[0])):
        if matrix[i][x] == 'x':
            course2 = courses[course_names.index(matrix[i][0])]

            # check if not-overlapping course is already scheduled at timeslot
            for activity in course2.activities:
                if activity.date == date:
                    return True

    # repeat preceding process for vertical direction of matrix
    for j in range(1, len(matrix[0])):
        if matrix[x][j] == 'x':
            course2 = courses[course_names.index(matrix[0][j])]
            for activity in course2.activities:
                if activity.date == date:
                    return True

    return False


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

    while hour.scheduled or matrix_checker(course.name, date, courses, course_names, matrix):
        room, randd, day, randh, hour, date = assign_roomdate(poss_days, rooms)

    # add class activity (lecture type) to hour and course and add group ID
    if group_id == 'x':
        hour.course = course.name + ' | ' + lect_type
        hour.scheduled = True
        course.activities.append(inf.Activity(lect_type, date, [" "], group_id))

    else:
        hour.course = course.name + ' | ' + lect_type + ' | ' + group_id
        hour.scheduled = True
        course.activities.append(inf.Activity(lect_type, date, [" "], group_id))


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
    for i in range(course.hoorcolleges):
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


def clear_schedule(rooms, courses):
    """
    Clears the schedule.
    """

    # iterate over all timeslots in days for every room and clear courses
    for room in rooms:
        for day in room.days:
            for hour in day.hours:
                hour.scheduled = False
                hour.course = ""

    # clear all memorised dates and types of courses
    for course in courses:
        course.dates = []
        course.types = []


def print_schedule(rooms):
    """
    Writes schedule to a csv file.
    """

    # open a csv file and write headers and timeslots
    with open('schedule.csv', 'w') as outf:
        header = ['Timeslot', 'Room', 'Monday', 'Tuesday'] + \
            ['Wednesday', 'Thursday', 'Friday']
        writer = csv.DictWriter(outf, fieldnames=header)
        writer.writeheader()
        hourslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]

        # iterate over hours
        for i in range(4):

            # iterate over rooms and give room a list of days
            for j in range(7):
                weekdays = []

                # append course at specified room and timeslot for every day to list
                for k in range(5):
                    weekdays.append(rooms[j].days[k].hours[i].course)

                # write row with coures for all days at a specific timeslot and room
                writer.writerow({"Timeslot": hourslots[i], "Room": rooms[j].name,\
                                 "Monday":weekdays[0], "Tuesday": weekdays[1],\
                                 "Wednesday": weekdays[2], "Thursday": weekdays[3],\
                                 "Friday": weekdays[4]})

        # write similar row for the evening timeslots only
        writer.writerow({"Timeslot": hourslots[4], "Room": rooms[5].name,\
                         "Monday": weekdays[0], "Tuesday": weekdays[1],\
                         "Wednesday": weekdays[2], "Thursday": weekdays[3],\
                         "Friday": weekdays[4]})
