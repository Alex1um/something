from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import numpy as np
import math
import re
from math import *
from pyqtgraph import PlotWidget

names = set(dir(math))
names -= {i for i in names if i[:2] == '__'}
names |= {'x'}


def is_equation(s: str):
    return False if set(re.findall('[a-z]+', s.lower())) - names else True


def make_fun_stable(f, default=None):
    def new_fun(*args, **kwargs):
        nonlocal f, default
        try:
            return f(*args, **kwargs)
        except Exception:
            return default

    return new_fun


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(805, 618)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Eq_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.Eq_edit.setGeometry(QtCore.QRect(0, 40, 801, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Eq_edit.setFont(font)
        self.Eq_edit.setText("")
        self.Eq_edit.setObjectName("Eq_edit")
        self.Eqlist = QtWidgets.QListWidget(self.centralwidget)
        self.Eqlist.setGeometry(QtCore.QRect(0, 170, 611, 391))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Eqlist.setFont(font)
        self.Eqlist.setObjectName("Eqlist")
        self.Eadd = QtWidgets.QPushButton(self.centralwidget)
        self.Eadd.setGeometry(QtCore.QRect(240, 110, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Eadd.setFont(font)
        self.Eadd.setObjectName("Eadd")
        self.Edelete = QtWidgets.QPushButton(self.centralwidget)
        self.Edelete.setGeometry(QtCore.QRect(400, 110, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.Edelete.setFont(font)
        self.Edelete.setObjectName("Edelete")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_list = QtWidgets.QLabel(self.centralwidget)
        self.lb_list.setGeometry(QtCore.QRect(10, 125, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_list.setFont(font)
        self.lb_list.setObjectName("lb_list")
        self.lb_edit = QtWidgets.QLabel(self.centralwidget)
        self.lb_edit.setGeometry(QtCore.QRect(10, 0, 771, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_edit.setFont(font)
        self.lb_edit.setObjectName("lb_edit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 805, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_file_new = QtWidgets.QAction(MainWindow)
        self.menu_file_new.setObjectName("menu_file_new")
        self.menu_plot_build = QtWidgets.QAction(MainWindow)
        self.menu_plot_build.setObjectName("menu_plot_build")
        self.menu_plot_sett = QtWidgets.QAction(MainWindow)
        self.menu_plot_sett.setObjectName("menu_plot_sett")
        self.menu_help = QtWidgets.QAction(MainWindow)
        self.menu_help.setObjectName("menu_help")
        self.menu_3.addAction(self.menu_plot_build)
        self.menu_3.addAction(self.menu_plot_sett)
        self.menu_4.addAction(self.menu_help)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Eadd.setText(_translate("MainWindow", "Добавить"))
        self.Edelete.setText(_translate("MainWindow", "Удалить"))
        self.lb_list.setText(_translate("MainWindow", "Текущие уравнения"))
        self.lb_edit.setText(_translate("MainWindow", "Уравнение"))
        self.menu_3.setTitle(_translate("MainWindow", "График"))
        self.menu_4.setTitle(_translate("MainWindow", "Помощь"))
        self.menu_file_new.setText(_translate("MainWindow", "Новый"))

        self.menu_plot_build.setText(_translate("MainWindow", "Построить"))
        self.menu_plot_sett.setText(_translate("MainWindow", "Настройки"))
        self.menu_help.setText(_translate("MainWindow", "Как пользоваться"))


class Plotting(QtWidgets.QMainWindow):
    """Основной Виджет"""
    def __init__(self):
        super().__init__()
        self.plot_widget = PlotWindow()
        # self.change_interface('Equations')
        self.current_ui = Equation(self)
        self.show()

    def show_exeption(self, message, title='Error'):
        """выброс ошибки(или текста)"""
        e_msg_box = QtWidgets.QMessageBox(self)
        e_msg_box.setWindowTitle(title)
        e_msg_box.setText(repr(message))
        e_msg_box.show()
        e_msg_box.exec()


class PlotWindow(QtWidgets.QWidget):
    """Виджет для рисования графиков"""
    def __init__(self):
        super().__init__()
        self.plot_w = PlotWidget(self)
        self.plot_w.setGeometry(QtCore.QRect(0,
                                             0,
                                             self.width(),
                                             self.height()))
        self.canvas = self.plot_w.getPlotItem()
        # self.panel = NavigationToolbar2QT(self.canvas, self, (0, 0))

    def plot(self, *data, mode='plot', **kwargs):
        """Рисование графов"""
        if mode == 'plot':
            self.canvas.addItem(self.canvas.plot(*data, **kwargs))
        return self.canvas

    def plot_clear(self):
        """Отчистка графика"""
        self.canvas.clear()


class Equation(Ui_MainWindow):
    """Класс модуля Уравнений"""

    def __init__(self, widget):
        """Инициализация элементов модуля"""
        self.settings = [-100, 100, 0.5]
        self.widget = widget
        self.setupUi(self.widget)
        self.eqs = []
        self.selected = 0
        self.default_item = 'New Equation'
        self.Eadd.pressed.connect(lambda: self.add_eq())
        self.Eqlist.itemSelectionChanged.connect(lambda: self.select_item())
        self.Eqlist.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.Eqlist.addItem(QtWidgets.QListWidgetItem(self.default_item))
        self.Eq_edit.textChanged.connect(lambda: self.rewrite_selection())
        self.Edelete.pressed.connect(lambda: self.delete_item())
        self.Eqlist.setCurrentRow(0)
        self.Eq_edit.setSelection(0, 12)
        self.widget.resizeEvent = self.resize

        """Инициализация меню"""
        self.menu_help.triggered.connect(lambda: self.show_help())
        self.menu_file_new.triggered.connect(lambda: self.reset())
        self.menu_plot_build.triggered.connect(
            lambda: (
                self.build_plot(), self.widget.plot_widget.show()))
        self.menu_plot_sett.triggered.connect(lambda: self.update_settings())

    def resize(self, *args, **kwargs):
        """Для масштабирования"""
        self.Eqlist.resize(self.widget.width(),
                           self.widget.height() - 164)
        self.Eq_edit.resize(self.widget.width(), self.Eq_edit.height())

    def reset(self):
        """Отчистка полей"""
        self.eqs = []
        self.Eqlist.clear()
        self.Eqlist.addItem(QtWidgets.QListWidgetItem(self.default_item))
        self.Eq_edit.setText(self.default_item)
        self.Eqlist.setCurrentRow(0)
        self.Eq_edit.setSelection(0, 12)
        self.selected = 0

    def show_help(self):
        """Вывод помощи"""
        mbox = QtWidgets.QMessageBox()
        mbox.setText('> Наберите Уравнение\n'
                     '> Нажмите добавить\n'
                     '> Постройте график\n')
        mbox.setWindowTitle('Как пользоваться')
        mbox.show()
        mbox.exec()

    def rewrite_selection(self):
        """Одновременное изменение текста в списке и поле"""
        try:  # TODO fix it
            self.Eqlist.selectedItems()[0].setText(self.Eq_edit.text())
        except Exception:
            pass

    def add_eq(self):
        """Добавление элемента в список."""
        try:
            new_eq = self.Eq_edit.text()
            if not self.selected and new_eq != self.default_item and \
                    new_eq not in self.eqs and is_equation(new_eq):
                self.eqs.append(new_eq)
                self.Eqlist.addItem(QtWidgets.QListWidgetItem(self.eqs[-1]))
                self.selected_to_default()
        except Exception as f:
            self.widget.show_exeption(f)

    def selected_to_default(self):
        """Сброс выделения"""
        self.Eq_edit.setText(self.default_item)
        self.Eqlist.setCurrentRow(0)
        self.Eqlist.selectedItems()[0].setText(self.default_item)
        self.Eq_edit.setSelection(0, 12)

    def delete_item(self):
        """Удаление элемента"""
        if self.selected:
            a = self.selected - 1
            self.selected = 0
            self.eqs.pop(a)
            self.selected_to_default()
            self.Eqlist.takeItem(a + 1)

    def select_item(self):
        """Выделение элемента

        Проверка, изменялся ли начальный элемент. если да -
        предупреждение, иначе - выделение выбранного элемента
        """
        if not self.selected and \
                self.Eqlist.item(0).text() != self.default_item:
            a = QtWidgets.QMessageBox()
            a.setWindowTitle('Внимание!')
            a.setText('Вы не сохранили измененное уравнение'
                      '. Вы уверены, что хотите отбросить изменения?')
            a.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Discard)
            a.show()
            res = a.exec()
            if res == QtWidgets.QMessageBox.Ok:
                try:
                    self.Eqlist.item(0).setText(self.default_item)
                except:
                    return
            elif res == QtWidgets.QMessageBox.Discard:
                try:
                    self.selected_to_default()
                except:
                    pass
                return
        elif self.selected:
            new_eq = self.Eq_edit.text()
            self.eqs[self.selected - 1] = new_eq
        try:
            self.Eq_edit.setText(self.Eqlist.selectedItems()[0].text())
            self.selected = self.Eqlist.currentRow()
        except Exception:
            pass

    def build_plot(self):
        """Построение общего графика функция"""
        self.widget.plot_widget.plot_clear()
        for eq in self.eqs:
            f = np.vectorize(make_fun_stable(eval('lambda x: ' + eq)))
            self.widget.plot_widget.plot(np.arange(*self.settings),
                                         f(np.arange(*self.settings)))

    def update_settings(self):
        """Настройки"""
        settbox = QtWidgets.QMessageBox()
        settbox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Discard)
        settbox.setWindowTitle('Настройки')
        settbox.setText('Минимально\tМаксимально\tШаг\t\t\n\n\n')
        r1, r2 = QtWidgets.QDoubleSpinBox(
            settbox), QtWidgets.QDoubleSpinBox(settbox)
        step = QtWidgets.QDoubleSpinBox(settbox)
        r2.setMinimum(-float('inf'))
        r2.setMaximum(float('inf'))
        step.setMinimum(-float('inf'))
        step.setMaximum(float('inf'))
        r1.setMinimum(-float('inf'))
        r1.setMaximum(float('inf'))
        dr1, dr2, dstep = self.settings
        r1.setValue(dr1)
        r2.setValue(dr2)
        step.setValue(dstep)
        r1.setSingleStep(0.01)
        r2.setSingleStep(0.01)
        step.setSingleStep(0.01)
        r1.move(30, 50)
        r2.move(150, 50)
        step.move(260, 50)
        settbox.show()
        ans = settbox.exec()
        if ans == QtWidgets.QMessageBox.Ok:
            r1v, r2v, stepv = r1.value(), r2.value(), step.value()
            self.settings = (min(r1v, r2v), max(r1v, r2v), stepv)


app = QtWidgets.QApplication(sys.argv)
a = Plotting()
app.exec()
