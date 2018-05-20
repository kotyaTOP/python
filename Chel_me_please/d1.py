with open('numbers1.rr', 'r') as f:
    RR_list = [int(x) for x in f.read().splitlines()]
RR_lena = []
for my_iter in range(len(RR_list)):
    RR_lena.append(my_iter + 1)
with open('start_curve.txt', 'a') as f:
    for my_iter in range(len(RR_list)):
        print('[', RR_lena[my_iter], ',', RR_list[my_iter], ']', sep='', end=', ', file=f)
new_RR = []
s = 0
for my_iter in range(9, len(RR_list)):
    for my_j in range(my_iter - 9, my_iter):
        s += RR_list[my_j]
    new_RR.append(0.1 * s)
    s = 0
for my_iter in range(len(RR_list), 9):
    for my_j in range(my_iter - 9, my_iter):
        s += RR_list[my_j]
    new_RR.append(0.1 * s)
    s = 0
with open('curve1.txt', 'a') as f:
    for my_iter in range(len(new_RR)):
        print('[', RR_lena[my_iter], ',', round(new_RR[my_iter], 2), ']', sep='', end=', ', file=f)
relax_list = []
work_list = []
for my_iter in range(len(RR_list)):
    if my_iter < 378 or my_iter >= 454:
        relax_list.append(RR_list[my_iter])
    else:
        work_list.append(RR_list[my_iter])

work_counter = relax_counter = 0
n = 500
while n <= 1000:
    for my_iter in range(len(relax_list)):
        if relax_list[my_iter] >= n:
            relax_counter += 1
    for my_iter in range(len(work_list)):
        if work_list[my_iter] <= n:
            work_counter += 1
    with open('curve1res.txt', 'a') as f:
        print('[', round(100 * work_counter / len(work_list), 2), ',', round(100 * relax_counter / len(relax_list), 2),
              ']', sep='', end=', ', file=f)
    work_counter = relax_counter = 0
    n += 20
