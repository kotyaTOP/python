import os
from PyQt5 import QtGui, Qt

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QWidget

from src.model.field import Field
from src.model.balls import *


class Presenter:
    def __init__(self, field: Field = None, view: QWidget = None) -> None:
        super().__init__()
        self.model = field
        self.view = view
        self.dr_x = 48
        self.dr_y = 48
        self.dr_border = 10

    def start(self):
        self.model.fill_all()

    def paint(self, qp: QPainter):
        for x, col in enumerate(self.model.matrix):
            for y, elem in enumerate(col):
                if elem is not None:
                    # qp.drawRect(QRect(x * 40, y * 40, 32, 32))
                    self.__paint_unit(qp, elem)

    def __paint_unit(self, qp: QPainter, b: Ball):
        if b.color == 1:
            color = QtGui.QColor(255, 10, 10, 255)
        elif b.color == 2:
            color = QtGui.QColor(10, 255, 10, 255)
        elif b.color == 3:
            color = QtGui.QColor(10, 10, 255, 255)
        else:
            color = QtGui.QColor(150, 150, 105, 255)
        qp.setBrush(QtGui.QBrush(color))
        qp.drawEllipse(QRect(self.dr_border + b.x * self.dr_x, self.dr_border + b.y * self.dr_y, self.dr_x, self.dr_y))

    def click(self, x: int, y: int):
        elem = self.__get_elem(x, y)
        if elem is not None:
            self.model.delete(elem)

    def __get_elem(self, x: int, y: int):
        real_x = (x - self.dr_border) // self.dr_x
        real_y = (y - self.dr_border) // self.dr_y
        try:
            return self.model.matrix[real_x][real_y]
        except IndexError:
            return None
