p = 5
q = 7
e = 11
f = (p - 1) * (q - 1)

for d in range(1, 40):
    g = ((d * e) % f == 1)
    print(d, g)

# 35