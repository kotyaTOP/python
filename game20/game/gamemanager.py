from model.field import *
import os
from copy import deepcopy


class Game:
    def __init__(self, level_number: int) -> None:
        super().__init__()
        self.levels = dict()
        self.levels[1] = ('1.txt', 15, 10)
        self.levels[2] = ('little_test.txt', 3, 3)
        self.current = self.levels[level_number]
        self.state = 0

    def start(self):
        self.field = Field(self.current[1], self.current[2])
        self.field.load_data(os.path.join(os.path.dirname(__file__), 'levels', self.current[0]))
        self.field_copy = deepcopy(self.field)

    def restart(self):
        self.state = 0
        self.field = deepcopy(self.field_copy)

    def a(self, x: int, y: int):
        self.field.a(x, y)
        if self.field.player.x == self.field.finish[0] and self.field.player.y == self.field.finish[1]:
            self.state = 1
            return True
        else:
            self.state = 0
            return False
