from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
import re

class TimesWidget(QtWidgets.QWidget):

  WORK_TIME = '08:00'
  TIMER_VALUE = 1000
  APP_TITLE = "Checkout Timer"
  NOTIFICATION__TEXT = "Hey, time is up, Time to go home!"

  def __init__(self, parent, tray_icon, settings_widget):
    super(TimesWidget, self).__init__(parent)

    self.notification_text = self.NOTIFICATION__TEXT

    self.settings_widget = settings_widget
    self.tray_icon = tray_icon
    self.initUI()

  def initUI(self):
    """
    This function initiates the Main Widget
    """
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.notification_event)
    self.timer.start(self.TIMER_VALUE)

    self.settings_widget.hide()
    self.settings_widget.notification_text_signal.connect(self.change_notification_text)

    self.textbox_one_label = QtWidgets.QLabel(text='Journey time:')
    self.textbox_one_label.setAlignment(QtCore.Qt.AlignRight)

    hour_time_range = "(?:[0-1]?[0-9]|2[0-3])"
    minute_time_range = "(?:[0-5]?[0-9]|2[0-3])"

    journey_time_range = QtCore.QRegExp("^" + hour_time_range + "\\:" + minute_time_range)
    journey_time_validator = QtGui.QRegExpValidator(journey_time_range, self)

    self.journey_times_checkbox = QtWidgets.QLineEdit(self)
    self.journey_times_checkbox.setText(self.WORK_TIME)
    self.journey_times_checkbox.setFixedWidth(170)
    self.journey_times_checkbox.setValidator(journey_time_validator)

    self.textbox_two_label = QtWidgets.QLabel(text='Worked times:')
    self.textbox_two_label.setAlignment(QtCore.Qt.AlignRight)

    self.worked_times_checkbox = QtWidgets.QLineEdit(self)
    self.worked_times_checkbox.setFixedWidth(170)
    self.worked_times_checkbox.setPlaceholderText('09:00  12:00  13:00')
    self.worked_times_checkbox.textChanged.connect(self.has_data)

    self.textbox_three_label = QtWidgets.QLabel(text='Checkout time:')
    self.textbox_three_label.setAlignment(QtCore.Qt.AlignRight)

    self.checkout_time_checkbox = QtWidgets.QLineEdit(self)
    self.checkout_time_checkbox.setFixedWidth(170)

    self.clear_data_button = QtWidgets.QPushButton('Clear data', self)
    self.clear_data_button.clicked.connect(self.clear_fields)
    self.clear_data_button.setEnabled(False)

    self.toggle_notifications = QtWidgets.QCheckBox('Enable notification')
    self.toggle_notifications.setChecked(True)

    self.calculate_button = QtWidgets.QPushButton('Calculate', self)
    self.calculate_button.clicked.connect(self.calculate_time)

    self.app_layout = QtWidgets.QGridLayout()

    self.app_layout.addWidget(self.textbox_one_label, 0, 0)
    self.app_layout.addWidget(self.journey_times_checkbox, 0, 1)
    self.app_layout.addWidget(self.textbox_two_label, 1, 0)
    self.app_layout.addWidget(self.worked_times_checkbox, 1, 1)
    self.app_layout.addWidget(self.textbox_three_label, 2, 0)
    self.app_layout.addWidget(self.checkout_time_checkbox, 2, 1)
    self.app_layout.addWidget(self.clear_data_button, 3, 0)
    self.app_layout.addWidget(self.toggle_notifications, 3, 1)
    self.app_layout.addWidget(self.calculate_button, 4, 0, 1, 2)

    self.setLayout(self.app_layout)

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

      assert self.time_is_greater(checkout_lunch, checkin_work)
      assert self.time_is_greater(checkin_lunch, checkout_lunch)

      checkout_time = self.sum_times(checkin_work, self.journey_times_checkbox.text())
      lunch_time = self.sub_times(checkout_lunch, checkin_lunch)
      checkout_time = self.sum_times(checkout_time, lunch_time)

      self.checkout_time_checkbox.setText(checkout_time)
      self.checkout_time_checkbox.setStyleSheet("color: black;")

      self.timer.start(self.TIMER_VALUE)

    except:
      self.clear_fields()
      self.checkout_time_checkbox.setText('Time input error!')
      self.checkout_time_checkbox.setStyleSheet("color: red;")

  def _convert_to_int(self, time):
    """
    This function gets the time string and return the hrs and minutes as integers
    """
    hrs = int(time[0:time.index(':')])
    mins = int(time[time.index(':') + 1 :])
    return(hrs, mins)

  def _change_to_minutes(self, time):
    """
    This function converts the time from hrs:mins to minutes
    """
    hrs, mins = self._convert_to_int(time)
    return(60 * hrs + mins)

  def _change_to_hours(self, minutes):
    """
    This function converts the time from minutes to hrs:mins format
    """
    mins = minutes % 60
    hrs = (minutes - mins) // 60
    return "{:02d}:{:02d}".format(hrs, mins)

  def time_is_greater(self, time_one, time_two):
    """
    This function checks if the time_one is greater than the time_two
    """
    if self._change_to_minutes(time_one) > self._change_to_minutes(time_two):
      return True
    else:
      return False

  def sum_times(self, time_one, time_two):
    """
    This function is responsible to add two times
    """
    time_minutes_one = self._change_to_minutes(time_one)
    time_minutes_two = self._change_to_minutes(time_two)

    return(self._change_to_hours(time_minutes_two + time_minutes_one))

  def sub_times(self, time_one, time_two):
    """
    This function is responsible to subtract two times
    """
    time_minutes_one = self._change_to_minutes(time_one)
    time_minutes_two = self._change_to_minutes(time_two)

    return(self._change_to_hours(time_minutes_two - time_minutes_one))

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
        if QtWidgets.QApplication.clipboard().text() == text:
          self.paste_event(text)
        else:
          hour_time_range = "(?:[0-1]?[0-9]|2[0-3])"
          minute_time_range = "(?:[0-5]?[0-9]|2[0-3])"
          worked_time_range = QtCore.QRegExp("^" + hour_time_range + "\\:" + minute_time_range + " "
                                                + hour_time_range + "\\:" + minute_time_range + " "
                                                + hour_time_range + "\\:" + minute_time_range + "$")
          worked_time_validator = QtGui.QRegExpValidator(worked_time_range, self)
          self.worked_times_checkbox.setValidator(worked_time_validator)
    else:
        self.clear_data_button.setEnabled(False)
        worked_time_range = QtCore.QRegExp(".*")
        worked_time_validator = QtGui.QRegExpValidator(worked_time_range, self)
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
    except:
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
    current_time = str(datetime.datetime.now().time())[0:5]
    if checkout_time == current_time and self.toggle_notifications.isChecked():
      self.tray_icon.showMessage(self.APP_TITLE, self.notification_text)
      self.timer.stop()