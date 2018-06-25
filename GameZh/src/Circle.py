class Circle:
    def __init__(self, val: int, row: int, col: int):
        self.val = val
        self.row = row
        self.col = col

    def __str__(self) -> str:
        return "(c:" + str(self.col) + ";r:" + str(self.row) + ";v:" + str(self.val) + ")"

    def copy(self):
        return Circle(self.val, self.row, self.col)

    def equals(self, circle):
        if type(circle) is not Circle:
            return False
        else:
            if self.row == circle.row and self.col == circle.col:
                return True
            return False
