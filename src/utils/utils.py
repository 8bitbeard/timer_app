"""
This file implements all the auxiliar functions, used to manipulate the time data,
such as converting time from "HH:MM" to minutes format and vice versa, and doing
basic operations to them
"""

import os
import sys
import datetime
import time
import calendar
import operator
import json
from functools import reduce
import yaml

import dill as pickle


LOG_DATA_PATH = "./src/resources/data/"


def convert_to_int(input_time):
    """
    This function gets the time string and return the hrs and minutes as integers
    """
    hrs = abs(int(input_time[0:input_time.index(':')]))
    mins = abs(int(input_time[input_time.index(':') + 1 :]))
    negative = bool('-' in input_time)
    return(hrs, mins, negative)

def change_to_minutes(input_time):
    """
    This function converts the time from hrs:mins to minutes
    """
    hrs, mins, negative = convert_to_int(input_time)
    result = 60 * hrs + mins
    return -result if (negative) else result

def change_to_hours(input_minutes):
    """
    This function converts the time from minutes to hrs:mins format
    """
    minutes = abs(input_minutes)
    mins = minutes % 60
    hrs = (minutes - mins) // 60
    return "-{:02d}:{:02d}".format(hrs, mins) if input_minutes < 0 else "{:02d}:{:02d}".format(hrs, mins)

def time_is_greater(time_one, time_two):
    """
    This function checks if the time_one is greater than the time_two
    """
    return change_to_minutes(time_one) > change_to_minutes(time_two)

def mult_time(input_time, factor):
    """
    This function is responsible to multiply the hour value
    """
    minutes = change_to_minutes(input_time)
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
    for input_time in input_list:
        total_sum = sum_times(total_sum, input_time)
    return total_sum

def sub_times(time_one, time_two):
    """
    This function is responsible to subtract two times
    """
    time_minutes_one = change_to_minutes(time_one)
    time_minutes_two = change_to_minutes(time_two)
    return change_to_hours(time_minutes_two - time_minutes_one)

def total_worked_time(*args):
    """
    This function is responsible for calculating the total time worked on a day
    """
    if isinstance(args[0], list):
        return sum_times(sub_times(args[0][0], args[0][1]), sub_times(args[0][2], args[0][3]))
    if len(args) == 4:
        return sum_times(sub_times(args[0], args[1]), sub_times(args[2], args[3]))
    return '00:00'

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

def  get_total_time_from(my_dict, year, month=None):
    """
    Method to return the total time by month or week
    """
    total_days = []
    if month:
        for day in my_dict[year][month]:
            try:
                total_days.append(my_dict[year][month][day]['total_time'])
            except TypeError:
                pass
    total_worked_days = [value for value in total_days if value != '00:00']
    total_worked = sum_times_list(total_worked_days)
    should_work = mult_time('08:00', len(total_worked_days))
    balance = sub_times(should_work, total_worked)
    my_dict[year][month]['month_balance'] = balance

def get_start_end_dates(year_input, week_input):
    """
    Method to return the fist and last date from a given week from a given year
    """
    date_input = datetime.date(year_input, 1, 1)
    if date_input.weekday() <= 3:
        date_input = date_input - datetime.timedelta(date_input.weekday())
    else:
        date_input = date_input + datetime.timedelta(7-date_input.weekday())
    delta = datetime.timedelta(days=(week_input-1)*7)
    return date_input + delta, date_input + delta + datetime.timedelta(days=6)

def sort_dates_list(input_list):
    """
    Method to sort a list of dates with the "yyyy-xx-xx" format
    """
    splitup = input_list.split('-')
    return splitup[0], splitup[1], splitup[2]

def get_month_from_week(year, week):
    """
    Method to get the month from a passed week number
    The returned month number will be the one most present on the week range
    """
    temp_date = datetime.date(year, 1, 1)
    delta = datetime.timedelta(days=(week-1)*7)
    first = temp_date + delta
    last = temp_date + delta + datetime.timedelta(days=6)
    if 4 < last.day < 7:
        return last.month
    return first.month

def get_ij_status(list_of_times):
    """
    Method to return all status from one day
    """
    work_one_ij = change_to_minutes(sub_times(list_of_times[0], list_of_times[1]))
    lunch_ij = change_to_minutes(sub_times(list_of_times[1], list_of_times[2]))
    work_two_ij = change_to_minutes(sub_times(list_of_times[2], list_of_times[3]))

    work_one_ij_status = "background-color : green" if 0 < work_one_ij <= 360 else "background-color : red"
    lunch_ij_status = "background-color : green" if 60 <= lunch_ij <= 120 else "background-color : red"
    work_two_ij_status = "background-color : green" if 0 < work_two_ij <= 360 else "background-color : red"

    return work_one_ij_status, lunch_ij_status, work_two_ij_status

