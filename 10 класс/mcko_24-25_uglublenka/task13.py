with open("13.txt", 'r') as file_in:
  mas = [int(i.strip()) for i in file_in.readlines()] #убераем символы переноса строки
  n = min(mas) #минимальное в файле число, т.к. можно посмотреть что это за число (8) можно 
               # не проверять делится ли оно на 15,т.к. 8 точно не делится и значит подходит нам
res = []
for i in range(len(mas)):
  if i < len(mas) - 1: #чтобы не выйти за массив, т.к. берем i+1
    if mas[i]%n==0 and mas[i+1]%n==0: #проверяем делимость на самое маленькое число в списке
      res.append(mas[i]+mas[i+1])
print(len(res), max(res))
