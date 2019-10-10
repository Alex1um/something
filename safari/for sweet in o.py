from n33d import *
from PyQt5 import QtCore, QtWidgets, QtGui
import sys
import time


class Road(QtWidgets.QWidget):

    class MovingObject:

        def __init__(self, x, y, w, h):
            self.x, self.y = x, y
            self.w, self.h = w, h

        def move(self, vx, vy):
            self.x += vx
            self.y += vy

        def draw(self, painter: QtGui.QPainter, color: QtGui.QBrush):
            painter.setBrush(color)
            kx = 10
            ky = 3
            painter.drawRect((self.x - self.w / 2) * kx, ky * self.y, self.w, self.h)

    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.petya = self.MovingObject(50, 40, 20, 40)
        self.m, self.n, self.p, self.a = map(int, input().split())
        self.sweets = tuple(tuple(map(int, input().split())) for _ in '*' * self.n)
        self.anna = self.MovingObject(50, 40 + self.m + 20, 20, 40)
        self.painter = QtGui.QPainter(self)
        self.sweet = self.MovingObject(self.sweets[0][0] + 50, 20, 20, 20)
        self.time = 0
        self.update()
        self.show()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter.begin(self)
        self.petya.draw(self.painter, QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.SolidPattern))
        self.anna.draw(self.painter, QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))
        self.sweet.draw(self.painter, QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))
        self.painter.end()


app = QtWidgets.QApplication(sys.argv)
a = Road()
app.exec()
# def signal(t, current, tred, tgreen, dt) -> ('signal', 'time'):
#     a = abs(t - dt) % (tred + tgreen)
#     if t - dt >= 0:
#         current = 2 if current == 1 else 1
#     if current == 1:
#         if a >= tgreen:
#             return 2, tred + tgreen - a
#         else:
#             return 1, tgreen - a
#     else:
#         if a >= tred:
#             return 1, tred + tgreen - a
#         else:
#             return 2, tred - a
#
#
# m, n, p, a = map(int, input().split())
# times = []
# for _ in '*' * n:
#     time = 0
#     s, tg, tr, cc, dt = map(int, input().split())
#     if m / p > tg:
#         continue
#     time += s / p
#     color, swt = signal(time, cc, tr, tg, dt)
#     if color == 1 and swt >= m / p:
#         time += m / p
#     else:
#         time += swt + tr + m / p
#     if s / a > time:
#         time += (s - a * time) / (a + p)
#     times.append(time)
# print(min(times))