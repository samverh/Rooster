"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program searches for key weaknesses in the case.
"""

# add code directories to path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "schedulers"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "code", "score_and_other_calculations"))
sys.path.append(os.path.join(directory, "code", "visualizer"))

import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import colored, cprint
import score as sc
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
    matrixfile = open("data/matrix.csv", 'r')
    coursenamefile = open("data/vakken.txt", 'r')

    # read matrix
    for line in matrixfile:
        matrix.append(line.split(";"))

    for line in coursenamefile:
        course_names.append(line.split(";")[0])

    # schedule 5 times
    for i in range(5):

        #read files
        coursefile = open("data/vakken.txt", 'r')
        roomfile = open("data/lokalen.txt", 'r')
        studentfile = open("data/studentenenvakken.csv", 'r', errors='ignore')

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

        # remove headers in students
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
    Takes an population of schedules and returns the schedules in the top 5 of
    scores.
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
    Unschedule a specific course in the whole schedule.
    """

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


def mutate_schedule(rooms, courses, students, score, matrix, course_names):
    """
    Mutate a fit schedule to 10 different schedules. Keep the orignal schedule.
    Furthermore, for 9 times: unschedule a random subset of the courses and
    reschedule this subset.
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

    # create evening timeslot in largest room
    for n_rooms in new_rooms:


        big_room_cap = 0

        for room in n_rooms:
            if room.cap > big_room_cap:
                big_room_cap = room.cap
                big_room = room

        for day in big_room.days:
            day.hours.append(inf.Hour())

    # copy orignal schedule onto mutations
    for k in range(10):
        new_rooms[k], new_courses[k], new_students[k] = bas_sch.copy_schedule(rooms, \
            courses, students, new_rooms[k], new_courses[k], new_students[k])

    # keep original schedule
    new_scores[0] = score

    # mutate 9 times
    for i in range(1, 10):

        # select random subset of scheduled courses
        indices = rd.sample(range(len(new_courses[i])), rd.randint(0, \
            len(new_courses[i]) - 7))

        # store names of subset
        unsched_names = []

        # unschedule subset
        for j in indices:
            unsched_names.append(new_courses[i][j].name)
            clear_schedule_of_course(new_rooms[i], new_courses[i][j], \
                new_students[i])

        # schedule all required classes
        schedulings = 0
        for j in indices:
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
    Simulate a lifetime of a population of schedules. Each propagation only
    the fittest survive and are mutated into a new population.
    """

    # initialise population
    scheduled_rooms, scheduled_courses, scheduled_students, scores, \
    course_names, matrix = initial_population()

    # 5 cycles of propagation
    for propagation in range(5):
        # select fittest group
        fittest_rooms, fittest_courses, fittest_students, fittest_scores = \
            survival_of_the_fittest(scheduled_rooms, scheduled_courses, \
                scheduled_students, scores)

        # store new population
        scheduled_rooms, scheduled_courses, scheduled_students, scores = \
            [], [], [], []

        # mutate fittest schedules and add to population
        for fit in range(len(fittest_students)):
            new_rooms, new_courses, new_students, new_scores = mutate_schedule(\
                fittest_rooms[fit], fittest_courses[fit], fittest_students[fit],\
                    fittest_scores[fit], matrix, course_names)

            for m in range(len(new_rooms)):
                scheduled_rooms.append(new_rooms[m])
                scheduled_courses.append(new_courses[m])
                scheduled_students.append(new_students[m])
                scores.append(new_scores[m])

    # select fittest schedules of end population
    fittest_rooms, fittest_courses, fittest_students, fittest_scores = \
        survival_of_the_fittest(scheduled_rooms, scheduled_courses, \
            scheduled_students, scores)

    # show best scores
    print(fittest_scores)

pop_based_algo()
