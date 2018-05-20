from __future__ import print_function
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from src.gamelems.twelve.Field import *
from src.gamelems.twelve.Square import *
from src.gamelems.twelve.Presenter import *


my_field = Field(2, 2)
square1 = Square(0, 0, 2)
square2 = Square(2, 2, 2)
my_field.add_square(square1, square1.row, square1.col)
my_field.add_square(square2, square2.row, square2.col)

for row in my_field.matrix:
    for elem in row:
        if elem is None:
            print(None, end=' ')
        else:
            print(elem.val, end=' '),
    print("\n", end="")

g = my_field.add_nodes()
print(g.nodes())
g.add_edges_from(my_field.add_edges(g))
print(g.edges())
print(my_field.has_ways(square1, 1, 2))
my_field.move_square(square1, 0, 1)
for row in my_field.matrix:
    for elem in row:
        if elem is None:
            print(None, end=' ')
        else:
            print(elem.val, end=' '),
    print("\n", end="")

app = QApplication(sys.argv)
mw = My_Window(my_field)
qp = QPainter()
pr = Presenter(my_field, mw)
pr.draw_field(qp)
mw.show()
sys.exit(app.exec_())
