import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

app = QApplication([])

widget = QWidget()

uic.loadUi("E:/Learning/00_Git/01_Tools/resize_image/UI.ui", widget)

widget.show()

sys.exit(app.exec())