from abc import ABCMeta, abstractmethod


class Movable:
    @abstractmethod
    def try_move(self, new_x: int, new_y: int): raise NotImplementedError


class HasCords:
    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value

    def del_x(self):
        self._x = None

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value

    def del_y(self):
        self._y = None

    x = property(get_x, set_x, del_x, 'Координата X.')
    y = property(get_y, set_y, del_y, 'Координата Y.')
