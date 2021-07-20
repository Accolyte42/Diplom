# import os
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import csd
from numpy.linalg import svd
from Mymodules import analitic_displ_array as an_displ
from Mymodules import peak_picking, one_degree_coef, h_per, arr_sensor
import Config


# print(os.listdir()) # нужно, чтобы правильно ввести название excel-файла

# Задание функции АЧХ аналитически для проверки
# Получение координаты по х и по у аналитически через коэффициенты
list_A_1 = [1, 5, 6]
list_lambda_1 = [0.1, 0.2, 1]
list_w_1 = [10, 50, 70]
diapason_1 = [70, 0.001]
displ_arr1 = an_displ(list_A_1, list_lambda_1, list_w_1, diapason_1)

list_A_2 = [2, 4, 7]
list_lambda_2 = [0.05, 0.15, 1.2]
list_w_2 = [10, 50, 70]
diapason_2 = [70, 0.001]
displ_arr_2 = an_displ(list_A_2, list_lambda_2, list_w_2, diapason_2)

list_A_3 = [7, 3, 8]
list_lambda_3 = [0.3, 0.10, 1.1]
list_w_3 = [10, 50, 70]
diapason_3 = [70, 0.001]
displ_arr_3 = an_displ(list_A_3, list_lambda_3, list_w_3, diapason_3)

list_A_4 = [4, 5, 6]
list_lambda_4 = [0.35, 0.20, 1.5]
list_w_4 = [10, 50, 70]
diapason_4 = [70, 0.001]
displ_arr_4 = an_displ(list_A_4, list_lambda_4, list_w_4, diapason_4)

displ_arr = displ_arr1 + displ_arr_2 + displ_arr_3 + displ_arr_4

noise = np.random.normal(0, 0.1, len(displ_arr1[0]))
for i in range(len(displ_arr1[0])):
    displ_arr[1][i] = displ_arr[1][i] + noise[i]
    displ_arr[3][i] = displ_arr[3][i] + noise[i]
    displ_arr[5][i] = displ_arr[5][i] + noise[i]
    displ_arr[7][i] = displ_arr[7][i] + noise[i]

X = displ_arr[0]
Y = [displ_arr[1], displ_arr[3], displ_arr[5], displ_arr[7]]
# print(Y)

fig = plt.figure()
plt.plot(X, Y[0], 'g')
plt.title('Заданный сигнал во временной области')
plt.xlim([0, 2])
plt.grid()
# plt.show()

# Кусок для ОМА обработки

dt = X[1] - X[0]
fs = 1/dt
dscrt = 3000
Gyy = [0] * len(Y)
Temp_Gyy = [0] * len(Y)
for i in range(len(Y)):
    for j in range(len(Y)):
        # print(i, j)
        f, Temp_Gyy[j] = csd(Y[i], Y[j], fs, nperseg=dscrt)
    Gyy[i] = Temp_Gyy
    Temp_Gyy = [0] * len(Y)
    # Короче, хз из-за чего, но при переходе к новому i и применению функции csd
    # при присваивании значений в новой строке начинают меняться значения в старой строке
    # Для решения этой проблемы придумал такой костыль, чтоб при окончании строки
    # мы отдельно запоминали старую и всё
del Temp_Gyy

Gyy = np.array(Gyy)
print(len(Gyy), len(Gyy[0]), len(Gyy[0][0]))
print(Gyy[:, :, 5], 'test')

print(len(Gyy[:, :, 0]))
A = []
for i in range(len(Gyy[0][0])):
    U, S, V = svd(Gyy[:, :, i])
    A.append(S[0])

# сохраняем компоненты U V (на итерации)
# умножить первую строку U на первый столбец V и на сингулярное значение
# обратная функция к cpd матрицу во врем ряд
# эта матрица

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(f, A, 'g', label='Взаимная спектральная плотность')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.set_xlim([0, 100])
ax.legend()
ax.grid()


#
# Кусок для ЭМА обработки
#

# Дискретное преобразование Фурье над двумерным массивом
N = len(Y[0])  # количество точек
freq = np.linspace(0, 1/(X[1] - X[0]), N)[:(N//2)]
Ampl_c = [0] * len(Y)
Ampl = [0] * len(Y)
Ampl_phs = [0] * len(Y)
for i in range(len(Y)):
    Ampl_c[i] = np.fft.fft(Y[i])  # Массив комплексных амплитуд в АЧХ
    # 1 / N is a normalization factor
    Ampl[i] = (1/N) * np.abs(Ampl_c[i])[:(N//2)] * 2     # Массив действительных амплитуд АЧХ
    Ampl_phs[i] = (1/N) * np.angle(Ampl_c[i])[:(N//2)]   # Массив фаз для ФЧХ

print(len(freq), len(Ampl), len(Ampl_phs))

# Построение графиков
# Построение графика АЧХ
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(freq, Ampl[0], 'g', label='Спектр сигнала для первого датчика')  # График АЧХ экспериментальный
ax.plot(freq, Ampl[1], 'k', label='Спектр сигнала для второго датчика')  # График АЧХ экспериментальный
ax.plot(freq, Ampl[2], 'b', label='Спектр сигнала для третьего датчика')  # График АЧХ экспериментальный
ax.plot(freq, Ampl[3], 'r', label='Спектр сигнала для четвертого датчика')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.set_xlim([0, 100])
ax.grid()
ax.legend()


#
# Обработка полученных графиков
#

# Выбранные интервалы для резонансной частоты
w_list = Config.w_list
# Получение по МПМ демпфирования для заданной частоты
dempf = [[0 for i in range(len(w_list))] for j in range(3)]

for i in range(len(Ampl)):
    temp = peak_picking(freq, Ampl[i], w_list)  # демпфирование по МПМ
    # print(temp, len(temp), len(temp[0]))
    for j in range(len(temp)):
        for k in range(len(temp[0])):
            dempf[j][k] += temp[j][k]

for j in range(len(temp)):
    for k in range(len(temp[0])):
        dempf[j][k] /= len(Ampl)

print('ЭМА:')
print('Найденный резонансные частоты', dempf[0], '\nНайденные демпфирования', dempf[1])

# Получение по МПМ демпфирования для заданной частоты
d = peak_picking(f, A, w_list)  # демпфирование по МПМ
print('OMA:')
print('Найденный резонансные частоты', d[0], '\nНайденные демпфирования', d[1])

print(len(A), len(Ampl[0]))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(freq, Ampl[0], 'g', label='ЭМА')  # График АЧХ экспериментальный
ax.plot(f, A, 'b', label='ОМА')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.set_xlim([0, 100])
ax.legend()
ax.grid()

plt.show()
