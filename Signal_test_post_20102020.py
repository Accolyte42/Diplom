# import os
import math
import matplotlib.pyplot as plt
import numpy as np
from Mymodules import analitic_disp_array as an_disp
from Mymodules import peak_picking

# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

w_list = [
        [4, 9],
        [22, 28]
]  # выбранная частота резонанса
print(len(w_list))

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [45, 34]
list_lambda = [0.7, 2]
list_w = [6, 25]
diapason = [60, 0.01]
displ_arr = an_disp(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(displ_arr[0], displ_arr[1], 'g')
# plt.xlim([0, 5])
# plt.show()

# Дискретное преобразование Фурье над двумерным массивом
X = np.fft.fft(displ_arr[1])
N = len(displ_arr[1])
freq = np.linspace(0, 1 / (displ_arr[0][1] - displ_arr[0][0]), N)[: (N // 2)]
X_amp = (1/N) * 2 * np.abs(X)[: (N // 2)]
X_phs = (1/N) * np.angle(X)[: (N // 2)]

# Получение по МПМ демпфирования для заданной частоты
dempf = peak_picking(freq, X_amp, w_list)  # демпфирование по МПМ
print('Найденный резонансные частоты', dempf[0], '\nНайденные демпфирования', dempf[1])
print('Демпф для частот резо ', dempf[0], ' \t', dempf[1])
print('Лог декр зат ', dempf[0][0]*2*math.pi*dempf[1][0], ' ,', dempf[0][1]*2*math.pi*dempf[1][1])

fig, ax = plt.subplots()
ax.plot(freq, X_amp, 'g')
plt.show()

# fig, ax = plt.subplots()
# ax.plot(freq, X_phs, 'g')
# plt.show()
