# libraries
from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
import pandas as pd
# other py-files
from Common_files.methods import *


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
        self.theory.triggered.connect(self.go_theory)
        self.practice.triggered.connect(self.go_practice)
        self.settings.triggered.connect(self.go_settings)
        self.exit.triggered.connect(self.go_enter)
        # progress table
        data = pd.DataFrame([
            [None, None, None],
            [None, None, None],
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ], columns=['Date', 'Theme', 'Progress'], index=list(range(1, 6)))
        self.model = TableModel(data)
        self.progress_table.setModel(self.model)

    # open theory window and close this
    def go_theory(self):
        try:
            drop_to_theory()
            self.close()
        except Exception as e:
            print(f'Profile widget: go_theory: {e}')

    # open practice window and close this
    def go_practice(self):
        try:
            drop_to_practice()
            self.close()
        except Exception as e:
            print(f'Profile widget: go_theory: {e}')

    # open settings window and close this
    def go_settings(self):
        pass

    # exit from profile to enter window
    def go_enter(self):
        try:
            # clear saves
            with open('../Data/save_last_enter.txt', 'w') as ent:
                ent.write('')
            drop_to_enter()
            self.close()
        except Exception as e:
            print(f'Profile widget: exit: {e}')
