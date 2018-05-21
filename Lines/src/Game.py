from random import randint
import networkx as nx
from src.Circle import *


class Field:

    def __init__(self, row_count: int, col_count: int):
        self.row_count = row_count
        self.col_count = col_count
        self.matrix = []
        self.create_matrix()
        self.add_random_circle()
        self.add_random_circle()
        self.add_random_circle()
        self.add_little_circle()

    def create_matrix(self):
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

    def add_random_little_circles(self):
        if self.none_count() > 0:
            if self.none_count() >= 3:
                self.add_little_circle()
                self.add_little_circle()
                self.add_little_circle()
            else:
                if self.none_count() == 2:
                    self.add_random_circle()
                    self.add_random_circle()
                else:
                    self.add_random_circle()

    def add_little_circle(self):
        new_place = randint(1, self.none_count())
        count = 0
        for y, row in enumerate(self.matrix):
            for x, square in enumerate(row):
                if square is None:
                    count += 1
                    if count == new_place:
                        new_circle = LittleCircle(y, x, randint(1, 6))
                        self.matrix[y][x] = new_circle
                        break

    def add_random_circle(self):
        new_place = randint(1, self.none_count())
        count = 0
        for y, row in enumerate(self.matrix):
            for x, square in enumerate(row):
                if square is None:
                    count += 1
                    if count == new_place:
                        new_circle = Circle(y, x, randint(1, 6))
                        self.matrix[y][x] = new_circle
                        break

    def transform_little_circle(self, circle):
        for row in self.matrix:
            for elem in row:
                if elem is LittleCircle:
                    circle = Circle(elem.row, elem.col, elem.val)

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
            if self.matrix[new_row][new_col] is not Circle:
                tmp_circle = circle.__copy__()
                self.add_circle(tmp_circle, new_row, new_col)
                self.delete_circle(circle)

    def get_nei_list(self, i, j):
        nei_list = []
        k = i - 1
        while k <= i + 1:
            l = j - 1
        while l <= j + 1:
            if 0 <= k < len(self.matrix) and 0 <= l < len(self.matrix[0]):
                if k != i or l != j:
                    nei_list.append(self.matrix[k][l])
        l += 1
        k += 1
        return nei_list

    def add_nodes(self):
        g = nx.Graph()
        for x, row in enumerate(self.matrix):
            for y, elem in enumerate(row):
                if elem is not Circle:
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
        self.check_hor_ver(circle)
        self.check_dial_ver(circle)

    def check_hor_ver(self, circle):
        hor_friends = self.find_hor_friends(circle)
        ver_friends = self.find_ver_friends(circle)
        if len(ver_friends) >= 5:
            if len(hor_friends) >= 5:
                ver_friends.remove(circle)
                hor_friends.extend(ver_friends)
            else:
                hor_friends = ver_friends
            for friend in hor_friends:
                self.delete_circle(friend)
        else:
            if len(hor_friends) >= 5:
                for friend in hor_friends:
                    self.delete_circle(friend)

    def check_dial_ver(self, circle):
        pos_friends = self.find_pos_dial_friends(circle)
        neg_friends = self.find_neg_dial_friends(circle)
        if len(neg_friends) >= 5:
            if len(pos_friends) >= 5:
                neg_friends.remove(circle)
                pos_friends.extend(neg_friends)
            else:
                pos_friends = neg_friends
            for friend in pos_friends:
                self.delete_circle(friend)
        else:
            if len(pos_friends) >= 5:
                for friend in pos_friends:
                    self.delete_circle(friend)

    def find_hor_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and self.matrix[circle.row][i] is not None and \
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
        reverse_matrix = [[row[i] for row in self.matrix] for i in range(len(self.matrix[0]))]
        i = circle.row + 1
        while i < self.row_count and self.matrix[i][circle.col] is not None and \
                self.matrix[i][circle.col].val == circle.val:
            friends.append(self.matrix[i][circle.col])
            i += 1
        j = circle.row - 1
        while j >= 0 and self.matrix[j][circle.col] is not None and \
                self.matrix[j][circle.col].val == circle.val:
            friends.append(self.matrix[i][circle.col])
            j -= 1
        return friends

    def find_pos_dial_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and circle.row + i - circle.col < self.row_count and \
                self.matrix[circle.row + i - circle.col][i] is not None and \
                self.matrix[circle.row + i - circle.col][i].val == circle.val:
            friends.append(self.matrix[circle.row + i - circle.col][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and circle.row - j + circle.col >= 0 and self.matrix[circle.row - j + circle.col][j] is not None \
                and self.matrix[circle.row - j + circle.col][j].val == circle.val:
            friends.append(self.matrix[circle.row - j + circle.col][j])
            j -= 1
        return friends

    def find_neg_dial_friends(self, circle: Circle):
        friends = [circle]
        i = circle.col + 1
        while i < self.col_count and circle.row - i + circle.col < self.row_count and \
                self.matrix[circle.row - i + circle.col][i] is not None and \
                self.matrix[circle.row - i + circle.col][i].val == circle.val:
            friends.append(self.matrix[circle.row - i + circle.col][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and circle.row + j - circle.col >= 0 and self.matrix[circle.row + j - circle.col][j] is not None \
                and self.matrix[circle.row + j - circle.col][j].val == circle.val:
            friends.append(self.matrix[circle.row + j - circle.col][j])
            j -= 1
        return friends


