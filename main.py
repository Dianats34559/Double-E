# libraries
import sys
# from screeninfo import get_monitors
# other py-files
from Common_files.client import request
from Common_files.methods import *
from Common_files.errors import *
# widget-files



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
            drop_to_profile(info[0], info[1], info[2])
    except LoginError:
        print('Wrong password saved')
    except Exception as e:
        print(f'Start: {e}')
        drop_to_enter()
    sys.exit(app.exec_())
