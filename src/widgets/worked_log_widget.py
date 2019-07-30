"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import re
from datetime import date

import pandas

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

        self.work_log_data = pandas.read_csv(utils.get_absolute_resource_path("resources/csv_data/log_data.csv"))

        self.total_work_days = utils.count_csv_values_from(self.work_log_data, 'work_day', True)
        self.total_workable_time = utils.mult_time('08:00', self.total_work_days)
        self.total_worked_time = utils.get_total_time_from(self.work_log_data)

        self.value_hours_bank = utils.sub_times(self.total_worked_time, self.total_workable_time)

        self.first_log_week = self.work_log_data.iloc[0]['week']
        self.last_log_week = self.work_log_data.iloc[-1]['week']

        actual_day = date.today()
        self.month = actual_day.month
        self.day = actual_day.day
        self.year, self.week, self.day_of_week = actual_day.isocalendar()

        self.get_week_and_month_data()
        self.init_user_interface()
        self.check_work_time_status()
        # self.check_interjourney_frames_status()
        self.update_log_data()

    def get_week_and_month_data(self):
        """
        Method to create the week and month datastructure from the data_log csv file
        """
        self.current_week_log_data = utils.get_current_week_data(self.work_log_data, self.week)
        self.current_month_log_data = utils.get_current_month_data(self.work_log_data, self.month)
        self.total_month_time = utils.get_total_time_from(self.work_log_data, month=self.month)

    def init_user_interface(self):
        """
        Method to initiate all the widgets and assign their first data
        """

        bold_font = QFont()
        bold_font.setBold(True)

        self.total_week_text_label = QLabel(text='Total Week:')
        self.total_week_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_week_time_value = QLabel()
        self.total_week_time_value.setFont(bold_font)
        self.hours_bank_text_label = QLabel(text='Hours bank:')
        self.hours_bank_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.hours_bank_value_label = QLabel(self.total_month_time)
        self.hours_bank_value_label.setFont(bold_font)

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
        self.monday_check_box.setChecked(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_check_box.stateChanged.connect(self.monday_checkbox_status_change)
        self.monday_week_day_label = QLabel(text=self.current_week_log_data.iloc[0]['day'])
        self.monday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[0]['work_in'])
        self.monday_checkin_label.setValidator(worked_time_validator)
        self.monday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkin_label.setEnabled(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[0]['lunch_in'])
        self.monday_lunch_checkin_label.setValidator(worked_time_validator)
        self.monday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_lunch_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[0]['lunch_out'])
        self.monday_lunch_checkout_label.setValidator(worked_time_validator)
        self.monday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_lunch_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[0]['work_out'])
        self.monday_checkout_label.setValidator(worked_time_validator)
        self.monday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkout_label.setEnabled(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[0]['total_time'])
        self.monday_worked_time_label.setFont(bold_font)
        self.monday_morning_interjourney_status = QFrame()
        self.monday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.monday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.monday_morning_interjourney_status.setToolTip('Interjourney Ok: 03:00h')
        self.monday_afternoon_interjourney_status = QFrame()
        self.monday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.monday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.monday_lunch_interjourney_status = QFrame()
        self.monday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.monday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.tuesday_check_box = QCheckBox(text='Tue')
        self.tuesday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.tuesday_check_box.setChecked(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_check_box.stateChanged.connect(self.tuesday_checkbox_status_change)
        self.tuesday_week_day_label = QLabel(text=self.current_week_log_data.iloc[1]['day'])
        self.tuesday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[1]['work_in'])
        self.tuesday_checkin_label.setValidator(worked_time_validator)
        self.tuesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkin_label.setEnabled(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[1]['lunch_in'])
        self.tuesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_lunch_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[1]['lunch_out'])
        self.tuesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.tuesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_lunch_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[1]['work_out'])
        self.tuesday_checkout_label.setValidator(worked_time_validator)
        self.tuesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkout_label.setEnabled(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[1]['total_time'])
        self.tuesday_worked_time_label.setFont(bold_font)
        self.tuesday_morning_interjourney_status = QFrame()
        self.tuesday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.tuesday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.tuesday_afternoon_interjourney_status = QFrame()
        self.tuesday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.tuesday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.tuesday_lunch_interjourney_status = QFrame()
        self.tuesday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.tuesday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")


        self.wednesday_check_box = QCheckBox(text='Wed')
        self.wednesday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.wednesday_check_box.setChecked(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_check_box.stateChanged.connect(self.wednesday_checkbox_status_change)
        self.wednesday_week_day_label = QLabel(text=self.current_week_log_data.iloc[2]['day'])
        self.wednesday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[2]['work_in'])
        self.wednesday_checkin_label.setValidator(worked_time_validator)
        self.wednesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkin_label.setEnabled(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[2]['lunch_in'])
        self.wednesday_lunch_checkin_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_lunch_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[2]['lunch_out'])
        self.wednesday_lunch_checkout_label.setValidator(worked_time_validator)
        self.wednesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_lunch_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[2]['work_out'])
        self.wednesday_checkout_label.setValidator(worked_time_validator)
        self.wednesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkout_label.setEnabled(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[2]['total_time'])
        self.wednesday_worked_time_label.setFont(bold_font)
        self.wednesday_morning_interjourney_status = QFrame()
        self.wednesday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.wednesday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.wednesday_afternoon_interjourney_status = QFrame()
        self.wednesday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.wednesday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.wednesday_lunch_interjourney_status = QFrame()
        self.wednesday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.wednesday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.thursday_check_box = QCheckBox(text='Thu')
        self.thursday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.thursday_check_box.setChecked(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_check_box.stateChanged.connect(self.thursday_checkbox_status_change)
        self.thursday_week_day_label = QLabel(text=self.current_week_log_data.iloc[3]['day'])
        self.thursday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[3]['work_in'])
        self.thursday_checkin_label.setValidator(worked_time_validator)
        self.thursday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkin_label.setEnabled(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[3]['lunch_in'])
        self.thursday_lunch_checkin_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[3]['lunch_out'])
        self.thursday_lunch_checkout_label.setValidator(worked_time_validator)
        self.thursday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[3]['work_out'])
        self.thursday_checkout_label.setValidator(worked_time_validator)
        self.thursday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkout_label.setEnabled(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[3]['total_time'])
        self.thursday_worked_time_label.setFont(bold_font)
        self.thursday_morning_interjourney_status = QFrame()
        self.thursday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.thursday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.thursday_afternoon_interjourney_status = QFrame()
        self.thursday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.thursday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.thursday_lunch_interjourney_status = QFrame()
        self.thursday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.thursday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.friday_check_box = QCheckBox(text='Fri')
        self.friday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.friday_check_box.setChecked(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_check_box.stateChanged.connect(self.friday_checkbox_status_change)
        self.friday_week_day_label = QLabel(text=self.current_week_log_data.iloc[4]['day'])
        self.friday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[4]['work_in'])
        self.friday_checkin_label.setValidator(worked_time_validator)
        self.friday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_checkin_label.setEnabled(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_checkin_label.textChanged.connect(self.calculate_friday_total_time)
        self.friday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[4]['lunch_in'])
        self.friday_lunch_checkin_label.setValidator(worked_time_validator)
        self.friday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_lunch_checkin_label.textChanged.connect(self.calculate_friday_total_time)
        self.friday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[4]['lunch_out'])
        self.friday_lunch_checkout_label.setValidator(worked_time_validator)
        self.friday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_lunch_checkout_label.textChanged.connect(self.calculate_friday_total_time)
        self.friday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[4]['work_out'])
        self.friday_checkout_label.setValidator(worked_time_validator)
        self.friday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.friday_checkout_label.setEnabled(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_checkout_label.textChanged.connect(self.calculate_friday_total_time)
        self.friday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[4]['total_time'])
        self.friday_worked_time_label.setFont(bold_font)
        self.friday_morning_interjourney_status = QFrame()
        self.friday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.friday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.friday_afternoon_interjourney_status = QFrame()
        self.friday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.friday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.friday_lunch_interjourney_status = QFrame()
        self.friday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.friday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.saturday_check_box = QCheckBox(text='Sat')
        self.saturday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.saturday_check_box.setChecked(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_check_box.stateChanged.connect(self.saturday_checkbox_status_change)
        self.saturday_week_day_label = QLabel(text=self.current_week_log_data.iloc[5]['day'])
        self.saturday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[5]['work_in'])
        self.saturday_checkin_label.setValidator(worked_time_validator)
        self.saturday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_checkin_label.setEnabled(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_checkin_label.textChanged.connect(self.calculate_saturday_total_time)
        self.saturday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[5]['lunch_in'])
        self.saturday_lunch_checkin_label.setValidator(worked_time_validator)
        self.saturday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_lunch_checkin_label.textChanged.connect(self.calculate_saturday_total_time)
        self.saturday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[5]['lunch_out'])
        self.saturday_lunch_checkout_label.setValidator(worked_time_validator)
        self.saturday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_lunch_checkout_label.textChanged.connect(self.calculate_saturday_total_time)
        self.saturday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[5]['work_out'])
        self.saturday_checkout_label.setValidator(worked_time_validator)
        self.saturday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.saturday_checkout_label.setEnabled(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_checkout_label.textChanged.connect(self.calculate_saturday_total_time)
        self.saturday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[5]['total_time'])
        self.saturday_worked_time_label.setFont(bold_font)
        self.saturday_morning_interjourney_status = QFrame()
        self.saturday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.saturday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.saturday_afternoon_interjourney_status = QFrame()
        self.saturday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.saturday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.saturday_lunch_interjourney_status = QFrame()
        self.saturday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.saturday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.sunday_check_box = QCheckBox(text='Sun')
        self.sunday_check_box.setLayoutDirection(Qt.LeftToRight)
        self.sunday_check_box.setChecked(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_check_box.stateChanged.connect(self.sunday_checkbox_status_change)
        self.sunday_week_day_label = QLabel(text=self.current_week_log_data.iloc[6]['day'])
        self.sunday_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[6]['work_in'])
        self.sunday_checkin_label.setValidator(worked_time_validator)
        self.sunday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkin_label.setEnabled(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkin_label = QLineEdit(text=self.current_week_log_data.iloc[6]['lunch_in'])
        self.sunday_lunch_checkin_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkin_label.setEnabled(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_lunch_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[6]['lunch_out'])
        self.sunday_lunch_checkout_label.setValidator(worked_time_validator)
        self.sunday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkout_label.setEnabled(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_lunch_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_checkout_label = QLineEdit(text=self.current_week_log_data.iloc[6]['work_out'])
        self.sunday_checkout_label.setValidator(worked_time_validator)
        self.sunday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkout_label.setEnabled(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_worked_time_label = QLabel(text=self.current_week_log_data.iloc[6]['total_time'])
        self.sunday_worked_time_label.setFont(bold_font)
        self.sunday_morning_interjourney_status = QFrame()
        self.sunday_morning_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sunday_morning_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.sunday_afternoon_interjourney_status = QFrame()
        self.sunday_afternoon_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sunday_afternoon_interjourney_status.setStyleSheet("QWidget { background-color: green}")
        self.sunday_lunch_interjourney_status = QFrame()
        self.sunday_lunch_interjourney_status.setFixedSize(self.COLOR_FRAME_SIZE)
        self.sunday_lunch_interjourney_status.setStyleSheet("QWidget { background-color: green}")

        self.week_backward_button = QPushButton('<<', self)
        self.week_backward_button.clicked.connect(lambda: self.change_week_display(False))
        self.week_foward_button = QPushButton('>>', self)
        self.week_foward_button.clicked.connect(lambda: self.change_week_display(True))
        self.back_to_main_button = QPushButton('Go back', self)
        self.back_to_main_button.clicked.connect(self.close_widget)

        self.widget_layout = QGridLayout()

        self.widget_layout.addWidget(self.total_week_text_label, 0, 0, 1, 2)
        self.widget_layout.addWidget(self.total_week_time_value, 0, 2)
        self.widget_layout.addWidget(self.hours_bank_text_label, 0, 3, 1, 2)
        self.widget_layout.addWidget(self.hours_bank_value_label, 0, 5)

        self.widget_layout.addWidget(self.monday_week_day_label, 1, 0)
        self.widget_layout.addWidget(self.monday_check_box, 2, 0)
        self.widget_layout.addWidget(self.monday_checkin_label, 3, 0)
        self.widget_layout.addWidget(self.monday_morning_interjourney_status, 4, 0)
        self.widget_layout.addWidget(self.monday_lunch_checkin_label, 5, 0)
        self.widget_layout.addWidget(self.monday_lunch_interjourney_status, 6, 0)
        self.widget_layout.addWidget(self.monday_lunch_checkout_label, 7, 0)
        self.widget_layout.addWidget(self.monday_afternoon_interjourney_status, 8, 0)
        self.widget_layout.addWidget(self.monday_checkout_label, 9, 0)
        self.widget_layout.addWidget(self.monday_worked_time_label, 10, 0)

        self.widget_layout.addWidget(self.tuesday_week_day_label, 1, 1)
        self.widget_layout.addWidget(self.tuesday_check_box, 2, 1)
        self.widget_layout.addWidget(self.tuesday_checkin_label, 3, 1)
        self.widget_layout.addWidget(self.tuesday_morning_interjourney_status, 4, 1)
        self.widget_layout.addWidget(self.tuesday_lunch_checkin_label, 5, 1)
        self.widget_layout.addWidget(self.tuesday_lunch_interjourney_status, 6, 1)
        self.widget_layout.addWidget(self.tuesday_lunch_checkout_label, 7, 1)
        self.widget_layout.addWidget(self.tuesday_afternoon_interjourney_status, 8, 1)
        self.widget_layout.addWidget(self.tuesday_checkout_label, 9, 1)
        self.widget_layout.addWidget(self.tuesday_worked_time_label, 10, 1)

        self.widget_layout.addWidget(self.wednesday_week_day_label, 1, 2)
        self.widget_layout.addWidget(self.wednesday_check_box, 2, 2)
        self.widget_layout.addWidget(self.wednesday_checkin_label, 3, 2)
        self.widget_layout.addWidget(self.wednesday_morning_interjourney_status, 4, 2)
        self.widget_layout.addWidget(self.wednesday_lunch_checkin_label, 5, 2)
        self.widget_layout.addWidget(self.wednesday_lunch_interjourney_status, 6, 2)
        self.widget_layout.addWidget(self.wednesday_lunch_checkout_label, 7, 2)
        self.widget_layout.addWidget(self.wednesday_afternoon_interjourney_status, 8, 2)
        self.widget_layout.addWidget(self.wednesday_checkout_label, 9, 2)
        self.widget_layout.addWidget(self.wednesday_worked_time_label, 10, 2)

        self.widget_layout.addWidget(self.thursday_week_day_label, 1, 3)
        self.widget_layout.addWidget(self.thursday_check_box, 2, 3)
        self.widget_layout.addWidget(self.thursday_checkin_label, 3, 3)
        self.widget_layout.addWidget(self.thursday_morning_interjourney_status, 4, 3)
        self.widget_layout.addWidget(self.thursday_lunch_checkin_label, 5, 3)
        self.widget_layout.addWidget(self.thursday_lunch_interjourney_status, 6, 3)
        self.widget_layout.addWidget(self.thursday_lunch_checkout_label, 7, 3)
        self.widget_layout.addWidget(self.thursday_afternoon_interjourney_status, 8, 3)
        self.widget_layout.addWidget(self.thursday_checkout_label, 9, 3)
        self.widget_layout.addWidget(self.thursday_worked_time_label, 10, 3)

        self.widget_layout.addWidget(self.friday_week_day_label, 1, 4)
        self.widget_layout.addWidget(self.friday_check_box, 2, 4)
        self.widget_layout.addWidget(self.friday_checkin_label, 3, 4)
        self.widget_layout.addWidget(self.friday_morning_interjourney_status, 4, 4)
        self.widget_layout.addWidget(self.friday_lunch_checkin_label, 5, 4)
        self.widget_layout.addWidget(self.friday_lunch_interjourney_status, 6, 4)
        self.widget_layout.addWidget(self.friday_lunch_checkout_label, 7, 4)
        self.widget_layout.addWidget(self.friday_afternoon_interjourney_status, 8, 4)
        self.widget_layout.addWidget(self.friday_checkout_label, 9, 4)
        self.widget_layout.addWidget(self.friday_worked_time_label, 10, 4)

        self.widget_layout.addWidget(self.saturday_week_day_label, 1, 5)
        self.widget_layout.addWidget(self.saturday_check_box, 2, 5)
        self.widget_layout.addWidget(self.saturday_checkin_label, 3, 5)
        self.widget_layout.addWidget(self.saturday_morning_interjourney_status, 4, 5)
        self.widget_layout.addWidget(self.saturday_lunch_checkin_label, 5, 5)
        self.widget_layout.addWidget(self.saturday_lunch_interjourney_status, 6, 5)
        self.widget_layout.addWidget(self.saturday_lunch_checkout_label, 7, 5)
        self.widget_layout.addWidget(self.saturday_afternoon_interjourney_status, 8, 5)
        self.widget_layout.addWidget(self.saturday_checkout_label, 9, 5)
        self.widget_layout.addWidget(self.saturday_worked_time_label, 10, 5)

        self.widget_layout.addWidget(self.sunday_week_day_label, 1, 6)
        self.widget_layout.addWidget(self.sunday_check_box, 2, 6)
        self.widget_layout.addWidget(self.sunday_checkin_label, 3, 6)
        self.widget_layout.addWidget(self.sunday_morning_interjourney_status, 4, 6)
        self.widget_layout.addWidget(self.sunday_lunch_checkin_label, 5, 6)
        self.widget_layout.addWidget(self.sunday_lunch_interjourney_status, 6, 6)
        self.widget_layout.addWidget(self.sunday_lunch_checkout_label, 7, 6)
        self.widget_layout.addWidget(self.sunday_afternoon_interjourney_status, 8, 6)
        self.widget_layout.addWidget(self.sunday_checkout_label, 9, 6)
        self.widget_layout.addWidget(self.sunday_worked_time_label, 10, 6)

        self.widget_layout.addWidget(self.week_backward_button, 11, 0, 1, 2)
        self.widget_layout.addWidget(self.back_to_main_button, 11, 2, 1, 3)
        self.widget_layout.addWidget(self.week_foward_button, 11, 5, 1, 2)

        self.setLayout(self.widget_layout)

    def update_log_data(self):
        """
        Method to update the
        """
        self.current_week_log_data = utils.get_current_week_data(self.work_log_data, self.week)
        self.hours_bank_value_label.setText(self.total_month_time)
        self.monday_check_box.setChecked(self.current_week_log_data.iloc[0]['work_day'])
        self.monday_week_day_label.setText(self.current_week_log_data.iloc[0]['day'])
        self.monday_checkin_label.setText(self.current_week_log_data.iloc[0]['work_in'])
        self.monday_lunch_checkin_label.setText(self.current_week_log_data.iloc[0]['lunch_in'])
        self.monday_lunch_checkout_label.setText(self.current_week_log_data.iloc[0]['lunch_out'])
        self.monday_checkout_label.setText(self.current_week_log_data.iloc[0]['work_out'])
        self.monday_worked_time_label.setText(self.current_week_log_data.iloc[0]['total_time'])
        self.tuesday_check_box.setChecked(self.current_week_log_data.iloc[1]['work_day'])
        self.tuesday_week_day_label.setText(self.current_week_log_data.iloc[1]['day'])
        self.tuesday_checkin_label.setText(self.current_week_log_data.iloc[1]['work_in'])
        self.tuesday_lunch_checkin_label.setText(self.current_week_log_data.iloc[1]['lunch_in'])
        self.tuesday_lunch_checkout_label.setText(self.current_week_log_data.iloc[1]['lunch_out'])
        self.tuesday_checkout_label.setText(self.current_week_log_data.iloc[1]['work_out'])
        self.tuesday_worked_time_label.setText(self.current_week_log_data.iloc[1]['total_time'])
        self.wednesday_check_box.setChecked(self.current_week_log_data.iloc[2]['work_day'])
        self.wednesday_week_day_label.setText(self.current_week_log_data.iloc[2]['day'])
        self.wednesday_checkin_label.setText(self.current_week_log_data.iloc[2]['work_in'])
        self.wednesday_lunch_checkin_label.setText(self.current_week_log_data.iloc[2]['lunch_in'])
        self.wednesday_lunch_checkout_label.setText(self.current_week_log_data.iloc[2]['lunch_out'])
        self.wednesday_checkout_label.setText(self.current_week_log_data.iloc[2]['work_out'])
        self.wednesday_worked_time_label.setText(self.current_week_log_data.iloc[2]['total_time'])
        self.thursday_check_box.setChecked(self.current_week_log_data.iloc[3]['work_day'])
        self.thursday_week_day_label.setText(self.current_week_log_data.iloc[3]['day'])
        self.thursday_checkin_label.setText(self.current_week_log_data.iloc[3]['work_in'])
        self.thursday_lunch_checkin_label.setText(self.current_week_log_data.iloc[3]['lunch_in'])
        self.thursday_lunch_checkout_label.setText(self.current_week_log_data.iloc[3]['lunch_out'])
        self.thursday_checkout_label.setText(self.current_week_log_data.iloc[3]['work_out'])
        self.thursday_worked_time_label.setText(self.current_week_log_data.iloc[3]['total_time'])
        self.friday_check_box.setChecked(self.current_week_log_data.iloc[4]['work_day'])
        self.friday_week_day_label.setText(self.current_week_log_data.iloc[4]['day'])
        self.friday_checkin_label.setText(self.current_week_log_data.iloc[4]['work_in'])
        self.friday_lunch_checkin_label.setText(self.current_week_log_data.iloc[4]['lunch_in'])
        self.friday_lunch_checkout_label.setText(self.current_week_log_data.iloc[4]['lunch_out'])
        self.friday_checkout_label.setText(self.current_week_log_data.iloc[4]['work_out'])
        self.friday_worked_time_label.setText(self.current_week_log_data.iloc[4]['total_time'])
        self.saturday_check_box.setChecked(self.current_week_log_data.iloc[5]['work_day'])
        self.saturday_week_day_label.setText(self.current_week_log_data.iloc[5]['day'])
        self.saturday_checkin_label.setText(self.current_week_log_data.iloc[5]['work_in'])
        self.saturday_lunch_checkin_label.setText(self.current_week_log_data.iloc[5]['lunch_in'])
        self.saturday_lunch_checkout_label.setText(self.current_week_log_data.iloc[5]['lunch_out'])
        self.saturday_checkout_label.setText(self.current_week_log_data.iloc[5]['work_out'])
        self.saturday_worked_time_label.setText(self.current_week_log_data.iloc[5]['total_time'])
        self.sunday_check_box.setChecked(self.current_week_log_data.iloc[6]['work_day'])
        self.sunday_week_day_label.setText(self.current_week_log_data.iloc[6]['day'])
        self.sunday_checkin_label.setText(self.current_week_log_data.iloc[6]['work_in'])
        self.sunday_lunch_checkin_label.setText(self.current_week_log_data.iloc[6]['lunch_in'])
        self.sunday_lunch_checkout_label.setText(self.current_week_log_data.iloc[6]['lunch_out'])
        self.sunday_checkout_label.setText(self.current_week_log_data.iloc[6]['work_out'])
        self.sunday_worked_time_label.setText(self.current_week_log_data.iloc[6]['total_time'])
        self.calculate_week_total_time()
        self.calculate_month_total_time()

    def check_interjourney_frames_status(self, dow, value):
        """
        temp
        """
        list_of_frames = [[self.monday_morning_interjourney_status, self.monday_lunch_interjourney_status,
                           self.monday_afternoon_interjourney_status],
                          [self.tuesday_morning_interjourney_status, self.tuesday_lunch_interjourney_status,
                           self.tuesday_afternoon_interjourney_status],
                          [self.wednesday_morning_interjourney_status, self.wednesday_lunch_interjourney_status,
                           self.wednesday_afternoon_interjourney_status],
                          [self.thursday_morning_interjourney_status, self.thursday_lunch_interjourney_status,
                           self.thursday_afternoon_interjourney_status],
                          [self.friday_morning_interjourney_status, self.friday_lunch_interjourney_status,
                           self.friday_afternoon_interjourney_status],
                          [self.saturday_morning_interjourney_status, self.saturday_lunch_interjourney_status,
                           self.saturday_afternoon_interjourney_status],
                          [self.sunday_morning_interjourney_status, self.sunday_lunch_interjourney_status,
                           self.sunday_afternoon_interjourney_status]]
        if value:
            sts = self.calculate_interjouney_status(dow)
            print(sts)
            list_of_frames[dow][0].setStyleSheet("QWidget { background-color: " + ('green' if sts[0] else 'red') +" }")
            list_of_frames[dow][1].setStyleSheet("QWidget { background-color: " + ('green' if sts[1] else 'red') +" }")
            list_of_frames[dow][2].setStyleSheet("QWidget { background-color: " + ('green' if sts[2] else 'red') +" }")
        else:
            list_of_frames[dow][0].setStyleSheet("QWidget { background-color: gray}")
            list_of_frames[dow][1].setStyleSheet("QWidget { background-color: gray}")
            list_of_frames[dow][2].setStyleSheet("QWidget { background-color: gray}")

    def calculate_interjouney_status(self, dow):
        """
        Temp
        """
        index_list = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()
        data = self.work_log_data
        morning_journey = utils.sub_times(data.iloc[index_list[dow]]['work_in'], data.iloc[index_list[dow]]['lunch_in'])
        lunch_journey = utils.sub_times(data.iloc[dow]['lunch_in'], data.iloc[dow]['lunch_out'])
        afternoon_journey = utils.sub_times(data.iloc[dow]['lunch_out'], data.iloc[dow]['work_out'])
        morning_status = utils.change_to_minutes(morning_journey) < 301
        lunch_status = utils.change_to_minutes(lunch_journey) < 121
        afternoon_status = utils.change_to_minutes(afternoon_journey) < 301
        return (morning_status, lunch_status, afternoon_status)

    def monday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.monday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=0, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[0]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.monday_checkin_label.setEnabled(bool(value))
        self.monday_lunch_checkin_label.setEnabled(bool(value))
        self.monday_lunch_checkout_label.setEnabled(bool(value))
        self.monday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def tuesday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.tuesday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=1, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[1]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.tuesday_checkin_label.setEnabled(bool(value))
        self.tuesday_lunch_checkin_label.setEnabled(bool(value))
        self.tuesday_lunch_checkout_label.setEnabled(bool(value))
        self.tuesday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def wednesday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.wednesday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=2, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[2]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.wednesday_checkin_label.setEnabled(bool(value))
        self.wednesday_lunch_checkin_label.setEnabled(bool(value))
        self.wednesday_lunch_checkout_label.setEnabled(bool(value))
        self.wednesday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def thursday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.friday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=3, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[3]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.thursday_checkin_label.setEnabled(bool(value))
        self.thursday_lunch_checkin_label.setEnabled(bool(value))
        self.thursday_lunch_checkout_label.setEnabled(bool(value))
        self.thursday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def friday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.friday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=4, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[4]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.friday_checkin_label.setEnabled(bool(value))
        self.friday_lunch_checkin_label.setEnabled(bool(value))
        self.friday_lunch_checkout_label.setEnabled(bool(value))
        self.friday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def saturday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.friday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=5, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[5]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.saturday_checkin_label.setEnabled(bool(value))
        self.saturday_lunch_checkin_label.setEnabled(bool(value))
        self.saturday_lunch_checkout_label.setEnabled(bool(value))
        self.saturday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def sunday_checkbox_status_change(self, value):
        """
        Temp
        """
        if not value:
            self.friday_worked_time_label.setStyleSheet('color: black')
        self.check_interjourney_frames_status(dow=6, value=value)
        index = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()[6]
        self.work_log_data.at[index, 'work_day'] = bool(value)
        self.sunday_checkin_label.setEnabled(bool(value))
        self.sunday_lunch_checkin_label.setEnabled(bool(value))
        self.sunday_lunch_checkout_label.setEnabled(bool(value))
        self.sunday_checkout_label.setEnabled(bool(value))
        self.check_work_time_status()
        self.update_csv_data()

    def update_csv_data(self):
        """
        Method to update the csv stored data
        """
        index_list = self.work_log_data.index[self.work_log_data['week'] == self.week].tolist()
        self.work_log_data.at[index_list[0], 'work_day'] = bool(self.monday_check_box.isChecked())
        self.work_log_data.at[index_list[0], 'work_in'] = self.monday_checkin_label.text()
        self.work_log_data.at[index_list[0], 'lunch_in'] = self.monday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[0], 'lunch_out'] = self.monday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[0], 'work_out'] = self.monday_checkout_label.text()
        self.work_log_data.at[index_list[0], 'total_time'] = self.monday_worked_time_label.text()

        self.work_log_data.at[index_list[1], 'work_day'] = bool(self.tuesday_check_box.isChecked())
        self.work_log_data.at[index_list[1], 'work_in'] = self.tuesday_checkin_label.text()
        self.work_log_data.at[index_list[1], 'lunch_in'] = self.tuesday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[1], 'lunch_out'] = self.tuesday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[1], 'work_out'] = self.tuesday_checkout_label.text()
        self.work_log_data.at[index_list[1], 'total_time'] = self.tuesday_worked_time_label.text()

        self.work_log_data.at[index_list[2], 'work_day'] = bool(self.wednesday_check_box.isChecked())
        self.work_log_data.at[index_list[2], 'work_in'] = self.wednesday_checkin_label.text()
        self.work_log_data.at[index_list[2], 'lunch_in'] = self.wednesday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[2], 'lunch_out'] = self.wednesday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[2], 'work_out'] = self.wednesday_checkout_label.text()
        self.work_log_data.at[index_list[2], 'total_time'] = self.wednesday_worked_time_label.text()

        self.work_log_data.at[index_list[3], 'work_day'] = bool(self.thursday_check_box.isChecked())
        self.work_log_data.at[index_list[3], 'work_in'] = self.thursday_checkin_label.text()
        self.work_log_data.at[index_list[3], 'lunch_in'] = self.thursday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[3], 'lunch_out'] = self.thursday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[3], 'work_out'] = self.thursday_checkout_label.text()
        self.work_log_data.at[index_list[3], 'total_time'] = self.thursday_worked_time_label.text()

        self.work_log_data.at[index_list[4], 'work_day'] = bool(self.friday_check_box.isChecked())
        self.work_log_data.at[index_list[4], 'work_in'] = self.friday_checkin_label.text()
        self.work_log_data.at[index_list[4], 'lunch_in'] = self.friday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[4], 'lunch_out'] = self.friday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[4], 'work_out'] = self.friday_checkout_label.text()
        self.work_log_data.at[index_list[4], 'total_time'] = self.friday_worked_time_label.text()

        self.work_log_data.at[index_list[5], 'work_day'] = bool(self.saturday_check_box.isChecked())
        self.work_log_data.at[index_list[5], 'work_in'] = self.saturday_checkin_label.text()
        self.work_log_data.at[index_list[5], 'lunch_in'] = self.saturday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[5], 'lunch_out'] = self.saturday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[5], 'work_out'] = self.saturday_checkout_label.text()
        self.work_log_data.at[index_list[5], 'total_time'] = self.saturday_worked_time_label.text()

        self.work_log_data.at[index_list[6], 'work_day'] = bool(self.sunday_check_box.isChecked())
        self.work_log_data.at[index_list[6], 'work_in'] = self.sunday_checkin_label.text()
        self.work_log_data.at[index_list[6], 'lunch_in'] = self.sunday_lunch_checkin_label.text()
        self.work_log_data.at[index_list[6], 'lunch_out'] = self.sunday_lunch_checkout_label.text()
        self.work_log_data.at[index_list[6], 'work_out'] = self.sunday_checkout_label.text()
        self.work_log_data.at[index_list[6], 'total_time'] = self.sunday_worked_time_label.text()

        self.work_log_data.to_csv(utils.get_absolute_resource_path("resources/csv_data/log_data.csv"), index=False)

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
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=0, value=True)
                self.update_csv_data()

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
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=1, value=True)
                self.update_csv_data()

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
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=2, value=True)
                self.update_csv_data()

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
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=3, value=True)
                self.update_csv_data()

    def calculate_friday_total_time(self, text):
        """
        Method to calculate the total worked time on friday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.friday_checkin_label.text(),
                                            self.friday_lunch_checkin_label.text(),
                                            self.friday_lunch_checkout_label.text(),
                                            self.friday_checkout_label.text())
            if '-' not in total:
                self.friday_worked_time_label.setText(total)
                self.calculate_week_total_time()
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=4, value=True)
                self.update_csv_data()

    def calculate_saturday_total_time(self, text):
        """
        Method to calculate the total worked time on sunday
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        if regex.match(text):
            total = utils.total_worked_time(self.saturday_checkin_label.text(),
                                            self.saturday_lunch_checkin_label.text(),
                                            self.saturday_lunch_checkout_label.text(),
                                            self.saturday_checkout_label.text())
            if '-' not in total:
                self.saturday_worked_time_label.setText(total)
                self.calculate_week_total_time()
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=5, value=True)
                self.update_csv_data()

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
                self.check_work_time_status()
                self.check_interjourney_frames_status(dow=6, value=True)
                self.update_csv_data()

    def check_work_time_status(self):
        """
        Method to check the total work time status from all week days
        """
        list_of_times = [self.monday_worked_time_label, self.tuesday_worked_time_label,
                         self.wednesday_worked_time_label, self.thursday_worked_time_label,
                         self.friday_worked_time_label, self.saturday_worked_time_label,
                         self.sunday_worked_time_label]
        list_of_checkboxes = [self.monday_check_box, self.tuesday_check_box, self.wednesday_check_box,
                              self.thursday_check_box, self.friday_check_box, self.saturday_check_box,
                              self.sunday_check_box]
        for time in list_of_times:
            if list_of_checkboxes[list_of_times.index(time)].isChecked():
                time_in_minutes = utils.change_to_minutes(time.text())
                if 300 < time_in_minutes < 480:
                    time.setStyleSheet('color: orange')
                elif time_in_minutes == 480:
                    time.setStyleSheet('color: green')
                elif 600 > time_in_minutes > 480:
                    time.setStyleSheet('color: blue')
                else:
                    time.setStyleSheet('color: red')
            else:
                time.setStyleSheet('color: gray')

    def calculate_week_total_time(self):
        """
        Method to calculate the total time worked on the week
        """
        total_week_time = utils.get_total_time_from(self.work_log_data, week=self.week)
        self.total_week_time_value.setText(total_week_time)

    def calculate_month_total_time(self):
        """
        Method to calculate the total time worked on the month
        """
        total_month_time = utils.get_total_time_from(self.work_log_data, month=self.month)
        self.hours_bank_value_label.setText(total_month_time)

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
        self.month = utils.get_month_from_week(self.year, self.week)
        self.update_log_data()

    def close_widget(self):
        """
        Method to send the signal to close the worked log widget
        """
        self.close_worked_log_signal.emit(True)
