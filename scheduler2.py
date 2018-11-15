"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen
Program makes random schedule based on information from information.py.
"""

from information import *
import random as rd
import csv

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

def matrix_checker(coursename, date, course_names):

    x = course_names.index(coursename) + 1

    # go through matrix
    for i in range(1,len(matrix)):
        if matrix[i][x] == 'x':
            course2 = courses[course_names.index(matrix[i][0])]
            for date2 in course2.dates:
                if date2 == date:
                    return True

    for j in range(i, len(matrix[0])):

            # if courses are connected
            if matrix[x][j] == 'x':
                course2 = courses[course_names.index(matrix[0][j])]
                for date2 in course2.dates:
                    if date2 == date:
                        return True
    return False
def assign_roomdate(rooms,poss_days):
    room = rooms[rd.randint(0,6)]
    randd = rd.choice(poss_days)
    day = room.days[randd]
    randh = rd.randint(0,3)
    hour = day.hours[randh]
    date = int("{}{}".format(randd,randh))

    return room, randd, day, randh, hour, date

# schedules on given days
def scheduler(course,rooms,lect_type,poss_days,course_names):
    # choose day and hour
    room, randd, day, randh, hour, date = assign_roomdate(rooms,poss_days)

    # make sure hour is free # We zouden ook uren, dagen en lokalen uit de lijst kunnen halen zodra ze vol zitten
    while hour.scheduled and matrix_checker(course.name, date,course_names):
        room, randd, day, randh, hour, date = assign_roomdate()

    hour.courses.append(course.name + ' - ' + lect_type)
    hour.scheduled = True
    # randd en randh bestaat niet meer?
    course.dates.append(date)
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
    else:
        return all[:2], all[2:], all[2:]

# course scheduler
def course_scheduler(rooms, course,course_names):
    hc_days, wc_days, pr_days = days_returner(course)

    # schedule all types
    for i in range(course.hoorcolleges):
        scheduler(course,rooms,"Hoorcollege",hc_days,course_names)
    for j in range(course.werkcolleges):
        scheduler(course,rooms,"Werkcollege",wc_days,course_names)
    for k in range(course.practica):
        scheduler(course,rooms,"Practica",pr_days,course_names)

# makes total_schedule
def total_schedule(rooms,courses,course_names):
    # keep track of amount of scheduled classes
    schedulings = 0

    # schedule all required classes
    for course in courses:
        # schedule all hoorcolleges
        course_scheduler(rooms, course,course_names)

    return rooms, courses

def print_schedule():
    with open('schedule.csv', 'w') as outf:
        header = ['Timeslot','Room', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        writer = csv.DictWriter(outf, fieldnames=header)
        hourslots = ["9-11", "11-13", "13-15", "15-17"]
        for i in range(4):
            for j in range(7):
                weekdays = []
                for k in range(5):
                    weekdays.append(rooms[j].days[k].hours[i].courses[0])
                writer.writerow({hourslots[i], rooms[j].name, weekdays[0], weekdays[1], weekdays[2], weekdays[3], weekdays[4]})
