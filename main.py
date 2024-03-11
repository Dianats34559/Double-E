# libraries
import sys
import pandas as pd
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
# from screeninfo import get_monitors


# other py-files
from client import request
from methods import *
from errors import *


# progress table model
class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])


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
        self.server_config.clicked.connect(self.change_server_ip)

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
            with open('Data/save_last_enter.txt', 'w') as data:
                data.write(f'{user_data[1]}!{user_data[4]}!{user_data[6]}!{password}')
            self.close()
        except LoginError:
            error_box('Не верный пароль')
        except Exception as e:
            error_box("Ошибка соединения с сервером")
            print(e)

    # use method when server ip has changed
    def change_server_ip(self):
        try:
            ip, okPressed = QInputDialog.getText(self, "IP-адрес сервера",
                                                 "Введите IP-адрес своего сервера:",
                                                 QLineEdit.Normal, "")
            if okPressed and ip != '':
                if ip.count('.') != 3 or len(list(filter(lambda x: 0 <= int(x) < 256, ip.split('.')))) != 4:
                    error_box('Невозможный ip-адрес')
                else:
                    with open('Data/server_ip', 'w') as server:
                        server.write(ip)
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
                with open('Data/save_last_enter.txt', 'w') as data:
                    data.write(f'{user_data[1]}!{user_data[4]}!{user_data[6]}!{password}')
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
        self.practice.clicked.connect(self.go_practice)
        # progress table
        data = pd.DataFrame([
            [1, 9, 2],
            [1, 0, -1],
            [3, 5, 2],
            [3, 3, 2],
            [5, 8, 9],
        ], columns=['Date', 'Theme', 'Progress'], index=list(range(1, 6)))
        self.model = TableModel(data)
        self.progress_table.setModel(self.model)

    def go_practice(self):
        try:
            self.practice = PracticeWidget()
            self.practice.show()
            self.close()
        except Exception as e:
            print(e)

    def exit(self):
        try:
            with open('Data/save_last_enter.txt', 'w') as ent:
                ent.write('')
            self.enter = EnterWidget()
            self.enter.show()
            self.close()
        except Exception as e:
            print(e)


# Practice Window
class PracticeWidget(QMainWindow):
    # installation window
    def __init__(self):
        super(PracticeWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Practice.ui', self)


# start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # try to fast enter
    try:
        with open('Data/save_last_enter.txt', 'r') as data:
            info = data.readline().split('!')
            usr_data = request(f'!gai {info[0]}')
            user_data = usr_data.split(' ')[1].split('!')
            if info[3] != user_data[3]:
                raise LoginError
            profile = ProfileWidget(info[0], info[1], info[2])
            profile.show()
    except Exception as e:
        print(e)
        enter = EnterWidget()
        enter.show()
    sys.exit(app.exec_())
