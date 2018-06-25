import sys
from PyQt5.QtWidgets import QApplication, QWidget
from src.Game import Field
from src.Window import MyWindow
from src.Presenter import Presenter

app = QApplication(sys.argv)
field = Field(3, 3)
window = MyWindow()
presenter = Presenter(field, window)
window.presenter = presenter
window.show()
sys.exit(app.exec_())
