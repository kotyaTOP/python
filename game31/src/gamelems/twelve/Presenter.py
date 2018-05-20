import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from src.gamelems.twelve.Field import *
from src.gamelems.twelve.Draw import *


class Presenter:

    def __init__(self, field: Field, window: My_Window):
        self.field = field
        self.window = window

    def draw_field(self, painter: QPainter):
        size = self.window.geometry()
        row_count = self.field.row_count
        col_count = self.field.col_count
        kx = size.width()/col_count
        ky = size.height()/row_count
        painter.setBrush(QBrush(Qt.SolidPattern))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for r in range(row_count):
            painter.drawLine(0, r*ky, size.width(), r*ky)
        for c in range(col_count):
            painter.drawLine(c*kx, 0, c*kx, size.height())



