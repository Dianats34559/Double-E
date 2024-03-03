# библиотеки
import sys
import pyperclip as pclip
import wikipedia
from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from pathlib import Path
from base64 import b64encode, b64decode
from io import BytesIO
# наши окна
from Enter import Ui_MainWindow as Main_Window
from Profile import Ui_MainWindow as Table_Widow
from Practice import Ui_MainWindow as
from Registration import Ui_MainWindow as Reg_Window
from Theory import Ui_MainWindow as



# класс Главного_Окна (ГОТОВО!!!)
class MainWidget(QMainWindow, Main_Window):
    # инициализация Главного_Окна
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # кнопки
        self.enter.clicked.connect(self.go_reg)
        self.registration.clicked.connect(self.go_table)

    # переход к Окну_Регистрации
    def go_reg(self):
        try:
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception as e:
            print(f'GOREG/80: {e}')

    def go_table(self):
        email = self.Edit_email.text()
        password = self.Edit_password.text()
        try:
            if not (email and password):
                raise DataExcept
            # поиск по базе данных
            data = fbh.check_user_sign(email, password)
            if data:
                self.table = TableWidget(data[1])
                self.table.show()
                self.close()
            else:
                raise PassExcept
        except DataExcept:
            error_box('Заполните все поля!')
        except fbh.UserExcept:
            error_box('Такого пользователя не существует!')
        except PassExcept:
            error_box('Неверный пароль!')
        except ConnectionExcept:
            error_box('Ошибка подключения!')
        except Exception as e:
            error_box('Произошла непредвиденная ошибка')
            print(f'GOTABLE/105: {e}')


# запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    sys.exit(app.exec_())