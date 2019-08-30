"""
File to implement the custom switch widget
"""

from PyQt5 import QtWidgets, QtCore, QtGui

class SwitchButton(QtWidgets.QWidget):
    def __init__(self, parent=None, width=50):
        super(SwitchButton, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.__background = Background(self)
        self.__circle = Circle(self)
        self.__circlemove = None
        self.__enabled = True
        self.__duration = 50
        self.__value = 1
        self.setFixedSize(width, 26)
        self.place_circle('off_day')

        self.__background.resize(width, 26)
        self.__background.move(0, 0)

    def place_circle(self, mode):
        if mode == 'work_day':
            self.__circle.move(self.width() - 23, 3)
        elif mode == 'off_day':
            self.__circle.move(self.width()/2 - 10, 3)
        elif mode == 'extra_day':
            self.__circle.move(3, 3)

    def setMode(self, mode):
        if mode == 'work_day':
            self.__value = 1
            self.__background.set_color(80, 199, 9)
        elif mode == 'off_day':
            self.__value = 2
            self.__background.set_color(150, 150, 150)
        elif mode == 'extra_day':
            self.__value = 0
            self.__background.set_color(13, 57, 255)
        self.place_circle(mode)

    def setDuration(self, time):
        self.__duration = time

    def mousePressEvent(self, event):
        if not self.__enabled:
            return

        self.__circlemove = QtCore.QPropertyAnimation(self.__circle, b"pos")
        self.__circlemove.setDuration(self.__duration)

        y  = 3
        if self.__value == 0:
            x_start = 3
            x_finish = self.width()/2 - 10
            self.__background.set_color(150, 150, 150)
        elif self.__value == 1:
            x_start = self.width()/2 - 10
            x_finish = self.width() - 23
            self.__background.set_color(80, 199, 9)
        else:
            x_start = self.width() - 23
            x_finish = 3
            self.__background.set_color(13, 57, 255)

        self.__circlemove.setStartValue(QtCore.QPoint(x_start, y))
        self.__circlemove.setEndValue(QtCore.QPoint(x_finish, y))

        self.__value = (self.__value + 1) % 3
        self.__circlemove.start()

class Circle(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Circle, self).__init__(parent)
        self.__enabled = True
        self.setFixedSize(20, 20)

    def paintEvent(self, event):
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(QtCore.Qt.NoPen)
        qp.setBrush(QtGui.QColor(255, 255, 255))
        qp.drawEllipse(0, 0, 20, 20)
        qp.end()

class Background(QtWidgets.QWidget):
    def __init__(self, parent=None, mode='work_off'):
        super(Background, self).__init__(parent)
        self.__enabled = True
        self.setFixedHeight(26)
        self.init_color(mode)

    def init_color(self, mode):
        if mode == 'work_day':
            self.color = QtGui.QColor(80, 199, 9)
        elif mode == 'extra_day':
            self.color = QtGui.QColor(13, 57, 255)
        else:
            self.color = QtGui.QColor(150, 150, 150)

    def set_color(self, color_r, color_g, color_b):
        self.color = QtGui.QColor(color_r, color_g, color_b)
        self.update()

    def paintEvent(self, event):
        s = self.size()
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        qp.setPen(pen)
        qp.setBrush(self.color)
        qp.drawRoundedRect(0, 0, s.width(), s.height(), 13, 13)
        qp.end()
