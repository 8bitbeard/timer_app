from PyQt5 import QtWidgets, QtCore, QtGui

class SettingsWidget(QtWidgets.QWidget):

  close_settings_signal = QtCore.pyqtSignal(bool)
  notification_text_signal = QtCore.pyqtSignal(str)

  def __init__(self, parent=None):
    super(SettingsWidget, self).__init__(parent)

    self.change_notification_label = QtWidgets.QLabel(text='Notification text')
    self.change_notification_label.setAlignment(QtCore.Qt.AlignCenter)

    self.change_notification_textbox = QtWidgets.QPlainTextEdit(self)
    self.change_notification_textbox.setFixedWidth(300)
    self.change_notification_textbox.setFixedHeight(120)

    self.apply_changes_button = QtWidgets.QPushButton('Apply changes', self)
    self.apply_changes_button.clicked.connect(self.apply_settings_changes)

    self.settings_layout = QtWidgets.QGridLayout()

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