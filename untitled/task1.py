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


def get_answer(list):
    answer_list = []
    list.append(' ')
    count_max = 0
    count_tmp = 0
    sum_max = 0
    sum_tmp = 0
    last = 0
    for i in range(len(list)):
        if list[i] != ' ' and  sum_tmp + int(list[i]) >= 0:
            sum_tmp += int(list[i])
            count_tmp += 1
        if list[i] == ' ' or sum_tmp + int(list[i]) < 0:
            if sum_tmp > sum_max:
                sum_max = sum_tmp
                count_max = count_tmp
                last = i
            elif sum_tmp == sum_max:
                if count_tmp < count_max:
                    sum_max = sum_tmp
                    count_max = count_tmp
                    la7\,st = i
            count_tmp = 0
            sum_tmp = 0
    i = last - count_max
    while i < last:
        answer_list.append(list[i])
        i += 1
    return answer_list


list = get_answer(list)
print(list)

f = open('answerlist.txt', 'w')
f.write(', '.join(map(str, list)))
f.close()
# return answerList
