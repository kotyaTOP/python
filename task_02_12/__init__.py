def get_matrix_from_file(f_name):
    f = open(f_name, 'r')
    a = [str(str(item).replace('\n', '')).split(' ') for item in f.readlines()]
    f.close()
    return a


def print_matrix_to_file(matrix, f_name):
    f = open(f_name, 'w')
    # b = [str(item) for item in matrix]
    result = [' '.join(item) for item in matrix]
    for item in result:
        f.write(item + '\n')
    f.close()


def get_cut_matrix(matrix):
    row_count = len(list(matrix))
    column_count = min([len(item) for item in matrix])
    a = min(row_count, column_count)
    for iter_var in range(a):
        matrix[iter_var] = matrix[iter_var][:a]
    matrix = matrix[:a]
    return matrix


print_matrix_to_file(get_cut_matrix(get_matrix_from_file('res/input.txt')), 'res/output.txt')
