# библиотеки
import sys
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from screeninfo import get_monitors

from client import request


class PasswordError(Exception):
    pass


class SymbolError(Exception):
    pass


class HardError(Exception):
    pass


class GenderError(Exception):
    pass


def error_box(msg: str):
    error = QMessageBox()
    error.setWindowTitle('Ошибка')
    error.setText(msg)
    error.setIcon(QMessageBox.Warning)
    error.exec()


def check_hard(pas: str):
    num = '1234567890-_'
    if pas == pas.upper():
        return False
    if pas == pas.lower():
        return False
    if len(pas) < 8:
        return False
    for i in pas:
        if i in num:
            return True
    return False


def check_symbol(word: str):
    with open('Data/bad_symbols.txt') as symbols:
        for i in symbols.readline():
            if i in word:
                return False
        return True



# класс Главного_Окна
class EnterWidget(QMainWindow):
    # инициализация Главного_Окна
    def __init__(self):
        super(EnterWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Enter.ui', self)
        self.show()
        self.reg = None
        # кнопки
        self.registration.clicked.connect(self.go_registration)

    def go_registration(self):
        try:
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception as e:
            print(e)


class RegWidget(QMainWindow):
    def __init__(self):
        super(RegWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Registration.ui', self)
        self.show()
        self.registration.clicked.connect(self.registrate)

    def registrate(self):
        try:
            name = self.login.text()
            password = self.password.text()
            c_password = self.password1.text()
            if password != c_password:
                raise PasswordError
            if self.M_radio.isChecked():
                gender = '1'
            elif self.F_radio.isChecked():
                gender = '0'
            else:
                raise GenderError
            ans = request(f'r! {name}!{password}!{gender}')
            if ans != '!Success':
                error_box(ans[1:])
        except PasswordError:
            error_box('Пароли не совпадают')
        except GenderError:
            error_box('Гендер не выбран')
        except SymbolError:
            error_box('Использованы недопустимые символы')
        except HardError:
            error_box('Пароль слишком простой')
        except Exception as e:
            error_box('Произошла непредвиденная ошибка')
            print(e)


# запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enter = EnterWidget()
    enter.show()
    sys.exit(app.exec_())