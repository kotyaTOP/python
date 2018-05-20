from collections import Counter


def get_list_from_file(f_name):
    f = open(f_name, 'r')
    a = str(f.read()).split(' ')
    f.close()
    return a


def print_to_file(list_for_print, f_name):
    f = open(f_name, 'w')
    f.write(' '.join(map(str, list_for_print)))
    f.close()


def get_new_list(input_list):
    input_list.reverse()
    return list(filter(lambda item: Counter(input_list)[item] % 2 == 0, Counter(input_list).keys()))


print(get_new_list(get_list_from_file('res/input.txt')))
print_to_file(get_new_list(get_list_from_file('res/input.txt')),'res/output.txt')
