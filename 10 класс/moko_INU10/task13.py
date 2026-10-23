file = open('13.txt').readlines()

m = [int(x) for x in file]

# n = 11111111111111111
# for x in m:
#     if x % 15 != 0:
#         if x < n:
#             n = x
print(min(m))

n = 8

# for i in range(len(m)-1):
#     print(m[i], m[i+1])

res = []
for a, b in zip(m, m[1:]):
    if a % n == 0 and b % n == 0:
        res.append(a + b)

print(len(res), max(res))