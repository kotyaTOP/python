from math import sqrt


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


def print_points_to_file(points, file_name):
    f = open(file_name, 'w')
    # b = [str(item) for item in matrix]
    result = [' '.join(item) for item in points]
    for item in result:
        f.write(item+'\n')
    f.close()



list = get_points_list_from_file('res/input.txt')


def get_len_line(p1,p2):
    return sqrt(pow(int(first(p1))-int(first(p2)),2) + pow(int(second(p1))-int(second(p2)),2))


def get_square(p1,p2,p3):
    a = get_len_line(p1,p2)
    b = get_len_line(p1,p3)
    c = get_len_line(p3,p2)
    p = 0.5*(a+b+c)
    return sqrt(p*(p-a)*(p-b)*(p-c))

# itertools

def get_max_square(points_list):
    p1 = 0
    max = 0
    list_of_max = []
    for i, points in enumerate(points_list):
        
    while p1 < len(points_list):
        p2 = p1+1
        while p2 < len(points_list):
            p3 = p2+1
            while p3 < len(points_list):
                square_tmp = get_square(points_list[p1], points_list[p2],points_list[p3])
                if square_tmp > max:
                    max = square_tmp
                    list_of_max = [points_list[p1], points_list[p2], points_list[p3]]
                p3 += 1
            p2 += 1
        p1 += 1
    return list_of_max


def get_list_from_points(points_list):
    answer_list = []
    for i in points_list:
        tmp = [first(i),second(i)]
        answer_list.append(tmp)
    return answer_list


print(get_list_from_points((get_max_square(list))))
print_points_to_file(get_list_from_points((get_max_square(list))),'res/output.txt')

