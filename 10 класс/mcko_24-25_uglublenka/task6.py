alph = 'АВЕНС'

count = 0
for c1 in alph:
    for c2 in alph:
        for c3 in alph:
            for c4 in alph:
                count += 1
                n = c1 + c2 + c3 + c4
                if 'Е' not in n and 'АА' not in n:
                    print(count, n)
# первое и есть ответ (27)