def generator_fib():
    prevprev = 0
    prev = 1
    yield prevprev
    yield  prev
    while True:
        tmp = prev + prevprev
        yield tmp
        prevprev, prev = prev, tmp



def first_n(fib, n):
    i = 0
    for v in fib:
        if i < n:
            yield v
            i += 1



fib = generator_fib()
for i in first_n(fib,10):
    print(i)


