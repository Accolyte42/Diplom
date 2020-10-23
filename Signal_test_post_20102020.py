# import os
# import sympy
# from numpy import array, arange, abs as np_abs
from numpy.fft import fft, fftfreq
# from numpy.random import uniform
from Mymodules import *

# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [10, 50]
list_lambda = [0.4, 3]
list_w = [10, 30]
diapason = [60, 0.01]
temp_f = analitic_disp_array(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(temp_f[0], temp_f[1], 'g')
# plt.xlim([0, 5])
# plt.show()

# Дискретное преобразование Фурье над двумерным массивом
spectrum = fft(temp_f[1], n=None, axis=-1)
spectrum = spectrum[:len(spectrum)//2]

# получение действительного массива
spectrum = absol(spectrum)
spctr = [0 for i in range(len(spectrum))]
for i in range(len(spectrum)):
    temp = spectrum[i]
    spctr[i] = temp.real

Disc_freq = diapason[1]
x = fftfreq(len(spctr), Disc_freq)  # в герцах
x = x[:len(x)//2]*math.pi # в радианах
y = spctr[:len(spctr)//2]


# Получение матрицы с 2 локальными экстремумами, отсортированными по убыванию
# Extremums = some_rezonanses(2, y, x)
# print('Рез амплитуды', Extremums[0], "\nРез частоты", Extremums[1], "\nРез индексы", Extremums[2] )

# Применение метода половинной мощности
# for i in range(2):
#     print("Демфирование для ", i+1, " резонанса ", peak_picking_an(Extremums[2][i], y, x))

# Получение по МПМ демпфирования для заданной частоты
chosen_rez = 10  # выбранная частота резонанса
dempf = peak_picking(x, y, chosen_rez)  # демпфирование по МПМ
print('Демфирование для резонанса ', chosen_rez, ' \t', dempf)
print('Логарифмический декремент затухания \t', chosen_rez*dempf)

# Построение графика
fig = plt.figure()
plt.plot(x, y, 'g')
plt.xlim([0, 50])
plt.show()
# добавил преобразоване Фурье
# Добавил ещё что-то



