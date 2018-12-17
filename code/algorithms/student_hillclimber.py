"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program tries to locally improve the solution for students.
"""

import random as rd
#import information as inf
#import schedule_basics as bas
import score as sc
#import schedule_basics as bas_sch
from termcolor import colored, cprint
import math


def students_group_switcher(course, student1, group_id1, student2, group_id2):
    """
    Function switches 2 students from groups within a course.
    """

    # index for the course in students' personal lists
    index1 = student1.courses.index(course.name)
    index2 = student2.courses.index(course.name)

    # store the switch in the student and course infomation
    for activity in course.activities:
        if activity.group_id == group_id1:
            student1.dates[index1].remove(activity.date)
            student2.dates[index2].append(activity.date)
            activity.students.remove(student1.student_number)
            activity.students.append(student2.student_number)
        if activity.group_id == group_id2:
            student1.dates[index1].append(activity.date)
            student2.dates[index2].remove(activity.date)
            activity.students.append(student1.student_number)
            activity.students.remove(student2.student_number)

    # switch students from group
    student1.group_id[index1] = group_id2
    student2.group_id[index2] = group_id1


def course_students_picker(course, poss_group_ids, students, old_student_score):
    """
    Function takes a course, picks 2 students from 2 different groups within
    the course. Then it calculates and returns a new score.
    """

    # choose two different groups
    group_id1 = rd.choice(poss_group_ids)
    group_id2 = rd.choice(poss_group_ids)
    while group_id2 == group_id1:
        group_id2 = rd.choice(poss_group_ids)

    # choose two studentnumbers from the two groups
    studentnumber1, studentnumber2 = "", ""
    while len(studentnumber1) < 2:
        activity = rd.choice(course.activities)
        if activity.group_id == group_id1:
            studentnumber1 = rd.choice(activity.students)
    while len(studentnumber2) < 2:
        activity = rd.choice(course.activities)
        if activity.group_id == group_id2:
            studentnumber2 = rd.choice(activity.students)

    # track the two students with the student numbers
    student1 = [student for student in students if student.student_number == studentnumber1][0]
    student2 = [student for student in students if student.student_number == studentnumber2][0]

    # switch the students in the groups
    students_group_switcher(course, student1, group_id1, student2, group_id2)

    # if the switch improves the score, keep it
    for student in students:
        student.goodbad = 0
    new_bonus, new_malus = sc.student_score(students)
    new_student_score = new_bonus + new_malus
    return new_student_score, student1, group_id2, student2, group_id1


def students_hillclimber(courses_special, students, old_student_score, max_iters):
    """
    Function keeps making switches until the max of unuseful switches is met.
    If a switch did not increase the score, the switch is reversed.
    """

    # store switches
    iters = 0

    # keep switching, until a max of unuseful switches in a row is made
    while iters < max_iters:
        course, poss_group_ids = rd.choice(courses_special)
        new_student_score, student1, group_id2, student2, group_id1 = course_students_picker(course, poss_group_ids, students, old_student_score)
        if new_student_score > old_student_score:
            old_student_score = new_student_score
            iters = 0
        else:
            students_group_switcher(course, student1, group_id2, student2, group_id1)
            iters += 1

    # return the improved score
    return old_student_score


def lineair(start_temp, end_temp, iteration, max_iters):
    """
    Linear simulated annealing.
    """

    temperature = start_temp-iteration * (start_temp-end_temp) / max_iters
    return temperature


def exponential(start_temp, end_temp, iteration, max_iters):
    """
    Exponential simulated annealing.
    """

    temperature = start_temp * (end_temp/start_temp) ** (iteration/max_iters)
    return temperature


def sigmoidal(start_temp, end_temp, iteration, max_iters):
    """
    Sigmoidal simulated annealing.
    """

    temperature = end_temp + (start_temp - end_temp)/(1 + math.exp(0.3 * (iteration - max_iters / 2)))
    return temperature


def geman(start_temp, iteration):
    """
    Geman simulated annealing.
    """

    temperature = start_temp/math.log(iteration + 2)
    return temperature


def students_sim_annealing(courses_special, students, old_student_score, max_iters, start_temp, end_temp, SA_type):
    """
    Function keeps making switches and determines wheter the switch is accepted
    with a hillclimber combined with a simulated annealing algorithm.
    """

    counter = 0

    for i in range(max_iters):
        course, poss_group_ids = rd.choice(courses_special)
        new_student_score, student1, group_id2, student2, group_id1 = course_students_picker(course, poss_group_ids, students, old_student_score)

        # use specified type of simulated annealing
        if SA_type == "linear":
            temperature = lineair(start_temp, end_temp, counter, max_iters)
        elif SA_type == "exponential":
            temperature = exponential(start_temp, end_temp, counter, max_iters)
        elif SA_type == "sigmoidal":
            temperature = sigmoidal(start_temp, end_temp, counter, max_iters)
        elif SA_type == "geman":
            temperature = geman(start_temp, counter)

        # make decision to keep new score based on acceptance factor
        decrease = new_student_score - old_student_score

        if new_student_score >= old_student_score:
            old_student_score = new_student_score
        elif rd.random() < math.exp(decrease/temperature):
            old_student_score = new_student_score
        else:
            students_group_switcher(course, student1, group_id2, student2, group_id1)
        counter += 1

    # return the improved score
    return old_student_score
