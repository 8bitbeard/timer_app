"""
File to implement the custom switch widget
"""

from PyQt5 import QtWidgets, QtCore, QtGui

class SwitchButton(QtWidgets.QWidget):
    """
    Class to implement the custom toggle switch
    """

    clicked = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, width=40):
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
        self.move_circle(0)

        self.__background.resize(width, 26)
        self.__background.move(0, 0)

    def move_circle(self, mode):
        """
        Method to move the circle from the widget
        """
        if mode == 0:
            self.__circle.move(self.width()/2 - 10, 3)
        elif mode == 1:
            self.__circle.move(self.width() - 23, 3)
        elif mode == 2:
            self.__circle.move(3, 3)

    # pylint: disable=invalid-name
    def setMode(self, mode):
        """
        Method to set the state of the switch
        """
        if mode == 0:
            self.__value = 0
            self.__background.set_color(150, 150, 150)
        elif mode == 1:
            self.__value = 1
            self.__background.set_color(80, 199, 9)
        elif mode == 2:
            self.__value = 2
            self.__background.set_color(13, 57, 255)
        self.move_circle(mode)

    # pylint: disable=invalid-name
    def isActive(self):
        """
        Method to return the state of the switch
        """
        return self.__value

    # pylint: disable=invalid-name
    def setDuration(self, time):
        """
        Method to set the duration of the animation
        """
        self.__duration = time

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    def mousePressEvent(self, event):
        """
        Method to define the mouse press animation
        """
        if not self.__enabled:
            return

        self.__circlemove = QtCore.QPropertyAnimation(self.__circle, b"pos")
        self.__circlemove.setDuration(self.__duration)

        y_position = 3
        if self.__value == 2:
            x_start = 3
            x_finish = self.width()/2 - 10
            self.__background.set_color(150, 150, 150)
        elif self.__value == 0:
            x_start = self.width()/2 - 10
            x_finish = self.width() - 23
            self.__background.set_color(80, 199, 9)
        else:
            x_start = self.width() - 23
            x_finish = 3
            self.__background.set_color(13, 57, 255)

        self.__circlemove.setStartValue(QtCore.QPoint(x_start, y_position))
        self.__circlemove.setEndValue(QtCore.QPoint(x_finish, y_position))

        self.__circlemove.start()

        self.__value = (self.__value + 1) % 3
        self.clicked.emit(self.__value)


class Circle(QtWidgets.QWidget):
    """
    Class to implement the circle element of the switch
    """
    def __init__(self, parent=None):
        super(Circle, self).__init__(parent)
        self.__enabled = True
        self.setFixedSize(20, 20)

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    def paintEvent(self, event):
        """
        Method to define the paint event of the class
        """
        q_paint = QtGui.QPainter()
        q_paint.begin(self)
        q_paint.setRenderHint(QtGui.QPainter.Antialiasing, True)
        q_paint.setPen(QtCore.Qt.NoPen)
        q_paint.setBrush(QtGui.QColor(255, 255, 255))
        q_paint.drawEllipse(0, 0, 20, 20)
        q_paint.end()

class Background(QtWidgets.QWidget):
    """
    Class to implement the background of the switch
    """
    def __init__(self, parent=None, mode=0):
        super(Background, self).__init__(parent)
        self.__enabled = True
        self.color = None
        self.setFixedHeight(26)
        self.init_color(mode)

    def init_color(self, mode):
        """
        Method to initialize the background colors
        """
        if mode == 1:
            self.color = QtGui.QColor(80, 199, 9)
        elif mode == 2:
            self.color = QtGui.QColor(13, 57, 255)
        else:
            self.color = QtGui.QColor(150, 150, 150)

    def set_color(self, color_r, color_g, color_b):
        """
        Method to update the background color
        """
        self.color = QtGui.QColor(color_r, color_g, color_b)
        self.update()

    # pylint: disable=invalid-name
    # pylint: disable=unused-argument
    def paintEvent(self, event):
        """
        Method to implement the background paint event
        """
        size = self.size()
        q_paint = QtGui.QPainter()
        q_paint.begin(self)
        q_paint.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        q_paint.setPen(pen)
        q_paint.setBrush(self.color)
        q_paint.drawRoundedRect(0, 0, size.width(), size.height(), 13, 13)
        q_paint.end()
