import os
from PyQt5 import QtGui, QtCore

from PyQt5.QtCore import QLine
from PyQt5.QtGui import *
from copy import deepcopy

from model.player import *
from src.model.boxes import *
from src.model.field import Field
from src.view.gamewindow import GameWindow, QRect


class Presenter:

    def __init__(self, model: Field, view: GameWindow) -> None:
        super().__init__()
        self.model = model
        self.view = view
        self.u_x = 32
        self.u_y = 32
        self.u_space = 3
        self.u_border_space = 4
        self.img = dict()
        self.img['Direction.Horizontal'] = QImage(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'hor.png'))
        self.img['Direction.Vertical'] = QImage(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'ver.png'))
        self.img['Direction.Blocked'] = QImage(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'block.png'))
        self.img['Direction.Both'] = QImage(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'both.png'))
        self.img['Player'] = QImage(
            os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'player.png'))
        self.copy_model = deepcopy(self.model)

    def paint(self, qp: QPainter):
        self.__paint_field(qp, self.model.width, self.model.height, self.model.finish[0])
        for y, row in enumerate(self.model.box_matrix):
            for x, elem in enumerate(row):
                if elem is not None:
                    self.__paint_unit(qp, elem)

    def __paint_field(self, qp: QPainter, width: int, height: int, finish_x: int):
        col = QColor(0, 0, 0)
        pen = QPen()
        pen.setColor(col)
        qp.setPen(pen)
        top_finish_line_x1 = self.u_border_space + (self.u_x + self.u_space) * finish_x
        top_field_y = self.u_border_space + 2 * (self.u_x + self.u_space)
        right_field_x = self.u_border_space + self.u_space + width * (self.u_x + self.u_space) - 1
        bottom_field_y = top_field_y + self.u_space + height * (self.u_x + self.u_space) - 1
        top_middle_left_x = self.u_border_space + (self.u_x + self.u_space) * finish_x
        top_finish_line = QLine(top_finish_line_x1, self.u_border_space,
                                top_finish_line_x1 + self.u_x + 2 * self.u_space, self.u_border_space)
        left_finish_line = QLine(top_finish_line_x1, self.u_border_space,
                                 top_finish_line_x1, top_field_y)
        right_finish_line = QLine(top_finish_line_x1 + self.u_x + 2 * self.u_space, self.u_border_space,
                                  top_finish_line_x1 + self.u_x + 2 * self.u_space, top_field_y)
        top_left_field_line = QLine(self.u_border_space, top_field_y,
                                    top_middle_left_x, top_field_y)
        top_right_field_line = QLine(top_middle_left_x + 2 * self.u_space + self.u_x, top_field_y,
                                     right_field_x, top_field_y)
        left_field_line = QLine(self.u_border_space, top_field_y, self.u_border_space, bottom_field_y)
        right_field_line = QLine(right_field_x, top_field_y, right_field_x, bottom_field_y)
        bottom_field_line = QLine(self.u_border_space, bottom_field_y, right_field_x, bottom_field_y)
        border = [top_finish_line, left_finish_line, right_finish_line, top_left_field_line, top_right_field_line,
                  left_field_line, right_field_line, bottom_field_line]
        qp.fillRect(QRect(0, 0, right_field_x + self.u_border_space, bottom_field_y + self.u_border_space),
                    QBrush(QtGui.QColor(245, 245, 245)))
        qp.fillRect(QRect(top_finish_line_x1, self.u_border_space, 2 * self.u_space + self.u_x,
                          2 * (self.u_space + self.u_y) + 1),
                    QBrush(QtGui.QColor(229, 229, 229)))
        qp.fillRect(QRect(self.u_border_space, top_field_y,
                          width * (self.u_space + self.u_x) + self.u_space,
                          height * (self.u_space + self.u_y) + self.u_space),
                    QBrush(QtGui.QColor(229, 229, 229)))
        for b in border:
            qp.drawLine(b)

    def __paint_unit(self, qp: QPainter, unit: HasCords):
        pos_x = self.u_border_space + unit.x * self.u_x + self.u_space * (unit.x + 1)
        pos_y = self.u_border_space + unit.y * self.u_y + self.u_space * unit.y + 2 * (
                self.u_y + self.u_space) + self.u_space
        col = QColor(0, 0, 0)
        pen = QPen()
        pen.setColor(col)
        qp.setPen(pen)
        rect = QRect(pos_x, pos_y, self.u_x, self.u_y)
        mg = None
        type_unit = type(unit)
        if type_unit is SlideBox:
            mg = self.img[str(unit.direction)]
        else:
            mg = self.img['Player']
        if mg is not None:
            qp.drawImage(rect, mg)

    def action(self, dir):
        if self.model.player.x == self.model.finish[0] and self.model.player.y == self.model.finish[1]:
            return False
        dx = 1 if dir == 1 else -1 if dir == 3 else 0
        dy = 1 if dir == 2 else -1 if dir == 0 else 0
        result = self.model.a(self.model.player.x + dx, self.model.player.y + dy)
        if self.model.player.x == self.model.finish[0] and self.model.player.y == self.model.finish[1]:
            self.view.win()
        return result

    def restart(self):
        self.model = deepcopy(self.copy_model)
