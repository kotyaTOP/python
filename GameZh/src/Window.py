from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.presenter = None
        self.old_x = None
        self.old_y = None

    def setup_ui(self):
        self.setWindowTitle('Lines')
        self.setFixedSize(6 * 50, 6 * 50 + 40)
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
        self.presenter.press(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.presenter.move(event.x(), event.y())
        self.update()

    def mouseReleaseEvent(self, event):
        self.presenter.release()
        self.update()
        if self.presenter.field.check_win():
            QMessageBox.about(self, 'WOW!', 'You are win!!!' + '\n' + 'Your score: ' + str(self.presenter.field.score))
            return 0

