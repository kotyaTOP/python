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


def reversed_function(func):
    def wrapper(*arg):
        return reversed(list(func(*arg)))
    return wrapper


@reversed_function
def get_new_list(input_list):
    return filter(lambda item: Counter(input_list)[item] % 2 == 0, Counter(input_list).keys())


input_list = get_list_from_file('res/input.txt')
print(list(get_new_list(input_list)))
print_to_file(list(get_new_list(input_list)),'res/output.txt')
