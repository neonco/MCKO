from ctypes import c_float

n = c_float(-27.125)
print(n)
b = bytes(n)
print(b)
# b'\x00\x00\xd9\xc1' в обратном порядке по паре
# в ответ C1D90000
