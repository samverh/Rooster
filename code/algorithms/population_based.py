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
#import visual as vis
import hillclimber as hill
import calculations as cal
import student_distribution as stu
import student_hillclimber as sthl
import random as rd

def initial_population():
    """
    Initial population.
    """

    # store different schedules
    scheduled_rooms = [[] for i in range(5)]
    scheduled_courses = [[] for i in range(5)]
    scheduled_students = [[] for i in range(5)]
    scores = [0 for i in range(5)]
    matrix = []
    course_names = []
    matrixfile = open("matrix.csv", 'r')
    coursenamefile = open("vakken.txt", 'r')

    # read matrix
    for line in matrixfile:
        matrix.append(line.split(";"))

    for line in coursenamefile:
        course_names.append(line.split(";")[0])

    # schedule 50 times
    for i in range(5):

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

        # create evening timeslot in largest room
        big_room_cap = 0

        for room in scheduled_rooms[i]:
            if room.cap > big_room_cap:
                big_room_cap = room.cap
                big_room = room

        for day in big_room.days:
            day.hours.append(inf.Hour())

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
                if activity.group_id not in poss_group_ids and activity.group_id != "x":
                    poss_group_ids.append(activity.group_id)

            if len(poss_group_ids) > 1:
                student_courses.append([course, poss_group_ids])


        # student hillclimber
        scores[i] += sthl.students_hillclimber(student_courses, scheduled_students[i], student_score, 100)

    return scheduled_rooms, scheduled_courses, scheduled_students, scores, course_names, matrix


def survival_of_the_fittest(scheduled_rooms, scheduled_courses, scheduled_students, scores):
    """
    Survival of the fittest.
    """

    # store fittest
    fittest_rooms = []
    fittest_courses = []
    fittest_students = []
    fittest_scores = []

    # select best score, add schedule to fittest and remove from old list
    for test in range(5):
        index = scores.index(max(scores))

        fittest_rooms.append(scheduled_rooms[index])
        scheduled_rooms.remove(scheduled_rooms[index])

        fittest_courses.append(scheduled_courses[index])
        scheduled_courses.remove(scheduled_courses[index])

        fittest_students.append(scheduled_students[index])
        scheduled_students.remove(scheduled_students[index])

        fittest_scores.append(scores[index])
        scores.remove(scores[index])

    return fittest_rooms, fittest_courses, fittest_students, fittest_scores


def clear_schedule_of_course(rooms, course, students):
    """
    Clear schedule.
    """

    # erase activities and score
    course.activities = []
    course.goodbad = 0

    # clear course out of rooms
    for room in rooms:
        for day in room.days:
            for hour in day.hours:
                if course.name == hour.course.split(" | ")[0]:
                    hour.course = ""
                    hour.scheduled = False

    # clear course out of students
    for student in students:
        if course.name in student.courses:
            student.dates[student.courses.index(course.name)] = []
            student.group_id[student.courses.index(course.name)] = ""


def copy_schedule(rooms, courses, students, rooms_2, courses_2, students_2):
    """
    Cope schedule.
    """

    for i in range(len(rooms_2)):
        for j in range(len(rooms_2[i].days)):
            for k in range(len(rooms_2[i].days[j].hours)):
                rooms_2[i].days[j].hours[k].scheduled = rooms[i].days[j].hours[k].scheduled
                rooms_2[i].days[j].hours[k].course = rooms[i].days[j].hours[k].course

    for i in range(len(courses)):
        for activity in courses[j].activities:
            courses_2[i].activities.append(inf.Activity(activity.id, \
                activity.date, activity.students, activity.group_id, \
                    activity.room, activity.capacity))

    for i in range(len(students)):
        students_2[i].dates = students[i].dates
        students_2[i].group_id = students[i].group_id


    return rooms_2, courses_2, students_2

