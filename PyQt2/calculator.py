# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from math import factorial
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget,\
    QPushButton, QLabel, QLCDNumber,\
    QRadioButton, QTextEdit, QApplication, QGroupBox
import sys


class Ui_Calc(QWidget):

    def __init__(self):
        super().__init__()

        self.setupUi()

    def setupUi(self):
        self.resize(250, 500)
        self.setMaximumSize(QtCore.QSize(250, 500))
        self.groupBox = QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(360, 330, 120, 80))
        self.groupBox.setObjectName("groupBox")
        self.btpow = QPushButton(self)
        self.btpow.setGeometry(QtCore.QRect(200, 80, 45, 45))
        self.btpow.pressed.connect(lambda: self.chandgeop(lambda x, y: x ** y))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btpow.setFont(font)
        self.btpow.setObjectName("btpow")
        self.btsqrt = QPushButton(self)
        self.btsqrt.setGeometry(QtCore.QRect(200, 130, 45, 45))
        self.btsqrt.pressed.connect(
            lambda: self.chandgeop(lambda x, y: round(x ** (1 / y), 2)))
        self.btsqrt.setFont(font)
        self.btsqrt.setObjectName("btsqrt")
        self.btfact = QPushButton(self)
        self.btfact.setGeometry(QtCore.QRect(200, 180, 45, 45))
        self.btfact.setFont(font)
        self.btfact.setObjectName("btfact")
        self.btnot = QPushButton('-n', self)
        self.btnot.setGeometry(QtCore.QRect(200, 230, 45, 45))
        self.btnot.setFont(font)
        self.btnot.setObjectName("btmin")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.operation = lambda x, y: x + y

        n = tuple(range(9, 0, -1))
        j = 0
        for y in (50, 100, 150):
            for x in (0, 50, 100):
                self.add_vt(x, y + 30, n[j])
                j += 1
        self.add_vt(50, 30 + 200, 0)
        self.add_vt(0, 30 + 200, '.')

        radiop = QPushButton('+', self)
        radiop.setGeometry(150, 80, 45, 45)
        radiop.setChecked(True)
        radiop.pressed.connect(lambda: self.chandgeop(lambda x, y: x + y))
        radiom = QPushButton('-', self)
        radiom.setGeometry(150, 130, 45, 45)
        radiom.pressed.connect(lambda: self.chandgeop(lambda x, y: x - y))
        radiou = QPushButton('*', self)
        radiou.setGeometry(150, 180, 45, 45)
        radiou.pressed.connect(lambda: self.chandgeop(lambda x, y: x * y))
        radiod = QPushButton('/', self)
        radiod.setGeometry(150, 230, 45, 45)
        radiod.pressed.connect(lambda: self.chandgeop(lambda x, y: x / y))

        self.ans = QLCDNumber(self)
        self.ans.setGeometry(35, 0, self.width() - 35, 75)
        self.ans.display(0)

        rs = QPushButton('C', self)
        rs.setGeometry(100, 230, 45, 45)
        rs.pressed.connect(self.reset)

        rse = QPushButton('CE', self)
        rse.resize(35, 75)
        rse.pressed.connect(self.resetcurrent)

        bt = QPushButton('Посчитать', self)
        bt.setGeometry(0, self.height() - 220, self.width(), 70)
        bt.pressed.connect(self.clicked)

        self.errorw = QLabel(self)
        self.errorw.setGeometry(0, self.height() - 150, self.width(), 150)
        self.errorw.setStyleSheet('background-color: black; color: white')
        self.reset()
        self.btfact.pressed.connect(self.fact)
        self.btnot.pressed.connect(self.setnot)
        self.show()

    def clicked(self):
        try:
            ans = self.operation(float(self.num1), float(self.num2))
            ans = str(int(ans)) if ans.is_integer() else str(ans)
            self.ans.display(ans)
            self.num1 = ans
            self.num = True
            self.new = True
        except Exception as f:
            self.errorw.setText(str(f))
            self.reset()

    def chandgeop(self, op):
        self.operation = op
        self.num = False

    def changenum(self, n):
        if self.num:
            if self.new:
                self.num1 = '0'
                self.num2 = '0'
            self.num1 = (self.num1 + n).replace('..', '.')
            self.ans.display(float(self.num1))
        else:
            if self.new:
                self.num2 = '0'
            self.num2 = (self.num2 + n).replace('..', '.')
            self.ans.display(float(self.num2))
        self.new = False

    def add_vt(self, x, y, n):
        n = str(n)
        bt = QPushButton(n, self)
        bt.setGeometry(x, y, 45, 45)
        bt.pressed.connect(lambda: self.changenum(n))

    def reset(self):
        self.num = True
        self.num1 = '0'
        self.num2 = '0'
        self.ans.display(0)
        self.new = False
        self.errorw.setText('')

    def resetcurrent(self):
        if self.num:
            self.num1 = '0' if self.num1 == '0' or len(
                self.num1) == 1 or len(self.num1) == 2 and '-' in self.num1 else self.num1[:-1]
            self.ans.display(float(self.num1))
        else:
            self.num2 = '0' if self.num2 == '0' or len(
                self.num2) == 1 or len(self.num2) == 2 and '-' in self.num2 else self.num2[:-1]
            self.ans.display(float(self.num2))

    def fact(self):
        try:
            if self.num:
                self.num1 = str(factorial(float(self.num1)))
                self.ans.display(float(self.num1))
            else:
                self.num2 = str(factorial(float(self.num2)))
                self.ans.display(float(self.num2))
        except ValueError as e:
            self.errorw.setText(str(e))

    def setnot(self):
        if self.num:
            ans = -float(self.num1)
            self.num1 = str(ans) if not ans.is_integer() else str(int(ans))
            self.ans.display(float(self.num1))
        else:
            ans = -float(self.num2)
            self.num2 = str(ans) if not ans.is_integer() else str(int(ans))
            self.ans.display(float(self.num2))

    def retranslateUi(self, Calc):
        _translate = QtCore.QCoreApplication.translate
        Calc.setWindowTitle(_translate("Calc", "Calculator"))
        self.groupBox.setTitle(_translate("Calc", "GroupBox"))
        self.btpow.setText(_translate("Calc", "^n"))
        self.btsqrt.setText(_translate("Calc", "^(1/n)"))
        self.btfact.setText(_translate("Calc", "n!"))


app = QApplication(sys.argv)
a = Ui_Calc()
a.show()
sys.exit(app.exec_())
