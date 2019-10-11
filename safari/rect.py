from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from threading import Thread
from math import sin, cos, pi, sqrt, atan
import time
import random


class Rekt(QtWidgets.QWidget, Thread):

    class Get_Rekt(Thread):

        def __init__(self, w, h, width, height, x, y, vx, vy, da, delay=0.5):
            super().__init__()
            xs, ys = x - width / 2, y - height / 2
            self.points = [QtCore.QPointF(xs, ys),
                           QtCore.QPointF(width + xs, ys),
                           QtCore.QPointF(width + xs, height + ys),
                           QtCore.QPointF(xs, height + ys)]
            self.center = [xs + width / 2, ys + height / 2]
            self.kx, self.ky = 1, 1
            self.r = sqrt((width / 2)**2 + (height / 2)**2)
            self.vx, self.vy = vx, vy
            self.angle = pi / 10
            self.width = w
            self.height = h
            self.angles = (atan(height / width) * 2, atan(width / height) * 2, atan(height / width) * 2, atan(width / height) * 2)
            self.da = da
            self.delay = delay
            # self.start()

        def run(self):
            while 1:
                self.move_rekt()
                time.sleep(self.delay)

        def move_rekt(self):
            self.center[0] += self.vx * self.kx
            self.center[1] += self.vy * self.ky
            for i, point in enumerate(self.points):
                self.rotate(point)
                self.angle += self.angles[i]
                # point.setX(point.x() + self.vx * self.kx)
                # point.setY(point.y() + self.vy + self.ky)
            if min(self.points, key=lambda e: e.x()).x() < 0:
                self.kx = 1
            elif max(self.points, key=lambda e: e.x()).x() > self.width:
                self.kx = -1
            if min(self.points, key=lambda e: e.y()).y() < 0:
                self.ky = 1
            elif max(self.points, key=lambda e: e.y()).y() > self.height:
                self.ky = -1
            self.angle += self.da

        def rotate(self, point: QtCore.QPointF):
            # point.setX(self.center[0] + (point.x() - self.center[0]) * cos(self.angle) - (point.y() - self.center[1]) * sin(self.angle) + 0.1)
            # point.setY(self.center[1] + (point.y() - self.center[1]) * cos(self.angle) + (point.x() - self.center[0]) * sin(self.angle) + 0.1)
            point.setX(self.r * cos(self.angle) + self.center[0])
            point.setY(self.r * sin(self.angle) + self.center[1])

    def __init__(self, width, height):
        super().__init__()
        self.resize(500, 500)
        self.rekts = []
        self.rekts.append(self.Get_Rekt(self.width(), self.height(), width, height, 250, 250, 1, 2, 0.05, 0.01))
        self.rekts.append(self.Get_Rekt(self.width(), self.height(), width, height, 0, 0, 0.1, 0.1, 0.1, 0.0001))
        for i in ' ' * random.randint(0, 10):
            self.rekts.append(self.Get_Rekt(self.width(), self.height(), random.randint(0, self.width() / 2), random.randint(0, self.height() / 2), 250, 250, random.uniform(0.1, 10), random.uniform(0.1, 10), random.uniform(0.01, 0.2), random.random() / 10))
        self.painter = QtGui.QPainter(self)

        self.update()
        self.show()

    def run(self) -> None:
        while 1:
            self.update()
            for rekt in self.rekts:
                rekt.move_rekt()
                rekt.width = self.width()
                rekt.height = self.height()
            time.sleep(1e-20)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter.begin(self)
        for rekt in self.rekts:
            for i in range(4):
                self.painter.drawLine(rekt.points[i-1], rekt.points[i])
        self.painter.end()


def to_radians(angle):
    return angle / 180 * pi


app = QtWidgets.QApplication(sys.argv)
a = Rekt(100, 50)
a.start()
app.exec()