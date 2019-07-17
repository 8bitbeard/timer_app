"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import re
from datetime import date, timedelta

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QCheckBox
from PyQt5.QtCore import QRegExp, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QRegExpValidator

from src.utils import utils


# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class WorkedLogWidget(QWidget):
    """
    Worked log widget
    """

    TIME_BOX_SIZE = QSize(57, 20)

    close_worked_log_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(WorkedLogWidget, self).__init__(parent)

        self.work_log_data = self.csv_to_dict('test_file.csv')

        self.first_log_week = list(self.work_log_data.keys())[0]
        self.last_log_week = list(self.work_log_data.keys())[-1]

        dt = date.today()
        year, self.week, self.dow = dt.isocalendar()

        self.init_user_interface()
        self.update_log_data()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """

        bold_font = QFont()
        bold_font.setBold(True)

        self.week_text_label = QLabel(text='Week:')
        self.week_text_label.setAlignment(Qt.AlignRight)
        # self.week_value_label = QLabel(self.work_log_data['data'].iloc[-5] + '-' + self.work_log_data['data'].iloc[-4])
        # self.week_value_label.setFont(bold_font)
        self.total_week_text_label = QLabel(text='Total Week:')
        self.total_week_text_label.setAlignment(Qt.AlignRight)
        self.total_week_time_value = QLabel()
        self.total_week_time_value.setFont(bold_font)
        self.total_month_text_label = QLabel(text='Total Month:')
        self.total_month_text_label.setAlignment(Qt.AlignRight)
        self.total_month_time_value = QLabel()
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

        self.monday_check_box = QCheckBox(text='Mon')
        self.monday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.monday_check_box.setChecked(self.work_log_data[self.week][1]['work_day'] in 'True')
        self.monday_week_day_label = QLabel(text=self.work_log_data[self.week][1]['day'])
        self.monday_checkin_label = QLineEdit(text=self.work_log_data[self.week][1]['work_in'])
        self.monday_checkin_label.setValidator(worked_time_validator)
        self.monday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.monday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][1]['lunch_in'])
        self.monday_lunch_checkin_label.setValidator(worked_time_validator)
        self.monday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.monday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][1]['lunch_out'])
        self.monday_lunch_checkout_label.setValidator(worked_time_validator)
        self.monday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.monday_checkout_label = QLineEdit(text=self.work_log_data[self.week][1]['work_out'])
        self.monday_checkout_label.setValidator(worked_time_validator)
        self.monday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.monday_worked_time_label = QLabel(text=self.work_log_data[self.week][1]['total_time'])

        self.tuesday_check_box = QCheckBox(text='Tue')
        self.tuesday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.tuesday_check_box.setChecked(self.work_log_data[self.week][2]['work_day'] in 'True')
        self.tuesday_week_day_label = QLabel(text=self.work_log_data[self.week][2]['day'])
        self.tuesday_checkin_label = QLineEdit(text=self.work_log_data[self.week][2]['work_in'])
        self.tuesday_checkin_label.setValidator(worked_time_validator)
        self.tuesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.tuesday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][2]['lunch_in'])
        self.tuesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.tuesday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][2]['lunch_out'])
        self.tuesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.tuesday_checkout_label = QLineEdit(text=self.work_log_data[self.week][2]['work_out'])
        self.tuesday_checkout_label.setValidator(worked_time_validator)
        self.tuesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.tuesday_worked_time_label = QLabel(text=self.work_log_data[self.week][2]['total_time'])

        self.wednesday_check_box = QCheckBox(text='Wed')
        self.wednesday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.wednesday_check_box.setChecked(self.work_log_data[self.week][3]['work_day'] in 'True')
        self.wednesday_week_day_label = QLabel(text=self.work_log_data[self.week][3]['day'])
        self.wednesday_checkin_label = QLineEdit(text=self.work_log_data[self.week][3]['work_in'])
        self.wednesday_checkin_label.setValidator(worked_time_validator)
        self.wednesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.wednesday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][3]['lunch_in'])
        self.wednesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.wednesday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][3]['lunch_out'])
        self.wednesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.wednesday_checkout_label = QLineEdit(text=self.work_log_data[self.week][3]['work_out'])
        self.wednesday_checkout_label.setValidator(worked_time_validator)
        self.wednesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.wednesday_worked_time_label = QLabel(text=self.work_log_data[self.week][3]['total_time'])

        self.thursday_check_box = QCheckBox(text='Thu')
        self.thursday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.thursday_check_box.setChecked(self.work_log_data[self.week][4]['work_day'] in 'True')
        self.thursday_week_day_label = QLabel(text=self.work_log_data[self.week][4]['day'])
        self.thursday_checkin_label = QLineEdit(text=self.work_log_data[self.week][4]['work_in'])
        self.thursday_checkin_label.setValidator(worked_time_validator)
        self.thursday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.thursday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][4]['lunch_in'])
        self.thursday_lunch_checkin_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.thursday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][4]['lunch_out'])
        self.thursday_lunch_checkout_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.thursday_checkout_label = QLineEdit(text=self.work_log_data[self.week][4]['work_out'])
        self.thursday_checkout_label.setValidator(worked_time_validator)
        self.thursday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.thursday_worked_time_label = QLabel(text=self.work_log_data[self.week][4]['total_time'])

        self.friday_check_box = QCheckBox(text='Fri')
        self.friday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.friday_check_box.setChecked(self.work_log_data[self.week][5]['work_day'] in 'True')
        self.friday_week_day_label = QLabel(text=self.work_log_data[self.week][5]['day'])
        self.friday_checkin_label = QLineEdit(text=self.work_log_data[self.week][5]['work_in'])
        self.friday_checkin_label.setValidator(worked_time_validator)
        self.friday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.friday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][5]['lunch_in'])
        self.friday_lunch_checkin_label.setValidator(worked_time_validator)
        self.friday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.friday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][5]['lunch_out'])
        self.friday_lunch_checkout_label.setValidator(worked_time_validator)
        self.friday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.friday_checkout_label = QLineEdit(text=self.work_log_data[self.week][5]['work_out'])
        self.friday_checkout_label.setValidator(worked_time_validator)
        self.friday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.friday_worked_time_label = QLabel(text=self.work_log_data[self.week][5]['total_time'])

        self.saturday_check_box = QCheckBox(text='Sat')
        self.saturday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.saturday_check_box.setChecked(self.work_log_data[self.week][6]['work_day'] in 'True')
        self.saturday_week_day_label = QLabel(text=self.work_log_data[self.week][6]['day'])
        self.saturday_checkin_label = QLineEdit(text=self.work_log_data[self.week][6]['work_in'])
        self.saturday_checkin_label.setValidator(worked_time_validator)
        self.saturday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.saturday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][6]['lunch_in'])
        self.saturday_lunch_checkin_label.setValidator(worked_time_validator)
        self.saturday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.saturday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][6]['lunch_out'])
        self.saturday_lunch_checkout_label.setValidator(worked_time_validator)
        self.saturday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.saturday_checkout_label = QLineEdit(text=self.work_log_data[self.week][6]['work_out'])
        self.saturday_checkout_label.setValidator(worked_time_validator)
        self.saturday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.saturday_worked_time_label = QLabel(text=self.work_log_data[self.week][6]['total_time'])

        self.sunday_check_box = QCheckBox(text='Sun')
        self.sunday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.sunday_check_box.setChecked(self.work_log_data[self.week][7]['work_day'] in 'True')
        self.sunday_week_day_label = QLabel(text=self.work_log_data[self.week][7]['day'])
        self.sunday_checkin_label = QLineEdit(text=self.work_log_data[self.week][7]['work_in'])
        self.sunday_checkin_label.setValidator(worked_time_validator)
        self.sunday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.sunday_lunch_checkin_label = QLineEdit(text=self.work_log_data[self.week][7]['lunch_in'])
        self.sunday_lunch_checkin_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.sunday_lunch_checkout_label = QLineEdit(text=self.work_log_data[self.week][7]['lunch_out'])
        self.sunday_lunch_checkout_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.sunday_checkout_label = QLineEdit(text=self.work_log_data[self.week][7]['work_out'])
        self.sunday_checkout_label.setValidator(worked_time_validator)
        self.sunday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.sunday_worked_time_label = QLabel(text=self.work_log_data[self.week][7]['total_time'])

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

        # self.widget_layout.addWidget(self.week_value_label, 2, 0)
        # self.widget_layout.addWidget(self.checkin_time_text_label, 3, 0)
        # self.widget_layout.addWidget(self.lunch_checkin_time_text_label, 4, 0)
        # self.widget_layout.addWidget(self.lunch_checkout_time_text_label, 5, 0)
        # self.widget_layout.addWidget(self.checkout_time_text_label, 6, 0)
        # self.widget_layout.addWidget(self.day_journey_time_text_label, 7, 0)

        self.widget_layout.addWidget(self.monday_week_day_label, 1 ,0)
        self.widget_layout.addWidget(self.monday_check_box, 2, 0)
        self.widget_layout.addWidget(self.monday_checkin_label, 3, 0)
        self.widget_layout.addWidget(self.monday_lunch_checkin_label, 4, 0)
        self.widget_layout.addWidget(self.monday_lunch_checkout_label, 5, 0)
        self.widget_layout.addWidget(self.monday_checkout_label, 6, 0)
        self.widget_layout.addWidget(self.monday_worked_time_label, 7, 0)

        self.widget_layout.addWidget(self.tuesday_week_day_label, 1, 1)
        self.widget_layout.addWidget(self.tuesday_check_box, 2, 1)
        self.widget_layout.addWidget(self.tuesday_checkin_label, 3, 1)
        self.widget_layout.addWidget(self.tuesday_lunch_checkin_label, 4, 1)
        self.widget_layout.addWidget(self.tuesday_lunch_checkout_label, 5, 1)
        self.widget_layout.addWidget(self.tuesday_checkout_label, 6, 1)
        self.widget_layout.addWidget(self.tuesday_worked_time_label, 7, 1)

        self.widget_layout.addWidget(self.wednesday_week_day_label, 1 ,2)
        self.widget_layout.addWidget(self.wednesday_check_box, 2, 2)
        self.widget_layout.addWidget(self.wednesday_checkin_label, 3, 2)
        self.widget_layout.addWidget(self.wednesday_lunch_checkin_label, 4, 2)
        self.widget_layout.addWidget(self.wednesday_lunch_checkout_label, 5, 2)
        self.widget_layout.addWidget(self.wednesday_checkout_label, 6, 2)
        self.widget_layout.addWidget(self.wednesday_worked_time_label, 7, 2)

        self.widget_layout.addWidget(self.thursday_week_day_label, 1 ,3)
        self.widget_layout.addWidget(self.thursday_check_box, 2, 3)
        self.widget_layout.addWidget(self.thursday_checkin_label, 3, 3)
        self.widget_layout.addWidget(self.thursday_lunch_checkin_label, 4, 3)
        self.widget_layout.addWidget(self.thursday_lunch_checkout_label, 5, 3)
        self.widget_layout.addWidget(self.thursday_checkout_label, 6, 3)
        self.widget_layout.addWidget(self.thursday_worked_time_label, 7, 3)

        self.widget_layout.addWidget(self.friday_week_day_label, 1 ,4)
        self.widget_layout.addWidget(self.friday_check_box, 2, 4)
        self.widget_layout.addWidget(self.friday_checkin_label, 3, 4)
        self.widget_layout.addWidget(self.friday_lunch_checkin_label, 4, 4)
        self.widget_layout.addWidget(self.friday_lunch_checkout_label, 5, 4)
        self.widget_layout.addWidget(self.friday_checkout_label, 6, 4)
        self.widget_layout.addWidget(self.friday_worked_time_label, 7, 4)

        self.widget_layout.addWidget(self.saturday_week_day_label, 1 ,5)
        self.widget_layout.addWidget(self.saturday_check_box, 2, 5)
        self.widget_layout.addWidget(self.saturday_checkin_label, 3, 5)
        self.widget_layout.addWidget(self.saturday_lunch_checkin_label, 4, 5)
        self.widget_layout.addWidget(self.saturday_lunch_checkout_label, 5, 5)
        self.widget_layout.addWidget(self.saturday_checkout_label, 6, 5)
        self.widget_layout.addWidget(self.saturday_worked_time_label, 7, 5)

        self.widget_layout.addWidget(self.sunday_week_day_label, 1 ,6)
        self.widget_layout.addWidget(self.sunday_check_box, 2, 6)
        self.widget_layout.addWidget(self.sunday_checkin_label, 3, 6)
        self.widget_layout.addWidget(self.sunday_lunch_checkin_label, 4, 6)
        self.widget_layout.addWidget(self.sunday_lunch_checkout_label, 5, 6)
        self.widget_layout.addWidget(self.sunday_checkout_label, 6, 6)
        self.widget_layout.addWidget(self.sunday_worked_time_label, 7, 6)

        self.widget_layout.addWidget(self.week_backward_button, 8, 0, 1, 2)
        self.widget_layout.addWidget(self.back_to_main_button, 8, 2, 1, 3)
        self.widget_layout.addWidget(self.week_foward_button, 8, 5, 1, 2)

        self.setLayout(self.widget_layout)

    def update_log_data(self):
        """
        Method to update the
        """
        self.monday_check_box.setChecked(self.work_log_data[self.week][1]['work_day'] in 'True')
        self.monday_week_day_label.setText(self.work_log_data[self.week][1]['day'])
        self.monday_checkin_label.setText(self.work_log_data[self.week][1]['work_in'])
        self.monday_lunch_checkin_label.setText(self.work_log_data[self.week][1]['lunch_in'])
        self.monday_lunch_checkout_label.setText(self.work_log_data[self.week][1]['lunch_out'])
        self.monday_checkout_label.setText(self.work_log_data[self.week][1]['work_out'])
        self.monday_worked_time_label.setText(self.work_log_data[self.week][1]['total_time'])
        self.tuesday_check_box.setChecked(self.work_log_data[self.week][2]['work_day'] in 'True')
        self.tuesday_week_day_label.setText(self.work_log_data[self.week][2]['day'])
        self.tuesday_checkin_label.setText(self.work_log_data[self.week][2]['work_in'])
        self.tuesday_lunch_checkin_label.setText(self.work_log_data[self.week][2]['lunch_in'])
        self.tuesday_lunch_checkout_label.setText(self.work_log_data[self.week][2]['lunch_out'])
        self.tuesday_checkout_label.setText(self.work_log_data[self.week][2]['work_out'])
        self.tuesday_worked_time_label.setText(self.work_log_data[self.week][2]['total_time'])
        self.wednesday_check_box.setChecked(self.work_log_data[self.week][3]['work_day'] in 'True')
        self.wednesday_week_day_label.setText(self.work_log_data[self.week][3]['day'])
        self.wednesday_checkin_label.setText(self.work_log_data[self.week][3]['work_in'])
        self.wednesday_lunch_checkin_label.setText(self.work_log_data[self.week][3]['lunch_in'])
        self.wednesday_lunch_checkout_label.setText(self.work_log_data[self.week][3]['lunch_out'])
        self.wednesday_checkout_label.setText(self.work_log_data[self.week][3]['work_out'])
        self.wednesday_worked_time_label.setText(self.work_log_data[self.week][3]['total_time'])
        self.thursday_check_box.setChecked(self.work_log_data[self.week][4]['work_day'] in 'True')
        self.thursday_week_day_label.setText(self.work_log_data[self.week][4]['day'])
        self.thursday_checkin_label.setText(self.work_log_data[self.week][4]['work_in'])
        self.thursday_lunch_checkin_label.setText(self.work_log_data[self.week][4]['lunch_in'])
        self.thursday_lunch_checkout_label.setText(self.work_log_data[self.week][4]['lunch_out'])
        self.thursday_checkout_label.setText(self.work_log_data[self.week][4]['work_out'])
        self.thursday_worked_time_label.setText(self.work_log_data[self.week][4]['total_time'])
        self.friday_check_box.setChecked(self.work_log_data[self.week][5]['work_day'] in 'True')
        self.friday_week_day_label.setText(self.work_log_data[self.week][5]['day'])
        self.friday_checkin_label.setText(self.work_log_data[self.week][5]['work_in'])
        self.friday_lunch_checkin_label.setText(self.work_log_data[self.week][5]['lunch_in'])
        self.friday_lunch_checkout_label.setText(self.work_log_data[self.week][5]['lunch_out'])
        self.friday_checkout_label.setText(self.work_log_data[self.week][5]['work_out'])
        self.friday_worked_time_label.setText(self.work_log_data[self.week][5]['total_time'])
        self.saturday_check_box.setChecked(self.work_log_data[self.week][6]['work_day'] in 'True')
        self.saturday_week_day_label.setText(self.work_log_data[self.week][6]['day'])
        self.saturday_checkin_label.setText(self.work_log_data[self.week][6]['work_in'])
        self.saturday_lunch_checkin_label.setText(self.work_log_data[self.week][6]['lunch_in'])
        self.saturday_lunch_checkout_label.setText(self.work_log_data[self.week][6]['lunch_out'])
        self.saturday_checkout_label.setText(self.work_log_data[self.week][6]['work_out'])
        self.saturday_worked_time_label.setText(self.work_log_data[self.week][6]['total_time'])
        self.sunday_check_box.setChecked(self.work_log_data[self.week][7]['work_day'] in 'True')
        self.sunday_week_day_label.setText(self.work_log_data[self.week][7]['day'])
        self.sunday_checkin_label.setText(self.work_log_data[self.week][7]['work_in'])
        self.sunday_lunch_checkin_label.setText(self.work_log_data[self.week][7]['lunch_in'])
        self.sunday_lunch_checkout_label.setText(self.work_log_data[self.week][7]['lunch_out'])
        self.sunday_checkout_label.setText(self.work_log_data[self.week][7]['work_out'])
        self.sunday_worked_time_label.setText(self.work_log_data[self.week][7]['total_time'])
        self.calculate_week_total_time(self.week)

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
                # self.calculate_week_total_time()

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
                # self.calculate_week_total_time()

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
                # self.calculate_week_total_time()

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
                # self.calculate_week_total_time()

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
                # self.calculate_week_total_time()

    def calculate_week_total_time(self, week_no):
        """
        Method to calculate the total time worked on the week
        """
        total = utils.sum_times(self.work_log_data[week_no][1]['total_time'],
                                self.work_log_data[week_no][2]['total_time'],
                                self.work_log_data[week_no][3]['total_time'],
                                self.work_log_data[week_no][4]['total_time'],
                                self.work_log_data[week_no][5]['total_time'],
                                self.work_log_data[week_no][6]['total_time'],
                                self.work_log_data[week_no][7]['total_time'])
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
            if self.week < self.last_log_week:
                self.week += 1
        else:
            if self.week > self.first_log_week:
                self.week -= 1
        self.update_log_data()

    def close_widget(self):
        """
        Method to send the signal to close the worked log widget
        """
        self.close_worked_log_signal.emit(True)

    def csv_to_dict(self, csv_file):
        """
        Method to convert the csv file to a dict
        """
        dict_from_csv = {}
        with open(utils.get_absolute_resource_path("resources/dictionaries/{}".format(csv_file))) as data_file:
            for row in data_file:
                row = row.strip().split(',')
                dict_from_csv.setdefault(int(row[0]), {})[int(row[1])] = {row[2] : row[3], row[4] : row[5],
                                                                          row[6] : row[7], row[8] : row[9],
                                                                          row[10] : row[11], row[12] : row[13],
                                                                          row[14] : row[15]}
        return dict_from_csv

    def dict_to_csv(self, dict):
        """
        Method to convert the dict to csv file
        """
