s = '3'*6 + '4'*75

while '35' in s or '355' in s or '3444' in s:
    if '35' in s:
        s = s.replace('35', '4', 1) # третий аргумент говорит что меняем только 1 вхождение слева
    if '355' in s:
        s = s.replace('355', '4', 1)
    if '3444' in s:
        s = s.replace('3444', '3', 1)

print(s)