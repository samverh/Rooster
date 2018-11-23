"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program loads in the data for the schedule.
"""

import os
import string

# class for info of a course
class Activity:
    def __init__(self,id,date,students,group_id):
        self.id = id
        self.date = date
        self.students = students
        self.group_id = group_id

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
        self.activities = []
        self.goodbad = 0

# nested class to store info of schedule of a room
class Hour:
    def __init__(self):
        self.scheduled = False
        self.course = ""
class Day:
    def __init__(self):
        self.hours = [Hour(),Hour(),Hour(), Hour()]
class Room_info:
    def __init__(self,name,capaciteit):
        self.name = name
        self.cap = capaciteit
        self.days = [Day(),Day(),Day(),Day(),Day()]
