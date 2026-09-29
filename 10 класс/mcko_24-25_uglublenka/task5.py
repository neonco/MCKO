for x in range(2):
    for y in range(2):
        for z in range(2):
            for w in range(2):
                f = (z == w) and (not x or y) or not w
                if f == 0:
                    print(w, x, z, y, f)