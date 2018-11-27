"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Basic schedule functions
"""

import information as inf
import csv

def roomsinfo(rooms):
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


def info_print(rooms, courses):
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
    roomsinfo(rooms)


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
