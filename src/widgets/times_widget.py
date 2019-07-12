"""
This file implements the CheckoutCalculatorWidget Class, which is responsible for all the checkout
calculator widgets
"""

import re
from time import localtime
from time import strftime

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QGridLayout, QApplication
from PyQt5.QtCore import QTimer, Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from src.utils import utils


# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class TimesWidget(QWidget):
    """
    Times widget docstring
    """
    WORK_TIME = '08:00'
    TIMER_VALUE = 1000
    APP_TITLE = "Checkout Timer"
    NOTIFICATION_TEXT = "Hey, time is up, Time to go home!"

    def __init__(self, parent, tray_icon, settings_widget, worked_log_widget):
        super(TimesWidget, self).__init__(parent)

        self.notification_text = self.NOTIFICATION_TEXT

        self.settings_widget = settings_widget
        self.worked_log_widget = worked_log_widget
        self.tray_icon = tray_icon

        self.init_user_interface()

    def init_user_interface(self):
        """
        This function initiates the Main Widget
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.notification_event)
        self.timer.start(self.TIMER_VALUE)

        self.worked_log_widget.hide()
        self.settings_widget.hide()
        self.settings_widget.notification_text_signal.connect(self.change_notification_text)

        self.textbox_one_label = QLabel(text='Journey time:')
        self.textbox_one_label.setAlignment(Qt.AlignRight)

        hour_time_range = "(?:[0-1]?[0-9]|2[0-3])"
        minute_time_range = "(?:[0-5]?[0-9]|2[0-3])"

        journey_time_range = QRegExp("^" + hour_time_range + "\\:" + minute_time_range)
        journey_time_validator = QRegExpValidator(journey_time_range, self)

        self.journey_times_checkbox = QLineEdit(self)
        self.journey_times_checkbox.setText(self.WORK_TIME)
        self.journey_times_checkbox.setFixedWidth(170)
        self.journey_times_checkbox.setValidator(journey_time_validator)

        textbox_two_label = QLabel(text='Worked times:')
        textbox_two_label.setAlignment(Qt.AlignRight)

        self.worked_times_checkbox = QLineEdit(self)
        self.worked_times_checkbox.setFixedWidth(170)
        self.worked_times_checkbox.setPlaceholderText('09:00  12:00  13:00')
        self.worked_times_checkbox.textChanged.connect(self.has_data)
        self.worked_times_checkbox.text()

        textbox_three_label = QLabel(text='Checkout time:')
        textbox_three_label.setAlignment(Qt.AlignRight)

        self.checkout_time_checkbox = QLineEdit(self)
        self.checkout_time_checkbox.setFixedWidth(170)

        self.clear_data_button = QPushButton('Clear data', self)
        self.clear_data_button.clicked.connect(self.clear_fields)
        self.clear_data_button.setEnabled(False)

        self.toggle_notifications = QCheckBox('Enable notification')
        self.toggle_notifications.setChecked(True)

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate_time)

        app_layout = QGridLayout()

        app_layout.addWidget(self.textbox_one_label, 0, 0)
        app_layout.addWidget(self.journey_times_checkbox, 0, 1)
        app_layout.addWidget(textbox_two_label, 1, 0)
        app_layout.addWidget(self.worked_times_checkbox, 1, 1)
        app_layout.addWidget(textbox_three_label, 2, 0)
        app_layout.addWidget(self.checkout_time_checkbox, 2, 1)
        app_layout.addWidget(self.clear_data_button, 3, 0)
        app_layout.addWidget(self.toggle_notifications, 3, 1)
        app_layout.addWidget(self.calculate_button, 4, 0, 1, 2)

        self.setLayout(app_layout)

    def calculate_time(self):
        """
        This function is responsible to calculate the workout time value
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')

        try:
            times = regex.findall(self.worked_times_checkbox.text())
            checkin_work = times[0]
            checkout_lunch = times[1]
            checkin_lunch = times[2]

            assert utils.time_is_greater(checkout_lunch, checkin_work)
            assert utils.time_is_greater(checkin_lunch, checkout_lunch)

            checkout_time = utils.sum_times(checkin_work, self.journey_times_checkbox.text())
            lunch_time = utils.sub_times(checkout_lunch, checkin_lunch)
            checkout_time = utils.sum_times(checkout_time, lunch_time)

            self.checkout_time_checkbox.setText(checkout_time)

            self.timer.start(self.TIMER_VALUE)

        except AssertionError:
            self.clear_fields()
            self.checkout_time_checkbox.setText('Time input error!')

    def change_notification_text(self, text):
        """
        This function is responsible for changing the checkout notification text
        """
        if text:
            self.notification_text = text

    def has_data(self, text):
        """
        This function checks if there is data in the worked times text box, and do some validations to it's text
        """
        if text:
            self.clear_data_button.setEnabled(True)
            if QApplication.clipboard().text() == text:
                self.paste_event(text)
            else:
                hour_time_range = "(?:[0-1]?[0-9]|2[0-3])"
                minute_time_range = "(?:[0-5]?[0-9]|2[0-3])"
                worked_time_range = QRegExp("^" + hour_time_range + "\\:" + minute_time_range +
                                            " " + hour_time_range + "\\:" + minute_time_range +
                                            " " + hour_time_range + "\\:" + minute_time_range + "$")
                worked_time_validator = QRegExpValidator(worked_time_range, self)
                self.worked_times_checkbox.setValidator(worked_time_validator)
        else:
            self.clear_data_button.setEnabled(False)
            worked_time_range = QRegExp(".*")
            worked_time_validator = QRegExpValidator(worked_time_range, self)
            self.worked_times_checkbox.setValidator(worked_time_validator)

    def paste_event(self, text):
        """
        This function handles the text paste on the worked times text box
        """
        regex = re.compile('([0-9]{2}:[0-9]{2})')
        finds = regex.findall(text)
        try:
            result = finds[0] + ' ' + finds[1] + ' ' + finds[2]
            self.worked_times_checkbox.setText(result)
        except IndexError:
            self.worked_times_checkbox.clear()

    def clear_fields(self):
        """
        This function is responsible to clear all the text input fields
        """
        self.worked_times_checkbox.clear()
        self.checkout_time_checkbox.clear()

    def notification_event(self):
        """
        This function is responsible for the Checkout time notification event
        """
        checkout_time = self.checkout_time_checkbox.text()
        current_time = strftime('%H:%M', localtime())
        if checkout_time == current_time and self.toggle_notifications.isChecked():
            self.tray_icon.showMessage(self.APP_TITLE, self.notification_text)
            self.timer.stop()
