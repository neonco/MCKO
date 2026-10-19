from sys import setrecursionlimit

setrecursionlimit(12000)

def f(n):
    if n == 1:
        return 1
    return f(n-1) * (n+1)


res = (f(11_000) + 5*f(10_999)) / f(10_998)
print(res)

# 121066000