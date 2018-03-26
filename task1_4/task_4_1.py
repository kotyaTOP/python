import re
from collections import Counter


def print_to_file(list_for_print, f_name):
    with open(f_name, 'w', encoding='UTF-8') as f:
        f.write(' '.join(map(str, list_for_print)))


def get_string_from_file(f_name):
    with open(f_name, encoding='UTF-8') as f:
        return f.readline()


def get_special_words(word_list, n_symbol):
    return filter(lambda word: max(Counter(word).values()) >= n_symbol, word_list)


print(list(get_special_words(filter(None, re.split('\W', get_string_from_file('res/input.txt'))), 3)))
print_to_file(list(get_special_words(filter(None, re.split('\W', get_string_from_file('res/input.txt'))),
                                     3)), 'res/output.txt')
