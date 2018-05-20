import math

import matplotlib.pyplot as plt


def plot_methods(methods):
    for method in methods:
        x_line = []
        y_line = []
        for i in range(len(method)):
            x_line.append(i)
            y_line.append(method[i])
        plt.plot(x_line, y_line)

    plt.xlabel("Time")
    plt.ylabel("Signal")
    plt.legend(("Original curve", "Smoothed curve (2х)", "Smoothed curve (4х)",
                "Deviation curve"))
    plt.show()


def plot_rocs(rocs):
    for roc in rocs:
        x_line = []
        y_line = []
        for item in roc:
            x_line.append(item[1])
            y_line.append(item[2])
        plt.plot(x_line, y_line)

    plt.xlabel("Sensitivity")
    plt.ylabel("Specificity")
    plt.legend(("Original curve", "Smoothed curve (2х)", "Smoothed curve (4х)",
                "Deviation curve"))
    plt.show()


def get_sequence(curve):
    sequence = []
    region = []
    desc = True if curve[1] < curve[0] else False
    for i in range(len(curve) - 1):
        region.append(curve[i])
        if desc:
            if curve[i + 1] > curve[i]:
                sequence.append(region)
                region = []
                desc = False
                continue
        else:
            if curve[i + 1] < curve[i]:
                sequence.append(region)
                region = []
                desc = True
                continue
    return sequence


def flatten_range_calculate(curve):
    sequence = get_sequence(curve)
    return sum(len(item) for item in sequence) / len(sequence) * 2


def flatten(curve):
    flatten_range = flatten_range_calculate(curve)
    flattened_curve = []
    for i in range(len(curve)):
        flatten_sum = 0
        skipped = 0
        for j in range(int(-flatten_range / 2), int(flatten_range / 2)):
            if i + j < 0 or i + j >= len(curve):
                skipped += 1
                continue
            flatten_sum += curve[i + j]
        flattened_curve.append(flatten_sum / (int(flatten_range / 2) * 2 - skipped))
    return flattened_curve


def average(curve):
    return sum(curve) / len(curve)


def get_rocs(curve, begin, end):
    double_flattened = flatten(flatten(curve))
    ultra_flattened = flatten(flatten(double_flattened))
    relative_reversed = [double_flattened[i] - curve[i] for i in range(len(curve))]
    mean = average(relative_reversed)
    relative = [mean - relative_reversed[i] for i in range(len(curve))]
    deviation = [math.sqrt(sum((relative[j] - relative[i]) ** 2 for j in range(len(curve))) / len(curve))
                 for i in range(len(curve))]
    methods = [curve, double_flattened, ultra_flattened, relative]
    rocs = []
    for method in methods:
        rest = method[:begin] + method[end:]
        stress = method[begin:end]
        roc = []
        minimum = int(min(method))
        maximum = int(max(method))
        step = int((maximum - minimum) / 50)
        if method == relative or method == deviation:
            rest = get_sequence(method[:begin]) + get_sequence(method[end:])
            stress = get_sequence(method[begin:end])
            rest = [item[-1] for item in rest]
            stress = [item[-1] for item in stress]
            if method == deviation:
                rest = [rest[i] for i in range(0, len(rest), 2)]
            for line in range(0, maximum, step if step > 0 else 1):
                sensitivity = len(list(filter(lambda x: abs(x) <= line, stress))) / len(stress) * 100
                specificity = len(list(filter(lambda x: abs(x) > line, rest))) / len(rest) * 100
                roc.append([line, round(sensitivity, 5), round(specificity, 5)])
            rocs.append(roc)
            continue
        for line in range(minimum, maximum, step if step > 0 else 1):
            sensitivity = len(list(filter(lambda x: x <= line, stress))) / len(stress) * 100
            specificity = len(list(filter(lambda x: x > line, rest))) / len(rest) * 100
            roc.append([line, round(sensitivity, 5), round(specificity, 5)])
        rocs.append(roc)
    plot_methods(methods)
    plot_rocs(rocs)
    return rocs


people = [[436, 509], [378, 454], [451, 535]]
current = 2
numbers = list(map(int, open("numbers" + str(current) + ".rr", "r").read().split("\n")[1:-1]))
result = get_rocs(numbers, people[current][0], people[current][1])
