def cycle_shift(array, n):
    slice_list = array[(len(array) - n):]
    slice_list.extend(array[:len(array) - n])
    return slice_list



def get_matrix_from_file(f_name):
    with open(f_name, 'r') as f:
        return [str(str(item).replace('\n', '')).split(' ') for item in f.readlines()]


def print_matrix_to_file(matrix, f_name):
    f = open(f_name, 'w')
    # b = [str(item) for item in matrix]
    result = (' '.join(item) for item in matrix)
    for item in result:
        f.write(item+'\n')
    f.close()


n = 3
l = get_matrix_from_file('res/input.txt')
result = [cycle_shift(list_item, n) for list_item in l]
print(cycle_shift(result, n))
print_matrix_to_file(cycle_shift(result, n), 'res/output.txt')
