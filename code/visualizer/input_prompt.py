"""
Heuristieken UvA 2018-2019
Lesroosters
Johan Diepstraten, Ya'gel Schoonderbeek, Sam Verhezen

This program is used by the main function to get user input on how to run the scheduler.
"""

from termcolor import colored
from colorama import init
init()


def course_input():
    """
    Gets input from user on how to run course scheduler.
    """

    # prompt user to specify how to run the course scheduler
    print(colored("\nWelcome to Team Tortuga's course scheduler!\n", 'green'))
    course_optim = input("Would you like to use an optimization technique to schedule the courses? (yes/no): ")
    while not (course_optim in ["yes", "no"]):
        course_optim = input("Incorrect input. Try again (yes/no): ")

    # prompt user to specify the optimization type
    if course_optim == "yes":
        course_optim_type = input("Please specify the optimization type (hillclimber/sim annealing): ")
        while not (course_optim_type in ["hillclimber", "sim annealing"]):
            course_optim_type = input("Incorrect input. Try again (hillclimber/sim annealing): ")
    else:
        course_optim_type = "none"

    # if optimization type is simulated annealing, prompt user for type
    if course_optim == "yes" and course_optim_type == "sim annealing":
        course_SA_type = input("Please enter type of simulated annealing (linear/exponential/sigmoidal/geman): ")
        while not course_SA_type in ["linear", "exponential", "sigmoidal", "geman"]:
            course_SA_type = input("Incorrect input. Try again (linear/exponential/sigmoidal/geman): ")
    else:
        course_SA_type = "none"

    # prompt user for amount of iterations for simulated annealing and hillclimber
    if course_optim == "yes":
        c_max_iterations = input("Please enter amount of iterations (integer): ")
        valid = False
        while not valid:
            c_max_iterations = input("Incorrect input. Try again (integer): ")
            try:
                c_max_iterations = int(c_max_iterations)
            except:
                c_max_iterations = input("Incorrect input. Try again (integer): ")
            else:
                valid = c_max_iterations > 0
                if not valid:
                    c_max_iterations = input("Incorrect input. Try again (integer): ")

    # return the obtained variables
    return course_optim, course_optim_type, course_SA_type, c_max_iterations


def students_input():
    """
    Gets input from user on how to include students in the schedule.
    """

    # propt user to specify whether or not to run student scheduler
    students_inc = input("Would you like to include the students in the schedule? (yes/no): ")
    while not (students_inc in ["yes", "no"]):
        students_inc = input("Incorrect input. Try again (yes/no): ")

    # propt user to specify how to run student scheduler
    if students_inc == "yes":
        stud_optim = input("Would you like to use an optimization technique to schedule the students? (yes/no): ")
        while not (stud_optim in ["yes", "no"]):
            stud_optim = input("Incorrect input. Try again (yes/no): ")

        # prompt user to specify the optimization type
        if stud_optim == "yes":
            stud_optim_type = input("Please specify the optimization type (hillclimber/sim annealing): ")
            while not (stud_optim_type in ["hillclimber", "sim annealing"]):
                stud_optim_type = input("Incorrect input. Try again (hillclimber/sim annealing): ")
        else:
            stud_optim_type = "none"

        # if optimization type is simulated annealing, prompt user for type
        if stud_optim_type == "sim annealing":
            stud_SA_type = input("Please enter type of simulated annealing (linear/exponential/sigmoidal/geman): ")
            while not stud_SA_type in ["linear", "exponential", "sigmoidal", "geman"]:
                stud_SA_type = input("Incorrect input. Try again (linear/exponential/sigmoidal/geman): ")
        else:
            stud_SA_type = "none"

        # prompt user for amount of iterations for simulated annealing and hillclimber
        if stud_optim == "yes":
            s_max_iterations = input("Please enter amount of iterations (integer): ")
            valid = False
            while not valid:
                s_max_iterations = input("Incorrect input. Try again (integer): ")
                try:
                    s_max_iterations = int(s_max_iterations)
                except:
                    s_max_iterations = input("Incorrect input. Try again (integer): ")
                else:
                    valid = s_max_iterations > 0
                    if not valid:
                        s_max_iterations = input("Incorrect input. Try again (integer): ")


        # return obtained variables
        return students_inc, stud_optim, stud_optim_type, stud_SA_type, s_max_iterations

    elif students_inc == "no":
        return students_inc, "", "", "", ""
