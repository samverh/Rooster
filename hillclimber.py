"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program tries to locally improve the solution and solve the
constrain relaxation.
"""

import random as rd
import information as inf
import schedule_basics as bas
import score as sc
import schedule_basics as bas_sch


def random_hour_finder(rooms):
    # choose random room and day, considering preferred sequence of activities
    randr = rd.randint(0, 6)
    room = rooms[randr]
    randd = rd.randint(0,4)
    day = room.days[randd]

    # largest lecture room has an additional timeslot, other rooms have four
    if room.cap == 117:
        randh = rd.randint(0, 4)

    else:
        randh = rd.randint(0, 3)

    # choose randomly timeslot in the selected day and room and remember the slot
    hour = day.hours[randh]
    date = int("{}{}".format(randd, randh))

    return room, date


def switcher(room1, date1, room2, date2, courses, course_names):
    hour1 = room1.days[date1//10].hours[date1%10]
    hour2 = room2.days[date2//10].hours[date2%10]
    if (not hour1.scheduled and not hour2.scheduled):
        return True

    elif not hour1.scheduled:
        course2 = courses[course_names.index(hour2.course.split(" | ")[0])]
        for activity in course2.activities:
            if activity.date == date2 and activity.room == room2.name:
                activity.date = date1
                activity.room = room1

    elif not hour2.scheduled:
        course1 = courses[course_names.index(hour1.course.split(" | ")[0])]
        for activity in course1.activities:
            if activity.date == date1 and activity.room == room1.name:
                activity.date = date2
                activity.room = room2

    else:
        course1 = courses[course_names.index(hour1.course.split(" | ")[0])]
        course2 = courses[course_names.index(hour2.course.split(" | ")[0])]
        for activity in course1.activities:
            if activity.date == date1 and activity.room == room1.name:
                activity.date = date2
                activity.room = room2
        for activity in course2.activities:
            if activity.date == date2 and activity.room == room2.name:
                activity.date = date1
                activity.room = room1

    temp_course = hour1.course
    temp_bool = hour1.scheduled
    hour1.course = hour2.course
    hour1.scheduled = hour2.scheduled
    hour2.course = temp_course
    hour2.scheduled = temp_bool


def calc_score(courses, rooms, course_names, matrix):
    for course in courses:
        course.goodbad = 0
    points = 0
    points += sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
    points += sc.student_checker(rooms, courses, course_names)
    dist_bonus, dist_malus = sc.distribution_checker(courses)
    points += dist_bonus + dist_malus
    points += sc.evening_checker(rooms, courses, course_names)

    return points


def climber(courses, rooms, course_names, max_iterations, old_score, matrix):
    i = 0
    while i < max_iterations:
        room1, date1 = random_hour_finder(rooms)
        room2, date2 = random_hour_finder(rooms)
        switcher(room1, date1, room2, date2, courses, course_names)
        switcher(room1, date1, room2, date2, courses, course_names)
        new_score = calc_score(courses, rooms, course_names, matrix)
        print(new_score)
        i += 1

    return old_score, max_iterations
