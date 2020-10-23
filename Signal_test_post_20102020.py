# import os
import math
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq
from Mymodules import analitic_disp_array as an_disp
from Mymodules import absol, peak_picking

# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [10, 50]
list_lambda = [0.4, 3]
list_w = [10, 30]
diapason = [60, 0.01]
displ_arr = an_disp(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(displ_arr[0], displ_arr[1], 'g')
# plt.xlim([0, 5])
# plt.show()

# Дискретное преобразование Фурье над двумерным массивом
spectrum = fft(displ_arr[1], n=None, axis=-1)
spectrum = spectrum[:len(spectrum)//2]

# получение действительного массива
spectrum = absol(spectrum)
spctr = [0 for i in range(len(spectrum))]
for i in range(len(spectrum)):
    temp = spectrum[i]
    spctr[i] = temp.real

Disc_freq = diapason[1]
x = fftfreq(len(spctr), Disc_freq)  # в герцах
x = x[:len(x)//2]*math.pi  # в радианах
y = spctr[:len(spctr)//2]


# Получение матрицы с 2 локальными экстремумами, отсортированными по убыванию
# Extremums = some_rezonanses(2, x, y)
# print('Рез амплитуды', Extremums[0], "\nРез частоты", Extremums[1], "\nРез индексы", Extremums[2] )

# Применение метода половинной мощности
# for i in range(2):
#     print("Демфирование для ", i+1, " резонанса ", peak_picking_an(Extremums[2][i], x, y)

# Получение по МПМ демпфирования для заданной частоты
chosen_rez = 10  # выбранная частота резонанса
dempf = peak_picking(x, y, chosen_rez)  # демпфирование по МПМ
print('Демфирование для частоты резонанса ', chosen_rez, ' \t', dempf)
print('Логарифмический декремент затухания \t\t', chosen_rez*dempf)

# Построение графика
fig, ax = plt.subplots()
ax.plot(x, y, 'g')
ax.grid()
plt.xlim([0, max(x)/3])
plt.ylim([0, max(y)])
plt.show()
# добавил преобразоване Фурье
# Добавил ещё что-то
