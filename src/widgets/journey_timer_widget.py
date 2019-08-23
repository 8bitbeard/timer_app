"""
This file implements the StopWatchWidget Class, which is responsible for all the checkout
calculator widgets
"""

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer


# pylint: disable=too-many-instance-attributes
# 10 instance attributes seems to be reasonably ok for this class
class JourneyTimerWidget(QWidget):
    """
    StopWatch Class
    """

    close_journey_timer_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super(JourneyTimerWidget, self).__init__(parent)

        self.init_user_interface()

        self.time = 0

    def init_user_interface(self):
        """
        This function initiates the Widget items
        """
        self.journey_time_text_label = QLabel()

        self.play_pause_button = QPushButton(text='Play')
        self.play_pause_button.clicked.connect(self.start_pause_action)
        self.stop_button = QPushButton(text='Stop')
        self.stop_button.clicked.connect(self.stop_action)
        self.reset_button = QPushButton(text='Reset')
        self.reset_button.clicked.connect(self.reset_action)

        self.journey_layout = QGridLayout()

        self.journey_layout.addWidget(self.journey_time_text_label, 0, 0)
        self.journey_layout.addWidget(self.play_pause_button, 1, 0)
        self.journey_layout.addWidget(self.stop_button, 1, 1)
        self.journey_layout.addWidget(self.reset_button, 1, 2)

        self.setLayout(self.journey_layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
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

    def stop_action(self):
        """
        Method to stop the journey timer
        """
        self.timer.stop()
        self.time = 0
        print("STOP")

    def reset_action(self):
        """
        Metho to reset the journey timer
        """
        print("RESET")

    def  update_time(self):
        """
        Method to update the journey timer
        """
        self.time += 1
        self.journey_time_text_label.setText(str(self.time))
