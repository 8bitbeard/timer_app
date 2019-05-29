"""
Checkout timer app.

This project started at 05/2019 as a python study and a team collaboration initiative
"""

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import Qt
from sample.main_window import MainWindow

def main():
    """
    Main app function
    """
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
