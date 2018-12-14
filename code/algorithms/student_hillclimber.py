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
    '''
    Function switches 2 students from groups within a course.
    '''
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

    student1.group_id[index1] = group_id2
    student2.group_id[index2] = group_id1

def course_students_picker(course, poss_group_ids, students, old_student_score):
    '''
    Function takes a course, picks 2 students from 2 different groups within
    the course. Then it requests a switch, which is kept only if the student
    score is improved.
    '''

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
    if new_bonus + new_malus <= old_student_score:
        students_group_switcher(course, student1, group_id2, student2, group_id1)
        return False, old_student_score

    return True, new_bonus + new_malus


def students_hillclimber(courses_special, students, old_student_score, max_iters):
    '''
    Function keeps making switches until the max of unuseful switches is met.
    '''
    # store switches
    iters = 0

    # keep switching, until a max of unuseful switches in a row is made
    while iters < max_iters:
        course, poss_group_ids = rd.choice(courses_special)
        switched, score = course_students_picker(course, poss_group_ids, students, old_student_score)

        if switched:
            iters = 0
            old_student_score = score
        else:
            iters += 1

    # return the improved score
    return old_student_score
