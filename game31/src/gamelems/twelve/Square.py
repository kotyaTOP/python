class Square:

    def __init__(self, row: int, col: int, val: int):
        self.row = row
        self.col = col
        self.val = val

    def __copy__(self):
        return Square(self.row, self.col, self.val)

