import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from Game import *
from Window import *
import os


class Presenter:

    def __init__(self, field: Field, window: MyWindow):
        self.field = field
        self.window = window
        self.i_size = 48
        self.i_top = 40
        self.i_data = dict()
        self.__init_data()
        self.prev_matrix = self.field.copy_matrix(self.field.matrix)
        self.prev_score = self.field.score

    def __init_data(self):
        self.i_data['b1'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b1.png'))
        self.i_data['b2'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b2.png'))
        self.i_data['b3'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b3.png'))
        self.i_data['b4'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b4.png'))
        self.i_data['b5'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b5.png'))
        self.i_data['b6'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b6.png'))
        self.i_data['b7'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'b7.png'))
        self.i_data['l1'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l1.png'))
        self.i_data['l2'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l2.png'))
        self.i_data['l3'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l3.png'))
        self.i_data['l4'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l4.png'))
        self.i_data['l5'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l5.png'))
        self.i_data['l6'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l6.png'))
        self.i_data['l7'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'l7.png'))

    def paint(self, qp: QPainter):
        # self.draw_field(qp)
        self.draw_circle(qp)

    def draw_circle(self, painter: QPainter):
        size = self.window.geometry()
        painter.fillRect(QRect(0, 0, size.width(), size.height()),
                         QBrush(QtGui.QColor(0, 0, 0)))
        painter.setFont(QFont('Decorative', 20))
        col = QColor(0, 0, 0)
        col.setNamedColor('#00FFFF')
        painter.setPen(col)
        height = QFontMetrics.height(painter.fontMetrics())
        str_score = 'Score:  ' + str(self.field.score)
        width = QFontMetrics.width(painter.fontMetrics(), str_score)
        painter.drawText((size.width() - width) // 2, height, str_score)
        col.setNamedColor('#FF0F00')
        painter.setPen(col)
        painter.setFont(QFont('Decorative', 10))
        str_cancel = " 'a' - cancel turn"
        str_subs = " 'r' - subs future circles"
        height = QFontMetrics.height(painter.fontMetrics())
        width = QFontMetrics.width(painter.fontMetrics(), str_subs)
        painter.drawText(0, height * 2, str_cancel)
        painter.drawText(size.width() - width, height * 2, str_subs)
        for y, row in enumerate(self.field.matrix):
            for x, elem in enumerate(row):
                rect = QRect(self.i_size * x, self.i_size * y + self.i_top, self.i_size, self.i_size)
                pic = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'empty.png'))
                painter.drawImage(rect, pic)
                if elem is not None:
                    if type(elem) is Circle:
                        painter.drawImage(rect, self.i_data['b'+str(elem.val)])
                    if type(elem) is LittleCircle:
                        painter.drawImage(rect, self.i_data['l'+str(elem.val)])
                    if elem.select:
                        self.draw_select(painter, elem.row, elem.col)

    def click(self, x: int, y: int):
        row = self.get_circle(x, y)[0]
        col = self.get_circle(x, y)[1]
        circle = self.field.matrix[row][col]
        if type(circle) is Circle:
            self.select_circle(circle)
        else:
            if self.count_select() == 1:
                circle = self.get_select_circle()
                if self.field.has_ways(circle, row, col):
                    self.prev_matrix = self.field.copy_matrix(self.field.matrix)
                    self.prev_score = self.field.score
                    self.field.move_circle(circle, row, col)
                    circle.select = False
                    if not self.field.check_delete(self.field.matrix[row][col]):
                        little_circle = self.field.get_little_circle()
                        self.field.add_random_little_circles()
                        for elem in little_circle:
                            self.field.check_delete(self.field.matrix[elem[0]][elem[1]])

    def cancel_turn(self):
        self.field.matrix = self.field.copy_matrix(self.prev_matrix)
        self.field.score = self.prev_score

    def select_circle(self, circle: Circle):
        if self.count_select() == 0:
            circle.select = True
        else:
            if self.count_select() == 1:
                if circle.select:
                    circle.select = False
                else:
                    circle2 = self.get_select_circle()
                    circle2.select = False
                    circle.select = True

    def count_select(self):
        count = 0
        for row in self.field.matrix:
            for elem in row:
                if elem is not None and elem.select:
                    count += 1
        return count

    def get_select_circle(self):
        for row in self.field.matrix:
            for elem in row:
                if type(elem) is Circle and elem.select:
                    return elem

    def get_circle(self, x: int, y: int):
        col = int(x // self.i_size)
        row = int(y - self.i_top) // self.i_size
        return [row, col]

    def draw_select(self, painter: QPainter, row: int, col: int):
        x = col * self.i_size
        y = row * self.i_size + self.i_top
        col = QColor(0, 0, 0)
        col.setNamedColor('#00FFFF')
        pen = QPen(col, 3, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawEllipse(x + 5, y + 5, 39, 39)





