for n in range(1, 300):

    b = bin(n)[2:]
    if n % 2 == 0:
        b = b + '11'
    else:
        b = '1' + b + '10'
    res = int(b, 2)
    if res > 505:
        print(n, res)