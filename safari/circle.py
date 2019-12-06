import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from math import sin, cos, pi
from threading import Thread
import time
import random


class Circles(QtWidgets.QWidget, Thread):
    
    class Circle(Thread):
        
        def __init__(self, parent, sr, r=0, delay=0.5, da=0.05):
            super().__init__()
            self.point = QtCore.QPointF(0, 0)
            self.r = r
            self.a = 0
            self.da = da
            self.sr = sr
            self.parent = parent
            self.delay = delay
            self.rotate()
            # self.start()

        def run(self):
            while 1:
                self.rotate()
                time.sleep(self.delay)

        def rotate(self):
            self.point.setX(self.sr * cos(self.a) + self.parent.point.x())
            self.point.setY(self.sr * sin(self.a) + self.parent.point.y())
            self.a += self.da

    def __init__(self, x, y, r, k):
        super().__init__()
        self.point = QtCore.QPointF(x, y)
        self.resize(1920, 1080)
        self.r = r
        self.circles = []
        c = self
        d = 0.1
        self.mpix = QtGui.QPixmap(self.width(), self.height())
        self.pixpainter = QtGui.QPainter(self.mpix)
        self.pixpainter.fillRect(0, 0, self.width(), self.height(), QtCore.Qt.white)
        k = 1
        for i in range(12):
            # k = random.uniform(0.3, 0.8)
            # c = self.Circle(c, c.r * k, c.r * (1 - k), d, random.uniform(0.001, 0.1))
            k = random.uniform(0.5, 1)
            c = self.Circle(c, c.r * k, random.randint(50, 100), d, random.uniform(0.05, 0.25))
            self.circles.append(c)
            d /= 5
        self.painter = QtGui.QPainter(self)
        # self.update()
        self.show()

    def run(self):
        vx, vy = 2, 1
        kx, ky = 1, 1
        while 1:
            self.point.setX(vx * kx + self.point.x())
            self.point.setY(self.point.y() + vy * ky)
            if self.point.x() + self.r > self.width():
                kx = -1
                self.point.setX(self.width() - self.r)
            elif self.point.x() - self.r < 0:
                kx = 1
                self.point.setX(self.r)
            if self.point.y() + self.r > self.height():
                ky = -1
                self.point.setY(self.height() - self.r)
            elif self.point.y() - self.r < 0:
                ky = 1
                self.point.setY(self.r)
            self.repaint()
            time.sleep(1e-20)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.pixpainter.begin(self.mpix)
        # self.pixpainter.drawEllipse(self.point, self.r, self.r)
        for circle in self.circles:
            self.pixpainter.setBrush(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))
            self.pixpainter.setPen(QtGui.QPen(QtCore.Qt.white, 1, QtCore.Qt.SolidLine))
            circle.rotate()
            self.pixpainter.drawEllipse(circle.point, circle.r, circle.r)
        self.pixpainter.end()
        self.painter.begin(self)
        self.painter.drawPixmap(0, 0, self.mpix)
        self.painter.end()


app = QtWidgets.QApplication(sys.argv)
a = Circles(500, 500, 200, 0.5)
a.start()
app.exec()