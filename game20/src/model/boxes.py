from src.model.directions import Direction
from math import fabs
from src.model.actions.moveact import *


class Box(HasCords):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y


class SlideBox(Box, Movable):

    def __init__(self, x: int, y: int, direction: Direction):
        super().__init__(x, y)
        self.direction = direction

    def try_move(self, new_x: int, new_y: int):
        return self.__can_move(new_x, new_y)

    def __can_move(self, new_x: int, new_y: int):
        if self.direction == Direction.Blocked:
            return False
        move_direction = Direction.Horizontal if new_x != self.x else Direction.Vertical
        dir_cond = self.direction == Direction.Both or self.direction == move_direction
        range_x_cond = fabs(self.x - new_x) <= 1
        range_y_cond = fabs(self.y - new_y) <= 1
        range_cond = fabs(fabs(self.x - new_x) - fabs(self.y - new_y)) == 1
        return dir_cond and range_cond

    def __str__(self) -> str:
        dir_str = dict();
        dir_str['Direction.Horizontal'] = 'Horizontal'
        dir_str['Direction.Vertical'] = 'Vertical'
        dir_str['Direction.Blocked'] = 'Blocked'
        dir_str['Direction.Both'] = 'Both'
        return 'sldbx({x}, {y}, {dir})'.format(x=self.x, y=self.y, dir=dir_str[str(self.direction)])
