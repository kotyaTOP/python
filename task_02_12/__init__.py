def get_list_from_file(f_name):
    f = open(f_name, 'r')
    a = str(f.read()).split(' ')
    f.close()
    result = [int(item) for item in a]
    return result


def print_to_file(list_for_print, f_name):
    f = open(f_name, 'w')
    f.write(' '.join(map(str, list_for_print)))
    f.close()


def get_matrix_from_file(f_name):
    f = open(f_name, 'r')



def print_matrix_to_file(matrix, f_name):
    f = open(f_name, 'w')
    f.writelines(map(' '.join([str(item) for item in matrix])))
    f.close()


def get_cut_matrix(matrix):
    column_count = len(list(matrix)[0])
    row_count = len(list(matrix))
    if column_count > row_count:
        for iter_var in range(len(matrix)):
            matrix[iter_var] = matrix[iter_var][:column_count]
    elif column_count < row_count:
        matrix = matrix[:row_count]
    return matrix


print_matrix_to_file(get_cut_matrix(get_matrix_form_file))
