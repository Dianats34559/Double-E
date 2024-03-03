# библиотеки
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize

from Enter import Ui_MainWindow as Enter


# класс Главного_Окна
class EnterWidget(QMainWindow, Enter):
    # инициализация Главного_Окна
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = EnterWidget()
    main.show()
    sys.exit(app.exec_())