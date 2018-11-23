"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

Program assigns a score to schedule.
"""


# adjusts score based on matrix
def matrix_checker(courses, course_names, matrix):
    malus_points = 0

    for course in courses:
        x = course_names.index(course.name) + 1

        # go through matrix
        for i in range(1, len(matrix[0])):
            if matrix[i][x] == 'x':
                course2 = courses[course_names.index(matrix[i][0])]
                for activity in course.activities:
                    for activity2 in course2.activities:
                        if activity2.date == activity.date:
                            malus_points -= 1000000

    return malus_points


# check hoorcolleges are before practica/werkcolleges
def order_checker(courses):
    order_points = 0

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

        if (first_werkcollege < first_hoorcollege) or (first_practicum < first_hoorcollege):
            order_points -= 10000

    return order_points


# adjust score based on students
def student_checker(rooms, courses, course_names):
    malus = 0

    for room in rooms:
        max = room.cap
        for day in room.days:
            for hour in day.hours:
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

    print("Student points:", malus)
    return malus

# adjust score based on use evening timeslot
def evening_checker(rooms):
    malus = 0
    room = rooms[5]

    for day in room.days:
        hour = day.hours[4]
        if hour.scheduled:
            malus -= 20

    print("Evening points:", malus)
    return malus

# bonus points for maximum distribution
# malus points for activities on same day
def distribution_checker(courses):
    bonus = 0
    malus = 0
    id_dates = []

    for course in courses:
        course_total = 0

        total = course.hoorcolleges + course.werkcolleges + course.practica
        id_s = 1

        for activity in course.activities:
            if activity.group_id != 'x':
                if ord(activity.group_id) - 96 > id_s:
                    id_s += 1

        id_dates = [[] for i in range(id_s)]

        for activity in course.activities:
            if activity.group_id == 'x':
                for dates in id_dates:
                    dates.append(activity.date)
            else:
                id = ord(activity.group_id) - 97
                id_dates[id].append(activity.date)

        for dates in id_dates:
            sorted = [int(date/10) for date in dates]
            sorted.sort()

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

            elif len(dates) == 4:
                day1, day2, day3, day4 = sorted
                if day1 == 0 and day2 == 1 and day3 == 3 and day4 == 4:
                    bonus += 20
                    course_total += 20

                difference = 4 - len(set(sorted))
                malus -= difference * 10
                course_total -= difference * 10

            elif len(dates) > 4:
                sorted = [int(date/10) for date in dates]
                difference = len(sorted) - len(set(sorted))
                malus -= difference * 10
                course_total -= difference * 10

        course.goodbad += course_total

    print("Distribution points:", bonus)
    print("Activities on one day:", malus)
    return bonus + malus
