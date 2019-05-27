from PyQt5 import QtWidgets, QtCore, QtGui
from sample.settings.settings_widget import SettingsWidget
from sample.times.times_widget import TimesWidget
import webbrowser

class MainWindow(QtWidgets.QMainWindow):

  APP_DIMENSIONS = QtCore.QSize(380, 250)

  APP_TITLE = "Checkout Timer"
  NOTIFICATION_MESSAGE = "The checkout Timer app is still here on tray!"

  def __init__(self, parent=None):
    super(MainWindow, self).__init__(parent)

    self.close_flag = False

    self.setWindowTitle(self.APP_TITLE)
    self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation))
    self.setFixedSize(self.APP_DIMENSIONS)

    self.initUI()

  def initUI(self):

    menubar = self.menuBar()
    file_menu = menubar.addMenu('File')
    help_menu = menubar.addMenu('Help')

    settings_menu = QtWidgets.QMenu('Settings', self)
    settings_action_one = QtWidgets.QAction('Edit notifications', self)
    settings_action_one.triggered.connect(self.open_settings)
    settings_menu.addAction(settings_action_one)

    exit_action = QtWidgets.QAction('Exit', self)
    exit_action.triggered.connect(self.close_window)

    documentation_action = QtWidgets.QAction('Documentation', self)
    documentation_action.triggered.connect(self.documentation)
    report_issue_action = QtWidgets.QAction('Report Issues', self)
    report_issue_action.triggered.connect(self.report_issue)
    suggestions_action = QtWidgets.QAction('Suggestion', self)
    suggestions_action.triggered.connect(self.suggestions)
    about_action = QtWidgets.QAction('About', self)
    about_action.triggered.connect(self.about_popup)

    file_menu.addMenu(settings_menu)
    file_menu.addAction(exit_action)
    help_menu.addAction(documentation_action)
    help_menu.addAction(report_issue_action)
    help_menu.addAction(suggestions_action)
    help_menu.addAction(about_action)

    self.tray_icon = QtWidgets.QSystemTrayIcon(self)
    self.tray_icon.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation))
    self.show_action = QtWidgets.QAction("Show", self)
    self.quit_action = QtWidgets.QAction("Exit", self)
    self.hide_action = QtWidgets.QAction("Hide", self)
    self.show_action.triggered.connect(self.show)
    self.hide_action.triggered.connect(self.hide)
    self.quit_action.triggered.connect(self.close_window)
    self.tray_menu = QtWidgets.QMenu()
    self.tray_menu.addAction(self.show_action)
    self.tray_menu.addAction(self.hide_action)
    self.tray_menu.addAction(self.quit_action)
    self.tray_icon.setContextMenu(self.tray_menu)
    self.tray_icon.show()

    self.central_widget = QtWidgets.QStackedWidget()
    self.setCentralWidget(self.central_widget)

    self.settings_widget = SettingsWidget(self)
    self.times_widget = TimesWidget(self, self.tray_icon, self.settings_widget)
    self.central_widget.addWidget(self.times_widget)
    self.central_widget.setCurrentWidget(self.times_widget)

  def report_issue(self):
    """
    This function opens the Report Issue project page on the primary SO webbrowser
    """
    URL = 'https://github.com/8bitbeard/timer_app/issues'
    webbrowser.open(URL)
    pass

  def documentation(self):
    """
    This function opens the Documentation project page on the primary SO webbrowser
    """
    URL = 'https://github.com/8bitbeard/timer_app/blob/master/README.md'
    webbrowser.open(URL)
    pass

  def suggestions(self):
    """
    This function opens the Suggestions/Feature Request google form on the browser
    """
    URL = 'https://docs.google.com/forms/d/1utsdfJFq2qi1WcU91PRsISRob3tKOb_tqtHgi2xaXf0'
    webbrowser.open(URL)

  def about_popup(self):
    """
    This function handles the About popup
    """
    github_url = "If you are interested, you can find the GitHub project link "\
                 "<a href='https://github.com/8bitbeard/timer_app'>Here</a>"

    about_text = "At first this app was created in a few minutes of python playing..."\
                 "but with colaboration i wonder... HOW FAR CAN WE GO?!'"

    message_box = QtWidgets.QMessageBox()
    message_box.setIcon(QtWidgets.QMessageBox.NoIcon)
    message_box.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxInformation))
    message_box.setText(about_text)
    message_box.setInformativeText(github_url)
    message_box.setWindowTitle("About")
    message_box.exec_()

  def open_settings(self):
    """
    This function handles the "Edit notification" press on the Toolbar menu
    """
    self.settings_widget.close_settings_signal.connect(self.close_settings)
    self.central_widget.addWidget(self.settings_widget)
    self.central_widget.setCurrentWidget(self.settings_widget)

  def close_settings(self, value):
    """
    This function handles the "Apply changes" button press on the settings page
    """
    if value:
      self.central_widget.setCurrentWidget(self.times_widget)


  def close_window(self):
    """
    This function handles the close app signal from the tray icon
    """
    self.close_flag = True
    self.close()

  def closeEvent(self, event):
    """
    This function handles the close app signal from all other close methods
    """
    if not self.close_flag:
      event.ignore()
      self.hide()
      self.tray_icon.showMessage(self.APP_TITLE, self.NOTIFICATION_MESSAGE,
                                 QtWidgets.QSystemTrayIcon.Information, msecs=100)
    else:
      self.tray_icon.hide()