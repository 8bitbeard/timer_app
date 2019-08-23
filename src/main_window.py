"""
This file implements the MainWindow Class, which is responsible for all the
main window widgets
"""

import webbrowser

from PyQt5.QtWidgets import QMainWindow, QStyle, QMenu, QAction, QSystemTrayIcon, QStackedWidget, QMessageBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

import qdarkstyle

from src.widgets.settings_widget import SettingsWidget
from src.widgets.checkout_calculator_widget import CheckoutCalculatorWidget
from src.widgets.worked_log_widget import WorkedLogWidget
from src.widgets.web_scrapper_widget import WebScrapperWidget
from src.widgets.journey_timer_widget import JourneyTimerWidget
from src.utils import utils


class MainWindow(QMainWindow):
    """
    MainWindow docstring
    """
    APP_DIMENSIONS = QSize(495, 400)
    APP_TITLE = "Checkout Timer"
    NOTIFICATION_MESSAGE = "The checkout Timer app is still here on tray!"

    def __init__(self, application_object, parent=None):
        super(MainWindow, self).__init__(parent)

        self.application_object = application_object
        self.close_flag = False
        self.dark_mode_flag = False

        self.setWindowTitle(self.APP_TITLE)
        self.setWindowIcon(QIcon(utils.get_absolute_resource_path("resources/images/clock.png")))
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

        settings_menu_two = QMenu('Theme', self)
        settings_action_two = QAction('Default', self)
        settings_action_two.triggered.connect(lambda: self.toggle_dark_mode(False))
        settings_action_three = QAction('Dark mode', self)
        settings_action_three.triggered.connect(lambda: self.toggle_dark_mode(True))

        worked_log_action = QAction('Worked log', self)
        worked_log_action.triggered.connect(self.open_worked_log)

        web_scrapper_action = QAction('WebScrapper', self)
        web_scrapper_action.triggered.connect(self.open_web_scrapper)

        journey_timer_action = QAction('Journey Timer', self)
        journey_timer_action.triggered.connect(self.open_journey_timer)

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
        file_menu.addAction(worked_log_action)
        file_menu.addAction(web_scrapper_action)
        file_menu.addAction(journey_timer_action)
        file_menu.addAction(exit_action)
        settings_menu.addMenu(settings_menu_two)
        settings_menu_two.addAction(settings_action_two)
        settings_menu_two.addAction(settings_action_three)
        help_menu.addAction(documentation_action)
        help_menu.addAction(report_issue_action)
        help_menu.addAction(suggestions_action)
        help_menu.addAction(about_action)

    def init_tray_icon(self):
        """
        This method handles the creation of the tray icon
        """
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(utils.get_absolute_resource_path("resources/images/clock.png")))
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

        self.worked_log_widget = WorkedLogWidget(self)
        self.settings_widget = SettingsWidget(self)
        self.web_scrapper_widget = WebScrapperWidget(self)
        self.journey_timer_widget = JourneyTimerWidget(self)
        self.checkout_calculator_widget = CheckoutCalculatorWidget(self, self.tray_icon, self.settings_widget,
                                                                   self.worked_log_widget, self.web_scrapper_widget,
                                                                   self.journey_timer_widget)
        self.central_widget.addWidget(self.checkout_calculator_widget)
        self.central_widget.setCurrentWidget(self.checkout_calculator_widget)

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

    def open_worked_log(self):
        """
        This method handles the "Work log" press on the Toolbar menu
        """
        self.worked_log_widget.close_worked_log_signal.connect(self.close_widget)
        self.worked_log_widget.get_log_data()
        self.worked_log_widget.update_log_data()
        self.central_widget.addWidget(self.worked_log_widget)
        self.central_widget.setCurrentWidget(self.worked_log_widget)

    def open_web_scrapper(self):
        """
        This method handles the "WebScrapper" press on the Toolbar menu
        """
        self.web_scrapper_widget.close_web_scrapper_signal.connect(self.close_widget)
        self.central_widget.addWidget(self.web_scrapper_widget)
        self.central_widget.setCurrentWidget(self.web_scrapper_widget)

    def open_journey_timer(self):
        """
        This method handles the "JourneyTimer" press on the Toolbar menu
        """
        self.journey_timer_widget.close_journey_timer_signal.connect(self.close_widget)
        self.central_widget.addWidget(self.journey_timer_widget)
        self.central_widget.setCurrentWidget(self.journey_timer_widget)

    def open_settings(self):
        """
        This function handles the "Edit notification" press on the Toolbar menu
        """
        self.settings_widget.close_settings_signal.connect(self.close_widget)
        self.central_widget.addWidget(self.settings_widget)
        self.central_widget.setCurrentWidget(self.settings_widget)

    def close_widget(self, value):
        """
        This function handles the "Apply changes" button press on the settings page
        """
        if value:
            self.central_widget.setCurrentWidget(self.checkout_calculator_widget)

    def toggle_dark_mode(self, value):
        """
        This method handles the dark mode change
        """
        if value:
            if not self.dark_mode_flag:
                self.application_object.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
                self.dark_mode_flag = True
        else:
            if self.dark_mode_flag:
                self.application_object.setStyleSheet("")
                self.dark_mode_flag = False

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
        self.worked_log_widget.close_widget()
