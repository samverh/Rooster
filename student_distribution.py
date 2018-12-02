"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program takes an existing schedule and distributes students over the
scheduled lectures they commited to.
"""

import information as inf
import random as rd
from termcolor import colored, cprint


def student_distribute(student, rooms, courses, course_names):
    for coursename in student.courses:
        student.dates.append([])
        course = courses[course_names.index(coursename)]
        poss_group_ids = []

        # get possible groups of course for student and choose one randomly
        for activity in course.activities:
            if activity.group_id != "x" and len(activity.students) < activity.capacity:
                poss_group_ids.append(activity.group_id)
        if len(poss_group_ids) > 0:
            student.group_id = rd.choice(poss_group_ids)

        # schedule students
        for activity in course.activities:
            if activity.id == "Hoorcollege" or activity.group_id == student.group_id:
                activity.students.append(student.student_number)
                student.dates[student.courses.index(coursename)].append(activity.date)


def distribute_all_students(students, rooms, courses, course_names):
    for student in students:
        student_distribute(student, rooms, courses, course_names)


def student_in_courses_checker(courses, students, course_names):
    for course in courses:
        total = course.e_students
        for activity in course.activities:
            if activity.capacity < len(activity.students):
                print(course.name)
                print("expected vs actually enrolled:")
                print(colored(total,'red'), colored(len(activity.students),'red'))

def stats_about_students(courses, students, course_names):
    check_students = [0 for x in range(len(courses))]
    real_values = [course.e_students for course in courses]

    for student in students:
        for coursename in student.courses:
            if len(coursename) > 2:
                check_students[course_names.index(coursename)] += 1
    for i in range(len(courses)):
        if real_values[i] == check_students[i]:
            cprint("ENROLLED EQUALS EXPECTED", 'green')
        else:
            cprint("ENROLLED DIFFERS FROM EXPECTED", 'red')
