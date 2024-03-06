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


class ConnectError(Exception):
    pass


# error message
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
        # windows
        self.profile = None
        # buttons
        self.registration.clicked.connect(self.registrate)

    # registration and open profile window
    def registrate(self):
        try:
            name = self.login.text()
            password = self.password.text()
            c_password = self.password1.text()
            if password != c_password:
                raise PasswordError
            if not check_hard(password):
                raise HardError
            if not check_symbol(password) or not check_symbol(name):
                raise SymbolError
            if self.M_radio.isChecked():
                gender = '1'
            elif self.F_radio.isChecked():
                gender = '0'
            else:
                raise GenderError
            # sending request on server
            try:
                ans = request(f'r! {name}!{password}!{gender}')
                if ans != '!Success':
                    error_box(ans[1:])
            except Exception:
                raise ConnectError
            try:
                user_data = request(f'!gai {name}').split(' ')[1].split('!')
                self.profile = ProfileWidget(user_data[1], user_data[4], user_data[6])
                self.profile.show()
                self.close()
            except Exception as e:
                raise ConnectError
        except ConnectError:
            error_box("Ошибка соединения с сервером")
        except PasswordError:
            error_box('Пароли не совпадают')
        except GenderError:
            error_box('Гендер не выбран')
        except SymbolError:
            error_box('''Использованы недопустимые символы:
!,./?\|'":;(){}[]@#$%^&*~`№><=+''')
        except HardError:
            error_box('''Пароль слишком простой:
1. Длина должна быть не менее 8 символов
2. Пароль должен содержать заглавные и строчные символы
3. Пароль должен содержать цифры, или "_", или "-"''')
        except Exception as e:
            error_box('Произошла непредвиденная ошибка')
            print(e)


# profile window
class ProfileWidget(QMainWindow):
    # initialisation window
    def __init__(self, username, avatar, dates):
        super(ProfileWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Profile.ui', self)
        self.show()
        # user info
        self.username = username
        self.avatar = avatar
        self.dates = dates


# start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enter = EnterWidget()
    enter.show()
    sys.exit(app.exec_())
