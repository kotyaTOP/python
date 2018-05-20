class KoefClass:
    def __init__(self, item):
        self.item = item
        if int(item[1]) == 0:
            self.k = float('inf')
            self.c = -int(item[2]) / int(item[0])
        else:
            self.k = -int(item[0]) / int(item[1])
            self.c = -int(item[2]) / int(item[1])


class Koefs:
    def __init__(self, data: list):
        self.data = data
        self.n = len(data)
        self.p = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.p += 1
        if self.p >= self.n:
            self.p = -1
            raise StopIteration
        return self.data[self.p]


def get_parallel_multiplies_decr(func):
    def returnee(*args, **kwargs):
        def get_parallel_multiplies(ll):
            ans = Koefs([KoefClass(item) for item in ll])
            mm = {item.k: list() for item in ans}
            for elem in ans:
                mm[elem.k].append(elem)
            return mm

        return get_parallel_multiplies(func(*args, **kwargs))

    return returnee


@get_parallel_multiplies_decr
def get_line_koef_list_from_file(f_name):
    f = open(f_name, 'r')
    lines = [str(item).replace('\n', '') for item in f.readlines()]
    result = [item.split(' ') for item in lines]
    result = [[int(i) for i in item] for item in result]
    f.close()
    return result


def get_top_from_multiple(mult_list: list):
    return max(mult_list, key=lambda x: x.c).item


all_mult = get_line_koef_list_from_file('res/input.txt')
for i in all_mult.values():
    print(get_top_from_multiple(i))
