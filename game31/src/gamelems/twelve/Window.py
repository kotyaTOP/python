from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from src.gamelems.twelve.Field import *


class My_Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.manager = None

    def level(self):
        lvl = QMessageBox()
        lvl.setWindowTitle('Select color theme')
        qbg = QButtonGroup(lvl)
        qbg.addButton(QCheckBox('Purple', lvl))
        qbg.buttons()[0].move(10, 20 * 0)
        qbg.addButton(QCheckBox('For mortals', lvl))
        qbg.buttons()[1].move(10, 20 * 1)
        qbg.buttons()[0].setCheckState(2)
        lvl.setStyleSheet('QLabel{min-width: 50px;' + 'min-height: {}px;'.format(str(len(qbg.buttons()) * 20)) + '}')
        lvl.setStandardButtons(QMessageBox.Ok)

        lvl.exec()

        for i, elem in enumerate(qbg.buttons()):
            if elem.checkState() == 2:
                self.manager.theme_dict = i

    def setup_ui(self):
        self.setWindowTitle('Twelve')
        self.setFixedSize(475, 475)
        self.center()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.manager.paint(qp)
        qp.end()

    def mousePressEvent(self, event: QMouseEvent):
        qp = QPainter()
        qp.begin(self)
        x = event.x()
        y = event.y()
        self.manager.click(x, y)
        qp.end()
        self.paintEvent(None)
        if self.manager.field.check_lose():
            QMessageBox.about(self, 'I am sorry!', 'Ты неудачник!')
            return 0
        self.update()

