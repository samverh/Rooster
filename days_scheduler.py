"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen
Program makes random schedule based on information from information.py.
"""

import random as rd
import information as inf
import csv


# print how the hours are scheduled
def roomsinfo():
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
    print("Free hours:", free)
    print("Single course scheduled hours:", good)
    print("Hours with multiple courses:", double)


# prints stats of schedule
def info_print():
    # general info
    nec_schedules = 0
    for course in courses:
        nec_schedules += course.practica + \
            course.werkcolleges + course.hoorcolleges
    print("GENERAL INFO:\nAvailable hours:", 4*5*7)
    print("Lectures to be scheduled:", nec_schedules, "\n")

    # print amount of schedulings & stats after scheduling
    print("\nAFTER SCHEDULING")
    roomsinfo(rooms, courses)


# explain true and false...
def matrix_checker(coursename, date, courses, course_names, matrix):

    x = course_names.index(coursename) + 1

    # go through matrix
    for i in range(1, len(matrix[0])):
        if matrix[i][x] == 'x':
            course2 = courses[course_names.index(matrix[i][0])]
            for activity in course2.activities:
                if activity.date == date:
                    return True

    for j in range(1, len(matrix[0])):
        # if courses are connected
        if matrix[x][j] == 'x':
            course2 = courses[course_names.index(matrix[0][j])]
            for activity in course2.activities:
                if activity.date == date:
                    return True

    return False


# assigns room and date for course_lecture
def assign_roomdate(poss_days,rooms):
    room = rooms[rd.randint(0, 6)]
    randd = rd.choice(poss_days)
    day = room.days[randd]
    if room.cap == 117:
        randh = rd.randint(0,4)
    else:
        randh = rd.randint(0,3)
    hour = day.hours[randh]
    date = int("{}{}".format(randd, randh))

    return room, randd, day, randh, hour, date


# schedules on given days
def scheduler(course, lect_type, poss_days, rooms, courses, course_names, matrix):
    # choose day and hour
    room, randd, day, randh, hour, date = assign_roomdate(poss_days,rooms)

    # make sure hour is free
    while hour.scheduled or matrix_checker(course.name, date, courses, course_names, matrix):
        room, randd, day, randh, hour, date = assign_roomdate(poss_days,rooms)

    # add activity to hour and course
    hour.course = course.name + ';' + lect_type
    hour.scheduled = True
    course.activities.append(inf.Activity(lect_type, date, [" "], 'a'))


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
    else:
        return all[:2], all[2:], all[2:]


# course scheduler
def course_scheduler(course,rooms,courses,course_names,matrix):
    hc_days, wc_days, pr_days = days_returner(course)
    i = 0
    # schedule all types
    for i in range(course.hoorcolleges):
        scheduler(course, "Hoorcollege", hc_days, rooms, courses, course_names, matrix)
        i += 1
    for j in range(course.werkcolleges):
        scheduler(course, "Werkcollege", wc_days, rooms, courses, course_names, matrix)
        i += 1
    for k in range(course.practica):
        scheduler(course, "Practica", pr_days, rooms, courses, course_names, matrix)
        i += 1

    return i


# makes total_schedule
def total_schedule(rooms, courses, course_names, matrix):
    # keep track of amount of scheduled classes
    schedulings = 0

    # schedule all required classes
    for course in courses:
        # schedule all hoorcolleges
        schedulings += course_scheduler(course,rooms,courses,course_names,matrix)
    print("Schedulings:", schedulings)


# clears schedule
def clear_schedule(rooms,courses):
    for room in rooms:
        for day in room.days:
            for hour in day.hours:
                hour.scheduled = False
                hour.course = ""

    for course in courses:
        course.dates = []
        course.types = []


# prints schedule into csv file
def print_schedule(rooms):
    with open('schedule.csv', 'w') as outf:
        header = ['Timeslot', 'Room', 'Monday', 'Tuesday'] + \
            ['Wednesday', 'Thursday', 'Friday']
        writer = csv.DictWriter(outf, fieldnames=header)
        writer.writeheader()
        hourslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        for i in range(4):
            for j in range(7):
                weekdays = []
                for k in range(5):
                    weekdays.append(rooms[j].days[k].hours[i].course)
                writer.writerow({"Timeslot": hourslots[i], "Room": rooms[j].name, "Monday":weekdays[0], "Tuesday": weekdays[1], "Wednesday": weekdays[2], "Thursday": weekdays[3], "Friday": weekdays[4]})
        writer.writerow({"Timeslot": hourslots[4], "Room": rooms[5].name, "Monday":weekdays[0], "Tuesday": weekdays[1],\
        "Wednesday": weekdays[2], "Thursday": weekdays[3], "Friday": weekdays[4]})
