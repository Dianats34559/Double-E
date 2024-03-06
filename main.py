# libraries
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
# from PyQt5.QtCore import Qt, QSize
# from screeninfo import get_monitors

from client import request


# error classes
class PasswordError(Exception):
    pass


class SymbolError(Exception):
    pass


class HardError(Exception):
    pass


class GenderError(Exception):
    pass


# error message
def error_box(msg):
    error = QMessageBox()
    error.setWindowTitle('Ошибка')
    error.setText(msg)
    error.setIcon(QMessageBox.Warning)
    error.exec()


# main window class
class EnterWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(EnterWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Enter.ui', self)
        self.show()
        # windows
        self.reg = None
        # buttons
        self.registration.clicked.connect(self.go_registration)

    # open registration window and close this
    def go_registration(self):
        try:
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception as e:
            print(e)


# registration window
class RegWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(RegWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Registration.ui', self)
        self.show()
        self.registration.clicked.connect(self.registrate)

    # registration and open profile window
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
            # sending request on server
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


# start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enter = EnterWidget()
    enter.show()
    sys.exit(app.exec_())
