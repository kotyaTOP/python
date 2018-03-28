from math import sqrt
from itertools import combinations
from functools import reduce


def get_points_list_from_file(file_name):
    f = open(file_name, 'r')
    a = [str(str(item).replace('\n', '')).split(' ') for item in f.readlines()]
    f.close()
    return a


def print_triangle_to_file(triangle_list, file_name):
    f = open(file_name, 'w')
    # result = [' '.join(item) for item in triangle]
    for triangle in triangle_list:
        for point in triangle:
            f.write('('+' '.join(point)+') ')
        f.write('\n')
    f.close()


def get_triangle_list(points_list):
    return combinations(points_list, 3)


def get_len_line(p1, p2):
    return sqrt(pow((int(p1[0]) - int(p2[0])), 2) + pow((int(p1[1]) - int(p2[1])), 2))


def get_square(triangle):
    a = get_len_line(triangle[0], triangle[1])
    b = get_len_line(triangle[0], triangle[2])
    c = get_len_line(triangle[1], triangle[2])
    p = 0.5 * (a + b + c)
    return sqrt(p * (p - a) * (p - b) * (p - c))


def sort_triangle(triangle_list):
    return sorted(triangle_list, key=lambda triangle: get_square(triangle))


input_list = list(get_triangle_list(get_points_list_from_file('res/input.txt')))
sorted_list = sort_triangle(input_list)
print(sorted_list)
print_triangle_to_file(sorted_list, 'res/output.txt')
