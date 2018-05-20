list = []


# with open('inputlist.txt') as il:
#   for line in il.readlines():
#      list.append([j for j in line.split()])


def try_parse(elem):
    try:
        return int(elem)
    except ValueError:
        return elem


def get_list_from_file(f_name):
    f = open(f_name, 'r')
    a = str(f.read()).split(' ')
    f.close()
    result = [try_parse(item) for item in a]
    return result


list = get_list_from_file('inputlist.txt')
print(list)


def get_answer(list):
    list_max = []
    list_tmp = []
    for i in list:
        sum_tmp = sum(list_tmp)
        sum_max = sum(list_max)
        if sum_tmp + i >= 0:
            list_tmp.append(i)
        if sum_tmp + i < 0:
            if sum_tmp > sum_max:
                list_max = list_tmp
            elif sum_tmp == sum_max:
                if len(list_tmp) < len(list_max):
                    list_max = list_tmp
            list_tmp = []
    return list_max


list = get_answer(list)
print(list)

f = open('answerlist.txt', 'w')
f.write(', '.join(map(str, list)))
f.close()

# def get_answer(s):
#    answer_list=[]
#    s.append(' ')
#    max_sum = 0
#    tmp_sum = 0
#    count_max = 0
#    count_tmp = 0
#    ind = 0
#    for i in range(len(s)):
#        if type(s[i]) is int:
#            count_tmp += 1
#            tmp_sum += int(s[i])
#        if type(s[i]) is not int or i == len(s)-1:
#            if count_tmp != 0:
#                if tmp_sum > max_sum:
#                    max_sum = tmp_sum
#                    count_max = count_tmp
#                    ind = i
#
#                if tmp_sum == max_sum:
#                    if count_tmp < count_max:
#                        max_sum = tmp_sum
#                        count_max = count_tmp
#                        ind = i
#
#                tmp_sum = 0
#                count_tmp = 0
#
#    i = ind - count_max
#    while i < ind:
#        answer_list.append(s[i])
#        i += 1
#    return answer_list

# return answerList
