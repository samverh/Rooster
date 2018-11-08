"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program loads in the data for the schedule.
"""

import os
import string

# class for info of a course
class Course:
    def __init__(self,name,hoorcolleges,werkcolleges,max_werkcolleges,practica,\
    max_practica,e_students):
        self.name = name
        self.hoorcolleges = hoorcolleges
        self.werkcolleges = werkcolleges
        self.practica = practica
        self.max_werkcolleges = max_werkcolleges
        self.max_practica = max_practica
        self.e_students = e_students

# nested class to store info of schedule of a room
class Hour:
    def __init__(self):
        self.scheduled = False
        self.courses = []
class Day:
    def __init__(self):
        self.hours = [Hour(),Hour(),Hour(), Hour()]
class Room_info:
    def __init__(self,name,capaciteit):
        self.room = name
        self.cap = capaciteit
        self.days = [Day(),Day(),Day(),Day(),Day()]

# function thats read info files into code
def read_info(courses,rooms):
    coursefile = open("vakken.txt",'r')
    roomfile = open("lokalen.txt",'r')
    for line in coursefile:
        info = line.split(";")
        courses.append(Course(info[0],int(info[1]),int(info[2]),int(info[3]),int(info[4]),int(info[5]),int(info[6])))
    for line in roomfile:
        info = line.split(",")
        rooms.append(Room_info(info[0],int(info[1])))
