from random import randint
import networkx as nx
from math import sin, cos, pi
from Circle import *


class Field:

    def __init__(self, row_count: int, col_count: int):
        self.row_count = row_count
        self.col_count = col_count
        self.matrix = []
        self.create_matrix()
        self.add_little_circle()
        self.add_little_circle()
        self.add_little_circle()
        self.add_random_little_circles()


    def add_random_little_circles(self):
        self.transform_little_circle()
        if self.none_count() > 0:
            if self.none_count() >= 3:
                self.add_little_circle()
                self.add_little_circle()
                self.add_little_circle()
            else:
                if self.none_count() == 2:
                    self.add_little_circle()
                    self.add_little_circle()
                else:
                    self.add_little_circle()

    def add_little_circle(self):
        new_place = randint(1, self.none_count())
        count = 0
        for y, row in enumerate(self.matrix):
            for x, square in enumerate(row):
                if square is None:
                    count += 1
                    if count == new_place:
                        new_circle = LittleCircle(y, x, randint(1, 7))
                        self.matrix[y][x] = new_circle
                        break

    def transform_little_circle(self):
        for row in self.matrix:
            for elem in row:
                if type(elem) is LittleCircle:
                    self.add_circle(Circle(elem.row, elem.col, elem.val), elem.row, elem.col)

    def check_lose(self):
        return not self.none_count()

    def add_circle(self, circle: Circle, new_row, new_col):
        circle.col = new_col
        circle.row = new_row
        self.matrix[new_row][new_col] = Circle(new_row, new_col, circle.val)

    def delete_circle(self, circle: Circle):
        self.matrix[circle.row][circle.col] = None

    def move_circle(self, circle: Circle, new_row, new_col):
        if self.has_ways(circle, new_row, new_col):
            if type(self.matrix[new_row][new_col]) is not Circle:
                tmp_circle = circle.__copy__()
                self.add_circle(tmp_circle, new_row, new_col)
                self.delete_circle(circle)

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
                if type(elem) is not Circle:
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

    def has_ways(self, circle: Circle, new_row: int, new_col: int):
        return self.find_way(circle.row, circle.col, new_row, new_col)

    def check_delete(self, circle):
        return self.check_hor_ver(circle) or self.check_dial_ver(circle)

    def check_hor_ver(self, circle):
        hor_friends = self.find_hor_friends(circle)
        ver_friends = self.find_ver_friends(circle)
        if len(ver_friends) >= 5:
            if len(hor_friends) >= 5:
                hor_friends.remove(circle)
                ver_friends.extend(hor_friends)
            for friend in ver_friends:
                self.delete_circle(friend)
            return True
        else:
            if len(hor_friends) >= 5:
                for friend in hor_friends:
                    self.delete_circle(friend)
                return True
            return False

    def check_dial_ver(self, circle):
        pos_friends = self.find_pos_dial_friends(circle)
        neg_friends = self.find_neg_dial_friends(circle)
        if len(neg_friends) >= 5:
            if len(pos_friends) >= 5:
                pos_friends.remove(circle)
                neg_friends.extend(pos_friends)
            for friend in neg_friends:
                self.delete_circle(friend)
            return True
        else:
            if len(pos_friends) >= 5:
                for friend in pos_friends:
                    self.delete_circle(friend)
                return True
            return False

    def find_hor_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and type(self.matrix[circle.row][i]) is Circle and \
                self.matrix[circle.row][i].val == circle.val:
            friends.append(self.matrix[circle.row][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and self.matrix[circle.row][j] is not None and \
                self.matrix[circle.row][j].val == circle.val:
            friends.append(self.matrix[circle.row][j])
            j -= 1
        return friends

    def find_ver_friends(self, circle: Circle):
        friends = [circle]
        i = circle.row + 1
        while i < self.row_count and type(self.matrix[i][circle.col]) is Circle and \
                self.matrix[i][circle.col].val == circle.val:
            friends.append(self.matrix[i][circle.col])
            i += 1
        j = circle.row - 1
        while j >= 0 and type(self.matrix[j][circle.col]) is Circle and \
                self.matrix[j][circle.col].val == circle.val:
            friends.append(self.matrix[j][circle.col])
            j -= 1
        return friends

    def find_pos_dial_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and circle.row + i - circle.col < self.row_count and \
                type(self.matrix[circle.row + i - circle.col][i]) is Circle and \
                self.matrix[circle.row + i - circle.col][i].val == circle.val:
            friends.append(self.matrix[circle.row + i - circle.col][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and circle.row + j - circle.col >= 0 and \
                type(self.matrix[circle.row + j - circle.col][j]) is Circle \
                and self.matrix[circle.row + j - circle.col][j].val == circle.val:
            friends.append(self.matrix[circle.row + j - circle.col][j])
            j -= 1
        return friends

    def find_neg_dial_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and circle.row - i + circle.col >= 0 and \
                self.matrix[circle.row - i + circle.col][i] is not None and \
                self.matrix[circle.row - i + circle.col][i].val == circle.val:
            friends.append(self.matrix[circle.row - i + circle.col][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and circle.row - j + circle.col < self.row_count \
                and self.matrix[circle.row - j + circle.col][j] is not None \
                and self.matrix[circle.row - j + circle.col][j].val == circle.val:
            friends.append(self.matrix[circle.row - j + circle.col][j])
            j -= 1
        return friends

    def get_little_circle(self):
        lc = []
        for row in self.matrix:
            for elem in row:
                if type(elem) is LittleCircle:
                    lc.append((elem.row, elem.col))
        return lc
