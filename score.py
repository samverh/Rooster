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

    return malus

# adjust score based on use evening timeslot
def evening_checker(rooms):
    malus = 0
    room = rooms[5]

    for day in room.days:
        hour = day.hours[4]
        if hour.scheduled:
            malus -= 20

    return malus


# TODO: checkt voor elke group_id dat er maximale spreiding is
def distribution_checker(courses):
    malus = 0
    id_dates = []

    for course in courses:
        total = course.hoorcolleges + course.werkcolleges + course.practica
        id_s = 1

        for activity in course.activities:
            if group_id != 'x':
                if int(group_id) - 96 > id_s:
                    id_s += 1

        id_dates = [[] for i in range(id_s)]

        for activity in course.activities:
            if activity.group_id == 'x':
                for dates in id_dates:
                    dates.append(activity.date)
            else:
                id = int(activity.group_id) - 97
                id_dates[id].append(activity.date)

    for dates in id_dates:
        if len(dates) == 2:
            continue

    return malus


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
