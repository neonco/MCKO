from itertools import product


c = 0
a = sorted('ВЕСНА')
for x, y, z, w in product(a, repeat=4):
    c += 1
    word = x + y + z + w
    if 'Е' not in word and 'АА' not in word:
        print(c, word)