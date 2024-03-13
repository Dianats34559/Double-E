# libraries
from PyQt5 import uic
# other py-files
from Common_files.client import request
from Common_files.methods import *
from Common_files.errors import *


# registration window
class RegWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(RegWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Registration.ui', self)
        self.show()
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
                print(f'Reg widget: registrate (registrate): {e}')
                raise ConnectError
            try:
                usr_data = request(f'!gai {name}')
                user_data = usr_data.split(' ')[1].split('!')
                drop_to_profile(user_data[1], user_data[4], user_data[6])
                with open('../Data/save_last_enter.txt', 'w') as data:
                    data.write(f'{user_data[1]}!{user_data[4]}!{user_data[6]}!{password}')
                self.close()
            except Exception as e:
                print(f'Reg widget: registrate (enter): {e}')
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
            print(f'Reg widget: registrate: {e}')
