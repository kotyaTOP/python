import re


def print_to_file(list_for_print, f_name):
    with open(f_name, 'w', encoding='UTF-8') as f:
        f.write(' '.join(map(str, list_for_print)))


def get_string_from_file(f_name):
    with open(f_name, encoding='UTF-8') as f:
        return f.readline()


def is_special_word(input_word):
    return len(re.findall('[аеёиоуыэюяАЕЁИОУЫЭЮЯ]', input_word)) > len(re.findall('[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]', input_word))


def get_special_words(input_list):
    return filter(lambda elem: is_special_word(elem), input_text)


input_text = filter(None, re.split('[^а-яА-Я]', get_string_from_file('res/input.txt')))
special_words = get_special_words(input_text)
print(list(special_words))
print_to_file(list(special_words), 'res/output.txt')
