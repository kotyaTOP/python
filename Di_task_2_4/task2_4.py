import itertools


def get_matrix_from_file(f_name):
    with open(f_name, 'r') as f:
        return [str(str(item).replace('\n', '')).split(' ') for item in f.readlines()]


def print_matrix_to_file(matrix, f_name):
    f = open(f_name, 'w')
    # b = [str(item) for item in matrix]
    result = (' '.join(item) for item in matrix)
    for item in result:
        f.write(item + '\n')
    f.close()


# def decorator_for_matrix(func):
#     def wrapper(arg):
#         arg = reverse_matrix(arg)
#         return func(arg)
#     return wrapper
#
#
# def reversed_matrix(func):
#     def wrapper(arg):
#         return reverse_matrix(func(arg))
#     return wrapper


def decorator_for_matrix(func):
    def wrapper(arg):
        arg = reverse_matrix(arg)
        return reverse_matrix(func(arg))
    return wrapper


def reverse_matrix(input_list):
    return [[row[i] for row in input_list] for i in range(len(input_list[0]))]


@decorator_for_matrix
def delete_clones(input_list):
    answer_list = []
    for elem in input_list:
        if not answer_list.__contains__(elem):
            answer_list.append(elem)
    return answer_list


input_list = get_matrix_from_file('res/input.txt')
answer_list = (delete_clones((input_list)))
print(answer_list)
print_matrix_to_file(answer_list, 'res/output.txt')
