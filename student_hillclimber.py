"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program tries to locally improve the solution for students.
"""

import random as rd
import information as inf
import schedule_basics as bas
import score as sc
import schedule_basics as bas_sch
from termcolor import colored, cprint

def students_group_switcher(course, student1, group_id1, student2, group_id2):
    index1 = student1.courses.index(course.name)
    index2 = student2.courses.index(course.name)

    for activity in course.activities:
        if activity.group_id == group_id1:
            student1.dates[index1].remove(activity.date)
            student2.dates[index2].append(activity.date)
        if activity.group_id == group_id2:
            student1.dates[index1].append(activity.date)
            student2.dates[index2].remove(activity.date)


def course_students_picker(course, students, old_score):
    poss_group_ids = []

    for activity in course.activities:
        if activity.group_id not in poss_group_ids and activity.group_id != 'x':
            poss_group_ids.append(activity.group_id)

    if len(poss_group_ids) < 2:
        return False

     group_id1 = rd.choice(poss_group_ids)
     poss_group_ids.remove(group_id1)
     group_id2 = rd.choice(poss_group_ids)
     studentnumber1, studentnumber2 = "", ""

     for activity in course.activities:
        if activity.group_id == group_id1 and len(studentnumber1) < 1:
            studentnumber1 = rd.choice(activity.students)
        elif activity.group_id == group_id2 and len(studentnumber2) < 1:
            studentnumber2 = rd.choice(activity.students)

    for student in students:
        if student.studentnumber == studentnumber1:
            student1 = student
        elif student.studentnumber == studentnumber2:
            student2 = student

    students_group_switcher(course, student1, group_id1, student2, group_id2)

    new_bonus, new_malus = sc.student_score(students)
    if new_bonus + new_malus <= old_score:
        students_group_switcher(course, student1, group_id1, student2, group_id2)
        return False

    return True
