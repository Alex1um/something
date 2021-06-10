# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calendar.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import datetime


class Ui_Calendar(object):

    def setupUi(self):
        self.setObjectName("self")
        self.resize(580, 499)
        self.calendar = QtWidgets.QCalendarWidget(self)
        self.calendar.setGeometry(QtCore.QRect(0, 0, 392, 250))
        self.calendar.setObjectName("calendar")
        self.dates = QtWidgets.QListWidget(self)
        self.dates.setGeometry(QtCore.QRect(0, 250, 571, 241))
        self.dates.setObjectName("dates")
        self.dates.setModelColumn(3)
        self.timew = QtWidgets.QTimeEdit(self)
        self.timew.setGeometry(QtCore.QRect(390, 0, 190, 21))
        self.timew.setObjectName("timew")
        self.addform = QtWidgets.QPushButton('add', self)
        self.addform.setGeometry(QtCore.QRect(390, 220, 180, 28))
        self.addform.setObjectName("addform")
        self.te = QtWidgets.QTextEdit(self)
        self.te.setGeometry(QtCore.QRect(390, 40, 180, 180))
        self.te.setObjectName("te")
        self.lb = QtWidgets.QLabel('Discription', self)
        self.lb.setGeometry(QtCore.QRect(390, 20, 190, 20))
        self.lb.setObjectName("lb")

        QtCore.QMetaObject.connectSlotsByName(self)


class Calendar(QtWidgets.QWidget, Ui_Calendar):

    def __init__(self):
        super().__init__()
        self.items = []
        self.setupUi()
        self.addform.pressed.connect(self.add_s)

    def add_s(self):
        self.items.append((self.calendar.selectedDate().toPyDate(), self.timew.time().toPyTime(), self.te.toPlainText()))
        self.items.sort(key=lambda x: (x[0], x[1]))
        self.dates.clear()
        for i in self.items:
            self.dates.addItem(QtWidgets.QListWidgetItem(' - '.join(map(str, i))))


app = QtWidgets.QApplication(sys.argv)
a = Calendar()
a.show()
sys.exit(app.exec_())