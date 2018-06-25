from PyQt5.QtWidgets import (QWidget, QToolTip, QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QPainter, QMouseEvent

import tkinter as tk

from src.presenter.presenter import Presenter

root = tk.Tk()


class GameWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.presenter = None

    def initUI(self):
        self.setWindowTitle('game window')

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(screen_width // 2 - 400, screen_height // 2 - 240, 800, 480)

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
        self.update()
        if self.presenter.is_win():
            self.win()

    def win(self):
        QMessageBox.about(self, 'Мои поздравления!', 'Вы победили!')

    def keyPressEvent(self, e):
        if e.key() in (ord('r'), ord('R'), ord('к'), ord('К')):
            self.presenter.recolor()
        if e.key() in (ord('a'), ord('A'), ord('ф'), ord('Ф')):
            self.presenter.model.fill_line()
        self.paintEvent(None)
        self.update()
