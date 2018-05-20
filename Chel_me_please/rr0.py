with open('1Relax.txt', 'r') as f:
    relax_list = [int(x) for x in f.read().splitlines()]
with open('1Work.txt', 'r') as f:
    work_list = [int(x) for x in f.read().splitlines()]
work_counter = relax_counter = 0
n = 500
while n <= 1000:
    for my_iter in range(len(relax_list)):
        if relax_list[my_iter] >= n:
            relax_counter += 1
    for my_iter in range(len(work_list)):
        if work_list[my_iter] <= n:
            work_counter += 1
    with open('res.txt', 'a') as f:
        print('[', 100 * relax_counter / len(relax_list), ', ',
              100 * work_counter / len(work_list), ']', sep='', end=', ', file=f)
    work_counter = relax_counter = 0
    n += 20
