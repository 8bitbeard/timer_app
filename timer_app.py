from PyQt5 import QtWidgets, QtCore, Qt
from sample.main_window import MainWindow
import sys
import re


if __name__ == '__main__':

  app = QtWidgets.QApplication(sys.argv)
  app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
  window = MainWindow()
  window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
  window.show()
  sys.exit(app.exec_())