from math import sin, cos, pi
from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class Lsystem(QtWidgets.QWidget):

    def __init__(self, stage, point, le):
        super().__init__()
        self.length = le
        self.resize(1000, 1000)
        self.x = point[0]
        self.y = self.height() - point[1]
        self.stage = stage
        self.init_system(QtWidgets.QFileDialog.getOpenFileName(self, 'Choose system')[0])
        self.painter = QtGui.QPainter(self)
        self.pbrushes = ((QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern),
                          QtGui.QPen(QtCore.Qt.white, 0)),
                         (QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern),
                          QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)))
        self.show()
        self.another_window()

    def another_window(self):

        def slide(val):
            lbstage.setText(str(val))

        set = QtWidgets.QMessageBox(self)
        set.setText('\t' * 8 + '\n' * 10)
        set.resize(500, 500)
        sl = QtWidgets.QSlider(set)
        sl.setSingleStep(1)
        sl.setMaximum(15)
        sl.valueChanged.connect(lambda: slide(sl.value()))
        sl.setGeometry(10, 50, 20, 200)
        lbstage = QtWidgets.QLineEdit('1', set)
        lbstage.setGeometry(35, 50, 20, 20)
        sl.setValue(self.stage)
        QtWidgets.QLabel('x', set).move(120, 0)
        tx = QtWidgets.QLineEdit('500', set)
        tx.move(140, 0)
        QtWidgets.QLabel('y', set).move(120, 40)
        ty = QtWidgets.QLineEdit('500', set)
        ty.move(140, 40)
        QtWidgets.QLabel('Length', set).move(80, 80)
        tle = QtWidgets.QLineEdit('10', set)
        tle.move(140, 80)
        bt = QtWidgets.QPushButton('Применить', set)
        bt.pressed.connect(lambda: self.remake(sl.value(), int(tx.text()), int(ty.text()), int(tle.text())))
        set.show()
        set.exec()

    def remake(self, stage, x, y, le):
        self.stage = stage
        self.x = x
        self.y = self.height() - y
        self.length = le
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        self.painter.setBrush(self.pbrushes[0][0])
        self.painter.setPen(self.pbrushes[0][1])
        self.painter.begin(self)
        self.painter.drawRect(0, 0, self.width(), self.height())
        self.painter.setBrush(self.pbrushes[1][0])
        self.painter.setPen(self.pbrushes[1][1])
        angle = self.angle
        brackets = []
        for e in self.get_stage(self.stage):
            if e == '+':
                angle += self.angle
            elif e == '-':
                angle -= self.angle
            elif e == 'F':
                dx = self.length * cos(angle)
                dy = - self.length * sin(angle)
                self.painter.drawLine(self.x, self.y, self.x + dx, self.y + dy)
                self.x, self.y = self.x + dx, self.y + dy
            elif e == '[':
                brackets.append((angle, self.x, self.y))
            elif e == ']':
                angle, self.x, self.y = brackets.pop()
        self.painter.end()

    def get_stage(self, stage):
        ans = self.acsioma
        ans1 = ''
        for i in ' ' * stage:
            for s in ans:
                if s in self.theorems.keys():
                    ans1 += self.theorems[s]
                else:
                    ans1 += s
            ans = ans1
            ans1 = ''
        return ans

    def init_system(self, file):

        with open(file, 'r', encoding='utf-8') as f:
            self.name = f.readline()
            self.angle = pi * 2 / int(f.readline())
            self.acsioma = f.readline()
            self.theorems = dict(i.split() for i in f.readlines())

    @staticmethod
    def bracket_parse(v, index=0, glans=''):
        ans = ''
        i = index
        while i < len(v):
            if v[i] == '[':
                a, i = Lsystem.bracket_parse(v, i + 1)
                glans += a
            elif v[i] == ']':
                return glans + ans, i
            else:
                ans += v[i]
            i += 1
        return glans + ans


app = QtWidgets.QApplication(sys.argv)
a = Lsystem(1, (500, 500), 10)
a.update()
app.exec()