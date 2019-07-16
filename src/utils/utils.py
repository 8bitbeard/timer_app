"""
This file implements all the auxiliar functions, used to manipulate the time data,
such as converting time from "HH:MM" to minutes format and vice versa, and doing
basic operations to them
"""

import os
import sys


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

def mult_time(time, factor):
    """
    This function is responsible to multiply the hour value
    """
    minutes = change_to_minutes(time)
    return change_to_hours(factor * minutes)

def sum_times(time_one, time_two, *args):
    """
    This function is responsible to add as many times as the user passes
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    total_sum = time_minutes_one + time_minutes_two
    for arg in args:
        total_sum += change_to_minutes(arg)
    return change_to_hours(total_sum)

def sum_times_list(input_list):
    """
    This function sums all the times inside a given list
    """
    total_sum = '00:00'
    for time in input_list:
        total_sum = sum_times(total_sum, time)
    return total_sum

def sub_times(time_one, time_two):
    """
    This function is responsible to subtract two times
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    return change_to_hours(time_minutes_two - time_minutes_one)

def total_worked_time(time_one, time_two, time_three, time_four):
    """
    This function is responsible for calculating the total time worked on a day
    """
    return sum_times(sub_times(time_one, time_two), sub_times(time_three, time_four))

# pylint: disable=no-member
# pylint: disable=protected-access
# pylint: disable=broad-except
def get_absolute_resource_path(relative_path):
    """
    Function to handle the pyinstaller added data relative path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        try:
            base_path = os.path.dirname(sys.modules['src'].__file__)
        except Exception:
            base_path = ''

        if not os.path.exists(os.path.join(base_path, relative_path)):
            base_path = 'src'

    path = os.path.join(base_path, relative_path)

    if not os.path.exists(path):
        return None

    return path

def get_dict_values_list(input_dict, key):
    """
    Method get a list of values from all occurences of a key on a dictionary
    """
    values_list = []
    for i, j in input_dict.items():
        for k in j.keys():
            values_list.append(input_dict[i][k][key])
    return values_list

def count_dict_value(input_dict, key, value):
    """
    Method to count the occurence of a value in the input dict
    """
    values_list = get_dict_values_list(input_dict, key)
    return int(values_list.count(value))

def csv_to_dict(csv_file):
    """
    Method to convert the csv file to a dict
    """
    dict_from_csv = {}
    with open(get_absolute_resource_path("resources/dictionaries/{}".format(csv_file))) as data_file:
        for row in data_file:
            row = row.strip().split(',')
            dict_from_csv.setdefault(int(row[0]), {})[int(row[1])] = {row[2] : row[3], row[4] : row[5],
                                                                      row[6] : row[7], row[8] : row[9],
                                                                      row[10] : row[11], row[12] : row[13],
                                                                      row[14] : row[15]}
    return dict_from_csv

def dict_to_csv(dict):
    """
    Method to convert the dict to csv file
    """
