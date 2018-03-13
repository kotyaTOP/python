def cycle_shift(array, n):
    slice = array[(len(array) - n):]
    slice.extend(array[:len(array) - n])
    return slice

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
        f.write(item+'\n')
    f.close()


n = 3
list = get_matrix_from_file('res/input.txt')
result = [cycle_shift(list_item,n) for list_item in list]
print(cycle_shift(result, n))
print_matrix_to_file(cycle_shift(result, n),'res/output.txt')
