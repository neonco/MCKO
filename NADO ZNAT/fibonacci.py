step = 100_000_001

# динамическое проганье (цикл + память)
m = [1, 1]
for _ in range(step-2):
    res = m[-1] + m[-2]
    m.append(res % 1000)

print(m[-1])
print(len(m))


# цикл, но без дополнительной памяти
a, b = 1, 1
for _ in range(step-2):
    a, b = b, (a+b) % 1000

print(a, b)


# рекурсия без памяти
def f(n):
    if n in (1, 2):
        return 1
    else:
        return f(n-1) + f(n-2)

print(f(10))