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
sys.path.append(os.path.join(directory, "code", "score_and_other_calculations"))
sys.path.append(os.path.join(directory, "code", "visualizer"))


import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import colored, cprint
from colorama import init
import score as sc
# import visual as vis
import hillclimber as hill
import calculations as cal
import student_distribution as stu
import student_hillclimber as sthl
init()

# read information files into code
rooms = []
courses = []
matrix = []
students = []

coursefile = open("data/vakkendeel.txt", 'r')
roomfile = open("data/lokalen.txt", 'r')
matrixfile = open("data/matrix2.csv", 'r')

for line in coursefile:
    info = line.split(";")
    courses.append(inf.Course(info[0], int(info[1]), int(info[2]), int(info[3]),\
                   int(info[4]), int(info[5]), int(info[6])))

for line in roomfile:
    info = line.split(",")
    rooms.append(inf.Room_info(info[0], int(info[1])))

for line in matrixfile:
    matrix.append(line.split(";"))

# create evening timeslot in largest room
big_room_cap = 0

for room in rooms:
    if room.cap > big_room_cap:
        big_room_cap = room.cap
        big_room = room

for day in big_room.days:
    day.hours.append(inf.Hour())

course_names = [course.name for course in courses]


# return total score
day_sch.total_schedule(rooms, courses, course_names, matrix)
score = sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
score += sc.student_checker(rooms, courses, course_names)
bonus, malus = sc.distribution_checker(courses)
score += bonus + malus
score += sc.evening_checker(rooms, courses, course_names)


# print stuff
print("Score before hillclimber:", score)
while score < 160:
    score = hill.sim_annealing(courses, rooms, course_names, 20000, score, matrix, 20, 0.001)
    print(score)
print("Score after hillclimber: ", score)

# highest SCORE
max_bonus = 0
for course in courses:
    if course.hoorcolleges + course.werkcolleges + course.practica > 1:
        m, n = 0, 0
        for j in range(course.werkcolleges):
            r = course.e_students

            while r > 0:
                m += 1
                r -= course.max_werkcolleges


        for k in range(course.practica):
            r = course.e_students

            while r > 0:
                n += 1
                r -= course.max_practica

        maxi = max(m,n)
        max_bonus += maxi * 20

cprint("MAX BONUS:{}".format(max_bonus), 'blue')

# check parts
goodbad = 0
for course in courses:
    goodbad += course.goodbad
    if course.goodbad >= 0:
        print(colored(course.name + ":",'green'), colored(course.goodbad, 'green'))
    else:
        print(colored(course.name + ":", 'red'), colored(course.goodbad, 'red'))
        print(student.student_number + ":", student.goodbad)

bas_sch.print_schedule(rooms)
bas_sch.clear_schedule(rooms, courses)
