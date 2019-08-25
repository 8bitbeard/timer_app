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

        self.time = '00:00:00'

        self.init_user_interface()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """
        self.journey_time_text_label = QLabel(text=self.time)
        self.journey_time_text_label.setStyleSheet("font: 30pt")

        self.play_pause_button = QPushButton(text='Play')
        self.play_pause_button.clicked.connect(self.start_pause_action)
        self.reset_button = QPushButton(text='Reset')
        self.reset_button.clicked.connect(self.reset_action)

        self.journey_layout = QGridLayout()

        self.journey_layout.addWidget(self.journey_time_text_label, 0, 0, 1, 2)
        self.journey_layout.addWidget(self.play_pause_button, 1, 0)
        self.journey_layout.addWidget(self.reset_button, 1, 1)

        self.setLayout(self.journey_layout)

        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_time)

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

    def  update_time(self):
        """
        Method to update the journey timer
        """
        self.time = utils.increment_time_by_second(input_time=self.time)
        self.journey_time_text_label.setText(self.time)
