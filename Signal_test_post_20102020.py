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
list_A = [8, 20]
list_lambda = [0.8, 5]
list_w = [10, 30]
diapason = [60, 0.01]
temp_f = analitic_disp_array(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(temp_f[0], temp_f[1], 'g')
# plt.xlim([0, 5])
# plt.show()

# Вытаскиваниие из лист координат х и у точек
# x = table_data(worksheet, 1)
# y = table_data(worksheet, 2)

# убирание точек вокруг локальных максимумов
# в принципе, здесь надо делать сглаживание/аппроксимацию/интерполяцию
# для входных данных, т.к. пик может получиться слишком тонким
# a = (reduce_loop(1, x, y))
# x = a[0]
# y = a[1]

# Дискретное преобразование Фурье над двумерным массивом
spectrum = fft(temp_f[1], n=None, axis=-1)
spectrum = spectrum[:len(spectrum)//2]

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
chosen_rez = (30, 200)
print('Демфирование для ', chosen_rez, ' резонанса ', peak_picking(x, y, chosen_rez[0], chosen_rez[1]))


# Построение графика
# plt.plot(temp_f[0],temp_f[1])
# rect = [0, 0, 1, 1]
fig = plt.figure()
# ax = fig.add_axes(rect)
plt.plot(x, y, 'g')
plt.xlim([0, 50])
plt.show()
# добавил преобразоване Фурье
# Добавил ещё что-то



