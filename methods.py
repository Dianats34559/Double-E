from base64 import b64encode, b64decode
from io import BytesIO
from PIL import Image
from PyQt5.QtWidgets import *


# error message
def error_box(msg: str):
    error = QMessageBox()
    error.setWindowTitle('Ошибка')
    error.setText(msg)
    error.setIcon(QMessageBox.Warning)
    error.exec()


# hardness of password
def check_hard(pas: str):
    num = '1234567890-_'
    if pas == pas.upper():
        return False
    if pas == pas.lower():
        return False
    if len(pas) < 8:
        return False
    for i in pas:
        if i in num:
            return True
    return False


# danger symbol check
def check_symbol(word: str):
    with open('Data/bad_symbols.txt') as symbols:
        for i in symbols.readline():
            if i in word:
                return False
        return True


# image to binary code
def image_to_binary(img_path: str):
    with open(img_path, 'rb') as f:
        binary = b64encode(f.read())
    return binary


# binary code to image
def image_from_binary(binary):
    img = BytesIO(b64decode(eval(binary)))
    pil_img = Image.open(img)
    pil_img.save('Data/Images/avatar.jpg')


# resize image (to do smaller)
def image_to_size(img_path: str, img_size: int):
    new_img = Image.open(img_path)
    if new_img.size[0] > new_img.size[1]:
        delta = img_size / float(new_img.size[1])
        x = int(float(new_img.size[0]) * delta)
        y = int(float(new_img.size[1]) * delta)
        cropy = ((x - img_size) // 2, 0, (x - img_size) // 2 + img_size, img_size)
        new_img = new_img.resize((x, y)).crop(cropy)
    else:
        delta = img_size / float(new_img.size[0])
        x = int(float(new_img.size[0]) * delta)
        y = int(float(new_img.size[1]) * delta)
        cropy = (0, (y - img_size) // 2, img_size, (y - img_size) // 2 + img_size)
        new_img = new_img.resize((x, y)).crop(cropy)
    return new_img
