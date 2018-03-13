def get_int_list_from_file(f_name):
    f = open(f_name, 'r')
    a = str(f.read()).split(' ')
    f.close()
    result = [int(item) for item in a]
    return result


def print_to_file(list_for_print, f_name):
    f = open(f_name, 'w')
    f.write(' '.join(map(str, list_for_print)))
    f.close()


def get_char_list_from_file(f_name):
    f = open(f_name, 'r')
    a = str(f.read()).split(' ')
    f.close()
    return a
