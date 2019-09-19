import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QBrush, QPen
from math import sqrt
from threading import Thread
from time import sleep


def circle(xc, x, r, width):
    return sqrt(r-(x - xc)**2*r/width/width)


def uncircle(xc, y, r, width):
    return sqrt(-(y**2 - r) * width**2 / r)


class Line:
    xs: int
    ys: int
    x: int
    y: int

    def __init__(self, point0, foo, points, i, k=1):
        self.point0 = point0
        x = points[i % (le + 1)][0]
        self.point1 = QPointF(x, foo(x) + yr)
        self.points = points
        self.i = i % (le + 1)
        self.k = k

    def move(self):
        if self.i == 0:
            self.k = 1
        elif self.i // le > 0:
            self.k = -1
        npoint = QPointF(self.points[self.i][0], self.points[self.i][1] * self.k + yr)
        self.point1 = npoint
        self.i += 1 * self.k


class Moover(Thread):
    objs: tuple

    def __init__(self, main, time=0.5, skelet=False, *args):
        super().__init__()
        self.objs = args
        self.time = time
        self.skelet = skelet
        self.main = main

    def run(self):
        while True:
            v = self.getvis()
            for i in range(len(self.objs)):
                self.objs[i].move()
                if not self.skelet:
                    if v[i] and v[i-1] and (self.objs[i].k != self.objs[i - 1].k or self.objs[i - 1].k == self.objs[i].k and self.objs[i].k == 1):
                        self.main.pyro.append((self.objs[i].point0, self.objs[i].point1, self.objs[i-1].point1))
            sleep(self.time)
            self.main.update()

    def getvis(self):
        v = []
        ko = 30
        mi, ma = min(self.objs, key=lambda x: x.point1.x()).point1.x(), max(self.objs, key=lambda x: x.point1.x()).point1.x()
        for i in self.objs:
            if mi + ko < i.point1.x() < ma - ko and i.k == -1 and i.point1.x() != mi and i.point1.x() != ma:
                v.append(False)
            else:
                v.append(True)
        return v


def get_points(foo, unfoo, yp=5, speed=1):
    ac = []
    for x in range(-1000, 1000):
        try:
            ac.append((x, foo(x)))
        except:
            pass
    for y in range(-10000, 10000):
        try:
            ac.append((unfoo(y / yp) + xs, foo(unfoo(y / yp) + xs)))
            ac.append((-unfoo(y / yp) + xs, foo(-(unfoo(y / yp)) + xs)))
        except:
            pass
    return list(sorted(ac, key=lambda x: x[0]))[::speed]


class Mooving_Pyramid(QMainWindow):

    def __init__(self):
        super().__init__()

        self.pyro = []
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1000, 1000)

        self.canvas = QLabel(self)
        self.canvas.setGeometry(0, 0, 200, 200)

        self.show()

    def paintEvent(self, event):
        a = QPainter(self)
        a.setBrush(QBrush(Qt.white, Qt.SolidPattern))
        a.setPen(QPen(Qt.white, 0))
        a.begin(self)
        a.drawRect(0, 0, self.width(), self.height())
        a.end()
        qp = QPainter(self)
        qp.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
        qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        qp.begin(self)
        for point in self.pyro:
            qp.drawPolygon(*point)
        qp.end()
        self.pyro = []


xs, ys = 500, 100
yr = 650
r = 1000
width = 500
point = get_points(lambda x: circle(xs, x, r, width), lambda y: uncircle(xs, y, r, width), yp=5, speed=1)
le = len(point) - 1
app = QApplication(sys.argv)
a = Mooving_Pyramid()
params = (QPointF(xs, ys), lambda x: circle(xs, x, r, width), point)
l4 = Line(*params, le // 4, -1)
l = Line(*params, le * 3 // 4, -1)
l1 = Line(*params, le // 4)
l2 = Line(*params, le * 3 // 4)
b = Moover(a, 0.005, False, l4, l1, l2, l).start()
sys.exit(app.exec_())