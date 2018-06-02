from __future__ import print_function
from src.Circle import *
from src.Game import *
from src.Presenter import *
from src.Window import *


my_field = Field(9, 9)
app = QApplication(sys.argv)
mw = MyWindow()
pr = Presenter(my_field, mw)
mw.presenter = pr
mw.show()
sys.exit(app.exec_())

