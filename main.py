"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Main function of scheduling.
"""

import information as inf
import random_scheduler as random_sch
import days_scheduler as day_sch
import score as sc

# function thats read info files into code
rooms = []
courses = []
matrix = []

coursefile = open("vakken.txt",'r')
roomfile = open("lokalen.txt",'r')
matrixfile = open("matrix.csv",'r')

for line in coursefile:
    info = line.split(";")
    courses.append(inf.Course(info[0],int(info[1]),int(info[2]),int(info[3]),int(info[4]),int(info[5]),int(info[6])))
for line in roomfile:
    info = line.split(",")
    rooms.append(inf.Room_info(info[0],int(info[1])))
for line in matrixfile:
    matrix.append(line.split(";"))

course_names = [course.name for course in courses]

# return total score
day_sch.total_schedule()
score = sc.matrix_checker() +  sc.order_checker()
print("Score:", score)
day_sch.print_schedule()
day_sch.clear_schedule()
