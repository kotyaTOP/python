from __future__ import print_function
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from src.gamelems.twelve.Field import *
from src.gamelems.twelve.Square import *
from src.gamelems.twelve.Presenter import *


my_field = Field(5, 5)
app = QApplication(sys.argv)
mw = My_Window()
pr = Presenter(my_field, mw)
mw.presenter = pr
mw.show()
sys.exit(app.exec_())
