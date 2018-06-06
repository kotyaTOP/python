from enum import Enum


class BallColor(Enum):
    Red = 1
    Green = 2
    Blue = 3


class HasLocationProperty:
    def get_x(self):
        return self.__x

    def set_x(self, value):
        self.__x = value

    def del_x(self):
        self.__x = None

    def get_y(self):
        return self.__y

    def set_y(self, value):
        self.__y = value

    def del_y(self):
        self.__y = None

    x = property(get_x, set_x, del_x, 'Координата X.')
    y = property(get_y, set_y, del_y, 'Координата Y.')


class Ball(HasLocationProperty):

    def __init__(self, x: int, y: int, b_color: BallColor) -> None:
        super().__init__()
        self.color = b_color
        self.x = x
        self.y = y
        self.ch = False
