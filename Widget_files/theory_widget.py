# libraries
from PyQt5 import uic
# other py-files
from Common_files.methods import *


# theory window
class TheoryWidget(QMainWindow):
    # initialisation window
    def __init__(self):
        super(TheoryWidget, self).__init__()
        uic.loadUi('Data/Ui_files/Theory.ui', self)