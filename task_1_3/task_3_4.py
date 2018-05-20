from math import sqrt
from itertools import combinations
from functools import reduce


def make_pair(x, y):
    return lambda n: x if n == 0 else y


def first(p):
    return p(0)


def second(p):
    return p(1)


def get_points_list_from_file(file_name):
    f = open(file_name, 'r')
    a = [str(str(item).replace('\n', '')).split(' ') for item in f.readlines()]
    a = [make_pair(b[0], b[1]) for b in a]
    f.close()
    return a


def get_list_from_points(points_list):
    answer_list = []
    for i in points_list:
        tmp = [first(i), second(i)]
        answer_list.append(tmp)
    return answer_list


def print_points_to_file(points, file_name):
    f = open(file_name, 'w')
    # b = [str(item) for item in matrix]
    result = [' '.join(item) for item in points]
    for item in result:
        f.write(item + '\n')
    f.close()


def get_len_line(p1, p2):
    return sqrt(pow(int(first(p1)) - int(first(p2)), 2) + pow(int(second(p1)) - int(second(p2)), 2))


def get_square(triangle):
    a = get_len_line(triangle[0], triangle[1])
    b = get_len_line(triangle[0], triangle[2])
    c = get_len_line(triangle[1], triangle[2])
    p = 0.5 * (a + b + c)
    return sqrt(p * (p - a) * (p - b) * (p - c))


def get_max_square(points_list):
    return reduce(lambda max_triangle, cur_triangle: cur_triangle if get_square(cur_triangle) >= get_square(
        max_triangle) else max_triangle, combinations(points_list, 3))


list = get_points_list_from_file('res/input.txt')
print(get_list_from_points((get_max_square(list))))
print_points_to_file(get_list_from_points((get_max_square(list))), 'res/output.txt')
