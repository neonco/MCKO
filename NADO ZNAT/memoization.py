from time import time
from functools import lru_cache, cache


@cache
def f(n):
    if n in (1, 2):
        return 1
    else:
        return f(n-1) + f(n-2)


# d = {1:1, 2:1}
# def f(n):
#     if n in d:
#         return d[n]
#     else:
#         res = f(n-1) + f(n-2)
#         d[n] = res
#         return res


for n in range(1, 500):
    start = time()
    res = f(n)
    end = time()
    print(n, res, end - start)

print(f.cache_info())