def mutate_schedule(rooms, courses, students, score, matrix, course_names):
    """
    Mutate schedule.
    """

    # store mutated schedules
    new_rooms = [[inf.Room_info(room.name, room.cap) for room in rooms] \
        for j in range(10)]

    new_courses = [[inf.Course(course.name, course.hoorcolleges, \
        course.werkcolleges, course.max_werkcolleges, course.practica, \
            course.max_practica, course.e_students) for course in courses] \
                for j in range(10)]

    new_students = [[inf.Student(student.surname, student.name, \
        student.student_number, student.courses) for student in students] \
            for j in range(10)]

    new_scores = [0 for j in range(10)]

    for n_rooms in new_rooms:

        # create evening timeslot in largest room
        big_room_cap = 0

        for room in n_rooms:
            if room.cap > big_room_cap:
                big_room_cap = room.cap
                big_room = room

        for day in big_room.days:
            day.hours.append(inf.Hour())

    for k in range(10):
        new_rooms[k], new_courses[k], new_students[k] = copy_schedule(rooms, \
            courses, students, new_rooms[k], new_courses[k], new_students[k])

    # keep original schedule
    new_scores[0] = score

    # mutate 9 times
    for i in range(1, 10):

        # select random subset of scheduled courses
        indices = rd.sample(range(len(new_courses[i])), rd.randint(0, \
            len(new_courses[i]) - 2))

        # store names
        unsched_names = []

        # unschedule subset
        for j in indices:
            unsched_names.append(new_courses[i][j].name)
            clear_schedule_of_course(new_rooms[i], new_courses[i][j], \
                new_students[i])

        # schedule all required classes
        schedulings = 0
        for j in indices:
            # schedule all hoorcolleges
            # zeg = new_courses[i][j]
            # print(zeg.hoorcolleges, zeg.werkcolleges, zeg.practica)
            # print(zeg.max_practica, zeg.max_werkcolleges)
            # print(zeg.e_students)
            schedulings += day_sch.course_scheduler(new_courses[i][j], new_rooms[i],\
                new_courses[i], course_names, matrix)
        print("Schedulings:", schedulings)

        # schedule students' unscheduled groups
        for student in new_students[i]:
            for coursename in student.courses:
                if coursename in unsched_names:
                    course = new_courses[i][course_names.index(coursename)]
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

        # calculate score
        new_scores[i] = sc.matrix_checker(new_courses[i], course_names, \
            matrix) + sc.order_checker(new_courses[i])
        new_scores[i] += sc.student_checker(new_rooms[i], new_courses[i], course_names)
        bonus, malus = sc.distribution_checker(new_courses[i])
        new_scores[i] += bonus + malus + sc.evening_checker(new_rooms[i], \
            new_courses[i], course_names)
        student_bonus, student_malus = sc.student_score(new_students[i])
        new_scores[i] += student_bonus + student_malus

    return new_rooms, new_courses, new_students, new_scores


def pop_based_algo():
    """
    Population based algorithm.
    """

    scheduled_rooms, scheduled_courses, scheduled_students, scores, \
    course_names, matrix = initial_population()

    for propagation in range(5):
        fittest_rooms, fittest_courses, fittest_students, fittest_scores = \
            survival_of_the_fittest(scheduled_rooms, scheduled_courses, \
                scheduled_students, scores)

        scheduled_rooms, scheduled_courses, scheduled_students, scores = \
            [], [], [], []

        for fit in range(len(fittest_students)):
            new_rooms, new_courses, new_students, new_scores = mutate_schedule(\
                fittest_rooms[fit], fittest_courses[fit], fittest_students[fit],\
                    fittest_scores[fit], matrix, course_names)

            for m in range(len(new_rooms)):
                scheduled_rooms.append(new_rooms[m])
                scheduled_courses.append(new_courses[m])
                scheduled_students.append(new_students[m])
                scores.append(new_scores[m])

    fittest_rooms, fittest_courses, fittest_students, fittest_scores = \
        survival_of_the_fittest(scheduled_rooms, scheduled_courses, \
            scheduled_students, scores)

    print(fittest_scores)

pop_based_algo()
