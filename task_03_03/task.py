def get_line_koef_list_from_file(f_name):
    f = open(f_name, 'r')
    lines = [str(item).replace('\n', '') for item in f.readlines()]
    result = [item.split(' ') for item in lines]
    result = [[int(i) for i in item] for item in result]
    f.close()
    return result


def get_pair(item):
    if int(item[1]) == 0:
        k = float('inf')
        c = -int(item[2]) / int(item[0])
    else:
        k = -int(item[0]) / int(item[1])
        c = -int(item[2]) / int(item[1])
    return k, c


def get_parallel_multiplies(ll):
    ans = [(get_pair(item), item) for item in ll]
    mm = {item[0][0]: list() for item in ans}
    for elem in ans:
        mm[elem[0][0]].append((elem[0][1], elem[1]))
    return mm


def get_top_from_multiple(mult_list):
    return max(mult_list, key=lambda x: x[0])[1]


all_mult = get_parallel_multiplies(get_line_koef_list_from_file('res/input.txt'))
print(all_mult)
for i in all_mult.values():
    print(get_top_from_multiple(i))
