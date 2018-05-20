from random import randint
import networkx as nx
from math import sin, cos, pi

from src.gamelems.twelve.Square import Square


class Field:

    def __init__(self, row_count: int, col_count: int):
        self.col_count = col_count
        self.row_count = row_count
        self.matrix = []
        self.create_field()
        self.add_random_square()
        self.add_random_square()
        self.add_random_square()

    def create_field(self):
        for r in range(self.row_count):
            one_row = []
            for c in range(self.col_count):
                one_row.append(None)
            self.matrix.append(one_row)

    def none_count(self):
        count = 0
        for row in self.matrix:
            for elem in row:
                if elem is None:
                    count += 1
        return count

    def check_lose(self):
        return not self.none_count()

    def add_random_square(self):
        new_place = randint(1, self.none_count())
        count = 0
        for y, row in enumerate(self.matrix):
            for x, square in enumerate(row):
                if square is None:
                    count += 1
                    if count == new_place:
                        new_square = Square(y, x, self.random())
                        self.matrix[y][x] = new_square
                        break

    @staticmethod
    def random():
        percent = randint(1, 15)
        if percent <= 10:
            return 1
        if 10 < percent <= 13:
            return 2
        if percent >= 14:
            return 3

    def add_square(self, square: Square, new_row, new_col):
        square.col = new_col
        square.row = new_row
        self.matrix[new_row][new_col] = Square(new_row, new_col, square.val)

    def delete_square(self, square: Square):
        self.matrix[square.row][square.col] = None

    def move_square(self, square: Square, new_row, new_col):
        if self.has_ways(square, new_row, new_col):
            if self.matrix[new_row][new_col] is None:
                self.simple_move(square, new_row, new_col)
            else:
                val2 = self.matrix[new_row][new_col].val
                if val2 == square.val:
                    square2 = Square(new_row, new_col, val2)
                    self.merge_square(square, square2)
                    self.add_square(square2, square2.row, square2.col)

    def simple_move(self, square: Square, new_row, new_col):
        tmp_square = square.__copy__()
        self.add_square(tmp_square, new_row, new_col)
        self.delete_square(square)

    def merge_square(self, square1: Square, square2: Square):
        self.delete_square(square1)
        square2.val += 1

    def get_nei_list(self, row, col):
        nei_list = []
        for a in range(3):
            rad = a * pi / 2
            neighbour_row = row - int(sin(rad))
            neighbour_col = col + int(cos(rad))
            if 0 <= neighbour_row < len(self.matrix) and 0 <= neighbour_col < len(self.matrix[0]):
                nei_list.append([neighbour_row, neighbour_col])
        return nei_list

    def add_nodes(self):
        g = nx.Graph()
        for x, row in enumerate(self.matrix):
            for y, elem in enumerate(row):
                if elem is None:
                    g.add_node((x, y))
        return g

    def add_edges(self, g: nx.Graph):
        for node in g:
            neighbour_list = self.get_nei_list(node[0], node[1])
            if len(neighbour_list) > 0:
                for neighbour in neighbour_list:
                    if g.nodes().__contains__((neighbour[0], neighbour[1])):
                        g.add_edge(node, (neighbour[0], neighbour[1]))
        return g.edges()

    def find_way(self, row1, col1, row2, col2):
        g = self.add_nodes()
        g.add_node((row1, col1))
        g.add_node((row2, col2))
        g.add_edges_from(self.add_edges(g))
        return nx.has_path(g, (row1, col1), (row2, col2))

    def has_ways(self, square1: Square, new_row: int, new_col: int):
        return self.find_way(square1.row, square1.col, new_row, new_col)
