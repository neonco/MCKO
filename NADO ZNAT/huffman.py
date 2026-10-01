s = 'АВИАЗАВОД'

# считаем буквы через метод count
for bukva in set(s):
    print(bukva, s.count(bukva))

# через словарь руками
d = dict()
for bukva in s:
    if bukva in d:
        d[bukva] += 1
    else:
        d[bukva] = 1

print(d)
