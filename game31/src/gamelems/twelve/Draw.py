from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from src.gamelems.twelve.Field import *


class My_Window(QMainWindow):
    def __init__(self, field: Field, parent=None):
        super().__init__(parent)
        self.field = field
        self.setup_ui()
        self.presenter = None

    def setup_ui(self):
        self.setWindowTitle('Twelve')
        self.resize(475, 475)
        self.center()
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.field.paint_event(qp)
        qp.end()

    # def mousePressEvent(self, event: QMouseEvent):
    #
    #
    #         super(My_Window, self).keyPressEvent(event)
    #
    #     self.paintEvent(event)
    #
    #     if self.board.check_victory():
    #         QMessageBox.about(self, 'Congratulations!', 'You are winner!')
    #         return 0
    #
    #     self.update()