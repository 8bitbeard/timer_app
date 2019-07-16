"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import re
from datetime import date, timedelta

import pandas

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtCore import QRegExp, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator

from src.utils import utils


# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class WorkedLogWidget(QWidget):
    """
    Worked log widget
    """

    TIME_BOX_SIZE = QSize(50, 20)

    close_worked_log_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(WorkedLogWidget, self).__init__(parent)

        self.week_timeline_number = 0

        # self.work_log_data = pandas.read_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"))
        # self.week_model_data = pandas.read_csv(utils.get_absolute_resource_path("resources/csv_data/week_model_data.csv"))

        self.work_log_data = self.csv_to_dict('test_file.csv')

        self.update_csv_data()
        self.init_user_interface()
        self.update_times()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """

        bold_font = QFont()
        bold_font.setBold(True)

        self.week_text_label = QLabel(text='Week:')
        self.week_text_label.setAlignment(Qt.AlignRight)
        self.week_value_label = QLabel(self.work_log_data['data'].iloc[-5] + '-' + self.work_log_data['data'].iloc[-4])
        self.week_value_label.setFont(bold_font)
        self.total_week_text_label = QLabel(text='Total Week:')
        self.total_week_text_label.setAlignment(Qt.AlignRight)
        self.total_week_time_value = QLabel(self.work_log_data['data'].iloc[-3])
        self.total_week_time_value.setFont(bold_font)
        self.total_month_text_label = QLabel(text='Total Month:')
        self.total_month_text_label.setAlignment(Qt.AlignRight)
        self.total_month_time_value = QLabel(self.work_log_data['data'].iloc[-2])
        self.total_month_time_value.setFont(bold_font)

        self.checkin_time_text_label = QLabel(text='Work in:')
        self.checkin_time_text_label.setAlignment(Qt.AlignRight)
        self.lunch_checkin_time_text_label = QLabel(text='Lunch in:')
        self.lunch_checkin_time_text_label.setAlignment(Qt.AlignRight)
        self.lunch_checkout_time_text_label = QLabel(text='Lunch out:')
        self.lunch_checkout_time_text_label.setAlignment(Qt.AlignRight)
        self.checkout_time_text_label = QLabel(text='Work out:')
        self.checkout_time_text_label.setAlignment(Qt.AlignRight)
        self.day_journey_time_text_label = QLabel(text='Day total:')
        self.day_journey_time_text_label.setAlignment(Qt.AlignRight)

        hour_time_range = "(?:[0-1][0-9]|2[0-3])"
        minute_time_range = "(?:[0-5][0-9]|2[0-3])"
        worked_time_range = QRegExp("^" + hour_time_range + "\\:" + minute_time_range + "$")
        worked_time_validator = QRegExpValidator(worked_time_range, self)

        self.sunday_text_label = QLabel(text='Sun')
        self.sunday_week_day_label = QLabel(text=self.work_log_data['sun'].iloc[-6 - self.week_timeline_number * 6])
        self.sunday_checkin_label = QLineEdit(text=self.work_log_data['sun'].iloc[-5 - self.week_timeline_number * 6])
        self.sunday_checkin_label.setValidator(worked_time_validator)
        self.sunday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkin_label = QLineEdit(text=self.work_log_data['sun'].iloc[-4 - self.week_timeline_number * 6])
        self.sunday_lunch_checkin_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkout_label = QLineEdit(text=self.work_log_data['sun'].iloc[-3 - self.week_timeline_number * 6])
        self.sunday_lunch_checkout_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_checkout_label = QLineEdit(text=self.work_log_data['sun'].iloc[-2 - self.week_timeline_number * 6])
        self.sunday_checkout_label.setValidator(worked_time_validator)
        self.sunday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_worked_time_label = QLabel(text=self.work_log_data['sun'].iloc[-1 - self.week_timeline_number * 6])

        self.monday_text_label = QLabel(text='Mon')
        self.monday_week_day_label = QLabel(text=self.work_log_data['mon'].iloc[-6 - self.week_timeline_number * 6])
        self.monday_checkin_label = QLineEdit(text=self.work_log_data['mon'].iloc[-5 - self.week_timeline_number * 6])
        self.monday_checkin_label.setValidator(worked_time_validator)
        self.monday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkin_label = QLineEdit(text=self.work_log_data['mon'].iloc[-4 - self.week_timeline_number * 6])
        self.monday_lunch_checkin_label.setValidator(worked_time_validator)
        self.monday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkout_label = QLineEdit(text=self.work_log_data['mon'].iloc[-3 - self.week_timeline_number * 6])
        self.monday_lunch_checkout_label.setValidator(worked_time_validator)
        self.monday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_checkout_label = QLineEdit(text=self.work_log_data['mon'].iloc[-2 - self.week_timeline_number * 6])
        self.monday_checkout_label.setValidator(worked_time_validator)
        self.monday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_worked_time_label = QLabel(text=self.work_log_data['mon'].iloc[-1 - self.week_timeline_number * 6])

        self.tuesday_text_label = QLabel(text='Tue')
        self.tuesday_week_day_label = QLabel(text=self.work_log_data['tue'].iloc[-6 - self.week_timeline_number * 6])
        self.tuesday_checkin_label = QLineEdit(text=self.work_log_data['tue'].iloc[-5 - self.week_timeline_number * 6])
        self.tuesday_checkin_label.setValidator(worked_time_validator)
        self.tuesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkin_label = QLineEdit(text=self.work_log_data['tue'].iloc[-4 - self.week_timeline_number * 6])
        self.tuesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkout_label = QLineEdit(text=self.work_log_data['tue'].iloc[-3 - self.week_timeline_number * 6])
        self.tuesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_checkout_label = QLineEdit(text=self.work_log_data['tue'].iloc[-2 - self.week_timeline_number * 6])
        self.tuesday_checkout_label.setValidator(worked_time_validator)
        self.tuesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_worked_time_label = QLabel(text=self.work_log_data['tue'].iloc[-1 - self.week_timeline_number * 6])

        self.wednesday_text_label = QLabel(text='Wed')
        self.wednesday_week_day_label = QLabel(text=self.work_log_data['wed'].iloc[-6 - self.week_timeline_number * 6])
        self.wednesday_checkin_label = QLineEdit(text=self.work_log_data['wed'].iloc[-5 - self.week_timeline_number * 6])
        self.wednesday_checkin_label.setValidator(worked_time_validator)
        self.wednesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkin_label = QLineEdit(text=self.work_log_data['wed'].iloc[-4 - self.week_timeline_number * 6])
        self.wednesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkout_label = QLineEdit(text=self.work_log_data['wed'].iloc[-3 - self.week_timeline_number * 6])
        self.wednesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_checkout_label = QLineEdit(text=self.work_log_data['wed'].iloc[-2 - self.week_timeline_number * 6])
        self.wednesday_checkout_label.setValidator(worked_time_validator)
        self.wednesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_worked_time_label = QLabel(text=self.work_log_data['wed'].iloc[-1 - self.week_timeline_number * 6])

        self.thursday_text_label = QLabel(text='Thu')
        self.thursday_week_day_label = QLabel(text=self.work_log_data['thu'].iloc[-6 - self.week_timeline_number * 6])
        self.thursday_checkin_label = QLineEdit(text=self.work_log_data['thu'].iloc[-5 - self.week_timeline_number * 6])
        self.thursday_checkin_label.setValidator(worked_time_validator)
        self.thursday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkin_label = QLineEdit(text=self.work_log_data['thu'].iloc[-4 - self.week_timeline_number * 6])
        self.thursday_lunch_checkin_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkout_label = QLineEdit(text=self.work_log_data['thu'].iloc[-3 - self.week_timeline_number * 6])
        self.thursday_lunch_checkout_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_checkout_label = QLineEdit(text=self.work_log_data['thu'].iloc[-2 - self.week_timeline_number * 6])
        self.thursday_checkout_label.setValidator(worked_time_validator)
        self.thursday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_worked_time_label = QLabel(text=self.work_log_data['thu'].iloc[-1 - self.week_timeline_number * 6])

        self.week_backward_button = QPushButton('<<', self)
        self.week_backward_button.clicked.connect(lambda: self.change_week_display(False))
        self.week_foward_button = QPushButton('>>', self)
        self.week_foward_button.clicked.connect(lambda: self.change_week_display(True))

        self.back_to_main_button = QPushButton('Go back', self)
        self.back_to_main_button.clicked.connect(self.close_widget)


        self.widget_layout = QGridLayout()

        self.widget_layout.addWidget(self.total_week_text_label, 0, 0, 1, 2)
        self.widget_layout.addWidget(self.total_week_time_value, 0, 2)
        self.widget_layout.addWidget(self.total_month_text_label, 0, 3, 1, 2)
        self.widget_layout.addWidget(self.total_month_time_value, 0, 5)

        self.widget_layout.addWidget(self.week_value_label, 2, 0)
        self.widget_layout.addWidget(self.checkin_time_text_label, 3, 0)
        self.widget_layout.addWidget(self.lunch_checkin_time_text_label, 4, 0)
        self.widget_layout.addWidget(self.lunch_checkout_time_text_label, 5, 0)
        self.widget_layout.addWidget(self.checkout_time_text_label, 6, 0)
        self.widget_layout.addWidget(self.day_journey_time_text_label, 7, 0)

        self.widget_layout.addWidget(self.sunday_week_day_label, 1 ,1)
        self.widget_layout.addWidget(self.sunday_text_label, 2, 1)
        self.widget_layout.addWidget(self.sunday_checkin_label, 3, 1)
        self.widget_layout.addWidget(self.sunday_lunch_checkin_label, 4, 1)
        self.widget_layout.addWidget(self.sunday_lunch_checkout_label, 5, 1)
        self.widget_layout.addWidget(self.sunday_checkout_label, 6, 1)
        self.widget_layout.addWidget(self.sunday_worked_time_label, 7, 1)

        self.widget_layout.addWidget(self.monday_week_day_label, 1 ,2)
        self.widget_layout.addWidget(self.monday_text_label, 2, 2)
        self.widget_layout.addWidget(self.monday_checkin_label, 3, 2)
        self.widget_layout.addWidget(self.monday_lunch_checkin_label, 4, 2)
        self.widget_layout.addWidget(self.monday_lunch_checkout_label, 5, 2)
        self.widget_layout.addWidget(self.monday_checkout_label, 6, 2)
        self.widget_layout.addWidget(self.monday_worked_time_label, 7, 2)

        self.widget_layout.addWidget(self.tuesday_week_day_label, 1, 3)
        self.widget_layout.addWidget(self.tuesday_text_label, 2, 3)
        self.widget_layout.addWidget(self.tuesday_checkin_label, 3, 3)
        self.widget_layout.addWidget(self.tuesday_lunch_checkin_label, 4, 3)
        self.widget_layout.addWidget(self.tuesday_lunch_checkout_label, 5, 3)
        self.widget_layout.addWidget(self.tuesday_checkout_label, 6, 3)
        self.widget_layout.addWidget(self.tuesday_worked_time_label, 7, 3)

        self.widget_layout.addWidget(self.wednesday_week_day_label, 1 ,4)
        self.widget_layout.addWidget(self.wednesday_text_label, 2, 4)
        self.widget_layout.addWidget(self.wednesday_checkin_label, 3, 4)
        self.widget_layout.addWidget(self.wednesday_lunch_checkin_label, 4, 4)
        self.widget_layout.addWidget(self.wednesday_lunch_checkout_label, 5, 4)
        self.widget_layout.addWidget(self.wednesday_checkout_label, 6, 4)
        self.widget_layout.addWidget(self.wednesday_worked_time_label, 7, 4)

        self.widget_layout.addWidget(self.thursday_week_day_label, 1 ,5)
        self.widget_layout.addWidget(self.thursday_text_label, 2, 5)
        self.widget_layout.addWidget(self.thursday_checkin_label, 3, 5)
        self.widget_layout.addWidget(self.thursday_lunch_checkin_label, 4, 5)
        self.widget_layout.addWidget(self.thursday_lunch_checkout_label, 5, 5)
        self.widget_layout.addWidget(self.thursday_checkout_label, 6, 5)
        self.widget_layout.addWidget(self.thursday_worked_time_label, 7, 5)

        self.widget_layout.addWidget(self.week_backward_button, 8, 0)
        self.widget_layout.addWidget(self.back_to_main_button, 8, 1, 1, 4)
        self.widget_layout.addWidget(self.week_foward_button, 8, 5)

        self.setLayout(self.widget_layout)

    def calculate_sunday_total_time(self, text):
        """
        Method to calculate the total worked time on sunday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.sunday_checkin_label.text(),
                                            self.sunday_lunch_checkin_label.text(),
                                            self.sunday_lunch_checkout_label.text(),
                                            self.sunday_checkout_label.text())
            if '-' not in total:
                self.sunday_worked_time_label.setText(total)
                self.calculate_week_total_time()

    def calculate_monday_total_time(self, text):
        """
        Method to calculate the total worked time on monday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.monday_checkin_label.text(),
                                            self.monday_lunch_checkin_label.text(),
                                            self.monday_lunch_checkout_label.text(),
                                            self.monday_checkout_label.text())
            if '-' not in total:
                self.monday_worked_time_label.setText(total)
                self.calculate_week_total_time()

    def calculate_tuesday_total_time(self, text):
        """
        Method to calculate the total worked time on tuesday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.tuesday_checkin_label.text(),
                                            self.tuesday_lunch_checkin_label.text(),
                                            self.tuesday_lunch_checkout_label.text(),
                                            self.tuesday_checkout_label.text())
            if '-' not in total:
                self.tuesday_worked_time_label.setText(total)
                self.calculate_week_total_time()

    def calculate_wednesday_total_time(self, text):
        """
        Method to calculate the total worked time on wednesday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.wednesday_checkin_label.text(),
                                            self.wednesday_lunch_checkin_label.text(),
                                            self.wednesday_lunch_checkout_label.text(),
                                            self.wednesday_checkout_label.text())
            if '-' not in total:
                self.wednesday_worked_time_label.setText(total)
                self.calculate_week_total_time()

    def calculate_thursday_total_time(self, text):
        """
        Method to calculate the total worked time on thursday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.thursday_checkin_label.text(),
                                            self.thursday_lunch_checkin_label.text(),
                                            self.thursday_lunch_checkout_label.text(),
                                            self.thursday_checkout_label.text())
            if '-' not in total:
                self.thursday_worked_time_label.setText(total)
                self.calculate_week_total_time()

    def calculate_week_total_time(self):
        """
        Method to calculate the total time worked on the week
        """
        total = utils.sum_times(self.sunday_worked_time_label.text(),
                                self.monday_worked_time_label.text(),
                                self.tuesday_worked_time_label.text(),
                                self.wednesday_worked_time_label.text(),
                                self.thursday_worked_time_label.text())
        self.total_week_time_value.setText(total)

    def calculate_month_total_time(self, month):
        """
        Method to calculate the total time worked on the month
        """

    def calculate_week_range(self, input_date):
        """
        Method to calculate the week range days
        """
        year, week, dow = input_date.isocalendar()

        if dow == 7:
            start_date = input_date
        else:
            start_date = input_date - timedelta(dow)

        end_date = start_date + timedelta(6)

        formated_start_date = '{:02d}/{:02d}'.format(start_date.day, start_date.month)
        formated_end_date = '{:02d}/{:02d}'.format(end_date.day, end_date.month)

        return (formated_start_date, formated_end_date)

    def change_week_display(self, value):
        """
        Method to change the week being displayed on the work log
        """
        if value:
            if self.week_timeline_number > 0:
                self.week_timeline_number -= 1
            else:
                pass
        else:
            self.week_timeline_number += 1
        self.update_log_data()
        print(self.week_timeline_number)

    def update_log_data(self):
        """
        Method to update the work log data being displayed
        """
        self.week_value_label.setText(self.work_log_data['data'].iloc[-5 - self.week_timeline_number * 6] + '-' +
                                      self.work_log_data['data'].iloc[-4 - self.week_timeline_number * 6])
        self.total_week_time_value.setText(self.work_log_data['data'].iloc[-3 - self.week_timeline_number * 6])
        self.total_month_time_value.setText(self.work_log_data['data'].iloc[-2 - self.week_timeline_number * 6])
        self.sunday_week_day_label.setText(self.work_log_data['sun'].iloc[-6 - self.week_timeline_number * 6])
        self.monday_week_day_label.setText(self.work_log_data['mon'].iloc[-6 - self.week_timeline_number * 6])
        self.tuesday_week_day_label.setText(self.work_log_data['tue'].iloc[-6 - self.week_timeline_number * 6])
        self.wednesday_week_day_label.setText(self.work_log_data['wed'].iloc[-6 - self.week_timeline_number * 6])
        self.thursday_week_day_label.setText(self.work_log_data['thu'].iloc[-6 - self.week_timeline_number * 6])
        self.sunday_checkin_label.setText(self.work_log_data['sun'].iloc[-5 - self.week_timeline_number * 6])
        self.sunday_lunch_checkin_label.setText(self.work_log_data['sun'].iloc[-4 - self.week_timeline_number * 6])
        self.sunday_lunch_checkout_label.setText(self.work_log_data['sun'].iloc[-3 - self.week_timeline_number * 6])
        self.sunday_checkout_label.setText(self.work_log_data['sun'].iloc[-2 - self.week_timeline_number * 6])
        self.sunday_worked_time_label.setText(self.work_log_data['sun'].iloc[-1 - self.week_timeline_number * 6])
        self.monday_checkin_label.setText(self.work_log_data['mon'].iloc[-5 - self.week_timeline_number * 6])
        self.monday_lunch_checkin_label.setText(self.work_log_data['mon'].iloc[-4 - self.week_timeline_number * 6])
        self.monday_lunch_checkout_label.setText(self.work_log_data['mon'].iloc[-3 - self.week_timeline_number * 6])
        self.monday_checkout_label.setText(self.work_log_data['mon'].iloc[-2 - self.week_timeline_number * 6])
        self.monday_worked_time_label.setText(self.work_log_data['mon'].iloc[-1 - self.week_timeline_number * 6])
        self.tuesday_checkin_label.setText(self.work_log_data['tue'].iloc[-5 - self.week_timeline_number * 6])
        self.tuesday_lunch_checkin_label.setText(self.work_log_data['tue'].iloc[-4 - self.week_timeline_number * 6])
        self.tuesday_lunch_checkout_label.setText(self.work_log_data['tue'].iloc[-3 - self.week_timeline_number * 6])
        self.tuesday_checkout_label.setText(self.work_log_data['tue'].iloc[-2 - self.week_timeline_number * 6])
        self.tuesday_worked_time_label.setText(self.work_log_data['tue'].iloc[-1 - self.week_timeline_number * 6])
        self.wednesday_checkin_label.setText(self.work_log_data['wed'].iloc[-5 - self.week_timeline_number * 6])
        self.wednesday_lunch_checkin_label.setText(self.work_log_data['wed'].iloc[-4 - self.week_timeline_number * 6])
        self.wednesday_lunch_checkout_label.setText(self.work_log_data['wed'].iloc[-3 - self.week_timeline_number * 6])
        self.wednesday_checkout_label.setText(self.work_log_data['wed'].iloc[-2 - self.week_timeline_number * 6])
        self.wednesday_worked_time_label.setText(self.work_log_data['wed'].iloc[-1 - self.week_timeline_number * 6])
        self.thursday_checkin_label.setText(self.work_log_data['thu'].iloc[-5 - self.week_timeline_number * 6])
        self.thursday_lunch_checkin_label.setText(self.work_log_data['thu'].iloc[-4 - self.week_timeline_number * 6])
        self.thursday_lunch_checkout_label.setText(self.work_log_data['thu'].iloc[-3 - self.week_timeline_number * 6])
        self.thursday_checkout_label.setText(self.work_log_data['thu'].iloc[-2 - self.week_timeline_number * 6])
        self.thursday_worked_time_label.setText(self.work_log_data['thu'].iloc[-1 - self.week_timeline_number * 6])

    def update_csv_data(self):
        """
        Method
        """
        start_date, end_date = self.calculate_week_range(date.today())
        stored_date = self.work_log_data['data'].iloc[-5]
        print(start_date, stored_date)
        print(start_date == stored_date)
        if self.work_log_data['data'].iloc[-5] != start_date:
            print(type(self.work_log_data['data'].iloc[-5]))
            print(start_date == self.work_log_data['data'].iloc[-5])
            append_csv = self.work_log_data.append(self.week_model_data)
            append_csv['data'].iloc[-5] = start_date
            append_csv['data'].iloc[-4] = end_date
            append_csv.to_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"), index = None)
            self.work_log_data = pandas.read_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"))

    def close_widget(self):
        """
        Method to send the signal to close the worked log widget
        """
        self.close_worked_log_signal.emit(True)

    def update_times(self):
        """
        Method to update the work log times
        """
        self.sunday_checkin_label.setText(self.work_log_data['sun'][0])

    def save_data_file(self):
        """
        Method to save the data on the csv file
        """
        self.work_log_data.to_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"))

    def csv_to_dict(self, csv_file):
        """
        Method to convert the csv file to a dict
        """
        dict_from_csv = {}
        with open(utils.get_absolute_resource_path("resources/dictionaries/{}".format(csv_file))) as data_file:
            for row in data_file:
                row = row.strip().split(',')
                dict_from_csv.setdefault(int(row[0]), {})[int(row[1])] = {row[2] : row[3],
                                                                          row[4] : row[5],
                                                                          row[6] : row[7],
                                                                          row[8] : row[9],
                                                                          row[10] : row[11],
                                                                          row[12] : row[13]}
        return dict_from_csv

    def dict_to_csv(self, dict):
        """
        Method to convert the dict to csv file
        """
