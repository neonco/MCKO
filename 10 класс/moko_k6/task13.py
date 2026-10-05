f = open('13.txt').readlines()

# t = []
# for string in f:
#     t.append(int(string))
# f = t

f = [int(string) for string in f]
n = min([x for x in f if x % 15 != 0])
print(n)

res = []
for i in range(len(f)):
    if f[i] % n == 0 and f[i+1] % n == 0:
        res.append(f[i] + f[i+1])

print(len(res), max(res))

# 157 176024