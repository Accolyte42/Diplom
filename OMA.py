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

displ_arr = displ_arr1 + displ_arr_2 + displ_arr_3

noise = np.random.normal(0, 1, len(displ_arr1[0]))
for i in range(len(displ_arr1[0])):
    displ_arr[1][i] = displ_arr[1][i] + noise[i]
    displ_arr[3][i] = displ_arr[3][i] + noise[i]
    displ_arr[5][i] = displ_arr[5][i] + noise[i]

X = displ_arr[0]
Y = [displ_arr[1], displ_arr[3], displ_arr[5]]
# print(Y)

fig = plt.figure()
plt.plot(X, Y[0], 'g', X, Y[1], 'k', X, Y[2], 'c')
# plt.plot(X, Y[0], 'g', X, displ_arr1[1], 'k')
plt.xlim([0, 2])
# plt.show()

# Чтение из файла Cur_FRF_wing.txt массив данных с датчиков
read_file = np.loadtxt("Cur_FRF_wing.txt")
# print(read_file.shape[0])  # 336
freq = read_file[:, 0]
Ampl_c_arr = arr_sensor(read_file)  # Массив перед ф-ций для всех точек
N = read_file.shape[0]  # количество точек
Ampl_arr = np.abs(Ampl_c_arr)    # Массив действительных амплитуд АЧХ
Ampl_phs_arr = np.angle(Ampl_c_arr)   # Массив фаз для ФЧХ
# print(Ampl_c_arr)
# np.savetxt('test1.txt', Ampl_c_arr)

# Рассматриваемый датчик
Src_snsr = Config.Src_snsr
Ampl = Ampl_arr[:, Src_snsr]
Ampl_phs = Ampl_phs_arr[:, Src_snsr]

# Построение графиков
# Построение графика АЧХ
fig = plt.figure()
ax = fig.add_subplot(311)
ax.plot(freq, Ampl, 'g', label='Действ')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
ax.legend()

# Построение графика ФЧХ
ax = fig.add_subplot(312)
ax.plot(freq, Ampl_phs, 'g', label='Мним')  # График ФЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
ax.legend()

# Построение графика АЧХ для всех датчиков
ax = fig.add_subplot(313)
ax.plot(freq, Ampl_arr, 'g')  # График ФЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.grid()
# Отображение
# plt.show()

dt = X[1] - X[0]
fs = 1/dt
dscrt = 3000
Gyy = [0] * len(Y)
Temp_Gyy = [0] * len(Y)
# print(len(Ampl_arr.transpose()))
fig = plt.figure()
counter = 1
for i in range(len(Y)):
    for j in range(len(Y)):
        # print(i, j)
        f, Temp_Gyy[j] = csd(Y[i], Y[j], fs, nperseg=dscrt)
        ax = fig.add_subplot(len(Y), len(Y), counter)
        ax.plot(f, Temp_Gyy[j], 'g', label=str([i,j]))  # График CSD
        ax.set_xlabel('FREQ')
        ax.set_ylabel('CSD')
        ax.legend()
        ax.grid()
        counter = counter + 1
    Gyy[i] = Temp_Gyy
    Temp_Gyy = [0] * len(Y)
    # Короче, хз из-за чего, но при переходе к новому i и применению функции csd
    # при присваивании значений в новой строке начинают меняться значения в старой строке
    # Для решения этой проблемы придумал такой костыль, чтоб при окончании строки
    # мы отдельно запоминали старую и всё
del counter, Temp_Gyy

Gyy = np.array(Gyy)
# print(Gyy[:][:][0][0])
print(len(Gyy), len(Gyy[0]), len(Gyy[0][0]))
print(Gyy[:, :, 5], 'test')
# print(Gyy[:, 0, :])
# print(Gyy[0, :, :])

print(len(Gyy[:, :, 0]))
A = []
for i in range(len(Gyy[0][0])):
    # print(i)
    U, S, V = svd(Gyy[:, :, i])
    A.append(S[0])

# сохраняем компоненты U V (на итерации)
# умножить первую строку U на первый столбец V и на сингулярное значение
# обратная функция к cpd матрицу во врем ряд
# эта матрица

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(f, A, 'g', label='Эксперимент')  # График АЧХ экспериментальный
ax.set_xlabel('Частота в герцах')
ax.set_ylabel('Амплитуда')
ax.legend()
ax.grid()

plt.show()
