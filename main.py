# libraries
import sys
import pandas as pd
import codecs
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt


# other py-files
from client import request
from methods import *
from errors import *


# progress table model (done)
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


# main window class (done)
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
            self.reg = RegWidget()
            self.reg.show()
            self.close()
        except Exception as e:
            print(f'Enter widget: go_registration: {e}')

    # open profile window and close this
    def go_profile(self):
        username = self.login.text()
        password = self.password.text()
        try:
            # уязвимость пользовательских данных!
            user_data = request(f'!gai {username}').split(' ')[1].split('!')
            if password != user_data[3]:
                raise LoginError
            with open('Data/save_last_enter.txt', 'w') as data:
                data.write('!'.join(user_data))
            self.profile = ProfileWidget()
            self.profile.show()
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
                    with open('Data/server_ip', 'w') as server:
                        server.write(ip)
        except Exception as e:
            print(f'Enter widget: change_server_ip: {e}')


# registration window (done)
class RegWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(RegWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Registration.ui', self)
        self.show()
        # buttons
        self.registration.clicked.connect(self.registrate)
        self.exit.clicked.connect(self.go_enter)

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
                user_data = request(f'!gai {name}').split(' ')[1].split('!')
                with open('Data/save_last_enter.txt', 'w') as data:
                    data.write('!'.join(user_data))
                self.profile = ProfileWidget()
                self.profile.show()
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

    # exit from profile to enter window
    def go_enter(self):
        try:
            self.enter = EnterWidget()
            self.enter.show()
            self.close()
        except Exception as e:
            print(f'Reg widget widget: exit: {e}')


# profile window (done)
class ProfileWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(ProfileWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Profile.ui', self)
        self.show()
        # user info
        try:
            with open('Data/save_last_enter.txt') as uinfo:
                u = uinfo.readline().split('!')
                self.username = u[1]
                self.avatar = u[4]
                self.dates = u[6]
        except Exception as e:
            print(f'Profile widget: user: {e}')
        # widgets
        try:
            self.name.setText(self.username)
            self.change_avatar.clicked.connect(self.change_photo)
            self.theory.triggered.connect(self.go_theory)
            self.practice.triggered.connect(self.go_practice)
            self.exit.triggered.connect(self.go_enter)
        except Exception as e:
            print(f'Profile widget: widgets: {e}')
        # progress table
        try:
            d = list(map(lambda x: x.split('!'), self.dates.split('?')))
            data = pd.DataFrame(d, columns=['Date', 'Theme', 'Progress'], index=list(range(1, len(d) + 1)))
            self.model = TableModel(data)
            self.progress_table.setModel(self.model)
        except Exception as e:
            print(f'Profile widget: table: {e}')
        # avatar image
        try:
            if self.avatar is not None:
                image_from_binary(self.avatar)
                self.photo.setPixmap(QtGui.QPixmap('Data/Images/avatar.jpg'))
        except Exception as e:
            print(f'Profile widget: avatar: {e}')

    # open theory window and close this
    def go_theory(self):
        try:
            self.theo = TheoryWidget()
            self.theo.show()
            self.close()
        except Exception as e:
            print(f'Profile widget: go_theory: {e}')

    # open practice window and close this
    def go_practice(self):
        try:
            self.prac = PracticeWidget()
            self.prac.show()
            self.close()
        except Exception as e:
            print(f'Profile widget: go_theory: {e}')

    # exit from profile to enter window
    def go_enter(self):
        try:
            # clear saves
            with open('Data/save_last_enter.txt', 'w') as ent:
                ent.write('')
            self.enter = EnterWidget()
            self.enter.show()
            self.close()
        except Exception as e:
            print(f'Profile widget: exit: {e}')

    # change photo
    def change_photo(self):
        try:
            avatar_d = QFileDialog.getOpenFileName(self, "Open file", 'C:',
                                                   'JPG File (*.jpg);;PNG File (*.png)')
            ava = Image.open(avatar_d[0])
            ava.save('Data/Images/avatar.jpg')
            new_avatar = image_to_size('Data/Images/avatar.jpg', 300)
            new_avatar.save('Data/Images/avatar.jpg')
            bin_img = image_to_binary('Data/Images/avatar.jpg')
            request(f'!ui {self.username}!{bin_img}')
            self.photo.setPixmap(QtGui.QPixmap('Data/Images/avatar.jpg'))
        except Exception as e:
            print(f'Profile widget: change_photo: {e}')


# theory window (done)
class TheoryWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(TheoryWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Theory.ui', self)
        # buttons
        self.profile.triggered.connect(self.go_profile)
        self.practice.triggered.connect(self.go_practice)
        self.probability.triggered.connect(self.get_probability)
        with codecs.open(u'Data/Theory/Probability.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))

    def go_profile(self):
        try:
            self.prof = ProfileWidget()
            self.prof.show()
            self.close()
        except Exception as e:
            print(f'Theory widget: go_profile: {e}')
            self.ent = EnterWidget()
            self.ent.show()
            self.close()

    def go_practice(self):
        try:
            self.prac = PracticeWidget()
            self.prac.show()
            self.close()
        except Exception as e:
            print(f'Theory widget: go_practice: {e}')

    def get_probability(self):
        with codecs.open(u'Data/Theory/Probability.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))


# Practice Window
class PracticeWidget(QMainWindow):
    # installation window
    def __init__(self):
        super(PracticeWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Practice.ui', self)
        # buttons
        self.save1.clicked.connect(self.check1)
        self.save2.clicked.connect(self.check2)
        self.save3.clicked.connect(self.check3)
        self.save4.clicked.connect(self.check4)
        self.save5.clicked.connect(self.check5)
        self.profile.triggered.connect(self.go_profile)
        self.theory.triggered.connect(self.go_theory)
        self.probability.triggered.connect(self.get_probability)
        self.planimetry.triggered.connect(self.get_planimetry)
        self.movement.triggered.connect(self.get_movement)
        self.work.triggered.connect(self.get_work)
        self.choose = 'Probability'
        with codecs.open(u'Data/Practice/Probability/Pr_1.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_2.html', 'r', 'utf-8') as html:
            self.textBrowser_2.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_3.html', 'r', 'utf-8') as html:
            self.textBrowser_3.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_4.html', 'r', 'utf-8') as html:
            self.textBrowser_4.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_5.html', 'r', 'utf-8') as html:
            self.textBrowser_5.setHtml(''.join(html.readlines()))

    def go_profile(self):
        try:
            self.prof = ProfileWidget()
            self.prof.show()
            self.close()
        except Exception as e:
            print(f'Practice widget: go_profile: {e}')
            self.ent = EnterWidget()
            self.ent.show()
            self.close()

    def go_theory(self):
        try:
            self.theory = TheoryWidget()
            self.theory.show()
            self.close()
        except Exception as e:
            print(f'Practice widget: go_practice: {e}')

    def get_probability(self):
        self.choose = 'Probability'
        with codecs.open(u'Data/Practice/Probability/Pr_1.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_2.html', 'r', 'utf-8') as html:
            self.textBrowser_2.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_3.html', 'r', 'utf-8') as html:
            self.textBrowser_3.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_4.html', 'r', 'utf-8') as html:
            self.textBrowser_4.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Probability/Pr_5.html', 'r', 'utf-8') as html:
            self.textBrowser_5.setHtml(''.join(html.readlines()))

    def get_planimetry(self):
        self.choose = 'Planimetry'
        with codecs.open(u'Data/Practice/Planimetry/Pl_1.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Planimetry/Pl_2.html', 'r', 'utf-8') as html:
            self.textBrowser_2.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Planimetry/Pl_3.html', 'r', 'utf-8') as html:
            self.textBrowser_3.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Planimetry/Pl_4.html', 'r', 'utf-8') as html:
            self.textBrowser_4.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Planimetry/Pl_5.html', 'r', 'utf-8') as html:
            self.textBrowser_5.setHtml(''.join(html.readlines()))

    def get_movement(self):
        self.choose = 'Tasks for movement'
        with codecs.open(u'Data/Practice/Tasks for movement/T_1.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Tasks for movement/T_2.html', 'r', 'utf-8') as html:
            self.textBrowser_2.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Tasks for movement/T_3.html', 'r', 'utf-8') as html:
            self.textBrowser_3.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Tasks for movement/T_4.html', 'r', 'utf-8') as html:
            self.textBrowser_4.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Tasks for movement/T_5.html', 'r', 'utf-8') as html:
            self.textBrowser_5.setHtml(''.join(html.readlines()))

    def get_work(self):
        self.choose = 'Work'
        with codecs.open(u'Data/Practice/Work/W_1.html', 'r', 'utf-8') as html:
            self.textBrowser.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Work/W_2.html', 'r', 'utf-8') as html:
            self.textBrowser_2.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Work/W_3.html', 'r', 'utf-8') as html:
            self.textBrowser_3.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Work/W_4.html', 'r', 'utf-8') as html:
            self.textBrowser_4.setHtml(''.join(html.readlines()))
        with codecs.open(u'Data/Practice/Work/W_5.html', 'r', 'utf-8') as html:
            self.textBrowser_5.setHtml(''.join(html.readlines()))

    def check1(self):
        try:
            if self.choose == 'Probability':
                with open('Data/Practice/Probability/Pr_1.txt', 'r') as ans:
                    if self.answer1.text() in ans.readline().split('!'):
                        self.answer1.setStyleSheet('background-color: rgb(0, 255, 0);')
                    else:
                        self.answer1.setStyleSheet('background-color: rgb(255, 0, 0);')
            elif self.choose == 'Planimetry':
                with open('Data/Practice/Planimetry/Pl_1.txt', 'r') as ans:
                    if self.answer1.text() in ans.readline().split('!'):
                        self.answer1.setStyleSheet('background-color: rgb(0, 255, 0);')
                    else:
                        self.answer1.setStyleSheet('background-color: rgb(255, 0, 0);')
            elif self.choose == 'Tasks for movement':
                with open('Data/Practice/Tasks for movement/T_1.txt', 'r') as ans:
                    if self.answer1.text() in ans.readline().split('!'):
                        self.answer1.setStyleSheet('background-color: rgb(0, 255, 0);')
                    else:
                        self.answer1.setStyleSheet('background-color: rgb(255, 0, 0);')
            elif self.choose == 'Work':
                with open('Data/Practice/Work/W_1.txt', 'r') as ans:
                    if self.answer1.text() in ans.readline().split('!'):
                        self.answer1.setStyleSheet('background-color: rgb(0, 255, 0);')
                    else:
                        self.answer1.setStyleSheet('background-color: rgb(255, 0, 0);')
        except Exception as e:
            print(e)

    def check2(self):
        if self.choose == 'Probability':
            with open('Data/Practice/Probability/Pr_2.txt', 'r') as ans:
                if self.answer2.text() in ans.readline().split('!'):
                    self.answer2.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer2.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Planimetry':
            with open('Data/Practice/Planimetry/Pl_2.txt', 'r') as ans:
                if self.answer2.text() in ans.readline().split('!'):
                    self.answer2.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer2.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Tasks for movement':
            with open('Data/Practice/Tasks for movement/T_2.txt', 'r') as ans:
                if self.answer2.text() in ans.readline().split('!'):
                    self.answer2.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer2.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Work':
            with open('Data/Practice/Work/W_2.txt', 'r') as ans:
                if self.answer2.text() in ans.readline().split('!'):
                    self.answer2.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer2.setStyleSheet('background-color: rgb(255, 0, 0);')

    def check3(self):
        if self.choose == 'Probability':
            with open('Data/Practice/Probability/Pr_3.txt', 'r') as ans:
                if self.answer3.text() in ans.readline().split('!'):
                    self.answer3.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer3.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Planimetry':
            with open('Data/Practice/Planimetry/Pl_3.txt', 'r') as ans:
                if self.answer3.text() in ans.readline().split('!'):
                    self.answer3.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer3.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Tasks for movement':
            with open('Data/Practice/Tasks for movement/T_3.txt', 'r') as ans:
                if self.answer3.text() in ans.readline().split('!'):
                    self.answer3.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer3.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Work':
            with open('Data/Practice/Work/W_3.txt', 'r') as ans:
                if self.answer3.text() in ans.readline().split('!'):
                    self.answer3.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer3.setStyleSheet('background-color: rgb(255, 0, 0);')

    def check4(self):
        if self.choose == 'Probability':
            with open('Data/Practice/Probability/Pr_4.txt', 'r') as ans:
                if self.answer4.text() in ans.readline().split('!'):
                    self.answer4.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer4.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Planimetry':
            with open('Data/Practice/Planimetry/Pl_4.txt', 'r') as ans:
                if self.answer4.text() in ans.readline().split('!'):
                    self.answer4.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer4.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Tasks for movement':
            with open('Data/Practice/Tasks for movement/T_4.txt', 'r') as ans:
                if self.answer4.text() in ans.readline().split('!'):
                    self.answer4.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer4.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Work':
            with open('Data/Practice/Work/W_4.txt', 'r') as ans:
                if self.answer4.text() in ans.readline().split('!'):
                    self.answer4.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer4.setStyleSheet('background-color: rgb(255, 0, 0);')

    def check5(self):
        if self.choose == 'Probability':
            with open('Data/Practice/Probability/Pr_5.txt', 'r') as ans:
                if self.answer5.text() in ans.readline().split('!'):
                    self.answer5.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer5.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Planimetry':
            with open('Data/Practice/Planimetry/Pl_5.txt', 'r') as ans:
                if self.answer5.text() in ans.readline().split('!'):
                    self.answer5.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer5.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Tasks for movement':
            with open('Data/Practice/Tasks for movement/T_5.txt', 'r') as ans:
                if self.answer5.text() in ans.readline().split('!'):
                    self.answer5.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer5.setStyleSheet('background-color: rgb(255, 0, 0);')
        elif self.choose == 'Work':
            with open('Data/Practice/Work/W_5.txt', 'r') as ans:
                if self.answer5.text() in ans.readline().split('!'):
                    self.answer5.setStyleSheet('background-color: rgb(0, 255, 0);')
                else:
                    self.answer5.setStyleSheet('background-color: rgb(255, 0, 0);')


# start
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # try to fast enter
    try:
        with open('Data/save_last_enter.txt', 'r') as data:
            info = data.readline().split('!')
            usr_data = request(f'!gai {info[1]}')
            user_data = usr_data.split(' ')[1].split('!')
            if info[3] != user_data[3]:
                raise LoginError
            profile = ProfileWidget()
            profile.show()
    except Exception as e:
        print(f'Start: {e}')
        enter = EnterWidget()
        enter.show()
    sys.exit(app.exec_())
