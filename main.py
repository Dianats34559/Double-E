# libraries
import sys
from PyQt5 import uic
# from PyQt5.QtCore import Qt, QSize
# from screeninfo import get_monitors


# other py-files
from client import request
from methods import *
from errors import *


# main window class
class EnterWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(EnterWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Enter.ui', self)
        self.show()
        # windows
        self.reg = None
        self.profile = None
        # widgets
        self.registration.clicked.connect(self.go_registration)
        self.enter.clicked.connect(self.go_profile)

    # open registration window and close this
    def go_registration(self):
        try:
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception as e:
            print(e)

    # open profile window and close this
    def go_profile(self):
        username = self.login.text()
        password = self.password.text()
        try:
            # уязвимость пользовательских данных!
            usr_data = request(f'!gai {username}')
            user_data = usr_data.split(' ')[1].split('!')
            if password != user_data[3]:
                raise LoginError
            self.profile = ProfileWidget(user_data[1], user_data[4], user_data[6])
            self.profile.show()
            self.close()
        except LoginError:
            error_box('Не верный пароль')
        except Exception as e:
            error_box("Ошибка соединения с сервером")
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
                ans = request(f'!r {name}!{password}!{gender}')
                print(ans)
                if ans != '!Success':
                    error_box(ans[1:])
            except Exception as e:
                print(e)
                raise ConnectError
            try:
                usr_data = request(f'!gai {name}')
                user_data = usr_data.split(' ')[1].split('!')
                self.profile = ProfileWidget(user_data[1], user_data[4], user_data[6])
                self.profile.show()
                self.close()
            except Exception as e:
                print(e)
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
        # widgets
        self.name.setText(self.username)


# start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    enter = EnterWidget()
    enter.show()
    sys.exit(app.exec_())
