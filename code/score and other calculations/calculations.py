"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program calculates specific bounds.
"""

from termcolor import colored, cprint


def product(above, under):
    """
    Determine the product.
    """

    if not above > under:
        return 1

    x = 1

    for i in range(under):
        x = x * (above - i)

    return x


def calcs(courses):
    """
    Function calculates the bounds.
    """

    max_bonus, state_space = 0, 1
    for course in courses:
        if course.hoorcolleges + course.werkcolleges + course.practica > 1:
            diff_ids = []

            for activity in course.activities:
                if not activity.group_id in diff_ids:
                    diff_ids.append(activity.group_id)

            diff_ids = set(diff_ids)

            if 'x' in diff_ids and len(diff_ids) > 1:
                diff_ids.remove('x')

            maxi = len(diff_ids)
            max_bonus += maxi * 20

            if maxi > 0:
                d = course.e_students // maxi
                l = course.e_students
                state = 1
                for f in range(maxi):
                    state = state * product(l, d)
                    l -= d

                state_space = state_space * state

    # determine the power factor
    power = 0
    while state_space > 10:
        state_space = state_space // 10
        power += 1

    cprint("MAX BONUS:{}".format(max_bonus), 'blue')
    cprint("STUDENT STATESPACE:{}x10^{}".format(state_space, power+232), 'magenta')
