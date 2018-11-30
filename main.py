"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program is the main function for scheduling classes.
"""

import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import colored, cprint
import score as sc
import visual as vis
import hillclimber as hill

# read information files into code
rooms = []
courses = []
matrix = []

coursefile = open("vakken.txt", 'r')
roomfile = open("lokalen.txt", 'r')
matrixfile = open("matrix.csv", 'r')

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
random_sch.total_schedule(rooms, courses, course_names, matrix)
score = sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
score += sc.student_checker(rooms, courses, course_names)
bonus, malus = sc.distribution_checker(courses)
score += bonus + malus
score += sc.evening_checker(rooms, courses, course_names)
print("Score before hillclimber:", score)
print("\n")
hill_score, iterations = hill.climber(courses, rooms, course_names, 100, score, matrix)
print("iterations: ", iterations)
print("Score after hillclimber: ", hill_score)
print("\n")
goodbad = 0
for course in courses:
    if course.goodbad > 0:
        print(colored(course.name + ":",'green'), colored(course.goodbad, 'green'))
    elif course.goodbad < -50:
        print(colored(course.name + ":", 'red'), colored(course.goodbad, 'red'))
    else:
        print(course.name + ":", course.goodbad)
    goodbad += course.goodbad
print("sum course.goodbad: ", goodbad)


bas_sch.print_schedule(rooms)
bas_sch.clear_schedule(rooms, courses)
