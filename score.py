"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program assigns a score to schedule.
"""

from scheduler2 import *
import csv

# keep track of stats
rooms = []
courses = []
matrix = []
score = 0

# schedule
read_info(rooms,courses, matrix)
course_names = [course.name for course in courses]
total_schedule(rooms, courses,course_names)


# adjusts score based on matrix
# def matrix_checker(course, hour, day):
#     # malus_points = 0
#     #
#     # reader = open("matrix.csv",'r')
#     # matrix = []
#     #
#     # for line in reader:
#     #     matrix.append(line.split(";"))
#     x = course_names.index(course)
#
#     # go through matrix
#     for i in range(1,len(matrix)):
#         if matrix[i][x] == 'x':
#             course2 = courses[course_names.index(matrix[i][0])]
#             for lok in range(7):
#                  if rooms[lok].days[day].hours[hour].courses[0] == course2:
#                      return True
#
#     for j in range(i, len(matrix[0])):
#
#             # if courses are connected
#             if matrix[x][j] == 'x':
#                 course2 = courses[course_names.index(matrix[0][j])]
#                 for lok in range(7):
#                     if rooms[lok].days[day].hours[hour].courses[0] == course2:
#                         return True
#     return False

    #             # check if they overlap
    #             overlapping = False
    #             course1 = courses[course_names.index(matrix[i][0])]
    #             course2 = courses[course_names.index(matrix[0][j])]
    #
    #             # iterate through course schedules
    #             for date1 in course1.dates:
    #                 for date2 in course2.dates:
    #                     if date1 == date2:
    #                         overlapping = True
    #                         malus_points  -= 1000000
    #
    # return malus_points

# check hoorcolleges are before practica/werkcolleges
def order_checker():
    order_points = 0

    for course in courses:
        first_hoorcollege = 0
        first_practicum = 6
        first_werkcollege = 6

        try:
            first_hoorcollege = course.dates[course.types.index("Hoorcollege")]
        except ValueError:
            continue
        try:
            first_practicum = course.dates[course.types.index("Practica")]
        except ValueError:
            continue
        try:
            first_werkcollege = course.dates[course.types.index("Werkcollege")]
        except ValueError:
            continue

        if (first_werkcollege < first_hoorcollege) or (first_practicum < first_hoorcollege):
            order_points -= 10000

    return order_points

# adjust score based on students

# calculate max amount of bonus points
def MAX_bonus_points():

    # keep track of max amount bonus points
    MAX_bonus = 0

    # Each course with 1+ activities gets 20 points if spreading is optimized
    spreading_bonus = 0
    for course in courses:
        if course.hoorcolleges + course.werkcolleges + course.practica > 1:
            spreading_bonus += 20
    MAX_bonus += spreading_bonus

    # Every student without overlap in courses gets 1 points
    student_bonus = 0

    # student_bonus += len(students)
    MAX_bonus += student_bonus

    # return max amount of bonus points (Upper Bound)
    print(MAX_bonus)
    return MAX_bonus


def MAX_malus_points():

    # keep track of max amount malus MAX_bonus_points
    MAX_malus = 0

    # Each time the biggest classroom uses the latest time frame gets 20 malus points
    room_malus = len(rooms[5].days) * 20 #IK WEET NIET HOE IK PRECIES C0.110 UIT DIE LIJST KAN HALEN
    MAX_malus += room_malus

    # Each time the amount of students exceeds the capacity of the classroom  gets 1 malus point
    capacity_malus = 0
    for course in courses:
        if course.e_students > 20:
            capacity_malus += course.hoorcolleges * (course.e_students - 20)
        if course.max_werkcolleges > 20:
            capacity_malus += course.werkcolleges * (course.max_werkcolleges - 20)
        if course.max_practica > 20:
            capacity_malus += course.practica * (course.max_practica - 20)
    MAX_malus += capacity_malus

    # Each course with x activities gives malus points if activities are scheduled on the same day
    # activities on x-1 days is 10 points, x-2 days is 20 points etcetera
    activity_malus = 0

    for course in courses:
        activities = course.hoorcolleges + course.werkcolleges + course.practica
        activity_malus += (activities-1) * 10

    MAX_malus += activity_malus

    # Every course conflict of a student gets 1 malus points
    student_malus = 0

    # TODO IF STUDENTS ARE UPLOADED
    MAX_malus += student_malus

    # return max amount of malus points (lower Bound)
    print(MAX_malus)
    return MAX_malus


# return total score
# score += matrix_checker()
score += order_checker()
print(score)
