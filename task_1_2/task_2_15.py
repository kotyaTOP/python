def decorator(func):
    def swapper_for_cycle_shift(args, n):
        new_args = [func(list_item, n) for list_item in args]
        return func(new_args, n)
    return swapper_for_cycle_shift


@decorator
def cycle_shift(array, n):
    n = n % len(array)
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


n = 5
l = get_matrix_from_file('res/input.txt')
answer = cycle_shift(l, n)
print_matrix_to_file(answer, 'res/output.txt')
print(answer)