from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from Game import *


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.presenter = None

    def setup_ui(self):
        self.setWindowTitle('Lines')
        self.setFixedSize(432, 472)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.presenter.paint(qp)
        qp.end()

    def mousePressEvent(self, event: QMouseEvent):
        qp = QPainter()
        qp.begin(self)
        x = event.x()
        y = event.y()
        self.presenter.click(x, y)
        qp.end()
        self.paintEvent(None)
        if self.presenter.field.check_lose():
            QMessageBox.about(self, 'I am sorry!', 'Ты неудачник!')
            return 0
        self.update()

