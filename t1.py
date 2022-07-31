from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

app = QApplication(sys.argv)

w = QWidget()
w.resize((1920 / 2), (1080 / 2))
palette = QPalette()
pix = QPixmap("./background.jpg")

pix = pix.scaled(w.width(),w.height())

palette.setBrush(QPalette.Background, QBrush(pix))
w.setPalette(palette)

w.show()

if __name__ == '__main__':
    sys.exit(app.exec_())
