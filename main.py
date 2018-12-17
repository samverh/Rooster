"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program is the main function for scheduling classes.
"""

# add code directories to path
import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "schedulers"))
sys.path.append(os.path.join(directory, "code", "classes"))
sys.path.append(os.path.join(directory, "code", "algorithms"))
sys.path.append(os.path.join(directory, "code", "score and other calculations"))
sys.path.append(os.path.join(directory, "code", "visualizer"))


import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import colored, cprint
from colorama import init
import score as sc
import hillclimber as hill
import calculations as cal
import student_distribution as stu
import student_hillclimber as sthl
import input_prompt as inp
init()

# get user input on how to run scheduler using the input Functions
course_optim, course_optim_type, course_SA_type, c_max_iterations = inp.course_input()
students_inc, stud_optim, stud_optim_type, stud_SA_type, s_max_iterations = inp.students_input()

# prompt user to specify amount of runs
runs = input("Please enter amount of runs (integer): ")
while not type(runs) == int:
    try:
        runs = int(runs)
    except:
        runs = input("Incorrect input. Try again (integer): ")
print("\nStart scheduling\n")

# run as many runs as specified and save scores in list
score_list = []
score_list_students = []
for l in range(runs):

    # read information files into code
    rooms = []
    courses = []
    matrix = []
    students = []

    coursefile = open("data/vakken.txt", 'r')
    roomfile = open("data/lokalen.txt", 'r')
    matrixfile = open("data/matrix.csv", 'r')
    studentfile = open("data/studentenenvakken.csv", 'r', errors="ignore")

    # parse csv files and append content to lists
    for line in coursefile:
        info = line.split(";")
        courses.append(inf.Course(info[0], int(info[1]), int(info[2]), int(info[3]),\
                       int(info[4]), int(info[5]), int(info[6])))

    for line in roomfile:
        info = line.split(",")
        rooms.append(inf.Room_info(info[0], int(info[1])))

    for line in matrixfile:
        matrix.append(line.split(";"))

    for line in studentfile:
        student_info = line.strip("\n").split(";")
        student_courses = []
        for coursename in student_info[3:]:
            if len(coursename) > 2:
                student_courses.append(coursename)

        students.append(inf.Student(student_info[0], student_info[1], student_info[2], student_courses))

    students = students[1:]

    # create eveniqng timeslot in largest room
    big_room_cap = 0

    for room in rooms:
        if room.cap > big_room_cap:
            big_room_cap = room.cap
            big_room = room

    for day in big_room.days:
        day.hours.append(inf.Hour())

    course_names = [course.name for course in courses]

    # return total score of schedule using the score calculator
    day_sch.total_schedule(rooms, courses, course_names, matrix)
    score = sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
    score += sc.student_checker(rooms, courses, course_names)
    bonus, malus = sc.distribution_checker(courses)
    score += bonus + malus
    score += sc.evening_checker(rooms, courses, course_names)

    # print scores before hillclimber
    if not course_optim_type == "none":
        print("Courses score before optimization:", score)

        # for course in courses:
        #     if course.goodbad < - 1000:
        #         score = hill.course_climber(courses[0], courses, rooms, course_names, 1000, score, matrix)
        #         print("Score after 1 course_climb: ", score)

        # run hillclimber if specified by user
        if course_optim_type == "hillclimber":
            score = hill.random_climber(courses, rooms, course_names, c_max_iterations, score, matrix)

        # run simulated annealing if specified by user, with specified type
        elif course_optim_type == "sim annealing":
            score = hill.sim_annealing(courses, rooms, course_names, c_max_iterations, score, matrix, 20, 0.001, course_SA_type)

        # print score after optimization and save obtained score in list
        print("Courses score after optimization: ", score)
    score_list.append(score)

    # check parts
    latest_score = hill.calc_score(courses, rooms, course_names, matrix)

    for course in courses:
        if course.goodbad >= 0:
            print(colored(course.name + ":", 'green'), colored(course.goodbad, 'green'))

            # append score to course for coloring course in schedule visualization
            for activity in course.activities:
                room = [room for room in rooms if room.name == activity.room][0]
                hour = room.days[activity.date // 10].hours[activity.date % 10]
                hour.course = hour.course + " - " + str(course.goodbad)

        else:
            print(colored(course.name + ":", 'red'), colored(course.goodbad, 'red'))

    # user specified to include students in scheduling
    if students_inc == "yes":

        # distribute all students over the courses
        stu.distribute_all_students(students, rooms, courses, course_names)

        # stu.student_in_courses_checker(courses, students, course_names)
        # stu.stats_about_students(courses, students, course_names)

        # calculate and print student score
        student_bonus, student_malus = sc.student_score(students)
        print("OLD STUDENTBONUS", student_bonus)
        print("OLD STUDENTMALUS", student_malus)
        student_score = student_bonus + student_malus

        # append score to list if no optimization is specified
        if stud_optim_type == "none":
            score_list_students.append(student_score + score)

        # pre-filter the relevant courses
        student_courses = []
        for course in courses:
            poss_group_ids = []

            for activity in course.activities:
                if activity.group_id not in poss_group_ids and activity.group_id != "x":
                    poss_group_ids.append(activity.group_id)

            if len(poss_group_ids) > 1:
                student_courses.append([course, poss_group_ids])

        # follow student score improvement when using optimization
        if stud_optim == "yes":
            print("STUDENT SCORE BEFORE OPTIMIZING:", student_score)

            # run hillclimber if specified
            if stud_optim_type == "hillclimber":
                student_climb_score = sthl.students_hillclimber(student_courses, students, student_score, s_max_iterations)

            # run sim annealing if specified
            elif stud_optim_type == "sim annealing":
                student_climb_score = sthl.students_sim_annealing(student_courses, students, student_score, s_max_iterations, 10, 0.001, stud_SA_type)

            # print student score improvement and save final score of the schedule
            print("STUDENT SCORE AFTER OPTIMIZING:", student_climb_score)
            print(colored("FINAL SCORE: {}".format(student_climb_score + score), 'green'))
            score_list_students.append(student_climb_score + score)

    # print the schedule and clear for next scheduling run
    bas_sch.print_schedule(rooms)
    bas_sch.clear_schedule(rooms, courses)

# print scores in list
print("\nFinished scheduling")
print("\nScores after scheduling courses: ", score_list)
if students_inc == "yes":
    print("Scores after including students in schedule: ", score_list_students)
