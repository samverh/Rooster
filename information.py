"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program loads in the data for the schedule.
"""

import os
import string
import csv


# Class for info of a course
class Course:
    def __init__(self, name, hoorcolleges, werkcolleges, max_werkcolleges, practica, max_practica, e_students):
        self.name = name
        self.hoorcolleges = hoorcolleges
        self.werkcolleges = werkcolleges
        self.practica = practica
        self.max_werkcolleges = max_werkcolleges
        self.max_practica = max_practica
        self.e_students = e_students


# Nested class to store info of schedule of a room
class Hour:
    def __init__(self):
        self.scheduled = False
        self.courses = []


class Day:
    def __init__(self):
        self.hours = [Hour(), Hour(), Hour(), Hour()]


class Room_info:
    def __init__(self, name, capaciteit):
        self.room = name
        self.cap = capaciteit
        self.days = [Day(), Day(), Day(), Day(), Day()]


# Function that reads info files into code
def read_info(courses, rooms):
    coursefile = open("vakken.txt", 'r')
    roomfile = open("lokalen.txt", 'r')

    for line in coursefile:
        info = line.split(";")
        courses.append(Course(info[0], int(info[1]), int(info[2]), int(info[3]), int(info[4]), int(info[5]), int(info[6])))

    for line in roomfile:
        info = line.split(",")
        rooms.append(Room_info(info[0], int(info[1])))


# Function that checks if courses in matrix can overlap
# (Header course is course1 and left course is (course2))
def matrix(course1, course2):

    # Open csv matrix file
    with open("matrix.csv", 'r') as mat:
        matrix = csv.reader(mat)
        matrix_dict = {}

        # Get each matrix cell as a list item
        for row in matrix:
            row = row[0].split(";")

            # Save first row as headers and get list length
            if row[0] == "":
                headers = row
                length = len(row)

            # Save other rows in matrix dictionary
            else:
                matrix_dict.setdefault(row[0], []).append(row[1:length])

        # Get place in matrix of header course and determine cell in matrix dictionary at this position
        for i in range(len(headers)):
            if headers[i] == course1:
                cell = matrix_dict[course2][0][i-1]

        # If cell in matrix is x, the courses cannot overlap
        if cell == "x":
            print("mag niet!!!")
