"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import pandas
import re

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton
from PyQt5.QtCore import QSize, Qt, pyqtSignal

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

        self.data_file = pandas.read_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"))

        self.init_user_interface()
        self.update_times()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """

        self.worked_time_title_label = QLabel(text='Week: ' +
                                              self.data_file['data'][0] + '-' + self.data_file['data'][1] +
                                              '     Total worked:' + self.data_file['data'][2])
        self.worked_time_title_label.setAlignment(Qt.AlignCenter)

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

        self.sunday_text_label = QLabel(text='Sun')
        self.sunday_checkin_label = QLineEdit(text=self.data_file['sun'][0])
        self.sunday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkout_label = QLineEdit(text=self.data_file['sun'][1])
        self.sunday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_lunch_checkin_label = QLineEdit(text=self.data_file['sun'][2])
        self.sunday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_lunch_checkin_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_checkout_label = QLineEdit(text=self.data_file['sun'][3])
        self.sunday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.sunday_checkout_label.textChanged.connect(self.calculate_sunday_total_time)
        self.sunday_worked_time_label = QLabel(text=self.data_file['sun'][4])

        self.monday_text_label = QLabel(text='Mon')
        self.monday_checkin_label = QLineEdit(text=self.data_file['mon'][0])
        self.monday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkout_label = QLineEdit(text=self.data_file['mon'][1])
        self.monday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_lunch_checkin_label = QLineEdit(text=self.data_file['mon'][2])
        self.monday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_lunch_checkin_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_checkout_label = QLineEdit(text=self.data_file['mon'][3])
        self.monday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.monday_checkout_label.textChanged.connect(self.calculate_monday_total_time)
        self.monday_worked_time_label = QLabel(text=self.data_file['mon'][4])

        self.tuesday_text_label = QLabel(text='Tue')
        self.tuesday_checkin_label = QLineEdit(text=self.data_file['tue'][0])
        self.tuesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkout_label = QLineEdit(text=self.data_file['tue'][1])
        self.tuesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_lunch_checkin_label = QLineEdit(text=self.data_file['tue'][2])
        self.tuesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_lunch_checkin_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_checkout_label = QLineEdit(text=self.data_file['tue'][3])
        self.tuesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.tuesday_checkout_label.textChanged.connect(self.calculate_tuesday_total_time)
        self.tuesday_worked_time_label = QLabel(text=self.data_file['tue'][4])

        self.wednesday_text_label = QLabel(text='Wed')
        self.wednesday_checkin_label = QLineEdit(text=self.data_file['wed'][0])
        self.wednesday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkout_label = QLineEdit(text=self.data_file['wed'][1])
        self.wednesday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_lunch_checkin_label = QLineEdit(text=self.data_file['wed'][2])
        self.wednesday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_lunch_checkin_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_checkout_label = QLineEdit(text=self.data_file['wed'][3])
        self.wednesday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.wednesday_checkout_label.textChanged.connect(self.calculate_wednesday_total_time)
        self.wednesday_worked_time_label = QLabel(text=self.data_file['wed'][4])

        self.thursday_text_label = QLabel(text='Thu')
        self.thursday_checkin_label = QLineEdit(text=self.data_file['thu'][0])
        self.thursday_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkout_label = QLineEdit(text=self.data_file['thu'][1])
        self.thursday_lunch_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_lunch_checkin_label = QLineEdit(text=self.data_file['thu'][2])
        self.thursday_lunch_checkin_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_lunch_checkin_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_checkout_label = QLineEdit(text=self.data_file['thu'][3])
        self.thursday_checkout_label.setFixedSize(self.TIME_BOX_SIZE)
        self.thursday_checkout_label.textChanged.connect(self.calculate_thursday_total_time)
        self.thursday_worked_time_label = QLabel(text=self.data_file['thu'][4])

        self.back_to_main_button = QPushButton('Go back', self)
        self.back_to_main_button.clicked.connect(self.close_widget)


        self.widget_layout = QGridLayout()

        self.widget_layout.addWidget(self.worked_time_title_label, 0, 0, 1, 6)

        # self.widget_layout.addWidget(self.week_days_range_label, 1, 0)
        self.widget_layout.addWidget(self.checkin_time_text_label, 2, 0)
        self.widget_layout.addWidget(self.lunch_checkin_time_text_label, 3, 0)
        self.widget_layout.addWidget(self.lunch_checkout_time_text_label, 4, 0)
        self.widget_layout.addWidget(self.checkout_time_text_label, 5, 0)
        self.widget_layout.addWidget(self.day_journey_time_text_label, 6, 0)

        self.widget_layout.addWidget(self.sunday_text_label, 1, 1)
        self.widget_layout.addWidget(self.sunday_checkin_label, 2, 1)
        self.widget_layout.addWidget(self.sunday_lunch_checkin_label, 3, 1)
        self.widget_layout.addWidget(self.sunday_lunch_checkout_label, 4, 1)
        self.widget_layout.addWidget(self.sunday_checkout_label, 5, 1)
        self.widget_layout.addWidget(self.sunday_worked_time_label, 6, 1)

        self.widget_layout.addWidget(self.monday_text_label, 1, 2)
        self.widget_layout.addWidget(self.monday_checkin_label, 2, 2)
        self.widget_layout.addWidget(self.monday_lunch_checkin_label, 3, 2)
        self.widget_layout.addWidget(self.monday_lunch_checkout_label, 4, 2)
        self.widget_layout.addWidget(self.monday_checkout_label, 5, 2)
        self.widget_layout.addWidget(self.monday_worked_time_label, 6, 2)

        self.widget_layout.addWidget(self.tuesday_text_label, 1, 3)
        self.widget_layout.addWidget(self.tuesday_checkin_label, 2, 3)
        self.widget_layout.addWidget(self.tuesday_lunch_checkin_label, 3, 3)
        self.widget_layout.addWidget(self.tuesday_lunch_checkout_label, 4, 3)
        self.widget_layout.addWidget(self.tuesday_checkout_label, 5, 3)
        self.widget_layout.addWidget(self.tuesday_worked_time_label, 6, 3)

        self.widget_layout.addWidget(self.wednesday_text_label, 1, 4)
        self.widget_layout.addWidget(self.wednesday_checkin_label, 2, 4)
        self.widget_layout.addWidget(self.wednesday_lunch_checkin_label, 3, 4)
        self.widget_layout.addWidget(self.wednesday_lunch_checkout_label, 4, 4)
        self.widget_layout.addWidget(self.wednesday_checkout_label, 5, 4)
        self.widget_layout.addWidget(self.wednesday_worked_time_label, 6, 4)

        self.widget_layout.addWidget(self.thursday_text_label, 1, 5)
        self.widget_layout.addWidget(self.thursday_checkin_label, 2, 5)
        self.widget_layout.addWidget(self.thursday_lunch_checkin_label, 3, 5)
        self.widget_layout.addWidget(self.thursday_lunch_checkout_label, 4, 5)
        self.widget_layout.addWidget(self.thursday_checkout_label, 5, 5)
        self.widget_layout.addWidget(self.thursday_worked_time_label, 6, 5)

        self.widget_layout.addWidget(self.back_to_main_button, 7, 0, 1, 6)

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
        self.worked_time_title_label.setText('Week: ' + '--/-----/--' + ' Total worked:' + total)

    def update_totals(self, text):
        """
        Method to update the totals of the log table
        """
        print(text)

    def close_widget(self):
        """
        Method to send the signal to close the worked log widget
        """
        self.close_worked_log_signal.emit(True)

    def update_times(self):
        """
        Method to update the work log times
        """
        self.sunday_checkin_label.setText(self.data_file['sun'][0])

    def save_data_file(self):
        """
        Method to save the data on the csv file
        """
        self.data_file.to_csv(utils.get_absolute_resource_path("resources/csv_data/work_log_data.csv"))
