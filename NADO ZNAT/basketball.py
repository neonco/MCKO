from time import time
from functools import cache

a, b, c = 1, 2, 4

for _ in range(100-3):
    a, b, c = b, c, a+b+c
print(c)
print(len(str(c)))

# a b c (a+b+c)
# 1 2 4 7
#   a b c

@cache
def f(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4
    return f(n-1) + f(n-2) + f(n-3)


for n in range(1, 10000+1):
    start = time()
    print(n, f(n), time()-start)