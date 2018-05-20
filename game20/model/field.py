from __future__ import print_function

from model.player import Player
from model.boxes import *
from math import fabs


class Field:
    def __init__(self, width: int, height: int, player: Player = None, finish: tuple = None):
        self.width = width
        self.height = height
        self.box_matrix = list()
        for row in range(height):
            self.box_matrix.append(list())
            for col in range(width):
                self.box_matrix[row].append(None)
        self.player = player
        self.finish = finish

    def a(self, new_x: int, new_y: int):
        if not self.__can_move(new_x, new_y):
            return False
        player_new_x = new_x
        player_new_y = new_y
        kx = new_x - self.player.x
        ky = new_y - self.player.y
        box_move_list = list()
        while self.box_matrix[new_y][new_x] is not None:
            if type(self.box_matrix[new_y][new_x]) is SlideBox:
                if not self.box_matrix[new_y][new_x].try_move(new_x + kx, new_y + ky):
                    return False
                else:
                    box_move_list.append((self.box_matrix[new_y][new_x], new_x + kx, new_y + ky))
                    new_x += kx
                    new_y += ky
                    if not (0 <= new_x < self.width and 0 <= new_y <= self.height):
                        return False
        list.reverse(box_move_list)
        for item in box_move_list:
            self.__move_unit(item[0].x, item[0].y, item[1], item[2])
        self.__move_unit(self.player.x, self.player.y, player_new_x, player_new_y)
        return True

    def __can_move(self, new_x: int, new_y: int):
        range_cond_x = fabs(self.player.x - new_x) <= 1
        range_cond_y = fabs(self.player.y - new_y) <= 1
        cord_are_equals_cond = fabs(self.player.x - new_x) != fabs(self.player.y - new_y)
        map_range_cond = 0 <= new_x < self.width and 0 <= new_y < self.height
        return range_cond_x and range_cond_y and cord_are_equals_cond and map_range_cond

    def __move_unit(self, old_x, old_y, new_x, new_y):
        unit = self.box_matrix[old_y][old_x]
        self.box_matrix[old_y][old_x] = None
        unit.x = new_x
        unit.y = new_y
        self.box_matrix[unit.y][unit.x] = unit
        if type(unit) is Player:
            self.player = unit

    def add_unit(self, unit: HasCords):
        self.box_matrix[unit.y][unit.x] = unit

    def p(self):
        for y, row in enumerate(self.box_matrix):
            for x, elem in enumerate(row):
                print(elem, end=' ')
            print('', end='\n')

    def load_data(self, file):
        types = dict()
        types['NO'] = None
        types['FI'] = None
        types['PL'] = Player, None
        types['BL'] = SlideBox, Direction.Blocked
        types['HO'] = SlideBox, Direction.Horizontal
        types['VE'] = SlideBox, Direction.Vertical
        types['BO'] = SlideBox, Direction.Both
        with open(file, 'r') as f:
            y = 0
            for line in f:
                l = line.split(sep=' ')
                for x, elem in enumerate(l):
                    elem = elem.rstrip('\r\n')
                    typed_elem = None
                    if types[elem] is None:
                        self.box_matrix[y][x] = None
                        if elem == 'FI':
                            self.finish = (x, y)
                    if type(types[elem]) is tuple:
                        type_of_elem = types[elem][0]
                        if type_of_elem is SlideBox:
                            typed_elem = SlideBox(x, y, types[elem][1])
                        if type_of_elem is Player:
                            typed_elem = Player(x, y)
                            self.player = type_of_elem
                            self.player.x = x  # fixme doesn't work without self.player.x = x and self.player.y = y
                            self.player.y = y
                        if typed_elem is None:
                            raise ValueError
                        self.add_unit(typed_elem)
                y += 1
