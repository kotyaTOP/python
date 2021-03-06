import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from src.gamelems.twelve.Field import *
from src.gamelems.twelve.Window import *


class Manager:

    def __init__(self, field: Field, window: My_Window):
        self.field = field
        self.window = window
        self.theme_dict = None

    def paint(self, qp: QPainter):
        self.draw_field(qp)
        self.draw_square(qp)

    def draw_field(self, painter: QPainter):
        size = self.window.geometry()
        row_count = self.field.row_count
        col_count = self.field.col_count
        kx = size.width() / col_count
        ky = size.height() / row_count
        col1 = QColor(0, 0, 0)
        col1.setNamedColor('#D8BFD8')
        pen = QPen(col1, 4, Qt.SolidLine)
        painter.setPen(pen)
        for r in range(row_count):
            painter.drawLine(0, r * ky, size.width(), r * ky)
        for c in range(col_count):
            painter.drawLine(c * kx, 0, c * kx, size.height())

    def draw_square(self, painter: QPainter):
        size = self.window.geometry()
        row_count = self.field.row_count
        col_count = self.field.col_count
        kx = size.width() // col_count
        ky = size.height() // row_count
        for y, row in enumerate(self.field.matrix):
            for x, elem in enumerate(row):
                col1 = QColor(0, 0, 0)
                if self.theme_dict == 0:
                    col1.setNamedColor('#FFDAB9')
                else:
                    col1.setNamedColor('#FFFFFF')
                col2 = QColor(0, 0, 0)
                if self.theme_dict == 0:
                    col2.setNamedColor('#FFEFD5')
                else:
                    col2.setNamedColor('#000000')
                painter.setPen(col2)
                painter.setFont(QFont('Decorative', 40))
                painter.setBrush(col1)
                painter.drawRect(kx * x + 2, ky * y + 2, kx - 4, ky - 4)
                if elem is not None:
                    if self.theme_dict == 0:
                        col1.setNamedColor(self.get_color(elem.val))
                    else:
                        col1.setNamedColor(self.get_color2(elem.val))
                    painter.setBrush(col1)
                    number = str(elem.val)
                    width = QFontMetrics.width(painter.fontMetrics(), number)
                    height = QFontMetrics.height(painter.fontMetrics())
                    painter.drawRect(kx * x + 10, ky * y + 10, kx - 20, ky - 20)
                    painter.drawText(kx * x + kx / 2 - width / 2, ky * y + height, number)
                    if elem.select:
                        self.draw_select_rect(painter, y, x)

    @staticmethod
    def get_color(val: int):
        if val == 1:
            return '#C71585'
        if val == 2:
            return '#DA70D6'
        if val == 3:
            return '#BA55D3'
        if val % 4 == 0:
            return '#8B008B'
        if val % 5 == 0:
            return '#4B0082'
        if val % 6 == 0:
            return '#DC143C'
        if val % 7 == 0:
            return '#000080'
        if val % 9 == 0:
            return '#CD5C5C'
        if val % 11 == 0:
            return '#483D8B'
        return '#8B008B'

    @staticmethod
    def get_color2(val: int):
        if val == 1:
            return '#00FF00'
        if val == 2:
            return '#20B2AA'
        if val == 3:
            return '#FFFF00'
        if val % 4 == 0:
            return '#8B008B'
        if val % 5 == 0:
            return '#00FFFF'
        if val % 6 == 0:
            return '#800000'
        if val % 7 == 0:
            return '#008000'
        if val % 9 == 0:
            return '#FA8072'
        if val % 11 == 0:
            return '#000080'
        return '#ADFF2F'

    def click(self, x: int, y: int):
        row = self.get_square(x, y)[0]
        col = self.get_square(x, y)[1]
        square = self.field.matrix[row][col]
        if square is not None:
            self.field.select_square(square)
        else:
            if self.field.count_select() == 1:
                square2 = self.field.get_select_square()
                if self.field.has_ways(square2, row, col):
                    self.field.move_square(square2, row, col)
                    self.field.add_random_square()

    def get_square(self, x: int, y: int):
        size = self.window.geometry()
        row_count = self.field.row_count
        col_count = self.field.col_count
        kx = size.width() / col_count
        ky = size.height() / row_count
        col = int(x // kx)
        row = int(y // ky)
        return [row, col]

    def draw_select_rect(self, painter: QPainter, row: int, col: int):
        size = self.window.geometry()
        row_count = self.field.row_count
        col_count = self.field.col_count
        kx = size.width() // col_count
        ky = size.height() // row_count
        x = col * kx
        y = row * ky
        col = QColor(0, 0, 0)
        if self.theme_dict == 0:
            col.setNamedColor('#00FFFF')
        else:
            col.setNamedColor('#FF0000')
        pen = QPen(col, 3, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(x + 10, y + 10, x + kx - 10, y + 10)
        painter.drawLine(x + kx - 10, y + 10, x + kx - 10, y + ky - 10)
        painter.drawLine(x + kx - 10, y + ky - 10, x + 10, y + ky - 10)
        painter.drawLine(x + 10, y + ky - 10, x + 10, y + 10)

