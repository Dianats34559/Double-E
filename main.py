# библиотеки
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from screeninfo import get_monitors

from Enter import Ui_MainWindow as Enter
from Registration import Ui_MainWindow as Registration


# класс Главного_Окна
class EnterWidget(QMainWindow, Enter):
    # инициализация Главного_Окна
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # кнопки
        self.registration.clicked.connect(self.go_registration)

    def go_registration(self):
        try:
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception:
            print("go_registration_error")


class RegWidget(QMainWindow, Registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enter = EnterWidget()
    enter.show()
    sys.exit(app.exec_())