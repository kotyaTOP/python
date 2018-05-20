def foo(all_nums, rest, stress):
    roc = []
    minimum = int(round(min([item[1] for item in all_nums]), -2))
    maximum = int(round(max([item[1] for item in all_nums]), -2))
    for line in range(minimum, maximum, 25):
        sensitivity = len(list(filter(lambda x: x[1] <= line and x in stress, all_nums))) / len(stress)
        sensitivity = sensitivity * 100 if sensitivity <= 1 else 100
        specificity = len(list(filter(lambda x: x[1] > line and x in rest, all_nums))) / len(rest)
        specificity = specificity * 100 if specificity <= 1 else 100
        roc.append([line, round(sensitivity, 2), round(specificity, 2)])
    return roc
