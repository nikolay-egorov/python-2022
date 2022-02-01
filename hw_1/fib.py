def fib(n):
    a = b = 1
    for i in range(0, n - 1):
        c = b
        b = a + b
        a = c

    return b
