"""
This file implements the MainWindow Class, which is responsible for all the
main window widgets
"""

import webbrowser
from PyQt5.QtWidgets import QMainWindow, QStyle, QMenu, QAction, QSystemTrayIcon, QStackedWidget, QMessageBox
from PyQt5.QtCore import QSize
from sample.settings.settings_widget import SettingsWidget
from sample.times.times_widget import TimesWidget


class MainWindow(QMainWindow):
    """
    MainWindow docstring
    """
    APP_DIMENSIONS = QSize(380, 250)
    APP_TITLE = "Checkout Timer"
    NOTIFICATION_MESSAGE = "The checkout Timer app is still here on tray!"

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.close_flag = False

        self.setWindowTitle(self.APP_TITLE)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.setFixedSize(self.APP_DIMENSIONS)

        self.init_menu_bar()
        self.init_tray_icon()
        self.init_user_interface()

    def init_menu_bar(self):
        """
        This method handles the creation of the menubar
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        help_menu = menubar.addMenu('Help')

        settings_menu = QMenu('Settings', self)
        settings_action_one = QAction('Edit notifications', self)
        settings_action_one.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action_one)

        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close_window)

        documentation_action = QAction('Documentation', self)
        documentation_action.triggered.connect(self.documentation)
        report_issue_action = QAction('Report Issues', self)
        report_issue_action.triggered.connect(self.report_issue)
        suggestions_action = QAction('Suggestion', self)
        suggestions_action.triggered.connect(self.suggestions)
        about_action = QAction('About', self)
        about_action.triggered.connect(self.about_popup)

        file_menu.addMenu(settings_menu)
        file_menu.addAction(exit_action)
        help_menu.addAction(documentation_action)
        help_menu.addAction(report_issue_action)
        help_menu.addAction(suggestions_action)
        help_menu.addAction(about_action)

    def init_tray_icon(self):
        """
        This method handles the creation of the tray icon
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close_window)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def init_user_interface(self):
        """
        This function handles the initialization of the main window widgets
        """

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.settings_widget = SettingsWidget(self)
        self.times_widget = TimesWidget(self, self.tray_icon, self.settings_widget)
        self.central_widget.addWidget(self.times_widget)
        self.central_widget.setCurrentWidget(self.times_widget)

    @staticmethod
    def report_issue():
        """
        This function opens the Report Issue project page on the primary SO webbrowser
        """
        github_url = 'https://github.com/8bitbeard/timer_app/issues'
        webbrowser.open(github_url)

    @staticmethod
    def documentation():
        """
        This function opens the Documentation project page on the primary SO webbrowser
        """
        documentation_url = 'https://github.com/8bitbeard/timer_app/blob/master/README.md'
        webbrowser.open(documentation_url)

    @staticmethod
    def suggestions():
        """
        This function opens the Suggestions/Feature Request google form on the browser
        """
        suggestions_url = 'https://docs.google.com/forms/d/1utsdfJFq2qi1WcU91PRsISRob3tKOb_tqtHgi2xaXf0'
        webbrowser.open(suggestions_url)

    def about_popup(self):
        """
        This function handles the About popup
        """
        github_url = "If you are interested, you can find the GitHub project link "\
                    "<a href='https://github.com/8bitbeard/timer_app'>Here</a>"

        about_text = "At first this app was created in a few minutes of python playing..."\
                    "but with colaboration i wonder... HOW FAR CAN WE GO?!'"

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.NoIcon)
        message_box.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
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

    # pylint: disable=invalid-name
    # This method can't be on snake_case, as it needs to override a PyQt5 method
    def closeEvent(self, event):
        """
        This function handles the close app signal from all other close methods
        """
        if not self.close_flag:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(self.APP_TITLE, self.NOTIFICATION_MESSAGE,
                                       QSystemTrayIcon.Information, msecs=100)
        else:
            self.tray_icon.hide()
