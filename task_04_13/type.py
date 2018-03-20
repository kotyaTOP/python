import MyFileManager.filemng


def sub(root, word):
    r = root[0].upper() if word[0].isupper() else root[0].lower()
    return r + root[1:] + word[len(root):]


def do_need_sub(root, word):
    if len(word) < len(root):
        return False
    error_count = 0
    for i in range(len(root)):
        if root[i].lower() != word[i].lower():
            error_count += 1
    return error_count == 1


def fix_type(roots, string):
    for root in roots:
        if do_need_sub(root, string):
            return sub(root, string)
    return string


def fix_all_types(roots, strings):
    for s_idx in range(len(strings)):
        strings[s_idx] = fix_type(roots, strings[s_idx])
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
        fix_all_types(roots_collection[idx], words_collection[idx])))
for elem in result_collection:
    print(elem)
