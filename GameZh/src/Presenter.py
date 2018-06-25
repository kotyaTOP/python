from PyQt5 import QtGui

from PyQt5.QtCore import *
from src.Game import *
from src.Window import *
import os


class Presenter:

    def __init__(self, field: Field, window: MyWindow):
        self.field = field
        self.window = window
        self.i_size = 50
        self.i_top = 40
        self.i_data = dict()
        self.__init_data()
        self.circle2 = None
        self.hor = None

    def __init_data(self):
        """
        Инициализирует изображения для игры.
        """
        self.i_data['c1'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c1.png'))
        self.i_data['c2'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c2.png'))
        self.i_data['c3'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c3.png'))
        self.i_data['c4'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c4.png'))
        self.i_data['c5'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c5.png'))
        self.i_data['c6'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c6.png'))
        self.i_data['c7'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'c7.png'))
        self.i_data['y1'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y1.png'))
        self.i_data['y2'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y2.png'))
        self.i_data['y3'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y3.png'))
        self.i_data['y4'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y4.png'))
        self.i_data['y5'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y5.png'))
        self.i_data['y6'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y6.png'))
        self.i_data['y7'] = QImage(os.path.join(os.path.dirname(__file__), '..', 'resources', 'y7.png'))

    def paint(self, qp: QPainter):
        """
        Выполняет прорисовку.
        :param qp: QPainter
        """
        self.__draw_field(qp, self.field.matrix if not self.field.in_action else self.field.visible_changed_matrix)

    def __draw_field(self, painter: QPainter, matrix: list):
        """
        Рисует игровое поле.
        :param painter: QPainter
        :param matrix: матрица "шаров"
        """
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
        painter.drawText((size.width() - width) / 2, height, str_score)
        for y, row in enumerate(matrix):
            for x, elem in enumerate(row):
                rect = QRect(self.i_size * x, self.i_size * y + self.i_top, self.i_size, self.i_size)
                if self.field.select_matrix[y][x]:
                    painter.drawImage(rect, self.i_data['y' + str(elem.val)])
                else:
                    painter.drawImage(rect, self.i_data['c' + str(elem.val)])

    def press(self, x: int, y: int):
        """
        Обрабатывает нажатие клавиши выши.
        :param x: координата Х
        :param y: координата Y
        """
        self.field.move_prepare(self.__get_circle(x, y))

    def move(self, x: int, y: int):
        """
        Обрабатывает движение выши.
        :param x: координата Х
        :param y: координата Y
        """
        current_c = self.__get_circle(x, y)
        self.field.move(current_c)

    def release(self):
        """
        Обрабатывает отжатие клавиши выши.
        """
        self.field.move_post()

    def __get_circle(self, x: int, y: int) -> Circle:
        """
        Возвращает шар, который находится в ячейке, которой принадлежат координаты.
        :param x: координата Х
        :param y: координата Y
        :return: ша. находящийся на этих координатах
        """
        col = int(x // self.i_size)
        row = int(y - self.i_top) // self.i_size
        return self.field.matrix[row][col]
