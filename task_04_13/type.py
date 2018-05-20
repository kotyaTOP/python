import MyFileManager.filemng


def sub(root, word):
    r = root[0].upper() if word[0].isupper() else root[0].lower()
    return r + root[1:] + word[len(root):]


def do_need_sub(root, word, err_c=1):
    if len(word) < len(root):
        return False
    error_count = 0
    for i in range(len(root)):
        if root[i].lower() != word[i].lower():
            error_count += 1
    return 0 < error_count <= err_c


def fix_type(roots, string, err_c=1):
    for root in roots:
        if do_need_sub(root, string, err_c):
            return sub(root, string)
    return string


def fix_all_types(roots, strings, err_c=1):
    for s_idx in range(len(strings)):
        strings[s_idx] = fix_type(roots, strings[s_idx], err_c)
    return strings


roots_collection = [
    MyFileManager.filemng.get_char_list_from_file('res/roots_1.txt'),
    MyFileManager.filemng.get_char_list_from_file('res/roots_2.txt')
]
words_collection = [
    MyFileManager.filemng.get_char_list_from_file('res/words_1.txt'),
    MyFileManager.filemng.get_char_list_from_file('res/words_2.txt')
]
result_collection = list()
for idx in range(len(roots_collection)):
    result_collection.append(' '.join(
        fix_all_types(roots_collection[idx], words_collection[idx], 2)))
for elem in result_collection:
    print(elem)
