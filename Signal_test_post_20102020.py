# import os
import math
import matplotlib.pyplot as plt
import numpy as np
from Mymodules import analitic_displ_array as an_displ
from Mymodules import peak_picking

# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# получение листа из таблицы
# worksheet = create_worksheet('Signal_Table.xls', 'Sheet_1')

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A = [45, 34]
list_lambda = [0.04, 0.1]
list_w = [6, 25]
diapason = [60, 0.01]
displ_arr = an_displ(list_A, list_lambda, list_w, diapason)

# fig = plt.figure()
# plt.plot(displ_arr[0], displ_arr[1], 'g')
# plt.xlim([0, 5])
# plt.show()


# Дискретное преобразование Фурье над двумерным массивом
Ampl_c = np.fft.fft(displ_arr[1])  # Массив комплексных амплитуд в АЧХ
N = len(displ_arr[1])  # количество точек
freq = np.linspace(0, 1/(displ_arr[0][1] - displ_arr[0][0]), N)[:(N//2)]
Ampl = (1/N) * np.abs(Ampl_c)[:(N//2)] * 2     # Массив действительных амплитуд АЧХ
Ampl_phs = (1/N) * np.angle(Ampl_c)[:(N//2)]   # Массив фаз для ФЧХ

# Выбранные интервалы для резонансной частоты
w_list = [[4,   9],
          [22, 28]]

# Получение по МПМ демпфирования для заданной частоты
dempf = peak_picking(freq, Ampl, w_list)  # демпфирование по МПМ
print('Найденный резонансные частоты', dempf[0], '\nНайденные демпфирования', dempf[1])
print('Лог декр зат ', dempf[0][0]*2*math.pi*dempf[1][0], ' ,', dempf[0][1]*2*math.pi*dempf[1][1])

fig, ax = plt.subplots()
ax.plot(freq, Ampl, 'g')
plt.show()

# fig, ax = plt.subplots()
# ax.plot(freq, X_phs, 'g')
# plt.show()
