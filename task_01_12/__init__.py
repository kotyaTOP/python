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


def get_chet_ne_chet_list(list1, list2):
    longest_list = list1 if len(list(list1)) > len(list(list2)) else list2
    another_list = list1 if len(list(list1)) < len(list(list2)) else list2
    chet_ne_chet_list = []
    iter_var = 0
    while iter_var < len(longest_list):
        if iter_var + 1 > len(another_list):
            chet_ne_chet_list.append(longest_list[iter_var])
        elif iter_var % 2 == 0:
            chet_ne_chet_list.append(list1[iter_var])
        else:
            chet_ne_chet_list.append(list2[iter_var])
        iter_var += 1
    return chet_ne_chet_list


print(get_chet_ne_chet_list(get_list_from_file('res/f1.txt'), get_list_from_file('res/f2.txt')))
