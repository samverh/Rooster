"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program searches for key weaknesses in the case.
"""

import days_scheduler as day_sch
import schedule_basics as bas_sch
from termcolor import cprint
import score as sc
import hillclimber as hill
import student_distribution as stu
import student_hillclimber as sthl


def search(rooms, courses, course_names, students, matrix):
    """
    Searches for painpoints in the case.
    """

    student_numbers = [student.student_number for student in students]
    student_weakness = [0 for number in student_numbers]
    course_weakness = [0 for coursename in course_names]

    for i in range(100):

        # schedule
        day_sch.total_schedule(rooms, courses, course_names, matrix)

        # calculate score and apply hillclimber
        score = sc.matrix_checker(courses, course_names, matrix) + sc.order_checker(courses)
        score += sc.student_checker(rooms, courses, course_names)
        bonus, malus = sc.distribution_checker(courses)
        score += bonus + malus
        score += sc.evening_checker(rooms, courses, course_names)
        score = hill.random_climber(courses, rooms, course_names, 1000, score, matrix)

        # schedule students
        stu.distribute_all_students(students, rooms, courses, course_names)

        # save score for hillclimber
        student_bonus, student_malus = sc.student_score(students)
        student_score = student_bonus + student_malus

        # pre filter the relevant courses
        student_courses = []
        for course in courses:
            poss_group_ids = []

            for activity in course.activities:
                if activity.group_id not in poss_group_ids and activity.group_id != "x":
                    poss_group_ids.append(activity.group_id)

            if len(poss_group_ids) > 1:
                student_courses.append([course, poss_group_ids])


        # student hillclimber
        student_climb_score = sthl.students_hillclimber(student_courses, students, student_score, 100)

        # update statistics
        for course in courses:
            if course.goodbad < 0:
                course_weakness[course_names.index(course.name)] += 1
        for student in students:
            if student.goodbad < - 12:
                student_weakness[student_numbers.index(student.student_number)] += 1

        bas_sch.print_schedule(rooms)
        bas_sch.clear_schedule(rooms, courses)
        bas_sch.clear_students(students)
        cprint(i, "blue")

    # print painpoints
    for f in range(len(student_numbers)):
        print(student_numbers[f] + ":", student_weakness[f])
    for j in range(len(course_names)):
        print(course_names[j] + ":", course_weakness[j])
