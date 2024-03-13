# libraries
from PyQt5 import uic
# other py-files
from Common_files.methods import *


# Practice Window
class PracticeWidget(QMainWindow):
    # installation window
    def __init__(self):
        super(PracticeWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Practice.ui', self)