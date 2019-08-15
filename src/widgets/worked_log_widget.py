"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import re
import datetime

from collections import defaultdict

import json
import dill as pickle

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QCheckBox, QFrame
from PyQt5.QtCore import QRegExp, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator

from src.utils import utils

# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class WorkedLogWidget(QWidget):
    """
    Class to implement the Work log Widget
    """

    TIME_BOX_SIZE = QSize(57, 20)
    COLOR_FRAME_SIZE = QSize(57, 5)

    close_worked_log_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(WorkedLogWidget, self).__init__(parent)

        actual_day = datetime.date.today()
        self.month = actual_day.month
        self.day = actual_day.day
        self.year, self.week, self.day_of_week = actual_day.isocalendar()

        self.data_dict = None
        self.week_total = []

        self.get_log_data()

        first_log_year = min([val for val in list(self.data_dict.keys()) if isinstance(val, int)])
        first_log_month = min([val for val in list(self.data_dict[first_log_year].keys()) if isinstance(val, int)])
        first_log_day = min([val for val in list(self.data_dict[first_log_year][first_log_month].keys())
                             if isinstance(val, int)])
        self.first_log_week = datetime.date(first_log_year, first_log_month, first_log_day).isocalendar()[1]
        self.last_log_week = self.week


        self.curr_week = utils.get_week_days_list(self.year, self.week)
        self.current_month_days = utils.get_month_days_list(self.year, self.month)

        self.init_user_interface()
        self.update_log_data()

    def get_log_data(self):
        """
        Method to get the log data
        """
        try:
            with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.pkl', 'rb') as pickle_file:
                self.data_dict = pickle.load(pickle_file)
            pickle_file.close()
        except (TypeError, FileNotFoundError):
            data_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(dict))))
            for year, month, day in utils.get_week_days_list(self.year, self.week):
                __, week, day_of_week = datetime.date(year, month, day).isocalendar()
                data_dict[year][month]['total_time'] = "00:00"
                data_dict[year][month]['month_work_days'] = 0
                data_dict[year][month]['hours_bank'] = '00:00'
                data_dict[year][month][day]['date'] = str(day).zfill(2) + '/' + str(month).zfill(2)
                data_dict[year][month][day]['day_of_week'] = day_of_week
                data_dict[year][month][day]['week'] = week
                data_dict[year][month][day]['work_day'] = False
                data_dict[year][month][day]['times_list'] = ['00:00', '00:00', '00:00', '00:00']
                data_dict[year][month][day]['ij_status'] = ["background-color : gray",
                                                            "background-color : gray",
                                                            "background-color : gray"]
                data_dict[year][month][day]['total_time'] = "00:00"
                data_dict[year][month][day]['total_status'] = "color : gray"

            self.data_dict = data_dict

            with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.pkl', 'wb') as pickle_file:
                pickle.dump(data_dict, pickle_file, pickle.HIGHEST_PROTOCOL)
            pickle_file.close()

    def init_user_interface(self):
        """
        Method to initiate all the widgets and assign their first data
        """

        bold_font = QFont()
        bold_font.setBold(True)

        self.week_total_lbl = QLabel(text='Total week:')
        self.week_total_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.week_total_val = QLabel()
        self.week_total_val.setFont(bold_font)
        self.bank_total_lbl = QLabel(text='Hours bank:')
        self.bank_total_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.bank_total_val = QLabel()
        self.bank_total_val.setFont(bold_font)

        self.checkin_time_text_lbl = QLabel(text='Work in:')
        self.checkin_time_text_lbl.setAlignment(Qt.AlignRight)
        self.lunch_checkin_time_text_lbl = QLabel(text='Lunch in:')
        self.lunch_checkin_time_text_lbl.setAlignment(Qt.AlignRight)
        self.lunch_checkout_time_text_lbl = QLabel(text='Lunch out:')
        self.lunch_checkout_time_text_lbl.setAlignment(Qt.AlignRight)
        self.checkout_time_text_lbl = QLabel(text='Work out:')
        self.checkout_time_text_lbl.setAlignment(Qt.AlignRight)
        self.day_journey_time_text_lbl = QLabel(text='Day total:')
        self.day_journey_time_text_lbl.setAlignment(Qt.AlignRight)

        hour_time_range = r"(?:[0-1][0-9]|2[0-3]|\-\-)"
        minute_time_range = r"(?:[0-5][0-9]|2[0-3]|\-\-)"
        worked_time_range = QRegExp("^" + hour_time_range + "\\:" + minute_time_range + "$")
        worked_time_validator = QRegExpValidator(worked_time_range, self)

        self.mon_checkbox = QCheckBox(text='Mon')
        self.mon_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.mon_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 0))
        self.mon_date_lbl = QLabel()
        self.mon_workin_lbl = QLineEdit()
        self.mon_workin_lbl.setValidator(worked_time_validator)
        self.mon_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.mon_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 0, 0))
        self.mon_lunchin_lbl = QLineEdit()
        self.mon_lunchin_lbl.setValidator(worked_time_validator)
        self.mon_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.mon_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 0, 1))
        self.mon_lunchout_lbl = QLineEdit()
        self.mon_lunchout_lbl.setValidator(worked_time_validator)
        self.mon_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.mon_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 0, 2))
        self.mon_workout_lbl = QLineEdit()
        self.mon_workout_lbl.setValidator(worked_time_validator)
        self.mon_workout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.mon_workout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 0, 3))
        self.mon_total_lbl = QLabel()
        self.mon_total_lbl.setFont(bold_font)
        self.mon_morning_stat = QFrame()
        self.mon_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.mon_lunch_stat = QFrame()
        self.mon_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.mon_afternoon_stat = QFrame()
        self.mon_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.tue_checkbox = QCheckBox(text='Tue')
        self.tue_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.tue_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 1))
        self.tue_date_lbl = QLabel()
        self.tue_checkin_lbl = QLineEdit()
        self.tue_checkin_lbl.setValidator(worked_time_validator)
        self.tue_checkin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.tue_checkin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 1, 0))
        self.tue_lunchin_lbl = QLineEdit()
        self.tue_lunchin_lbl.setValidator(worked_time_validator)
        self.tue_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.tue_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 1, 1))
        self.tue_lunchout_lbl = QLineEdit()
        self.tue_lunchout_lbl.setValidator(worked_time_validator)
        self.tue_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.tue_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 1, 2))
        self.tue_checkout_lbl = QLineEdit()
        self.tue_checkout_lbl.setValidator(worked_time_validator)
        self.tue_checkout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.tue_checkout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 1, 3))
        self.tue_total_lbl = QLabel()
        self.tue_total_lbl.setFont(bold_font)
        self.tue_morning_stat = QFrame()
        self.tue_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.tue_lunch_stat = QFrame()
        self.tue_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.tue_afternoon_stat = QFrame()
        self.tue_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.wed_checkbox = QCheckBox(text='Wed')
        self.wed_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.wed_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 2))
        self.wed_date_lbl = QLabel()
        self.wed_workin_lbl = QLineEdit()
        self.wed_workin_lbl.setValidator(worked_time_validator)
        self.wed_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.wed_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 2, 0))
        self.wed_lunchin_lbl = QLineEdit()
        self.wed_lunchin_lbl.setValidator(worked_time_validator)
        self.wed_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.wed_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 2, 1))
        self.wed_lunchout_lbl = QLineEdit()
        self.wed_lunchout_lbl.setValidator(worked_time_validator)
        self.wed_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.wed_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 2, 2))
        self.wed_checkout_lbl = QLineEdit()
        self.wed_checkout_lbl.setValidator(worked_time_validator)
        self.wed_checkout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.wed_checkout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 2, 3))
        self.wed_total_lbl = QLabel()
        self.wed_total_lbl.setFont(bold_font)
        self.wed_morning_stat = QFrame()
        self.wed_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.wed_lunch_stat = QFrame()
        self.wed_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.wed_afternoon_stat = QFrame()
        self.wed_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.thu_checkbox = QCheckBox(text='Thu')
        self.thu_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.thu_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 3))
        self.thu_date_lbl = QLabel()
        self.thu_workin_lbl = QLineEdit()
        self.thu_workin_lbl.setValidator(worked_time_validator)
        self.thu_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.thu_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 3, 0))
        self.thu_lunchin_lbl = QLineEdit()
        self.thu_lunchin_lbl.setValidator(worked_time_validator)
        self.thu_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.thu_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 3, 1))
        self.thu_lunchout_lbl = QLineEdit()
        self.thu_lunchout_lbl.setValidator(worked_time_validator)
        self.thu_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.thu_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 3, 2))
        self.thu_workout_lbl = QLineEdit()
        self.thu_workout_lbl.setValidator(worked_time_validator)
        self.thu_workout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.thu_workout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 3, 3))
        self.thu_total_lbl = QLabel()
        self.thu_total_lbl.setFont(bold_font)
        self.thu_morning_stat = QFrame()
        self.thu_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.thu_lunch_stat = QFrame()
        self.thu_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.thu_afternoon_stat = QFrame()
        self.thu_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.fri_checkbox = QCheckBox(text='Fri')
        self.fri_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.fri_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 4))
        self.fri_date_lbl = QLabel()
        self.fri_workin_lbl = QLineEdit()
        self.fri_workin_lbl.setValidator(worked_time_validator)
        self.fri_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.fri_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 4, 0))
        self.fri_lunchin_lbl = QLineEdit()
        self.fri_lunchin_lbl.setValidator(worked_time_validator)
        self.fri_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.fri_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 4, 1))
        self.fri_lunchout_lbl = QLineEdit()
        self.fri_lunchout_lbl.setValidator(worked_time_validator)
        self.fri_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.fri_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 4, 2))
        self.fri_workout_lbl = QLineEdit()
        self.fri_workout_lbl.setValidator(worked_time_validator)
        self.fri_workout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.fri_workout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 4, 3))
        self.fri_total_lbl = QLabel()
        self.fri_total_lbl.setFont(bold_font)
        self.fri_morning_stat = QFrame()
        self.fri_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.fri_lunch_stat = QFrame()
        self.fri_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.fri_afternoon_stat = QFrame()
        self.fri_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.sat_checkbox = QCheckBox(text='Sat')
        self.sat_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.sat_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 5))
        self.sat_date_lbl = QLabel()
        self.sat_workin_lbl = QLineEdit()
        self.sat_workin_lbl.setValidator(worked_time_validator)
        self.sat_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sat_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 5, 0))
        self.sat_lunchin_lbl = QLineEdit()
        self.sat_lunchin_lbl.setValidator(worked_time_validator)
        self.sat_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sat_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 5, 1))
        self.sat_lunchout_lbl = QLineEdit()
        self.sat_lunchout_lbl.setValidator(worked_time_validator)
        self.sat_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sat_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 5, 2))
        self.sat_workout_lbl = QLineEdit()
        self.sat_workout_lbl.setValidator(worked_time_validator)
        self.sat_workout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sat_workout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 5, 3))
        self.sat_total_lbl = QLabel()
        self.sat_total_lbl.setFont(bold_font)
        self.sat_morning_stat = QFrame()
        self.sat_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sat_lunch_stat = QFrame()
        self.sat_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sat_afternoon_stat = QFrame()
        self.sat_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.sun_checkbox = QCheckBox(text='Sun')
        self.sun_checkbox.setLayoutDirection(Qt.LeftToRight)
        self.sun_checkbox.stateChanged.connect(lambda check: self.checkbox_change_stat(check, 6))
        self.sun_date_lbl = QLabel()
        self.sun_workin_lbl = QLineEdit()
        self.sun_workin_lbl.setValidator(worked_time_validator)
        self.sun_workin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sun_workin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 6, 0))
        self.sun_lunchin_lbl = QLineEdit()
        self.sun_lunchin_lbl.setValidator(worked_time_validator)
        self.sun_lunchin_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sun_lunchin_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 6, 1))
        self.sun_lunchout_lbl = QLineEdit()
        self.sun_lunchout_lbl.setValidator(worked_time_validator)
        self.sun_lunchout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sun_lunchout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 6, 2))
        self.sun_workout_lbl = QLineEdit()
        self.sun_workout_lbl.setValidator(worked_time_validator)
        self.sun_workout_lbl.setFixedSize(self.TIME_BOX_SIZE)
        self.sun_workout_lbl.textChanged.connect(lambda text: self.calculate_total_time(text, 6, 3))
        self.sun_total_lbl = QLabel()
        self.sun_total_lbl.setFont(bold_font)
        self.sun_morning_stat = QFrame()
        self.sun_morning_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sun_lunch_stat = QFrame()
        self.sun_lunch_stat.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sun_afternoon_stat = QFrame()
        self.sun_afternoon_stat.setFixedSize(self.COLOR_FRAME_SIZE)

        self.week_backward_button = QPushButton('<<', self)
        self.week_backward_button.clicked.connect(lambda: self.change_week_display(False))
        self.week_forward_button = QPushButton('>>', self)
        self.week_forward_button.clicked.connect(lambda: self.change_week_display(True))
        self.back_to_main_button = QPushButton('Go back', self)
        self.back_to_main_button.clicked.connect(self.close_widget)

        self.widget_layout = QGridLayout()

        self.widget_layout.addWidget(self.week_total_lbl, 0, 0, 1, 2)
        self.widget_layout.addWidget(self.week_total_val, 0, 2)
        self.widget_layout.addWidget(self.bank_total_lbl, 0, 3, 1, 2)
        self.widget_layout.addWidget(self.bank_total_val, 0, 5)

        self.widget_layout.addWidget(self.mon_date_lbl, 1, 0)
        self.widget_layout.addWidget(self.mon_checkbox, 2, 0)
        self.widget_layout.addWidget(self.mon_workin_lbl, 3, 0)
        self.widget_layout.addWidget(self.mon_morning_stat, 4, 0)
        self.widget_layout.addWidget(self.mon_lunchin_lbl, 5, 0)
        self.widget_layout.addWidget(self.mon_lunch_stat, 6, 0)
        self.widget_layout.addWidget(self.mon_lunchout_lbl, 7, 0)
        self.widget_layout.addWidget(self.mon_afternoon_stat, 8, 0)
        self.widget_layout.addWidget(self.mon_workout_lbl, 9, 0)
        self.widget_layout.addWidget(self.mon_total_lbl, 10, 0)

        self.widget_layout.addWidget(self.tue_date_lbl, 1, 1)
        self.widget_layout.addWidget(self.tue_checkbox, 2, 1)
        self.widget_layout.addWidget(self.tue_checkin_lbl, 3, 1)
        self.widget_layout.addWidget(self.tue_morning_stat, 4, 1)
        self.widget_layout.addWidget(self.tue_lunchin_lbl, 5, 1)
        self.widget_layout.addWidget(self.tue_lunch_stat, 6, 1)
        self.widget_layout.addWidget(self.tue_lunchout_lbl, 7, 1)
        self.widget_layout.addWidget(self.tue_afternoon_stat, 8, 1)
        self.widget_layout.addWidget(self.tue_checkout_lbl, 9, 1)
        self.widget_layout.addWidget(self.tue_total_lbl, 10, 1)

        self.widget_layout.addWidget(self.wed_date_lbl, 1, 2)
        self.widget_layout.addWidget(self.wed_checkbox, 2, 2)
        self.widget_layout.addWidget(self.wed_workin_lbl, 3, 2)
        self.widget_layout.addWidget(self.wed_morning_stat, 4, 2)
        self.widget_layout.addWidget(self.wed_lunchin_lbl, 5, 2)
        self.widget_layout.addWidget(self.wed_lunch_stat, 6, 2)
        self.widget_layout.addWidget(self.wed_lunchout_lbl, 7, 2)
        self.widget_layout.addWidget(self.wed_afternoon_stat, 8, 2)
        self.widget_layout.addWidget(self.wed_checkout_lbl, 9, 2)
        self.widget_layout.addWidget(self.wed_total_lbl, 10, 2)

        self.widget_layout.addWidget(self.thu_date_lbl, 1, 3)
        self.widget_layout.addWidget(self.thu_checkbox, 2, 3)
        self.widget_layout.addWidget(self.thu_workin_lbl, 3, 3)
        self.widget_layout.addWidget(self.thu_morning_stat, 4, 3)
        self.widget_layout.addWidget(self.thu_lunchin_lbl, 5, 3)
        self.widget_layout.addWidget(self.thu_lunch_stat, 6, 3)
        self.widget_layout.addWidget(self.thu_lunchout_lbl, 7, 3)
        self.widget_layout.addWidget(self.thu_afternoon_stat, 8, 3)
        self.widget_layout.addWidget(self.thu_workout_lbl, 9, 3)
        self.widget_layout.addWidget(self.thu_total_lbl, 10, 3)

        self.widget_layout.addWidget(self.fri_date_lbl, 1, 4)
        self.widget_layout.addWidget(self.fri_checkbox, 2, 4)
        self.widget_layout.addWidget(self.fri_workin_lbl, 3, 4)
        self.widget_layout.addWidget(self.fri_morning_stat, 4, 4)
        self.widget_layout.addWidget(self.fri_lunchin_lbl, 5, 4)
        self.widget_layout.addWidget(self.fri_lunch_stat, 6, 4)
        self.widget_layout.addWidget(self.fri_lunchout_lbl, 7, 4)
        self.widget_layout.addWidget(self.fri_afternoon_stat, 8, 4)
        self.widget_layout.addWidget(self.fri_workout_lbl, 9, 4)
        self.widget_layout.addWidget(self.fri_total_lbl, 10, 4)

        self.widget_layout.addWidget(self.sat_date_lbl, 1, 5)
        self.widget_layout.addWidget(self.sat_checkbox, 2, 5)
        self.widget_layout.addWidget(self.sat_workin_lbl, 3, 5)
        self.widget_layout.addWidget(self.sat_morning_stat, 4, 5)
        self.widget_layout.addWidget(self.sat_lunchin_lbl, 5, 5)
        self.widget_layout.addWidget(self.sat_lunch_stat, 6, 5)
        self.widget_layout.addWidget(self.sat_lunchout_lbl, 7, 5)
        self.widget_layout.addWidget(self.sat_afternoon_stat, 8, 5)
        self.widget_layout.addWidget(self.sat_workout_lbl, 9, 5)
        self.widget_layout.addWidget(self.sat_total_lbl, 10, 5)

        self.widget_layout.addWidget(self.sun_date_lbl, 1, 6)
        self.widget_layout.addWidget(self.sun_checkbox, 2, 6)
        self.widget_layout.addWidget(self.sun_workin_lbl, 3, 6)
        self.widget_layout.addWidget(self.sun_morning_stat, 4, 6)
        self.widget_layout.addWidget(self.sun_lunchin_lbl, 5, 6)
        self.widget_layout.addWidget(self.sun_lunch_stat, 6, 6)
        self.widget_layout.addWidget(self.sun_lunchout_lbl, 7, 6)
        self.widget_layout.addWidget(self.sun_afternoon_stat, 8, 6)
        self.widget_layout.addWidget(self.sun_workout_lbl, 9, 6)
        self.widget_layout.addWidget(self.sun_total_lbl, 10, 6)

        self.widget_layout.addWidget(self.week_backward_button, 11, 0, 1, 2)
        self.widget_layout.addWidget(self.back_to_main_button, 11, 2, 1, 3)
        self.widget_layout.addWidget(self.week_forward_button, 11, 5, 1, 2)

        self.setLayout(self.widget_layout)

    def update_log_data(self):
        """
        Method to update the
        """
        # self.week_total_val.setText(utils.get_from_dict(self.data_dict, self.curr_week[0][1])['total_time'])
        self.week_total_val.setText(utils.get_week_total_time(self.data_dict, self.curr_week))
        self.bank_total_val.setText(self.data_dict[self.year][self.month]['hours_bank'])

        self.mon_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[0], 'work_day'))
        self.mon_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'date'))
        self.mon_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'times_list')[0])
        self.mon_workin_lbl.setEnabled(self.mon_checkbox.isChecked())
        self.mon_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'times_list')[1])
        self.mon_lunchin_lbl.setEnabled(self.mon_checkbox.isChecked())
        self.mon_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'times_list')[2])
        self.mon_lunchout_lbl.setEnabled(self.mon_checkbox.isChecked())
        self.mon_workout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'times_list')[3])
        self.mon_workout_lbl.setEnabled(self.mon_checkbox.isChecked())
        self.mon_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[0], 'total_time'))
        self.mon_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[0], 'total_status'))
        self.mon_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[0], 'ij_status')[0])
        self.mon_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[0], 'ij_status')[1])
        self.mon_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[0], 'ij_status')[2])
        self.tue_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[1], 'work_day'))
        self.tue_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'date'))
        self.tue_checkin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'times_list')[0])
        self.tue_checkin_lbl.setEnabled(self.tue_checkbox.isChecked())
        self.tue_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'times_list')[1])
        self.tue_lunchin_lbl.setEnabled(self.tue_checkbox.isChecked())
        self.tue_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'times_list')[2])
        self.tue_lunchout_lbl.setEnabled(self.tue_checkbox.isChecked())
        self.tue_checkout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'times_list')[3])
        self.tue_checkout_lbl.setEnabled(self.tue_checkbox.isChecked())
        self.tue_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[1], 'total_time'))
        self.tue_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[1], 'total_status'))
        self.tue_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[1], 'ij_status')[0])
        self.tue_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[1], 'ij_status')[1])
        self.tue_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[1], 'ij_status')[2])
        self.wed_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[2], 'work_day'))
        self.wed_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'date'))
        self.wed_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'times_list')[0])
        self.wed_workin_lbl.setEnabled(self.wed_checkbox.isChecked())
        self.wed_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'times_list')[1])
        self.wed_lunchin_lbl.setEnabled(self.wed_checkbox.isChecked())
        self.wed_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'times_list')[2])
        self.wed_lunchout_lbl.setEnabled(self.wed_checkbox.isChecked())
        self.wed_checkout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'times_list')[3])
        self.wed_checkout_lbl.setEnabled(self.wed_checkbox.isChecked())
        self.wed_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[2], 'total_time'))
        self.wed_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[2], 'total_status'))
        self.wed_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[2], 'ij_status')[0])
        self.wed_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[2], 'ij_status')[1])
        self.wed_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[2], 'ij_status')[2])
        self.thu_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[3], 'work_day'))
        self.thu_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'date'))
        self.thu_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'times_list')[0])
        self.thu_workin_lbl.setEnabled(self.thu_checkbox.isChecked())
        self.thu_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'times_list')[1])
        self.thu_lunchin_lbl.setEnabled(self.thu_checkbox.isChecked())
        self.thu_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'times_list')[2])
        self.thu_lunchout_lbl.setEnabled(self.thu_checkbox.isChecked())
        self.thu_workout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'times_list')[3])
        self.thu_workout_lbl.setEnabled(self.thu_checkbox.isChecked())
        self.thu_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[3], 'total_time'))
        self.thu_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[3], 'total_status'))
        self.thu_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[3], 'ij_status')[0])
        self.thu_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[3], 'ij_status')[1])
        self.thu_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[3], 'ij_status')[2])
        self.fri_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[4], 'work_day'))
        self.fri_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'date'))
        self.fri_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'times_list')[0])
        self.fri_workin_lbl.setEnabled(self.fri_checkbox.isChecked())
        self.fri_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'times_list')[1])
        self.fri_lunchin_lbl.setEnabled(self.fri_checkbox.isChecked())
        self.fri_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'times_list')[2])
        self.fri_lunchout_lbl.setEnabled(self.fri_checkbox.isChecked())
        self.fri_workout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'times_list')[3])
        self.fri_workout_lbl.setEnabled(self.fri_checkbox.isChecked())
        self.fri_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[4], 'total_time'))
        self.fri_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[4], 'total_status'))
        self.fri_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[4], 'ij_status')[0])
        self.fri_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[4], 'ij_status')[1])
        self.fri_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[4], 'ij_status')[2])
        self.sat_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[5], 'work_day'))
        self.sat_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'date'))
        self.sat_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'times_list')[0])
        self.sat_workin_lbl.setEnabled(self.sat_checkbox.isChecked())
        self.sat_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'times_list')[1])
        self.sat_lunchin_lbl.setEnabled(self.sat_checkbox.isChecked())
        self.sat_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'times_list')[2])
        self.sat_lunchout_lbl.setEnabled(self.sat_checkbox.isChecked())
        self.sat_workout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'times_list')[3])
        self.sat_workout_lbl.setEnabled(self.sat_checkbox.isChecked())
        self.sat_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[5], 'total_time'))
        self.sat_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[5], 'total_status'))
        self.sat_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[5], 'ij_status')[0])
        self.sat_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[5], 'ij_status')[1])
        self.sat_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[5], 'ij_status')[2])
        self.sun_checkbox.setChecked(utils.get_from_dict(self.data_dict, self.curr_week[6], 'work_day'))
        self.sun_date_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'date'))
        self.sun_workin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'times_list')[0])
        self.sun_workin_lbl.setEnabled(self.sun_checkbox.isChecked())
        self.sun_lunchin_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'times_list')[1])
        self.sun_lunchin_lbl.setEnabled(self.sun_checkbox.isChecked())
        self.sun_lunchout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'times_list')[2])
        self.sun_lunchout_lbl.setEnabled(self.sun_checkbox.isChecked())
        self.sun_workout_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'times_list')[3])
        self.sun_workout_lbl.setEnabled(self.sun_checkbox.isChecked())
        self.sun_total_lbl.setText(utils.get_from_dict(self.data_dict, self.curr_week[6], 'total_time'))
        self.sun_total_lbl.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[6], 'total_status'))
        self.sun_morning_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[6], 'ij_status')[0])
        self.sun_lunch_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[6], 'ij_status')[1])
        self.sun_afternoon_stat.setStyleSheet(utils.get_from_dict(self.data_dict, self.curr_week[6], 'ij_status')[2])

    def checkbox_change_stat(self, value, day):
        """
        Method to activate or deactivate the day labels
        """
        if value:
            utils.get_from_dict(self.data_dict, self.curr_week[day])['work_day'] = True
            times_list = utils.get_from_dict(self.data_dict, self.curr_week[day])['times_list']
            ij_status = list(utils.get_ij_status(times_list))
            total_status = utils.get_work_time_status(times_list)
            utils.get_from_dict(self.data_dict, self.curr_week[day])['ij_status'] = ij_status
            utils.get_from_dict(self.data_dict, self.curr_week[day])['total_status'] = total_status
        else:
            utils.get_from_dict(self.data_dict, self.curr_week[day])['work_day'] = False
            utils.get_from_dict(self.data_dict, self.curr_week[day])['total_status'] = "color : gray"
            utils.get_from_dict(self.data_dict, self.curr_week[day])['ij_status'] = ["background-color : gray",
                                                                                     "background-color : gray",
                                                                                     "background-color : gray"]
        self.update_log_data()

    def calculate_total_time(self, text, day, time):
        """
        Method to calculate the total worked time on monday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            day_times = utils.get_from_dict(self.data_dict, self.curr_week[day])['times_list']
            day_times[time] = text
            total = utils.total_worked_time(day_times)

            if '-' not in total:
                utils.get_from_dict(self.data_dict, self.curr_week[day])['times_list'][time] = text
                utils.get_from_dict(self.data_dict, self.curr_week[day])['total_time'] = total
                times_list = utils.get_from_dict(self.data_dict, self.curr_week[day])['times_list']
                day_status = utils.get_from_dict(self.data_dict, self.curr_week[day])['work_day']
                utils.get_from_dict(self.data_dict, self.curr_week[day])['total_status'] =\
                    utils.get_work_time_status(times_list)
                if day_status:
                    ij_status = list(utils.get_ij_status(times_list))
                    utils.get_from_dict(self.data_dict, self.curr_week[day])['ij_status'] = ij_status
                utils.get_total_time_from(self.data_dict, self.year, month=self.month)
                self.update_log_data()

    def change_week_display(self, value):
        """
        Method to change the current week and month data being displayed on the app
        """
        if value:
            if self.week < self.last_log_week:
                self.week += 1
        else:
            if self.week > self.first_log_week:
                self.week -= 1
        self.curr_week = utils.get_week_days_list(self.year, self.week)
        self.month = self.curr_week[3][1]
        self.update_log_data()

    def close_widget(self):
        """
        Method to send the signal to close the worked log widget
        """
        with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.pkl', 'wb') as pickle_file:
            pickle.dump(self.data_dict, pickle_file, pickle.HIGHEST_PROTOCOL)
        pickle_file.close()
        with open(utils.get_absolute_resource_path('resources/data/') + 'log_data.json', 'w') as json_file:
            json.dump(self.data_dict, json_file, indent=4)
        json_file.close()
