"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program assigns a score to the schedule.
"""


def student_score(students):
    """
    Determines the score per student.
    """

    malus = 0
    bonus = 0

    # Iterate through all students and calculate confilcts
    for student in students:
        noconflicts = True

        for i in range(len(student.dates)):
            for j in range(i + 1, len(student.dates)):
                for date in student.dates[i]:
                    if date in student.dates[j]:
                        noconflicts = False
                        malus -= 1
                        student.goodbad -= 1

        if noconflicts:
            bonus += 1
            student.goodbad += 1

    return bonus, malus


def matrix_checker(courses, course_names, matrix):
    """
    Adjusts score based on matrix.
    """

    malus_points = 0

    # iterate through positions of every course in matrix
    for course in courses:
        x = course_names.index(course.name) + 1

        # determine courses with which no overlap may occur
        for i in range(1, len(matrix[0])):
            if matrix[i][x] == "x":
                course2 = courses[course_names.index(matrix[i][0])]

                # assign penalty points if overlap does occur
                for activity in course.activities:
                    for activity2 in course2.activities:
                        if activity2.date == activity.date:
                            malus_points -= 1000000
                            course.goodbad -= 1000000

    return malus_points


def order_checker(courses):
    """
    Checks if preferred sequence of course activities is respected.
    """

    order_points = 0

    # Iterate through courses and check for each course if order is correct
    for course in courses:
        first_hoorcollege = -1
        first_practicum = 44
        first_werkcollege = 44

        for activity in course.activities:

            if activity.id == "Werkcollege":
                first_werkcollege = min(activity.date, first_werkcollege)

            elif activity.id == "Practica":
                first_practicum = min(activity.date, first_practicum)

            elif activity.id == "Hoorcollege":

                if first_hoorcollege < 0:
                    first_hoorcollege = activity.date

                else:
                    first_hoorcollege = min(activity.date, first_hoorcollege)

        # assign penalty points for wrong order
        if (first_werkcollege < first_hoorcollege) or (first_practicum < first_hoorcollege):
            order_points -= 10000
            course.goodbad -= 10000

    return order_points


def student_checker(rooms, courses, course_names):
    """
    Adjusts score based on students.
    """

    malus = 0

    # iterate through all rooms on all possible times
    for room in rooms:
        max = room.cap
        for day in room.days:
            for hour in day.hours:

                #  compare amount of expected students in room with room capacity
                #  assign malus points for each student that exceeds the capacity
                if hour.scheduled:
                    course_name, type = hour.course.split(" | ")[:2]
                    course = courses[course_names.index(course_name)]
                    expected = course.e_students

                    if type == "Werkcollege":
                        expected = course.max_werkcolleges

                    elif type == "Practica":
                        expected = course.max_practica

                    if max < expected:
                        malus += max - expected
                        course.goodbad += max - expected

    return malus


def evening_checker(rooms, courses, course_names):
    """
    Adjusts score based on usage of evening timeslot.
    """

    malus = 0
    room = rooms[5]

    # iterate through evening timeslot, give penalty for each time it is scheduled
    for day in room.days:
        hour = day.hours[4]

        if hour.scheduled:
            course_name = hour.course.split(" | ")[0]
            course = courses[course_names.index(course_name)]
            malus -= 20
            course.goodbad -= 20

    return malus


def distribution_checker(courses):
    """
    Assigns bonus points for maximum distribution of course activities across
    the weekdays.
    Assigns penalty points for course activities on the same day.
    """

    # start off with zero points and create list for all date id's
    bonus = 0
    malus = 0
    id_dates = []

    # iterate through all activities of each course and check distribution
    for course in courses:
        course_total = 0

        id_s = 1

        for activity in course.activities:
            if activity.group_id != "x" and activity.group_id != "a":
                if ord(activity.group_id) - 96 > id_s:
                    id_s += 1

        id_dates = [[] for i in range(id_s)]

        for activity in course.activities:
            if activity.group_id == "x":
                for dates in id_dates:
                    dates.append(activity.date)
            else:
                id = ord(activity.group_id) - 97
                id_dates[id].append(activity.date)

        for dates in id_dates:
            sorted = [int(date/10) for date in dates]
            sorted.sort()

            # assign bonus or malus points based on the amount of activities
            if len(dates) == 2:
                day1, day2 = sorted
                if day2 - day1 == 3:
                    bonus += 20
                    course_total += 20
                if day1 == day2:
                    malus -= 10
                    course_total -= 10

            elif len(dates) == 3:
                day1, day2, day3 = sorted
                if day1 == 0 and day2 == 2 and day3 == 4:
                    bonus += 20
                    course_total += 20

                difference = 3 - len(set(sorted))
                malus -= difference * 10
                course.goodbad -= difference * 10

            elif len(dates) == 4:
                if sorted == [0, 1, 3, 4]:
                    bonus += 20
                    course_total += 20

                difference = 4 - len(set(sorted))
                malus -= difference * 10
                course_total -= difference * 10

            elif len(dates) > 4:
                if sorted == [0, 1, 2, 3, 4]:
                    bonus += 20
                    course_total += 20
                difference = len(sorted) - len(set(sorted))
                malus -= difference * 10
                course_total -= difference * 10

        course.goodbad += course_total

    return bonus, malus
