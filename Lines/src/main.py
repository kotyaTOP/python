from __future__ import print_function
from src.Circle import *
from src.Game import *

my_field = Field(5,5)
circle = Circle(0, 0, 3)
circle2 = Circle(1, 1, 3)
circle3 = Circle(2, 2, 3)
circle4 = Circle(3, 3, 3)
circle5 = Circle(4, 4, 3)
circle6 = Circle(1, 0, 3)
circle7 = Circle(2, 0, 3)
circle8 = Circle(3, 0, 3)
circle9 = Circle(4, 0, 3)


my_field.add_circle(circle, 0, 4)
my_field.add_circle(circle2, 1, 3)
my_field.add_circle(circle3, 2, 2)
my_field.add_circle(circle4, 3, 1)
my_field.add_circle(circle5, 4, 0)
my_field.add_circle(circle6, 0, 0)
my_field.add_circle(circle7, 1, 1)
my_field.add_circle(circle8, 3, 3)
my_field.add_circle(circle9, 4, 4)

for row in my_field.matrix:
    for elem in row:
        if elem is not None:
            print(elem.val, end=' ')
        else:
            print(elem, end=' ')
    print('\n')

print ('Стало')
my_field.check_delete(my_field.matrix[2][2])
for row in my_field.matrix:
    for elem in row:
        if elem is not None:
            print(elem.val, end=' ')
        else:
            print(elem, end=' ')
    print('\n')
