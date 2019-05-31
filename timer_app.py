"""
Checkout timer app.

This project started at 05/2019 as a python study and a team collaboration initiative
"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from sample.main_window import MainWindow


def main():
    """
    Main app function
    """
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
