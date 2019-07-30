"""
This file implements the StopWatchWidget Class, which is responsible for all the checkout
calculator widgets
"""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt


# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class JourneyTimerWidget(QWidget):
    """
    StopWatch Class
    """

    def __init__(self, parent=None):
        super(JourneyTimerWidget, self).__init__(parent)

        self.init_user_interface()

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """

        self.journey_time_text_label = QLabel()

        self.play_pause_button = QPushButton()
        self.play_pause_button.clicked.connect(self.start_journey_timer)
        self.stop_button = QPushButton()
        self.reset_button = QPushButton()

        self.timer = Qt.QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_time)

    def start_journey_timer(self):
        """
        Method to start the journey timer
        """
        self.timer.start()

    def  update_time(self):
        """
        Method to update the journey timer
        """
        self.journey_time_text_label.setText()
        print('tick!')
