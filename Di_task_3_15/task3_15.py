from math import sqrt


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
            f.write('(' + ' '.join(point) + ') ')
        f.write('\n')
    f.close()


# def get_triangle_list(points_list):
# return combinations(points_list, 3)


def gen_of_triangle(points_list):
    i = 0
    while i < len(points_list):
        j = i + 1
        while j < len(points_list):
            k = j + 1
            while k < len(points_list):
                yield (points_list[i], points_list[j], points_list[k])
                k += 1
            j += 1
        i += 1


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


triangle_list = list(gen_of_triangle(get_points_list_from_file('res/input.txt')))
print(triangle_list)
sorted_list = sort_triangle(triangle_list)
print(sorted_list)
print_triangle_to_file(sorted_list, 'res/output.txt')
