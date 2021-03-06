"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program tries to locally improve the solution and solve the
constrain relaxation.
"""

import random as rd
import score as sc
from termcolor import colored, cprint
import math


def random_hour_finder(rooms):
    """
    Function returns a random room and date.
    """

    # choose random room and day, considering preferred sequence of activities
    randr = rd.randint(0, 6)
    room = rooms[randr]
    randd = rd.randint(0, 4)
    day = room.days[randd]

    # largest lecture room has an additional timeslot, other rooms have four
    if room.cap == 117:
        randh = rd.randint(0, 4)

    else:
        randh = rd.randint(0, 3)

    # choose randomly timeslot in the selected day and room and remember the slot
    date = int("{}{}".format(randd, randh))

    return room, date


def activity_switcher(course, date1, room1, date2, room2):
    """
    Function replaces the schedule of a course activity from one room and date
    to another room and date.
    """

    for activity in course.activities:
        if activity.date == date1 and activity.room == room1.name:
            activity.date = date2
            activity.room = room2.name
        elif activity.date == date2 and activity.room == room2.name:
            activity.date = date1
            activity.room = room1.name


def switcher2(room1, date1, room2, date2, courses, course_names):
    """
    Switch courses.
    """

    hour1 = room1.days[date1 // 10].hours[date1 % 10]
    hour2 = room2.days[date2 // 10].hours[date2 % 10]

    # check if picked hours are scheduled or not
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

    # make sure the right activity is switched
    for activity in course2.activities:
        if activity.date == date1 and activity.room == room1.name:
            activity.date = date2
            activity.room = room2
        if activity.date == date2 and activity.room == room2.name:
            activity.date = date1
            activity.room = room1

    # switch the activities
    temp_course = hour1.course
    temp_bool = hour1.scheduled
    hour1.course = hour2.course
    hour1.scheduled = hour2.scheduled
    hour2.course = temp_course
    hour2.scheduled = temp_bool


def switcher(room1, date1, room2, date2, courses, course_names):
    """
    Switch courses.
    """

    hour1 = room1.days[date1 // 10].hours[date1 % 10]
    hour2 = room2.days[date2 // 10].hours[date2 % 10]

    # check if picked hours are scheduled or not to act apropriate
    if (not hour1.scheduled and not hour2.scheduled):
        return True

    elif not hour1.scheduled:
        course2 = courses[course_names.index(hour2.course.split(" | ")[0])]
        activity_switcher(course2, date1, room1, date2, room2)

    elif not hour2.scheduled:
        course1 = courses[course_names.index(hour1.course.split(" | ")[0])]
        activity_switcher(course1, date1, room1, date2, room2)

    else:
        course1 = courses[course_names.index(hour1.course.split(" | ")[0])]
        course2 = courses[course_names.index(hour2.course.split(" | ")[0])]
        activity_switcher(course1, date1, room1, date2, room2)
        activity_switcher(course2, date1, room1, date2, room2)

    # switch the activities
    temp_course = hour1.course
    temp_bool = hour1.scheduled
    hour1.course = hour2.course
    hour1.scheduled = hour2.scheduled
    hour2.course = temp_course
    hour2.scheduled = temp_bool


def calc_score(courses, rooms, course_names, matrix):
    """
    Score calculation.
    """

    #  iterate through courses and set all scores to zero
    for course in courses:
        course.goodbad = 0

    # calculate points for all categories and add them
    points = 0
    points += sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
    points += sc.student_checker(rooms, courses, course_names)
    dist_bonus, dist_malus = sc.distribution_checker(courses)
    points += dist_bonus + dist_malus
    points += sc.evening_checker(rooms, courses, course_names)

    return points


def course_climber(course, courses, rooms, course_names, max_iterations, old_score, matrix):
    """
    Courses hillclimber.
    """

    i = 0
    for activity in course.activities:
        while i < max_iterations:

            date1 = activity.date
            for room in rooms:
                if room.name == activity.room:
                    room1 = room

            room2, date2 = random_hour_finder(rooms)
            switcher(room1, date1, room2, date2, courses, course_names)
            new_score = calc_score(courses, rooms, course_names, matrix)

            if new_score > old_score:
                old_score = new_score
                i = 0
            else:
                switcher(room1, date1, room2, date2, courses, course_names)
                i += 1

    final_score = calc_score(courses, rooms, course_names, matrix)

    return final_score


def random_climber(courses, rooms, course_names, max_iterations, old_score, matrix):
    """
    Random schedule hillclimber.
    """

    i = 0

    #  repeat untill no better score is found for the length of max_iterations
    while i < max_iterations:

        # choose two random rooms on a random date and switch them
        room1, date1 = random_hour_finder(rooms)
        room2, date2 = random_hour_finder(rooms)
        switcher(room1, date1, room2, date2, courses, course_names)

        # calculate score for new schedule
        new_score = calc_score(courses, rooms, course_names, matrix)

        # keep scedule if score is higher
        if new_score > old_score:
            old_score = new_score
            i = 0

        # switch back if score is not higher
        else:
            switcher(room1, date1, room2, date2, courses, course_names)
            i += 1

    final_score = calc_score(courses, rooms, course_names, matrix)

    return final_score


def lineair(start_temp, end_temp, iteration, max_iterations):
    """
    Linear simulated annealing.
    """

    temperature = start_temp-iteration * (start_temp-end_temp) / max_iterations
    return temperature


def exponential(start_temp, end_temp, iteration, max_iterations):
    """
    Exponential simulated annealing.
    """

    temperature = start_temp * (end_temp/start_temp) ** (iteration/max_iterations)
    return temperature


def sigmoidal(start_temp, end_temp, iteration, max_iterations):
    """
    Sigmoidal simulated annealing.
    """

    temperature = end_temp + (start_temp - end_temp)/(1 + math.exp(0.3 * (iteration-max_iterations / 2)))
    return temperature


def geman(start_temp, iteration):
    """
    Geman simulated annealing.
    """

    temperature = start_temp/math.log(iteration + 2)
    return temperature


def sim_annealing(courses, rooms, course_names, max_iterations, old_score, matrix, start_temp, end_temp, SA_type):
    """
    Simulated annealing.
    """

    counter = 0

    for i in range(max_iterations):

        # choose two random rooms on a random date and switch them
        room1, date1 = random_hour_finder(rooms)
        room2, date2 = random_hour_finder(rooms)
        switcher(room1, date1, room2, date2, courses, course_names)

        # calculate score for new schedule
        new_score = calc_score(courses, rooms, course_names, matrix)

        # use specified type of simulated annealing
        if SA_type == "linear":
            temperature = lineair(start_temp, end_temp, counter, max_iterations)
        elif SA_type == "exponential":
            temperature = exponential(start_temp, end_temp, counter, max_iterations)
        elif SA_type == "sigmoidal":
            temperature = sigmoidal(start_temp, end_temp, counter, max_iterations)
        elif SA_type == "geman":
            temperature = geman(start_temp, counter)

        # make decision to keep new score based on acceptance factor
        decrease = new_score - old_score

        if new_score >= old_score:
            old_score = new_score

        elif rd.random() < math.exp(decrease/temperature):
            old_score = new_score

        else:
            switcher(room1, date1, room2, date2, courses, course_names)
        counter += 1

    final_score = old_score

    return final_score
