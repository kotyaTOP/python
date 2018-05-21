from src.model.actions.moveact import *


class Player(HasCords):

    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return 'pl({x}, {y})'.format(x=self.x, y=self.y)
