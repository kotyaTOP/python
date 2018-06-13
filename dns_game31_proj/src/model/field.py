from src.model.balls import *
from random import randint
from math import pi, sin, cos


class Field:
    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        self.matrix = list()
        self.width = width
        self.height = height
        for col in range(width):
            self.matrix.append(list())
            for row in range(height):
                self.matrix[col].append(None)

    def add(self, ball: Ball):
        if not 0 <= ball.x < self.width or not 0 <= ball.y < self.height:
            raise IndexError
        self.matrix[ball.x][ball.y] = ball

    def delete(self, b: Ball):
        # self.matrix[b.x][b.y] = None
        self.__ch(b, b.color)
        self.__del_ch()
        self.__update()
        self.delete_empty_col()

    def __del_ch(self):
        chlist = list()
        for x, col in enumerate(self.matrix):
            for y, elem in enumerate(col):
                if elem is not None and elem.ch:
                    chlist.append(elem)
        for i in chlist:
            i.ch = False
            if len(chlist) >= 2:
                self.matrix[i.x][i.y] = None

    def __ch(self, b: Ball, c: int):
        if b.color == c:
            b.ch = True
            rad = pi / 2
            for k in range(4):
                real_rad = k * rad
                try:
                    x = b.x + int(sin(real_rad))
                    y = b.y + int(cos(real_rad))
                    if 0 <= x and 0 <= y:
                        elem = self.matrix[x][y]
                        if elem is not None and not elem.ch:
                            self.__ch(elem, c)
                except IndexError:
                    pass

    def fill_all(self):
        for x, col in enumerate(self.matrix):
            for y, elem in enumerate(col):
                if elem is None:
                    self.add(Ball(x, y, randint(1, 3)))

    def fill_line(self):
        for x, col in enumerate(self.matrix):
            last_index = 0
            for y, elem in enumerate(col):
                if elem is None:
                    last_index = y
                else:
                    break
            if last_index != len(col) - 1:
                self.add(Ball(x, last_index, randint(1, 3)))

    def __update(self):
        for x, col in enumerate(self.matrix):
            for y, elem in enumerate(col):
                if self.matrix[x][y] is None:
                    self.__sdvig(x, y)

    def __sdvig(self, x: int, y: int):
        count = 0
        while count < y and self.matrix[x][y] is None:
            while y > 0:
                self.matrix[x][y] = self.matrix[x][y - 1]
                if self.matrix[x][y] is not None:
                    self.matrix[x][y].y += 1
                y -= 1
            self.matrix[x][0] = None
            count += 1

    def delete_empty_col(self):
        for x, col in enumerate(self.matrix):
            while x < len(self.matrix) and list.count(self.matrix[x], None) == len(self.matrix[x]):
                list.remove(self.matrix, self.matrix[x])
                self.width -= 1
                for x_p, col_p in enumerate(self.matrix[x:]):
                    for y_p, elem_p in enumerate(col_p):
                        if elem_p is not None:
                            elem_p.x -= 1
