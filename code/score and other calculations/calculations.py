"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program calculates specific bounds.
"""

from termcolor import colored, cprint

def product(above, under):
    if not above > under:
        return 1

    x = 1

    for i in range(under):
        x = x * (above - i)

    return x

def calcs(courses):
    max_bonus, state_space = 0, 1
    for course in courses:
        if course.hoorcolleges + course.werkcolleges + course.practica > 1:
            m, n = 0, 0
            for j in range(course.werkcolleges):
                r = course.e_students

                while r > 0:
                    m += 1
                    r -= course.max_werkcolleges


            for k in range(course.practica):
                r = course.e_students

                while r > 0:
                    n += 1
                    r -= course.max_practica

            maxi = max(m,n)
            max_bonus += maxi * 20

            if maxi > 0:
                d = course.e_students // maxi
                l = course.e_students
                state = 1
                for f in range(maxi):
                    state = state * product(l, d)
                    l -= d

                state_space = state_space * state

    power = 0
    while state_space > 10:
        state_space = state_space // 10
        power += 1

    cprint("MAX BONUS:{}".format(max_bonus), 'blue')
    cprint("STUDENT STATESPACE:{}x10^{}".format(state_space, power+238), 'magenta')
