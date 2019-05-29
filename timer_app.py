"""
Checkout timer app.

This project started at 05/2019 as a python study and a team collaboration initiative
"""

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from sample.main_window import MainWindow


def custom_palette():
    """
    This function creates a custom palete for the theme Fusion
    """
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(15, 15, 15))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)

    palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette

def main():
    """
    Main app function
    """
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    app.setPalette(custom_palette())
    window = MainWindow()
    window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
