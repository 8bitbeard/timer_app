"""
This file uses The PyQt5 module QTest, alongside unittest
to implement some unittesting for the timer_app widget app

This file must be updated with new tests for new features
"""

import sys
import unittest

from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from src.main_window import MainWindow


app = QApplication(sys.argv)

class TimerAppTest(unittest.TestCase):
    """
    Testing the timer_app GUI
    """

    def setUp(self):
        """
        Creating the GUI to be tested
        """

        self.gui = MainWindow()

    def clear_all_data(self):
        """
        Method to erase all the vlaues from the QLineEdits of the app
        """
        # TODO: Implement this method

    def test_default_values(self):
        """
        Method to test all the GUI default values
        """
        self.assertEqual(self.gui.times_widget.journey_times_checkbox.text(), '08:00')
        self.assertEqual(self.gui.times_widget.worked_times_checkbox.text(), '')
        self.assertEqual(self.gui.times_widget.checkout_time_checkbox.text(), '')
        self.assertEqual(self.gui.times_widget.toggle_notifications.isEnabled(), True)
        self.assertEqual(self.gui.times_widget.clear_data_button.isEnabled(), False)
        self.assertEqual(self.gui.times_widget.calculate_button.isEnabled(), False)

    def test_calculate_button_valid_data(self):
        """
        Method to test the calculate checkout time with valid worked times
        """
        # Method still needs to be implemented

    def test_calculate_button_invalid_data(self):
        """
        Method to test the worked times time input error
        """
        # Method still needs to be implemented


    def test_clear_data_button(self):
        """
        Method to test the clear data button
        """
        # Method still needs to be implemented
