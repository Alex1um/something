import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from threading import Thread
import time


class Rect(QtWidgets.QWidget, Thread):

    class Rect:

        def __init__(self, parent, x, y, w, h, vx, vy):
            self.x, self.y, self.w, self.h = x, y, w, h
            self.vx, self.vy = vx, vy
            self.parent = parent
            self.kx, self.ky = 1, 1

        def width(self):
            return self.w

        def height(self):
            return self.h

        def move(self):
            self.x += self.vx * self.kx
            self.y += self.vy * self.ky
            if self.x + self.w > self.parent.width():
                self.x = self.parent.width() - self.w
                self.kx = -1
            elif self.x < 0:
                self.kx = 1
                self.x = 0
            if self.y + self.h > self.parent.height():
                self.y = self.parent.height() - self.h
                self.ky = -1
            elif self.y < 0:
                self.y = 0
                self.ky = 1

        def draw(self, painter: QtGui.QPainter):
            painter.drawRect(self.x, self.y, self.w, self.h)

    class Circle:

        def __init__(self, parent, x, y, r, vx, vy):
            self.x, self.y, self.r = x, y, r
            self.vx, self.vy = vx, vy
            self.kx, self.ky = 1, 1
            self.parent = parent

        def draw(self, painter: QtGui.QPainter):
            painter.drawEllipse(QtCore.QPointF(self.x, self.y), self.r, self.r)

        def move(self):
            self.x += self.kx * self.vx
            self.y += self.ky * self.vy
            if self.x + self.r > self.parent.x + self.parent.w:
                self.x = self.parent.x + self.parent.w - self.r
                self.kx = -1
            elif self.x - self.r < self.parent.x:
                self.x = self.r + self.parent.x
                self.kx = 1
            if self.y + self.r > self.parent.y + self.parent.h:
                self.y = self.parent.y + self.parent.h - self.r
                self.ky = -1
            elif self.y - self.r < self.parent.y:
                self.y = self.r + self.parent.y
                self.ky = 1

    def __init__(self):
        super().__init__()
        self.resize(1000, 1000)
        self.rect = self.Rect(self, 500, 500, 200, 100, 5, 5)
        self.circle = self.Circle(self.rect, 500, 500, 15, 10, 10)
        self.painter = QtGui.QPainter(self)
        self.update()
        self.show()

    def run(self):
        while 1:
            self.update()
            self.rect.move()
            self.circle.move()
            time.sleep(1e-2)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter.begin(self)
        self.rect.draw(self.painter)
        self.circle.draw(self.painter)
        self.painter.end()


app = QtWidgets.QApplication(sys.argv)
a = Rect()
a.start()
app.exec()