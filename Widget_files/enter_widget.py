# libraries
from PyQt5 import uic
# other py-files
from Common_files.client import request
from Common_files.methods import *
from Common_files.errors import *


# main window class
class EnterWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(EnterWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Enter.ui', self)
        self.show()
        # widgets
        self.registration.clicked.connect(self.go_registration)
        self.enter.clicked.connect(self.go_profile)
        self.server_config.clicked.connect(self.change_server_ip)

    # open registration window and close this
    def go_registration(self):
        try:
            drop_to_registration()
            self.close()
        except Exception as e:
            print(f'Enter widget: go_registration: {e}')

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
            drop_to_profile(user_data[1], user_data[4], user_data[6])
            with open('../Data/save_last_enter.txt', 'w') as data:
                data.write(f'{user_data[1]}!{user_data[4]}!{user_data[6]}!{password}')
            self.close()
        except LoginError:
            error_box('Не верный пароль')
        except Exception as e:
            error_box("Ошибка соединения с сервером")
            print(f'Enter widget: go_profile: {e}')

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
                    with open('../Data/server_ip', 'w') as server:
                        server.write(ip)
        except Exception as e:
            print(f'Enter widget: change_server_ip: {e}')
