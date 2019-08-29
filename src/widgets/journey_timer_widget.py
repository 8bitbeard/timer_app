"""
This file implements the StopWatchWidget Class, which is responsible for all the checkout
calculator widgets
"""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer

from src.utils import utils

# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class JourneyTimerWidget(QWidget):
    """
    StopWatch Class
    """

    close_journey_timer_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(JourneyTimerWidget, self).__init__(parent)

        self.times_list = []
        self.time = '00:00:00'

        self.init_user_interface()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """

        self.lbl_first_journey = QLabel(text='First half')
        self.lbl_lunch_journey = QLabel(text='Lunch')
        self.lbl_second_journey = QLabel(text='Second half')

        self.val_first_journey = QLabel(text='00:00:00')
        self.val_lunch_journey = QLabel(text='00:00:00')
        self.val_second_journey = QLabel(text='00:00:00')

        self.journey_time_text_label = QLabel(text=self.time)
        self.journey_time_text_label.setAlignment(Qt.AlignCenter)
        self.journey_time_text_label.setStyleSheet("font: 30pt")

        self.play_pause_button = QPushButton(text='Play')
        self.play_pause_button.clicked.connect(self.start_pause_action)
        self.reset_button = QPushButton(text='Reset')
        self.reset_button.clicked.connect(self.reset_action)
        self.workflow_button = QPushButton(text='Start Day!')
        self.workflow_button.clicked.connect(self.workflow_action)

        self.journey_layout = QGridLayout()

        self.journey_layout.addWidget(self.lbl_first_journey, 0, 0)
        self.journey_layout.addWidget(self.lbl_lunch_journey, 0, 1)
        self.journey_layout.addWidget(self.lbl_second_journey, 0, 2)
        self.journey_layout.addWidget(self.val_first_journey, 1, 0)
        self.journey_layout.addWidget(self.val_lunch_journey, 1, 1)
        self.journey_layout.addWidget(self.val_second_journey, 1, 2)
        self.journey_layout.addWidget(self.journey_time_text_label, 2, 0, 1, 3)
        self.journey_layout.addWidget(self.play_pause_button, 3, 0)
        self.journey_layout.addWidget(self.reset_button, 3, 1)
        self.journey_layout.addWidget(self.workflow_button, 3, 2)

        self.setLayout(self.journey_layout)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_time)

    def workflow_action(self):
        """
        Method to add the work day times to a list
        """
        if self.workflow_button.text() == "Start Day!":
            self.workflow_button.setText("Start Lunch")
            self.time = '00:00:00'
            self.timer.start()
        elif self.workflow_button.text() == "Start Lunch":
            self.workflow_button.setText("End Lunch")
        elif self.workflow_button.text() == "End Lunch":
            self.workflow_button.setText("End Day")
        elif self.workflow_button.text() == "End Day":
            self.workflow_button.setText("Start Day!")
            self.timer.stop()

    def start_pause_action(self):
        """
        Method to start/pause the journey timer
        """
        if self.play_pause_button.text() == 'Play':
            self.timer.start()
            self.play_pause_button.setText('Pause')
        else:
            self.timer.stop()
            self.play_pause_button.setText('Play')

    def reset_action(self):
        """
        Method to stop the journey timer
        """
        self.timer.stop()
        self.time = '00:00:00'
        self.journey_time_text_label.setText(self.time)
        self.val_first_journey.setText(self.time)
        self.val_lunch_journey.setText(self.time)
        self.val_second_journey.setText(self.time)

    def  update_time(self):
        """
        Method to update the journey timer
        """
        self.time = utils.increment_time_by_second(input_time=self.time)
        self.journey_time_text_label.setText(self.time)
        if self.workflow_button.text() == "Start Lunch":
            self.val_first_journey.setText(utils.increment_time_by_second(input_time=self.val_first_journey.text()))
        elif self.workflow_button.text() == "End Lunch":
            self.val_lunch_journey.setText(utils.increment_time_by_second(input_time=self.val_lunch_journey.text()))
        elif self.workflow_button.text() == "End Day":
            self.val_second_journey.setText(utils.increment_time_by_second(input_time=self.val_second_journey.text()))
