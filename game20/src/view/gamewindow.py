from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMessageBox


class GameWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.presenter = None

    def setup_ui(self):
        self.setWindowTitle('CYBERBOX')
        self.setFixedSize(536, 431)
        self.center()

    def __restart(self):
        self.presenter.restart()
        self.paintEvent(None)
        self.update()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.presenter.paint(qp)
        qp.end()

    def keyPressEvent(self, event):
        key = event.key()
        result = False
        if key == Qt.Key_Left:
            result = result or self.presenter.action(3)
        elif key == Qt.Key_Right:
            result = result or self.presenter.action(1)
        elif key == Qt.Key_Down:
            result = result or self.presenter.action(2)
        elif key == Qt.Key_Up:
            result = result or self.presenter.action(0)
        elif key in (ord('r'), ord('R'), ord('к'), ord('К')):
            self.__restart()
        if result:
            self.paintEvent(event)
            self.update()

    def win(self):
        QMessageBox.about(self, 'Мои поздравления!', 'Вы победили!')
        return 0
