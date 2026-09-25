from string import digits, ascii_uppercase

alph = digits + ascii_uppercase
print(alph)
# 154x3 + 1x365
for x in range(12):
    a = 1 * 12**4 + 5 * 12**3 + 4 * 12**2 + x * 12**1 + 3 * 12**0
    b = 1 * 12**4 + x * 12**3 + 3 * 12**2 + 6 * 12**1 + 5 * 12**0
    s = a + b
    print(x, s / 13)

# 4340

# for x in alph[:12]:
for x in '0123456789AB':
    a = int(f'154{x}3', 12)
    b = int(f'1{x}365', 12)
    s = a + b
    print(x, s / 13)

# 4340
