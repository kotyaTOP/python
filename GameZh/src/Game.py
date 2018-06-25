from random import randint
from src.Circle import Circle


class Field:
    def __init__(self, row_count: int, col_count: int):
        self.row_count = row_count
        self.col_count = col_count
        self.score = 0
        self.matrix = []
        self.select_matrix = []
        self.__create_matrix()
        self.__create_select_matrix()
        self.__fill_matrix(self.matrix)
        self.__check_create()
        self.start_c = None
        self.direction = None
        self.in_action = False
        self.visible_changed_matrix = None
        self.diff = None

    def __create_matrix(self):
        for r in range(self.row_count):
            one_row = []
            for c in range(self.col_count):
                one_row.append(None)
            self.matrix.append(one_row)

    def __create_select_matrix(self):
        for r in range(self.row_count):
            one_row = []
            for c in range(self.col_count):
                one_row.append(False)
            self.select_matrix.append(one_row)

    def __unselect_count(self):
        count = 0
        for row in self.select_matrix:
            for elem in row:
                if not elem:
                    count += 1
        return count

    def check_win(self):
        if self.__unselect_count() == 0:
            return True
        return False

    @staticmethod
    def __fill_matrix(matrix: list):
        for y in range(len(matrix)):
            for x in range(len(matrix[y])):
                if matrix[y][x] is None:
                    new_circle = Circle(randint(1, 3), y, x)
                    matrix[y][x] = new_circle

    def __check_create(self):
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[y])):
                if self.__subs_friends(self.matrix[y][x]):
                    self.__check_create()
                    return

    def __subs_friends(self, circle: Circle):
        def __subs_circle(inner_circle):
            inner_circle = Circle(randint(1, 3), inner_circle.row, inner_circle.col)
            self.matrix[inner_circle.row][inner_circle.col] = inner_circle

        hor_friends = self.__get_friends_horizontal(circle, self.matrix)
        ver_friends = self.__get_friends_vertical(circle, self.matrix)
        if len(ver_friends) >= 3:
            if len(hor_friends) >= 3:
                hor_friends.remove(circle)
                ver_friends.extend(hor_friends)
            for friend in ver_friends:
                __subs_circle(friend)
            return True
        else:
            if len(hor_friends) >= 3:
                for friend in hor_friends:
                    __subs_circle(friend)
                return True
            return False

    def __score_count(self, ver_friends, hor_friends):
        if len(ver_friends) > 3:
            if len(hor_friends) > 3:
                self.score += 60
            else:
                self.score += 20

    def __update(self):
        for y, row in enumerate(self.visible_changed_matrix):
            for x, elem in enumerate(row):
                if self.visible_changed_matrix[y][x] is None:
                    self.__fall(y, x)

    def __fall(self, y: int, x: int):
        """
        Спускает "вниз" на пустые ячейки шарики, находящиеся сверху
        :param y: координата Y
        :param x: координата X
        """
        count = 0
        while count < y and self.visible_changed_matrix[y][x] is None:
            while y > 0:
                self.visible_changed_matrix[y][x] = self.visible_changed_matrix[y - 1][x]
                if type(self.visible_changed_matrix[y][x]) is Circle:
                    self.visible_changed_matrix[y][x].row += 1
                y -= 1
                self.visible_changed_matrix[0][x] = None
            count += 1

    @staticmethod
    def copy_matrix(matrix):
        copy = []
        for row in matrix:
            one_row = []
            for elem in row:
                one_row.append(elem.copy())
            copy.append(one_row)
        return copy

    def move_prepare(self, start_c: Circle):
        self.start_c = start_c

    def move(self, current_c: Circle):
        if self.direction is None and not self.start_c.equals(current_c):
            self.direction = self.__get_direction(current_c)
        if self.direction == 0:
            self.__move_vertical(self.start_c.col, current_c.row - self.start_c.row)
        elif self.direction == 1:
            self.__move_horizontal(self.start_c.row, current_c.col - self.start_c.col)

    def move_post(self):
        self.in_action = False
        self.direction = None
        self.start_c = None
        does_combos_exist = self.__remove_combos_from_matrix()
        if does_combos_exist:
            self.matrix = self.copy_matrix(self.visible_changed_matrix)

    def __remove_combos_from_matrix(self):
        """
        Удаляет комбинации из матрицы.
        :return: True если комбинации были найдены и удалены, False если комбинации найдены не было
        """
        for y in range(len(self.visible_changed_matrix)):
            for x in range(len(self.visible_changed_matrix[y])):
                if self.__remove_combos_near_circle(self.visible_changed_matrix[y][x]):
                    self.__update()
                    self.__fill_matrix(self.visible_changed_matrix)
                    self.__remove_combos_from_matrix()
                    return True
        return False

    def __remove_combos_near_circle(self, circle: Circle) -> bool:
        """
        Удаляет комбинации вблизи шара.
        :param circle: шар, вблизи которого будут искаться комбинации
        :return: True если комбинации были найдены и удалены, False если не были найдены
        """

        def __delete_circle_from_matrix(circle_for_delete):
            """
            Удаляет шар из матрицы.
            :param circle_for_delete: шар для удаления
            """
            self.visible_changed_matrix[circle_for_delete.row][circle_for_delete.col] = None
            self.select_matrix[circle_for_delete.row][circle_for_delete.col] = True
            self.score += 10

        hor_friends = self.__get_friends_horizontal(circle, self.visible_changed_matrix)
        ver_friends = self.__get_friends_vertical(circle, self.visible_changed_matrix)
        self.__score_count(ver_friends, hor_friends)
        if len(ver_friends) >= 3:
            if len(hor_friends) >= 3:
                hor_friends.remove(circle)
                ver_friends.extend(hor_friends)
            for friend in ver_friends:
                __delete_circle_from_matrix(friend)
            return True
        else:
            if len(hor_friends) >= 3:
                for friend in hor_friends:
                    __delete_circle_from_matrix(friend)
                return True
            return False

    def __get_friends_horizontal(self, circle: Circle, matrix: list):
        hor_friends = [circle]
        i = circle.col + 1
        while i < self.col_count and matrix[circle.row][i].val == circle.val:
            hor_friends.append(matrix[circle.row][i])
            i += 1
        j = circle.col - 1
        while j >= 0 and matrix[circle.row][j].val == circle.val:
            hor_friends.append(matrix[circle.row][j])
            j -= 1
        return hor_friends

    def __get_friends_vertical(self, circle: Circle, matrix: list):
        ver_friends = [circle]
        i = circle.row + 1
        while i < self.row_count and matrix[i][circle.col].val == circle.val:
            ver_friends.append(matrix[i][circle.col])
            i += 1
        j = circle.row - 1
        while j >= 0 and matrix[j][circle.col].val == circle.val:
            ver_friends.append(matrix[j][circle.col])
            j -= 1
        return ver_friends

    def __move_horizontal(self, row_number: int, diff: int):
        """
        Движение по горизонтали.
        :param row_number: номер движущейся строки
        :param diff: смещение
        """
        self.visible_changed_matrix = Field.copy_matrix(self.matrix)
        values = [None for i in range(len(self.visible_changed_matrix))]
        for i in range(len(self.visible_changed_matrix[0])):
            new_col_number = (i + diff) % len(values)
            values[new_col_number] = self.visible_changed_matrix[row_number][i]
            values[new_col_number].col = new_col_number
        for i in range(len(values)):
            self.visible_changed_matrix[row_number][i] = values[i]
        self.in_action = True

    def __move_vertical(self, column_number: int, diff: int):
        """
        Движение по вертикали.
        :param column_number: номер движущегося столбца
        :param diff: смещение
        """
        self.visible_changed_matrix = Field.copy_matrix(self.matrix)
        values = [None for i in range(len(self.visible_changed_matrix))]
        for i in range(len(self.visible_changed_matrix)):
            new_row_number = (i + diff) % len(values)
            values[new_row_number] = self.visible_changed_matrix[i][column_number]
            values[new_row_number].row = new_row_number
        for i in range(len(values)):
            self.visible_changed_matrix[i][column_number] = values[i]
        self.in_action = True

    def __get_direction(self, current_c: Circle) -> int:
        """
        Возвращает направление движения.
        :param current_c: направление движения - к current_c
        :return: 0 - вертикальное, 1 - горизонтальное
        """
        if current_c.col == self.start_c.col:
            return 0
        else:
            return 1
