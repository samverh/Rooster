"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program searches for key weaknesses in the case.
"""

import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import colored, cprint
import score as sc
import visual as vis
import hillclimber as hill
import calculations as cal
import student_distribution as stu
import student_hillclimber as sthl

def initial_population(course_names):
    # store different schedules
    scheduled_rooms = [[] for i in range(50)]
    scheduled_courses = [[] for i in range(50)]
    scheduled_students = [[] for i in range(50)]
    scores = [0 for i in range(50)]
    matrixfile = open("matrix.csv", 'r')

    # read matrix
    for line in matrixfile:
        matrix.append(line.split(";"))

    # schedule 50 times
    for i in range(50):
        #read files
        coursefile = open("vakken.txt", 'r')
        roomfile = open("lokalen.txt", 'r')
        studentfile = open("studentenenvakken.csv", 'r', errors='ignore')

        for line in coursefile:
            info = line.split(";")
            scheduled_courses[i].append(inf.Course(info[0], int(info[1]), int(info[2]), int(info[3]),\
                           int(info[4]), int(info[5]), int(info[7])))

        for line in roomfile:
            info = line.split(",")
            scheduled_rooms[i].append(inf.Room_info(info[0], int(info[1])))

        for line in studentfile:
            student_info = line.strip("\n").split(";")
            student_courses = []
            for coursename in student_info[3:]:
                if len(coursename) > 2:
                    student_courses.append(coursename)

            scheduled_students[i].append(inf.Student(student_info[0], student_info[1], student_info[2], student_courses))

        scheduled_students[i] = scheduled_students[i][1:]

        # schedule
        day_sch.total_schedule(scheduled_rooms[i], scheduled_courses[i], course_names, matrix)

        # calculate score and apply hillclimber
        scores[i] = sc.matrix_checker(scheduled_courses[i], course_names, matrix) + sc.order_checker(scheduled_courses[i])
        scores[i] += sc.student_checker(scheduled_rooms[i], scheduled_courses[i], course_names)
        bonus, malus = sc.distribution_checker(scheduled_courses[i])
        scores[i] += bonus + malus
        scores[i] += sc.evening_checker(scheduled_rooms[i], scheduled_courses[i], course_names)
        scores[i] = hill.random_climber(scheduled_courses[i], scheduled_rooms[i], course_names, 1000, scores[i], matrix)

        # schedule students
        stu.distribute_all_students(scheduled_students[i], scheduled_rooms[i], scheduled_courses[i], course_names)

        # Save score for hillclimber
        student_bonus, student_malus = sc.student_score(scheduled_students[i])
        student_score = student_bonus + student_malus

        # pre filter the relevant courses
        student_courses = []
        for course in scheduled_courses[i]:
            poss_group_ids = []

            for activity in course.activities:
                if activity.group_id not in poss_group_ids and activity.group_id != 'x':
                    poss_group_ids.append(activity.group_id)

            if len(poss_group_ids) > 1:
                student_courses.append([course, poss_group_ids])


        # student hillclimber
        scores[i] += sthl.students_hillclimber(student_courses, scheduled_students[i], student_score, 100)

    return scheduled_rooms, scheduled_courses, scheduled_students, scores


def survival_of_the_fittest(scheduled_rooms, scheduled_courses, scheduled_students, scores):
    # store fittest
    fittest_rooms = []
    fittest_courses = []
    fittest_students = []
    fittest_scores = []

    # select best score, add schedule to fittest and remove from old list
    while len(fittest_rooms < 5):
        index = fittest_scores.index(max(fittest_scores))

        fittest_rooms.append(scheduled_rooms[index])
        scheduled_rooms.remove(scheduled_rooms[index])

        fittest_courses.append(scheduled_courses[index])
        scheduled_courses.remove(scheduled_courses[index])

        fittest_students.append(scheduled_students[index])
        scheduled_students.remove(scheduled_students[index])

        fittest_scores.append(scores[index])
        scores.remove(scores[index])

    return fittest_rooms, fittest_courses, fittest_students, fittest_scores


def clear_schedule_of_course(rooms,course,students):
    # erase activities and score
    course.activities = []
    course.goodbad = 0

    # clear course out of rooms
    for room in rooms:
        for day in room.days:
            for hour in day.hours:
                if course.name in hour.course.split(" | "):
                    hour.course = ""
                    hour.scheduled = False

    # clear course out of students
    for student in students:
        if course.name in student.courses:
            student.dates[student.courses.index(course.name)] = []
            student.group_id[student.courses.index(course.name)] = ""


def mutate_schedule(rooms, courses, students, score):
    # store mutated schedules
    new_rooms = [[] for j in range(10)]
    new_courses = [[] for j in range(10)]
    new_students = [[] for j in range(10)]
    new_scores = [0 for j in range(10)]

    # first schedule is original one
    new_rooms[0] = rooms
    new_courses[0] = courses
    new_students[0] = students
    new_scores[0] = score

    # mutate 9 times
    for i in range(1,10):
        # select random subset
        indices = rd.sample(range(len(courses)), rd.randint(0,len(courses)-1))
        sched_courses = []
        unsched_courses = []

        for j in range(len(courses)):
            if j in indices:
                sched_courses.append(courses[i])
            else:
                unsched_courses.append(courses[i])
                clear_schedule_of_course(rooms,course,students)

        # store names
        unsched_names = [course.name for course in unsched_courses]

        # schedule unscheduled courses
        for course in unsched_courses:
            day_sch.total_schedule(rooms, courses, course_names, matrix)

        # schedule students' unscheduled groups
        for student in students:
            for coursename in student.courses:
                if coursename in unsched_names:
                    course = courses[course_names.index(coursename)]
                    poss_group_ids = []
                    student_id = ""

                    # get possible groups of course for student and choose one randomly
                    for activity in course.activities:
                        if activity.group_id != "x" and len(activity.students) < activity.capacity:
                            poss_group_ids.append(activity.group_id)
                    if len(poss_group_ids) > 0:
                        student_id = rd.choice(poss_group_ids)

                    student.group_id[student.courses.index(course.name)] = student_id

                    # schedule student
                    for activity in course.activities:
                        if activity.id == "Hoorcollege" or activity.group_id == student_id:
                            activity.students.append(student.student_number)
                            student.dates[student.courses.index(coursename)].append(activity.date)


    return new_rooms, new_courses, new_students, new_scores