def get_work_time_status(times_list):
    """
    Method to check the total work time status from all week days
    """
    if '00:00' in times_list:
        return "color : gray"
    total_time = change_to_minutes(total_worked_time(times_list))
    if 300 < total_time < 480:
        return "color : orange"
    if total_time == 480:
        return "color : green"
    if 600 > total_time > 480:
        return "color : blue"
    return "color : red"

def get_week_days_list(year, week):
    """
    Method to return a list of lists containing the days af a given week
    """
    startdate = time.asctime(time.strptime('{} {} 1'.format(year, week-1), '%Y %W %w'))
    startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    days = [[(startdate + datetime.timedelta(days=i)).year, (startdate + datetime.timedelta(days=i)).month,
             (startdate + datetime.timedelta(days=i)).day] for i in range(0, 7)]
    return days

def get_month_days_list(year, month):
    """
    Method to return a list of lists containg the days of a given month
    """
    num_days = calendar.monthrange(year, month)[1]
    days = [[year, month, day] for day in range(1, num_days+1)]
    # days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    return days

def get_from_dict(data_dict, map_list, extra_key=None):
    """
    Method to return the values from a dict path specified on a list
    """
    input_list = map_list.copy()
    if extra_key:
        input_list.append(extra_key)
    return reduce(operator.getitem, input_list, data_dict)

def set_in_dict(data_dict, map_list, extra_key, value):
    """
    Method to set the values from a dict path specified on a list
    """
    # get_from_dict(data_dict, map_list[:-1])[map_list[-1]] = value
    get_from_dict(data_dict, map_list)[extra_key] = value

def get_month_worked_days(my_dict, month_list):
    """
    Temp
    """
    counter = 0
    for year, month, day in month_list:
        if my_dict[year][month][day]['day_type']:
            counter += 1
    return counter

def get_week_balance(my_dict, year, week):
    """
    T
    """
    total_time_list = []
    for month in my_dict[year]:
        for day in my_dict[year][month]:
            try:
                if my_dict[year][month][day]['week'] == week:
                    if my_dict[year][month][day]['day_type']:
                        total_time_list.append(my_dict[year][month][day]['total_time'])
            except TypeError:
                pass
    return sum_times_list(total_time_list)


def get_month_balance(my_dict, year, month):
    """
    T
    """
    total_time_list = []
    total_extra_list = []
    total_extra = '00:00'
    counter_normal = 0
    counter_extra = 0
    for day in my_dict[year][month].keys():
        try:
            if my_dict[year][month][day]['day_type'] == 1:
                counter_normal += 1
                total_time_list.append(my_dict[year][month][day]['total_time'])
            elif my_dict[year][month][day]['day_type'] == 2:
                counter_extra += 1
                total_extra_list.append(my_dict[year][month][day]['total_time'])
        except TypeError:
            pass
    total_time = sum_times_list(total_time_list)
    total_extra = sum_times_list(total_extra_list)
    total_should = mult_time('08:00', counter_normal)
    balance_normal = sub_times(total_should, total_time)
    balance = sum_times(balance_normal, total_extra)
    my_dict[year][month]['month_work_days'] = counter_normal
    my_dict[year][month]['month_extra_days'] = counter_extra
    my_dict[year][month]['month_balance'] = balance
    return balance

def get_week_total_time(my_dict, week_days_list):
    """
    Method to calculate and return the total worked time from a given week
    """
    total_time_list = []
    for year, month, day in week_days_list:
        total_time_list.append(my_dict[year][month][day]['total_time'])
    return sum_times_list(total_time_list)

def increment_time_by_second(input_time):
    """
    Method to increment a time string
    """
    hours, minutes, seconds = [int(x) for x in input_time.split(":")]
    seconds += 1
    if seconds > 59:
        seconds = 0
        minutes += 1
        if minutes > 59:
            minutes = 0
            hours += 1
            if hours > 23:
                hours = 0
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def read_file():
    """
    Method to open the pickle file
    """
    with open(LOG_DATA_PATH + 'log_data.pkl', 'rb') as pickle_file:
        data_dict = pickle.load(pickle_file)
    pickle_file.close()
    return data_dict

def dump_files(input_value):
    """
    Method to dump the dictionary to pickle and json files
    """
    if not os.path.exists(LOG_DATA_PATH):
        os.makedirs(LOG_DATA_PATH)
    with open(LOG_DATA_PATH + 'log_data.pkl', 'wb') as pickle_file:
        pickle.dump(input_value, pickle_file, pickle.HIGHEST_PROTOCOL)
    pickle_file.close()
    with open(LOG_DATA_PATH + 'log_data.json', 'w') as json_file:
        json.dump(input_value, json_file, indent=4)
    json_file.close()
    with open(LOG_DATA_PATH + 'log_data.yaml', 'w') as yaml_file:
        yaml.dump(input_value, yaml_file, indent=4)
    yaml_file.close()
