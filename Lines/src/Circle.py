class Circle:

    def __init__(self, row: int, col: int, val: int):
        self.row = row
        self.col = col
        self.val = val
        self.select = False

    def __copy__(self):
        return Circle(self.row, self.col, self.val)


class LittleCircle(Circle):

    def __init__(self, row: int, col: int, val: int):
        super().__init__(row, col, val)
