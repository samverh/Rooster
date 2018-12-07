"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program loads in the data for the schedule.
"""

import os
import string


class Activity:
    """
    Class defining all information of a course activity.
    """
    def __init__(self, id, date, students, group_id, room, capacity):
        self.id = id
        self.date = date
        self.room = room
        self.students = students
        self.group_id = group_id
        self.capacity = capacity


class Course:
    """
    Class defining the course itself.
    """
    def __init__(self, name, hoorcolleges, werkcolleges, max_werkcolleges,\
                 practica, max_practica, e_students):
        self.name = name
        self.hoorcolleges = hoorcolleges
        self.werkcolleges = werkcolleges
        self.practica = practica
        self.max_werkcolleges = max_werkcolleges
        self.max_practica = max_practica
        self.e_students = e_students
        self.activities = []
        self.goodbad = 0


class Hour:
    """
    Nested class to store information of schedule of a room.
    Hour stores the course given at this timeslot.
    """
    def __init__(self):
        self.scheduled = False
        self.course = ""


class Day:
    """
    Class defining the teaching days of a roomself.
    Days contain four timeslots for lecturing by default.
    """
    def __init__(self):
        self.hours = [Hour(), Hour(), Hour(), Hour()]


class Room_info:
    """
    Class defining information of a lecture roomself.
    Rooms contain five days on which lectures can take place.
    """
    def __init__(self, name, capaciteit):
        self.name = name
        self.cap = capaciteit
        self.days = [Day(), Day(), Day(), Day(), Day()]

class Student:
    """"
    Class defining information of a student, i.e. the name, studentnumber,
    courses and the dates of courses.

    """
    def __init__(self, surname, name, student_number, courses):
        self.surname = surname
        self.name = name
        self.student_number = student_number
        self.courses = courses
        self.dates = []
        self.group_id = []
        self.goodbad = 0
