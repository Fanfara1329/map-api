import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QByteArray

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.getImage()

    def getImage(self):
        params = {
            'll': ",".join(map(str, (self.lng.value(), self.lat.value()))),
            'spn': ",".join((map(str, (self.spn.value(), self.spn.value())))),
            'l': 'map'
        }
        map_request = "http://static-maps.yandex.ru/1.x/"
        print(params)
        response = requests.get(map_request, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        ba = QByteArray(response.content)
        self.pixmap = QPixmap()
        ok = self.pixmap.loadFromData(ba, "PNG")
        if ok:
            self.image.setPixmap(self.pixmap)

    def initUI(self):
        uic.loadUi("maps.ui", self)
        self.updateMap.clicked.connect(self.getImage)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())