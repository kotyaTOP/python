def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]


import math
from functools import reduce


def foo(all_nums, rest, stress):
    roc = []
    rest_some_nums = split_list(rest, 10)
    rest_some_nums_average_values = [reduce(lambda a, x: a + x[1], item, 0) / len(item) for item in rest_some_nums]
    rest_some_nums_mid_sqr = [
        math.sqrt(reduce(lambda a, x: a + (x[1] - rest_some_nums_average_values[idx]) ** 2, item, 0) / len(item))
        for idx, item, in enumerate(rest_some_nums)]
    stress_some_nums = split_list(rest, 10)
    stress_some_nums_average_values = [reduce(lambda a, x: a + x[1], item, 0) / len(item) for item in stress_some_nums]
    stress_some_nums_mid_sqr = [
        math.sqrt(reduce(lambda a, x: a + (x[1] - stress_some_nums_average_values[idx]) ** 2, item, 0) / len(item))
        for idx, item, in enumerate(stress_some_nums)]
    rest_average_value = reduce(lambda a, x: a + x[1], rest, 0) / len(rest)
    rest_mid_sqr = math.sqrt(reduce(lambda a, x: a + (x[1] - rest_average_value) ** 2, rest, 0) / len(rest))
    stress_average_value = reduce(lambda a, x: a + x[1], stress, 0) / len(stress)
    stress_mid_sqr = math.sqrt(reduce(lambda a, x: a + (x[1] - stress_average_value) ** 2, stress, 0) / len(stress))

    diff = math.fabs(rest_mid_sqr - stress_mid_sqr)
    # minimum = int(min(rest_mid_sqr, stress_mid_sqr) - 10)
    # maximum = int(max(rest_mid_sqr, stress_mid_sqr) + 10)
    for line in range(0, int(diff), 3):
        sensitivity = len(list(
            filter(lambda x: math.fabs(x - stress_mid_sqr) <= line, stress_some_nums_mid_sqr))) / (
                              len(stress_some_nums) + len(rest_some_nums))
        sensitivity = sensitivity * 100 if sensitivity <= 1 else 100
        specificity = len(list(filter(lambda x: math.fabs(x - rest_mid_sqr) <= line, rest_some_nums_mid_sqr))) / (
                len(stress_some_nums) + len(rest_some_nums))
        specificity = specificity * 100 if specificity <= 1 else 100
        roc.append([line, round(sensitivity, 2), round(specificity, 2)])
    return roc
