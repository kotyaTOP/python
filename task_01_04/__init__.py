from MyFileManager.filemng import get_int_list_from_file
from MyFileManager.filemng import print_to_file


def get_list_neg_begin(list_of_values):
    i = 0
    for a in range(len(list(list_of_values))):
        if int(list_of_values[a]) < 0:
            replace_all(list_of_values, i, a)
            i += 1
    return list_of_values

def decorator(func):
    def swarpe(list_of_values):
        i = 0
        for a in range(len(list(list_of_values))):
            if int(list_of_values[a]) < 0:
                func(list_of_values, first_pos = i, second_pos = a)
                i += 1
        return list_of_values
    return swarpe

@decorator
def replace_all(list_for_replace, first_pos = None, second_pos = None):
    if first_pos == second_pos:
        return list_for_replace
    temp_var = list(list_for_replace)[int(second_pos)]
    iter_var = int(second_pos)
    while iter_var > int(first_pos):
        list_for_replace[int(iter_var)] = list_for_replace[int(iter_var) - 1]
        iter_var -= 1
    list_for_replace[first_pos] = temp_var
    return list_for_replace


print_to_file(replace_all(get_int_list_from_file('res/input.txt')), 'res/output1.txt')
print_to_file(replace_all([-1, 1, -2, 2, -3, 3, -4]), 'res/output2.txt')
print_to_file(replace_all([-1, 1, -2, 2, -3, 3]), 'res/output3.txt')
print_to_file(replace_all([1, 1, -2, 2, -3, 3, -4]), 'res/output4.txt')
print_to_file(replace_all([1, 1, -2, 2, -3, 3]), 'res/output5.txt')
