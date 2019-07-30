"""
This file implements the SettingsWidget Class, which is responsible for all the settings
screen widgets
"""
from PyQt5.QtWidgets import QWidget, QLabel, QPlainTextEdit, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal


class SettingsWidget(QWidget):
    """
    Settings class docstring
    """
    close_settings_signal = pyqtSignal(bool)
    notification_text_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)

        self.change_notification_label = QLabel(text='Notification text')
        self.change_notification_label.setAlignment(Qt.AlignCenter)

        self.change_notification_textbox = QPlainTextEdit(self)

        self.apply_changes_button = QPushButton('Apply changes', self)
        self.apply_changes_button.clicked.connect(self.apply_settings_changes)

        self.settings_layout = QGridLayout()

        self.settings_layout.addWidget(self.change_notification_label, 0, 0)
        self.settings_layout.addWidget(self.change_notification_textbox, 1, 0)
        self.settings_layout.addWidget(self.apply_changes_button, 2, 0)

        self.setLayout(self.settings_layout)

    def apply_settings_changes(self):
        """
        This function is called after pressing the save changes on the settings page
        """
        new_notification_text = self.change_notification_textbox.toPlainText()
        self.notification_text_signal.emit(new_notification_text)
        self.close_settings_signal.emit(True)
