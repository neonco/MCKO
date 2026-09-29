from functools import cache

@cache
def f(x, end):
    if x == end:
        return 1
    if x > end:
        return 0
    if x == 32:
        return 0
    return f(x+3, end) + f(x+4, end) + f(x*3, end)


print(f(4, 16) * f(16, 46))
