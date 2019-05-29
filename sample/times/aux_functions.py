"""
This file implements all the auxiliar functions, used to manipulate the time data,
such as converting time from "HH:MM" to minutes format and vice versa, and doing
basic operations to them
"""

def convert_to_int(time):
    """
    This function gets the time string and return the hrs and minutes as integers
    """
    hrs = int(time[0:time.index(':')])
    mins = int(time[time.index(':') + 1 :])
    return(hrs, mins)

def change_to_minutes(time):
    """
    This function converts the time from hrs:mins to minutes
    """
    hrs, mins = convert_to_int(time)
    return 60 * hrs + mins

def change_to_hours(minutes):
    """
    This function converts the time from minutes to hrs:mins format
    """
    mins = minutes % 60
    hrs = (minutes - mins) // 60
    return "{:02d}:{:02d}".format(hrs, mins)

def time_is_greater(time_one, time_two):
    """
    This function checks if the time_one is greater than the time_two
    """
    return change_to_minutes(time_one) > change_to_minutes(time_two)

def sum_times(time_one, time_two):
    """
    This function is responsible to add two times
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    return change_to_hours(time_minutes_two + time_minutes_one)

def sub_times(time_one, time_two):
    """
    This function is responsible to subtract two times
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    return change_to_hours(time_minutes_two - time_minutes_one)
