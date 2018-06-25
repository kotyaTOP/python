from __future__ import print_function
from Circle import *
from Game import *
from Presenter import *
from Window import *


my_field = Field(9, 9)
app = QApplication(sys.argv)
mw = MyWindow()
pr = Presenter(my_field, mw)
mw.presenter = pr
mw.show()
sys.exit(app.exec_())

