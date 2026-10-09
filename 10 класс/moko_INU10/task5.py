# for x in range(2):
#     for y in (0, 1):
#         for z in (True, False):
#             for w in range(2):

from itertools import product, combinations, combinations_with_replacement, permutations

for x, y, z, w in product(range(2), repeat=4):
    f = (not(not y == x) or not (not y or z)) or w
    if f == 0:
        print(y, z, w, x, f)

# yzwx

print('------')
for x in product('ABC', repeat=2):
    print(x)

print('------')
for x in combinations('ABC', r=2):
    print(x)

print('------')
for x in combinations_with_replacement('ABC', r=2):
    print(x)

print('------')
for x in permutations('ABC', r=2):
    print(x)